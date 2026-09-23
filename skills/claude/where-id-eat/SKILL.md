---
name: where-id-eat
description: Execute the Where I’d Eat command for predictable traveler food guides centered on a hotel or other anchor. Research into a strict JSON contract, then use the canonical renderer and validators instead of writing HTML free-form. Requires restaurant photography when available, a documented SVG fallback only after best-effort image search, Yelp resolution, same-day availability, maps, and a full coffee or dessert companion section.
---

# Where I’d Eat

Use a command pipeline: research -> strict JSON -> canonical renderer -> validator -> final HTML.

## Resolve inputs

Before research, resolve the anchor, target date, meal, and preference mode. Ask for breakfast, lunch, or dinner if meal is missing. Use the default profile unless the user chooses a short interview. Default to 6 primary recommendations and 4 companion recommendations, never fewer than 5 and 4 respectively.

Dinner uses Dessert. Breakfast and lunch use Coffee.

## Research

Research a broad candidate set before choosing the active list. Prefer current local editorial sources, official sites, and current business signals. Yelp is required as a community signal, but do not invent ratings.

Every active recommendation must have official hours plus a second current verification source, a restaurant/food/exterior photo with source credit when one can be verified, official website, directions, at least one local editorial source, specific order suggestions, travel friction from the anchor, and Yelp resolution. Resolve menu and reservation links when relevant.

Real photography is the default. For a missing recommendation image, search the official restaurant site first, then the direct Yelp business page or Yelp photo search, then reputable editorial, reservation, social, and current business-listing sources. Yelp is a required image-source check before any SVG fallback. If direct Yelp access is blocked, document the attempted Yelp URL and continue. If no usable recommendation photo can be found after at least three documented source checks, including the official source, Yelp, and another independent current source, generate a simple neutral SVG fallback and record the reason plus all photo-search evidence URLs. Do not use SVG merely for convenience. The hero must still use a real location or destination-food photograph.

Do not reuse an older generated HTML report as the basis for a new report or map test. Reuse only structured JSON that passes the current schema; otherwise research again. This prevents legacy image placeholders and layout behavior from leaking into current output.

Exclude unresolved closures before ranking.

## Data contract

Populate `schema/report.schema.json` in a repository checkout or `runtime/schema/report.schema.json` in an installed package. Do not write HTML directly.

Do not assign ranks. Provide one final score. The renderer sorts the recommendations and assigns rank deterministically.

Use `profiles/default.json` or `runtime/profiles/default.json` unless the user chose an interview.

## Build

Repository checkout:

```bash
python bin/where-id-eat build report.json report.html
```

Installed package:

```bash
python runtime/bin/where-id-eat build report.json report.html
```

Fix all validator errors. Undocumented SVG fallbacks, fallbacks with fewer than three photo-source checks, and missing image attribution are hard failures. The renderer owns report structure, section order, map behavior, tables, cards, buttons, and scoring presentation. Do not manually modify the generated HTML except to fix the canonical renderer itself.

Keep report-facing copy focused on the diner and meal. Do not mention repositories, schemas, validators, renderers, internal tooling, or implementation details in the report narrative.

Deliver the validated HTML artifact.
