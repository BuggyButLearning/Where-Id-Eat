# Where I’d Eat v2 Report Contract

The report is generated from structured JSON. The model researches; the renderer formats.

Canonical section order:

1. Hero
2. Trip context and verification summary
3. Best bets
4. Anchor-centered interactive map
5. Primary comparison table
6. Primary recommendation cards
7. Companion comparison table
8. Companion recommendation cards
9. Method
10. Sources
11. Generated and verified timestamp

Primary lists require at least 5 recommendations. Companion lists require at least 4. Dinner uses Dessert. Breakfast and lunch use Coffee.

Every active recommendation requires one final score, official website, directions, Yelp resolution, at least one local editorial source, two availability verification sources including the official source, spend, distance/travel time, requested-day hours, ordering guidance, practical strategy, and current signal.

Ranks are renderer-generated from final score. Never type ranks into research JSON.

Image rules:

- The hero must use a real location or destination-food photograph.
- Primary and companion cards should use a real restaurant, food, or exterior photograph with source credit whenever a usable image can be verified.
- Search the official restaurant site first, then the direct Yelp business page or Yelp photo search, then reputable editorial, reservation, social, and current business-listing sources.
- Do not use an SVG fallback merely because a photo is inconvenient to retrieve.
- Yelp is a required photo-source check before fallback. If Yelp blocks automated access, record the attempted Yelp business or photo URL as evidence and continue the search.
- If no usable photo can be found after at least three documented photo-source checks, including official, Yelp, and another independent current source, generate a simple neutral SVG fallback for that recommendation.
- SVG fallbacks must use `type: generated_svg_fallback`, include a human-readable `fallback_reason`, and include at least three `photo_search_evidence` URLs.
- Generic gradients, undocumented placeholders, unrelated stock photos, and synthetic restaurant scenes remain prohibited.
- Do not derive a new report from legacy HTML; use current schema-valid JSON or research again.

Report-facing title, subtitle, summaries, and recommendation copy must be written for the diner. Do not mention repositories, schemas, validators, renderers, internal tooling, or implementation details in the report narrative.
