#!/usr/bin/env python3
import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlparse

TEMPLATE = Path(__file__).resolve().parent / "template.html"
PHOTO_TYPES={"official_restaurant","official_food","official_exterior","editorial_restaurant","editorial_food"}
FALLBACK_TYPE="generated_svg_fallback"
HERO_TYPES={"location_photo","editorial_location_photo","destination_food_photo"}


def e(value):
    return html.escape(str(value), quote=True)


def is_svg_url(url):
    u=str(url or '').strip().lower()
    if u.startswith('data:image/svg') or 'image/svg+xml' in u: return True
    try:
        p=urlparse(u)
        if p.path.endswith(('.svg','.svgz')): return True
        return any(token in p.query for token in ('format=svg','fm=svg','type=svg','image=svg'))
    except Exception:
        return False


def require_photo(img, context, allowed_types):
    url=str(img.get('url',''))
    if img.get('type') not in allowed_types:
        raise ValueError(f"{context}: real photography is required; fallback/generated image type is not allowed")
    if url.startswith('data:image'):
        raise ValueError(f"{context}: data URI images are not allowed")
    if is_svg_url(url):
        raise ValueError(f"{context}: SVG images are not allowed")
    if urlparse(url).scheme not in {'http','https'}:
        raise ValueError(f"{context}: photo URL must use http(s)")


def money(spend):
    currency = spend.get("currency", "$")
    if currency == "USD": currency = "$"
    return f"{currency}{spend['min']:g} to {currency}{spend['max']:g}"


def yelp_text(yelp):
    if yelp.get("verified") and yelp.get("rating") is not None:
        count = yelp.get("review_count")
        suffix = f" · {count:,} reviews" if isinstance(count, int) else ""
        return f"{yelp['rating']:.1f}/5{suffix}"
    if yelp.get("resolution") == "search_fallback": return "Listing not directly resolved"
    return "Rating not verified"


def button(url, label, kind="secondary", data_link=None):
    if not url: return ""
    attr = f' data-link="{e(data_link)}"' if data_link else ""
    return f'<a class="btn {kind}"{attr} href="{e(url)}" target="_blank" rel="noopener">{e(label)}</a>'


def editorial_buttons(urls):
    return "".join(button(u, "Local editorial", "secondary", "editorial") for u in urls)


def image_block(rec):
    img = rec["image"]
    if img.get("type") == FALLBACK_TYPE:
        url = str(img.get("url", ""))
        checks = len(img.get("photo_search_evidence") or [])
        if not is_svg_url(url):
            raise ValueError(f"recommendation {rec.get('name','?')}: generated fallback must be SVG")
        if not (url.startswith("data:image/svg") or urlparse(url).scheme in {"http", "https"}):
            raise ValueError(f"recommendation {rec.get('name','?')}: SVG fallback must use data URI or http(s)")
        caption = f'Generated SVG fallback after {checks} photo-source checks. {e(img.get("fallback_reason","No usable photograph was found."))}'
        search_attr = f' data-photo-search-count="{checks}"'
    else:
        require_photo(img, f"recommendation {rec.get('name','?')}", PHOTO_TYPES)
        caption = f'Photo: <a href="{e(img["source_url"])}" target="_blank" rel="noopener">{e(img["credit"])}</a>.'
        search_attr = ''
    return f'<figure class="photo"><img src="{e(img["url"])}" alt="{e(img["alt"])}" data-image-type="{e(img["type"])}"{search_attr} onerror="this.closest(\'figure\').classList.add(\'image-error\')"><figcaption class="caption">{caption}</figcaption></figure>'


def card(rec, rank, kind):
    companion = kind == "companion"
    rank_label = f"C{rank}" if companion else str(rank)
    rank_class = " companion" if companion else ""
    yelp = rec["yelp"]
    yelp_label = "Yelp" if yelp["resolution"] == "direct" else "Search Yelp"
    links = rec["links"]
    order_items = "".join(f"<li>{e(x)}</li>" for x in rec["order"])
    buttons = button(links["website"], "Website", "", "website") + button(links.get("menu"), "Menu", "secondary", "menu") + button(links["directions"], "Directions", "secondary", "directions") + button(yelp["url"], yelp_label, "secondary", "yelp") + editorial_buttons(links["editorial"]) + button(links.get("reservation"), "Reservation", "secondary", "reservation")
    return f'''<article class="card restaurant-card" id="{e(rec['id'])}" data-kind="{kind}" data-score="{rec['score']:.2f}" data-yelp-resolution="{e(yelp['resolution'])}" data-verified="{str(rec['hours']['verified']).lower()}" data-verification-count="{len(rec['hours']['verification_sources'])}">
<div class="card-head"><div class="rankline"><span class="rank{rank_class}">{rank_label}</span><h3>{e(rec['name'])}</h3></div><div class="badges"><span class="pill">{e(rec['category'])}</span><span class="pill ok">Where I’d Eat {rec['score']:.1f}/10</span><span class="pill ok">Today verified</span></div></div>
<div class="card-grid">{image_block(rec)}<div class="facts"><div class="factgrid"><div class="fact"><b>Typical spend</b>{e(money(rec['spend']))}</div><div class="fact"><b>From anchor</b>{e(rec['distance']['summary'])}</div><div class="fact"><b>Hours</b>{e(rec['hours']['label'])}</div><div class="fact"><b>Availability</b>{e(rec['availability']['note'])}</div></div><div class="yelp-line"><b>Yelp:</b> {e(yelp_text(yelp))}</div><h4>Why it made the cut</h4><p>{e(rec['why'])}</p><h4>What I’d order</h4><ul>{order_items}</ul><h4>Practical strategy</h4><p>{e(rec['strategy'])}</p><h4>Current signal</h4><p>{e(rec['current_signal'])}</p><div class="links">{buttons}</div></div></div></article>'''


