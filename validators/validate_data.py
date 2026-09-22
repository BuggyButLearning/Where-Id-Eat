#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema" / "report.schema.json"
PHOTO_TYPES = {"official_restaurant", "official_food", "official_exterior", "editorial_restaurant", "editorial_food"}
FALLBACK_TYPE = "generated_svg_fallback"


def is_http(url):
    try:
        return urlparse(url).scheme in {"http", "https"}
    except Exception:
        return False


def is_svg_image_url(url):
    u = str(url or "").strip().lower()
    if u.startswith("data:image/svg") or "image/svg+xml" in u:
        return True
    try:
        parsed = urlparse(u)
        if parsed.path.endswith((".svg", ".svgz")):
            return True
        q = parsed.query
        return any(token in q for token in ("format=svg", "fm=svg", "type=svg", "image=svg"))
    except Exception:
        return False


def validate_schema(data, errors, warnings):
    try:
        import jsonschema  # type: ignore
    except Exception:
        warnings.append("jsonschema is not installed; using built-in contract checks only")
        return
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = ".".join(str(x) for x in err.path) or "root"
        errors.append(f"schema {loc}: {err.message}")


def validate_recommendation(rec, kind, errors, warnings):
    prefix = f"{kind}:{rec.get('id', '?')}"
    if not rec.get("hours", {}).get("verified"):
        errors.append(f"{prefix}: hours must be verified")
    verification = rec.get("hours", {}).get("verification_sources", [])
    if len(verification) < 2:
        errors.append(f"{prefix}: requires at least two availability verification sources")
    source_types = {v.get("type") for v in verification}
    if "official" not in source_types:
        errors.append(f"{prefix}: availability verification must include an official source")
    if len(source_types - {"official"}) < 1:
        errors.append(f"{prefix}: availability verification must include a second independent current signal")

    image = rec.get("image", {})
    image_url = str(image.get("url", ""))
    image_type = image.get("type")
    if image_type == FALLBACK_TYPE:
        evidence = image.get("photo_search_evidence") or []
        if len(evidence) < 3:
            errors.append(f"{prefix}: SVG fallback requires at least three documented photo-source checks")
        for u in evidence:
            if not is_http(str(u)):
                errors.append(f"{prefix}: invalid photo_search_evidence URL {u}")
        if not str(image.get("fallback_reason") or "").strip():
            errors.append(f"{prefix}: SVG fallback requires fallback_reason")
        if not is_svg_image_url(image_url):
            errors.append(f"{prefix}: generated_svg_fallback must use SVG content")
        if image_url.startswith("data:image") and not image_url.lower().startswith("data:image/svg"):
            errors.append(f"{prefix}: fallback data URI must be SVG")
        elif not image_url.startswith("data:image") and not is_http(image_url):
            errors.append(f"{prefix}: fallback SVG must use data:image/svg or http(s)")
    else:
        if image_type not in PHOTO_TYPES:
            errors.append(f"{prefix}: image type must be a verified photograph or documented SVG fallback")
        if image_url.startswith("data:image"):
            errors.append(f"{prefix}: photographic images cannot use embedded data URIs")
        if is_svg_image_url(image_url):
            errors.append(f"{prefix}: SVG is allowed only for documented generated_svg_fallback images")
        if not is_http(image_url):
            errors.append(f"{prefix}: recommendation photo must use a resolvable http(s) URL")
    if not is_http(str(image.get("source_url", ""))):
        errors.append(f"{prefix}: image source_url must be http(s)")

    yelp = rec.get("yelp", {})
    yelp_url = str(yelp.get("url", ""))
    resolution = yelp.get("resolution")
    if resolution == "direct":
        if "/search?" in yelp_url or "find_desc=" in yelp_url:
            errors.append(f"{prefix}: Yelp is marked direct but points to a search URL")
        if not yelp.get("verified"):
            warnings.append(f"{prefix}: direct Yelp URL is present but numeric rating is not verified")
    elif resolution == "search_fallback":
        warnings.append(f"{prefix}: Yelp direct listing was not resolved; search fallback will be shown")
        if yelp.get("verified"):
            errors.append(f"{prefix}: search-fallback Yelp entry cannot be marked rating-verified")
    elif resolution == "unavailable":
        errors.append(f"{prefix}: Yelp resolution is required for an active recommendation")

    if yelp.get("verified") and (yelp.get("rating") is None or yelp.get("review_count") is None):
        errors.append(f"{prefix}: verified Yelp data requires rating and review_count")

    links = rec.get("links", {})
    for key in ("website", "directions"):
        if not is_http(str(links.get(key, ""))):
            errors.append(f"{prefix}: missing valid {key} URL")
    if not links.get("editorial"):
        errors.append(f"{prefix}: at least one local/editorial source is required")
    for u in links.get("editorial", []):
        if not is_http(str(u)):
            errors.append(f"{prefix}: invalid editorial URL {u}")
    if len(rec.get("order", [])) < 2:
        errors.append(f"{prefix}: provide at least two concrete things to order")


def validate(data):
    errors, warnings = [], []
    validate_schema(data, errors, warnings)
    if data.get("version") != "2.0": errors.append("version must be 2.0")
    command = data.get("command", {})
    primary = data.get("primary", [])
    companion = data.get("companion", [])
    if len(primary) < 5: errors.append("primary recommendations must contain at least 5 places")
    if len(companion) < 4: errors.append("companion recommendations must contain at least 4 places")
    if command.get("primary_count") != len(primary): errors.append("command.primary_count must equal the primary array length")
    if command.get("companion_count") != len(companion): errors.append("command.companion_count must equal the companion array length")

    meal = command.get("meal")
    expected_companion = "Dessert" if meal == "dinner" else "Coffee"
    if data.get("report", {}).get("companion_label") != expected_companion:
        errors.append(f"{meal} reports must use {expected_companion} as the companion section")

    hero = data.get("report", {}).get("hero", {})
    hero_url = str(hero.get("url", ""))
    if hero_url.startswith("data:image"):
        errors.append("hero image cannot be a generated/base64 data URI")
    if is_svg_image_url(hero_url):
        errors.append("hero image cannot be SVG; use a real location or destination food photo")
    if not is_http(hero_url):
        errors.append("hero image must be a location-specific http(s) photo")
    if not is_http(str(hero.get("source_url", ""))):
        errors.append("hero source_url must be http(s)")

    ids=[]
    for kind,recs in (("primary",primary),("companion",companion)):
        for rec in recs:
            rid=rec.get("id")
            if rid in ids: errors.append(f"duplicate recommendation id: {rid}")
            ids.append(rid)
            validate_recommendation(rec,kind,errors,warnings)

    primary_ids={r.get("id") for r in primary}
    for qp in data.get("report", {}).get("quick_picks", []):
        if qp.get("recommendation_id") not in primary_ids:
            errors.append(f"quick pick target must reference a primary recommendation: {qp.get('recommendation_id')}")

    if len(data.get("sources", [])) < 4: errors.append("report requires at least four cited sources")
    return errors,warnings


def main():
    ap=argparse.ArgumentParser(description="Validate Where I'd Eat v2 research JSON before rendering.")
    ap.add_argument("input")
    args=ap.parse_args()
    try: data=json.loads(Path(args.input).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: cannot parse JSON: {exc}"); return 2
    errors,warnings=validate(data)
    for w in warnings: print("WARN:",w)
    for err in errors: print("ERROR:",err)
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)"); return 1
    print(f"OK: data contract passed ({len(data['primary'])} primary, {len(data['companion'])} companion, {len(warnings)} warning(s))")
    return 0

if __name__=="__main__": raise SystemExit(main())
