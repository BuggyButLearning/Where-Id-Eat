#!/usr/bin/env python3
import shutil
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
RUNTIME_DIRS=['schema','renderer','validators','profiles']
RUNTIME_FILES=[Path('bin/where-id-eat')]


def add_tree(zf, src, arcroot):
    for p in sorted(src.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            zf.write(p, arcroot / p.relative_to(src))


def package(platform):
    skill=ROOT/'skills'/platform/'where-id-eat'
    if not skill.exists():
        raise SystemExit(f'missing {skill}')
    outdir=DIST/platform
    outdir.mkdir(parents=True,exist_ok=True)
    out=outdir/'where-id-eat.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as zf:
        add_tree(zf,skill,Path('where-id-eat'))
        for name in RUNTIME_DIRS:
            add_tree(zf,ROOT/name,Path('where-id-eat/runtime')/name)
        for rel in RUNTIME_FILES:
            zf.write(ROOT/rel,Path('where-id-eat/runtime')/rel)
    print(out)


def main():
    if DIST.exists(): shutil.rmtree(DIST)
    package('chatgpt')
    package('claude')

if __name__=='__main__':
    main()
