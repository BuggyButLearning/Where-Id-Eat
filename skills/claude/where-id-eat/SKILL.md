---
name: where-id-eat
description: Execute the Where I’d Eat command for predictable traveler food guides centered on a hotel or other anchor. Research into a strict JSON contract, then use the canonical renderer and validators instead of writing HTML free-form. Includes real images, Yelp resolution, same-day availability, maps, and a full coffee or dessert companion section.
---

# Where I’d Eat

Use a command pipeline: research -> strict JSON -> canonical renderer -> validator -> final HTML.

## Resolve inputs

Before research, resolve the anchor, target date, meal, and preference mode. Ask for breakfast, lunch, or dinner if meal is missing. Use the default profile unless the user chooses a short interview. Default to 6 primary recommendations and 4 companion recommendations, never fewer than 5 and 4 respectively.

Dinner uses Dessert. Breakfast and lunch use Coffee.

## Research

Research a broad candidate set before choosing the active list. Prefer current local editorial sources, official sites, and current business signals. Yelp is required as a community signal, but do not invent ratings.

Every active recommendation must have official hours plus a second current verification source, a real photo with source credit, official website, directions, at least one local editorial source, specific order suggestions, travel friction from the anchor, and Yelp resolution. Resolve menu and reservation links when relevant.

Do not generate restaurant art or base64 SVG title cards. Real official or editorial photography is the default. Use the standardized repository fallback only when a real image cannot be verified.

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

Fix all validator errors. The renderer owns report structure, section order, map behavior, tables, cards, buttons, and scoring presentation. Do not manually modify the generated HTML except to fix the canonical renderer itself.

Deliver the validated HTML artifact.
