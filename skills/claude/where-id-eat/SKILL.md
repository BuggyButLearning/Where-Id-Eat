---
name: where-id-eat
description: Build polished, location-centered restaurant guides for travelers, with ranked meal recommendations, same-day availability verification, hotel-centered maps, images, price and distance tables, Yelp and official links, and a full dessert or coffee section. Use this skill whenever a user asks where to eat on a trip, wants restaurant recommendations near a hotel or landmark, asks for breakfast/lunch/dinner ideas in a city, wants a dining itinerary or food guide, or asks to turn restaurant research into a reusable HTML report. Prefer this skill even when the user only asks for a short list if a location-centered guide would materially help.
---

# Where I’d Eat

Create a traveler-friendly HTML dining guide centered on one anchor such as a hotel, conference venue, attraction, neighborhood, or address.

## First interaction

Collect only the information that materially changes the result:

1. Resolve the central anchor and target date. If already supplied, do not ask again.
2. Ask which meal the user wants: **breakfast, lunch, or dinner**. If they want multiple meals, generate separate ranked sections or separate reports.
3. Ask whether to use the default taste profile or run a short preference interview. Use the default profile unless the user chooses the interview.
4. If the user chooses the interview, ask concise questions about budget, maximum ride time, cuisines or foods to seek/avoid, dietary constraints, reservation tolerance, and whether they prefer iconic local institutions, newer openings, specialists, or a mixture.

Read `references/default-taste-profile.md` for the default ranking preferences. Read `references/report-spec.md` before building the final report.

## Research workflow

1. Establish a candidate set wider than the final ranking. Search recent local editorial sources, respected critics, official restaurant sites, and current community review signals.
2. Favor local publications such as Eater city sites, Infatuation city guides, local newspapers, city magazines, chefs/critics, and high-quality local food writers.
3. Treat Yelp as a useful community signal and always include a Yelp link, but never fabricate a Yelp rating. If an exact Yelp score is not reliably available, omit the numeric claim.
4. Verify official hours and current menu information.
5. For a specific day, perform the availability check before ranking: cross-check official hours with a booking platform, live business listing, or same-day closure notice when practical. If evidence conflicts and cannot be resolved, exclude the venue from the active ranking.
6. Estimate travel from the anchor. Favor walking when practical, but allow a short ride when the food improvement is meaningful.
7. Rank by fit using the default taste profile or the user's interview adjustments. Do not simply sort by star rating.
8. For dinner, research dessert destinations with the same rigor as restaurants. For breakfast or lunch, research coffee with the same rigor as the meal list.

## Output rules

Use the repository template at `template/where-id-eat-template.html` as the visual and structural baseline when available. Preserve its dark responsive layout, sticky anchors, comparison tables, detailed cards, interactive Leaflet map, image credits, and source section.

Make the map center the anchor on initial load. Do not auto-fit the entire city. Main meal markers should match ranking numbers. Dessert or coffee markers should use a distinct marker style.

Every recommendation card must include image, score, spend, distance, practical travel time, hours, same-day verification, solo/reservation strategy, why it made the cut, specific orders, local signal, Website, Menu when available, Directions, Yelp, local editorial source, and Reservation when relevant.

Do not include a handwritten-note section, a local-list-check section, or an "Important correction" / closed-place appendix. Availability checking belongs inside the research process and visible status fields. Closed or unresolved candidates are omitted from active rankings.

For dinner, default the secondary section to **Dessert**. For breakfast or lunch, default it to **Coffee**. Make that section nearly as useful as the main meal section, not an afterthought.

## Validation

After writing the HTML, run `scripts/validate_report.py <report.html>`. Fix every reported issue. Also inspect for broken image URLs when the environment can test them. Ensure every internal anchor resolves and every recommendation has a Yelp, official website, and directions link.
