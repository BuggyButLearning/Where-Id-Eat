#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import sys

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set(); self.hrefs=[]; self.images=[]; self.title=''
        self._in_title=False
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if 'id' in d: self.ids.add(d['id'])
        if tag=='a' and 'href' in d: self.hrefs.append(d['href'])
        if tag=='img': self.images.append(d)
        if tag=='title': self._in_title=True
    def handle_endtag(self, tag):
        if tag=='title': self._in_title=False
    def handle_data(self, data):
        if self._in_title: self.title += data

def main(path):
    html=Path(path).read_text(encoding='utf-8')
    p=Parser(); p.feed(html)
    errors=[]
    for href in p.hrefs:
        if href.startswith('#') and len(href)>1 and href[1:] not in p.ids:
            errors.append(f'broken internal anchor: {href}')
    for i,img in enumerate(p.images,1):
        if not img.get('alt','').strip(): errors.append(f'image {i} missing alt text')
        if not img.get('src','').strip(): errors.append(f'image {i} missing src')
    required=['Yelp','Directions','Website']
    for item in required:
        if item.lower() not in html.lower(): errors.append(f'missing expected link/content: {item}')
    if '<div' not in html or '<table' not in html: errors.append('report structure appears incomplete')
    if errors:
        print('\n'.join('ERROR: '+e for e in errors)); return 1
    print(f'OK: {path} ({len(p.ids)} ids, {len(p.images)} images, {len(p.hrefs)} links)')
    return 0

if __name__=='__main__':
    if len(sys.argv)!=2:
        print('usage: validate_report.py <report.html>'); raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