def row(rec, rank, kind):
    label = f"C{rank}." if kind == "companion" else f"{rank}."
    return f'''<tr data-kind="{kind}" data-id="{e(rec['id'])}"><td><a href="#{e(rec['id'])}">{label} {e(rec['name'])}</a><div class="muted">{e(rec['category'])}</div></td><td class="score">{rec['score']:.1f}</td><td>{e(money(rec['spend']))}</td><td>{e(rec['distance']['summary'])}</td><td>{e(rec['hours']['label'])}</td><td>{e(yelp_text(rec['yelp']))}</td><td>{e(rec['availability']['note'])}</td></tr>'''


def hero(report):
    h = report["hero"]
    require_photo(h, "hero", HERO_TYPES)
    return f'''<figure><img src="{e(h['url'])}" alt="{e(h['alt'])}" data-image-type="{e(h['type'])}" onerror="this.style.display='none'"><figcaption class="caption">Photo: <a href="{e(h['source_url'])}" target="_blank" rel="noopener">{e(h['credit'])}</a>.</figcaption></figure>'''


def quick_picks(items, rec_by_id):
    out=[]
    for item in items:
        rec=rec_by_id[item["recommendation_id"]]
        out.append(f'<div data-quick-target="{e(rec["id"])}"><b>{e(item["label"])}</b><br><a href="#{e(rec["id"])}">{e(rec["name"])}</a><br><span class="muted">{e(item["note"])}</span></div>')
    return "".join(out)


def render(data):
    primary=sorted(data["primary"],key=lambda x:(-x["score"],x["name"].lower()))
    companion=sorted(data["companion"],key=lambda x:(-x["score"],x["name"].lower()))
    rec_by_id={r["id"]:r for r in primary+companion}
    meal=data["command"]["meal"].lower()
    expected="Dessert" if meal=="dinner" else "Coffee"
    if data["report"]["companion_label"]!=expected: raise ValueError(f"companion_label must be {expected} for {meal}")
    map_data={"anchor":{"name":data["anchor"]["name"],"lat":data["anchor"]["lat"],"lng":data["anchor"]["lng"]},"primary":[{"rank":i,"id":r["id"],"name":r["name"],"score":r["score"],"lat":r["lat"],"lng":r["lng"]} for i,r in enumerate(primary,1)],"companion":[{"rank":i,"id":r["id"],"name":r["name"],"score":r["score"],"lat":r["lat"],"lng":r["lng"]} for i,r in enumerate(companion,1)]}
    replacements={"@@TITLE@@":e(data["report"]["title"]),"@@SUBTITLE@@":e(data["report"]["subtitle"]),"@@HERO@@":hero(data["report"]),"@@TOP_PICK@@":e(data["report"]["top_pick_summary"]),"@@VERIFICATION@@":e(data["report"]["verification_summary"]),"@@QUICK_PICKS@@":quick_picks(data["report"]["quick_picks"],rec_by_id),"@@ANCHOR_NAME@@":e(data["anchor"]["name"]),"@@ANCHOR_MAP_URL@@":e(data["anchor"]["map_url"]),"@@COMPANION_LABEL@@":e(data["report"]["companion_label"]),"@@PRIMARY_ROWS@@":"".join(row(r,i,"primary") for i,r in enumerate(primary,1)),"@@COMPANION_ROWS@@":"".join(row(r,i,"companion") for i,r in enumerate(companion,1)),"@@PRIMARY_CARDS@@":"".join(card(r,i,"primary") for i,r in enumerate(primary,1)),"@@COMPANION_CARDS@@":"".join(card(r,i,"companion") for i,r in enumerate(companion,1)),"@@SOURCES@@":"".join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["label"])}</a></li>' for s in data["sources"]),"@@GENERATED_AT@@":e(data["report"]["generated_at"]),"@@MAP_DATA@@":json.dumps(map_data,ensure_ascii=False).replace("<","\\u003c"),"@@PRIMARY_COUNT@@":str(len(primary)),"@@COMPANION_COUNT@@":str(len(companion))}
    out=TEMPLATE.read_text(encoding="utf-8")
    for key,value in replacements.items(): out=out.replace(key,value)
    if "@@" in out: raise ValueError("unresolved template token remains")
    return out


def main():
    ap=argparse.ArgumentParser(description="Render a canonical Where I'd Eat HTML report from validated JSON data.")
    ap.add_argument("input"); ap.add_argument("output")
    args=ap.parse_args()
    data=json.loads(Path(args.input).read_text(encoding="utf-8"))
    Path(args.output).write_text(render(data),encoding="utf-8")
    print(f"Rendered {args.output}")

if __name__=="__main__": main()
