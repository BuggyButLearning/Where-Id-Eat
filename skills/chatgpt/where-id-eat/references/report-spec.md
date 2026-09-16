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

Every active recommendation requires one final score, a real restaurant/food/exterior photograph with source credit, official website, directions, Yelp resolution, at least one local editorial source, two availability verification sources including the official source, spend, distance/travel time, requested-day hours, ordering guidance, practical strategy, and current signal.

Ranks are renderer-generated from final score. Never type ranks into research JSON.

Image requirements are hard rules:

- hero uses a real location or destination-food photograph
- every primary and companion card uses a real restaurant, food, or exterior photograph
- generated restaurant illustrations, SVGs, base64 SVG title cards, generic gradients, branded fallback graphics, and synthetic restaurant imagery are prohibited
- if a candidate lacks a usable verifiable photograph, replace the candidate before rendering
- do not derive a new report from legacy HTML; use current schema-valid JSON or research again
