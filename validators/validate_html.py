#!/usr/bin/env python3
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

PHOTO_TYPES={"location_photo","editorial_location_photo","destination_food_photo","official_restaurant","official_food","official_exterior","editorial_restaurant","editorial_food"}
FALLBACK_TYPE="generated_svg_fallback"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.hrefs=[]; self.images=[]; self.metas={}; self.cards=[]; self.rows=[]; self.quick=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if 'id' in d: self.ids.append(d['id'])
        if tag=='a' and 'href' in d: self.hrefs.append(d['href'])
        if tag=='img': self.images.append(d)
        if tag=='meta' and d.get('name'): self.metas[d['name']]=d.get('content','')
        if tag=='article' and 'restaurant-card' in d.get('class',''): self.cards.append(d)
        if tag=='tr' and d.get('data-kind') in {'primary','companion'}: self.rows.append(d)
        if tag=='div' and d.get('data-quick-target'): self.quick.append(d.get('data-quick-target'))


def segment_for_card(text, card_id):
    m=re.search(rf'<article[^>]+id=["\']{re.escape(card_id)}["\'][\s\S]*?</article>',text,re.I)
    return m.group(0) if m else ''


def is_svg_src(src):
    s=str(src or '').strip().lower()
    if s.startswith('data:image/svg') or 'image/svg+xml' in s:
        return True
    try:
        p=urlparse(s)
        if p.path.endswith(('.svg','.svgz')): return True
        return any(token in p.query for token in ('format=svg','fm=svg','type=svg','image=svg'))
    except Exception:
        return False


