---
name: where-id-eat
description: Run the Where I’d Eat command to research and build a predictable location-centered breakfast, lunch, or dinner guide. Produces validated JSON first, then uses the canonical renderer for fixed HTML structure, real restaurant images, Yelp resolution, current availability checks, an anchor-centered map, and a full coffee or dessert companion section.
---

# Where I’d Eat

Treat this as a command, not a free-form report-writing prompt.

## 1. Resolve the command

Normalize the user request into these inputs before research:

- `anchor`: hotel, address, venue, neighborhood, or landmark
- `date`
- `meal`: `breakfast`, `lunch`, or `dinner`
- `profile`: default unless the user asks to customize
- `preference_mode`: `default` or `interview`
- `primary_count`: default 6, minimum 5
- `companion_count`: default 4, minimum 4
- optional party size, budget, and maximum travel time

If meal is missing, ask breakfast, lunch, or dinner. If preference mode is not specified, offer the default taste profile or a short interview. The interview should cover budget, travel tolerance, dietary constraints, cuisines to seek or avoid, reservation tolerance, and whether to favor local institutions, newer openings, specialists, or a mix.

Dinner always uses Dessert as the companion section. Breakfast and lunch always use Coffee.

## 2. Research only

Do not write HTML during research. Build a broad candidate set, verify the active candidates, then populate the v2 report data contract.

Use current local and web sources. Prefer official restaurant information plus respected local editorial sources. Yelp is a community signal, not the ranking authority.

For every active recommendation:

- verify official hours for the requested date
- obtain a second independent current signal such as a live business listing, reservation inventory, or same-day notice
- resolve the direct Yelp business page when possible
- use a numeric Yelp rating only when directly verified
- obtain a real restaurant or food photograph, preferring official photography and then reputable editorial photography
- never generate a restaurant title card, gradient placeholder, base64 SVG, or fake restaurant image
- if no real image can be verified, explicitly use the standardized repository fallback and accept the validator warning
- include official website, directions, at least one local editorial source, menu when available, and reservation link when relevant

Exclude unresolved closures from the active ranking.

## 3. Produce strict JSON

Write the research to a JSON file that conforms to `schema/report.schema.json` in the repo, or `runtime/schema/report.schema.json` in an installed package.

Do not manually assign ranks. Supply one final `score` per recommendation. The renderer sorts by score and assigns ranks so score and rank cannot disagree.

Use `profiles/default.json` or `runtime/profiles/default.json` for the default weighting.

## 4. Build with the canonical command

Do not hand-author the final HTML.

Repository checkout:

```bash
python bin/where-id-eat build report.json report.html
```

Installed skill package:

```bash
python runtime/bin/where-id-eat build report.json report.html
```

The command performs data validation, deterministic rendering, and HTML validation. Fix every error before delivery. Warnings are allowed only when they accurately describe an unavoidable fallback such as an unresolved direct Yelp page or standardized image fallback.

## 5. Deliver

Return the rendered HTML artifact. Do not substitute a prose-only list when the user requested a guide.

The canonical renderer owns the section order, tables, cards, buttons, map, scoring explanation, and companion section. Do not add, remove, reorder, or redesign report sections in the generated HTML.
