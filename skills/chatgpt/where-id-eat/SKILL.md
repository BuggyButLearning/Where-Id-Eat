---
name: where-id-eat
description: Create reusable, polished travel dining reports centered on a hotel or other anchor, with ranked breakfast/lunch/dinner picks, live availability checks, an interactive map, images, prices, distance and solo logistics, Yelp and official links, and a full dessert or coffee companion section. Use for restaurant discovery, city food guides, trip meal planning, hotel-nearby food searches, and HTML dining-report generation.
---

# Where I’d Eat

Build a complete HTML food guide around a central location.

## Inputs

Resolve these before research, asking only when missing:

1. Central anchor: hotel, address, venue, neighborhood, or landmark.
2. Target date or day.
3. Meal: ask **breakfast, lunch, or dinner**.
4. Preference mode: offer **use the default taste profile** or **interview me to customize it**.

If the user selects the interview, ask a short batch of questions covering budget, maximum ride time, dietary restrictions, cuisines or foods to avoid, reservation tolerance, and whether to favor local institutions, newer openings, specialist shops, or a balanced mix.

Read `references/default-taste-profile.md` for the default preferences and `references/report-spec.md` for the non-negotiable output structure.

## Research and ranking

Use current web/local-search tools when freshness matters. Build a broad candidate list before ranking. Weight food quality and focus first, then destination-specific character, current local critical support, standout dishes, value, and logistics from the anchor. Use recent local sources before generic national listicles.

Always include a Yelp link. Use a numeric Yelp score only if the tool can verify it directly. Never infer or invent it.

For a date-specific guide, cross-check official hours with at least one live signal when practical: reservation inventory, structured business hours, same-day social/closure notice, or another current listing. If the evidence conflicts and cannot be resolved, exclude the place from the active ranking. Do not create a separate correction section.

Prefer places with a specialist mentality and a clear reason to exist. Penalize tourist traps, generic menus, reputation-only picks, and places that are inconvenient without enough culinary payoff.

## Meal-specific companion section

- Dinner: create a **Dessert** section by default.
- Breakfast: create a **Coffee** section by default.
- Lunch: create a **Coffee** section by default.

Research and present the companion section with the same core fields, links, images, verification, ranking logic, and map treatment as the main meal list.

## Build the artifact

Start from the repository template at `template/where-id-eat-template.html` when available. Populate a location-specific header image under the title, quick picks, anchor-centered Leaflet map, comparison tables, detailed recommendation cards, companion section, methodology, source list, and generated timestamp.

Keep the map initially centered on the anchor. Use numbered markers for the meal ranking and distinct markers for dessert/coffee. Link marker popups back to internal report anchors and to live Google Maps directions.

Each recommendation card must contain:

- rank and tailored fit score
- cuisine/specialty and standout reason
- image with alt text and credit
- spend estimate
- distance and practical travel time from anchor
- requested-day hours
- availability verification status
- solo/walk-in/reservation guidance
- specific order suggestions
- current local/critical signal
- official Website
- Menu when available
- Directions from anchor
- Yelp
- local editorial source
- Reservation when relevant

Do not include handwritten-note analysis, a local-list-check section, or an "Important correction: unavailable tonight" section. The active rankings should already reflect the availability check.

## Final checks

Run `scripts/validate_report.py <report.html>` and fix every issue. Confirm the companion section is substantive rather than a token list. Confirm every internal anchor resolves. Confirm remote images have alt text and an onerror fallback. If live URL testing is available, test the hero image and recommendation image URLs before delivery.
