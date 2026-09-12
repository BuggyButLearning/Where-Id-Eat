#!/usr/bin/env python3
"""Compatibility wrapper. Prefer runtime/bin/where-id-eat build."""
import subprocess, sys
from pathlib import Path
here=Path(__file__).resolve()
candidates=[here.parents[1]/'runtime'/'validators'/'validate_html.py', here.parents[4]/'validators'/'validate_html.py']
validator=next((p for p in candidates if p.exists()),None)
if not validator:
    print('ERROR: canonical validator not found. Repackage the skill with tools/package_skills.py.'); raise SystemExit(2)
raise SystemExit(subprocess.run([sys.executable,str(validator),*sys.argv[1:]]).returncode)