def validate(path):
    text=Path(path).read_text(encoding='utf-8')
    p=Parser(); p.feed(text)
    errors=[]; warnings=[]
    sections=['best-bets','map','compare','primary','companion','method','sources']
    positions=[]
    for sid in sections:
        pos=text.find(f'id="{sid}"')
        if pos<0: errors.append(f'missing required section #{sid}')
        positions.append(pos)
    if all(x>=0 for x in positions) and positions!=sorted(positions): errors.append('required sections are not in canonical order')

    seen=set()
    for ident in p.ids:
        if ident in seen: errors.append(f'duplicate id: {ident}')
        seen.add(ident)
    for href in p.hrefs:
        if href.startswith('#') and len(href)>1 and href[1:] not in seen: errors.append(f'broken internal anchor: {href}')

    primary_cards=[c for c in p.cards if c.get('data-kind')=='primary']
    companion_cards=[c for c in p.cards if c.get('data-kind')=='companion']
    primary_rows=[r for r in p.rows if r.get('data-kind')=='primary']
    companion_rows=[r for r in p.rows if r.get('data-kind')=='companion']
    if len(primary_cards)<5: errors.append('primary recommendation card count must be at least 5')
    if len(companion_cards)<4: errors.append('companion recommendation card count must be at least 4')
    if len(primary_cards)!=len(primary_rows): errors.append('primary comparison row count does not match card count')
    if len(companion_cards)!=len(companion_rows): errors.append('companion comparison row count does not match card count')

    try:
        if int(p.metas.get('where-id-eat-primary-count','-1'))!=len(primary_cards): errors.append('primary count metadata does not match cards')
        if int(p.metas.get('where-id-eat-companion-count','-1'))!=len(companion_cards): errors.append('companion count metadata does not match cards')
    except ValueError: errors.append('invalid recommendation count metadata')

    for kind,cards in [('primary',primary_cards),('companion',companion_cards)]:
        try:
            scores=[float(c.get('data-score','nan')) for c in cards]
            if scores!=sorted(scores,reverse=True): errors.append(f'{kind} cards are not sorted by displayed final score')
        except Exception: errors.append(f'{kind} card score metadata invalid')

    expected_images=len(primary_cards)+len(companion_cards)+1
    if len(p.images)!=expected_images:
        errors.append(f'report must contain exactly one hero photo plus one photo per recommendation ({expected_images} expected, {len(p.images)} found)')
    for i,img in enumerate(p.images,1):
        src=img.get('src','')
        image_type=img.get('data-image-type','')
        if not img.get('alt','').strip(): errors.append(f'image {i} missing alt text')
        if not src: errors.append(f'image {i} missing src')
        if image_type == FALLBACK_TYPE:
            if not is_svg_src(src): errors.append(f'image {i} fallback is not SVG content')
            try:
                if int(img.get('data-photo-search-count','0')) < 3:
                    errors.append(f'image {i} SVG fallback has fewer than three documented photo-source checks')
            except ValueError:
                errors.append(f'image {i} SVG fallback has invalid photo search count')
        else:
            if src.startswith('data:image'): errors.append(f'image {i} photograph uses prohibited embedded data URI')
            if is_svg_src(src): errors.append(f'image {i} uses SVG without documented fallback state')
            if image_type not in PHOTO_TYPES: errors.append(f'image {i} has invalid or missing data-image-type: {image_type or "(missing)"}')
    lower=text.lower()
    fallback_start=lower.find('id="guide-map-fallback"')
    if fallback_start < 0:
        errors.append('missing embedded offline map fallback')
    else:
        fallback_open=lower.rfind('<div',0,fallback_start)
        fallback_end=lower.find('</div>',fallback_start)
        fallback_segment=lower[fallback_open:fallback_end+6] if fallback_open>=0 and fallback_end>=0 else ''
        if '<svg' not in fallback_segment:
            errors.append('offline map fallback must contain an embedded SVG proximity map')
        outside_svg=lower[:fallback_open] + lower[fallback_end+6:] if fallback_open>=0 and fallback_end>=0 else lower
        if '<svg' in outside_svg:
            errors.append('inline SVG is allowed only inside the offline map fallback')
    if 'generated placeholder' in lower or 'custom report illustration' in lower or 'image unavailable' in lower:
        errors.append('report contains an undocumented generic fallback')

    for c in p.cards:
        cid=c.get('id','?'); seg=segment_for_card(text,cid)
        for required in ('website','directions','yelp','editorial'):
            if f'data-link="{required}"' not in seg: errors.append(f'{cid}: missing required {required} link')
        if c.get('data-verified')!='true': errors.append(f'{cid}: not marked availability-verified')
        try:
            if int(c.get('data-verification-count','0'))<2: errors.append(f'{cid}: fewer than two availability verification sources')
        except ValueError: errors.append(f'{cid}: invalid verification count')
        if c.get('data-yelp-resolution')=='search_fallback': warnings.append(f'{cid}: Yelp direct listing unresolved; report shows search fallback')
        if c.get('data-yelp-resolution')=='unavailable': errors.append(f'{cid}: Yelp resolution unavailable')

    card_ids={c.get('id') for c in primary_cards}
    for target in p.quick:
        if target not in card_ids: errors.append(f'quick pick points outside primary recommendations: {target}')

    if 'tile.openstreetmap.org' in lower or 'unpkg.com/leaflet' in lower or 'l.tilelayer(' in lower:
        errors.append('legacy Leaflet/OpenStreetMap runtime tile map is prohibited; use the portable map contract')
    if 'data-map-engine="maplibre-pmtiles"' not in lower:
        errors.append('map must declare the MapLibre/PMTiles engine')
    if 'pmtiles://' not in lower:
        errors.append('map must use a PMTiles source instead of per-tile OpenStreetMap requests')

    m=re.search(r'<script id="where-id-eat-map-data" type="application/json">([\s\S]*?)</script>',text,re.I)
    if not m: errors.append('missing map data JSON')
    else:
        try:
            d=json.loads(m.group(1))
            if len(d.get('primary',[]))!=len(primary_cards): errors.append('map primary marker count does not match cards')
            if len(d.get('companion',[]))!=len(companion_cards): errors.append('map companion marker count does not match cards')
        except Exception as exc: errors.append(f'invalid map JSON: {exc}')
    return errors,warnings


def main():
    ap=argparse.ArgumentParser(description="Validate canonical Where I'd Eat rendered HTML."); ap.add_argument('input'); args=ap.parse_args()
    errors,warnings=validate(args.input)
    for w in warnings: print('WARN:',w)
    for err in errors: print('ERROR:',err)
    if errors:
        print(f'FAILED: {len(errors)} error(s), {len(warnings)} warning(s)'); return 1
    print(f'OK: HTML contract passed ({len(warnings)} warning(s))'); return 0

if __name__=='__main__': raise SystemExit(main())
