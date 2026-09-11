# Where I’d Eat

![Where I’d Eat banner](assets/where-id-eat-banner.png)

**Personalized, location-centered food guides that rank what is actually worth eating near where you are staying.**

Where I’d Eat is a reusable research and reporting skill for building practical food guides around a central location such as a hotel, Airbnb, conference venue, neighborhood, or address.

Instead of dumping a long list of popular restaurants, it researches the city, checks what is open for the requested meal and date, weighs trusted local sources, and produces a ranked guide with the details you actually need to make a decision.

## What it makes

Each guide can include:

- A central location, usually a hotel or other trip anchor
- Ranked restaurant recommendations
- A hotel-centered interactive map
- Photos for each recommendation
- Current hours and same-day availability checks
- Price range and realistic solo food spend
- Distance and practical travel time from the anchor
- What to order
- Reservation and walk-in guidance
- Official website and menu links
- Yelp links
- Local editorial sources such as Eater, local publications, and trusted critics
- Google Maps directions
- A full source section
- A separate dessert section for dinner
- A separate coffee section for breakfast and lunch
- Responsive HTML that works well on a phone

## The point

Most food discovery tools optimize for volume, popularity, proximity, or advertising. Where I’d Eat is designed around a narrower question:

> If I were staying here, where would I actually eat?

The default taste profile favors strong execution, focused menus, standout dishes, destination-specific food, local critical support, sensible value, and places worth making a short trip for.

It intentionally penalizes generic restaurants that are merely convenient, old reputation that is no longer supported by current signals, and recommendations that do not fit the requested meal.

## Meal behavior

| Meal | Primary guide | Secondary section |
| --- | --- | --- |
| Breakfast | Breakfast recommendations | Coffee |
| Lunch | Lunch recommendations | Coffee |
| Dinner | Dinner recommendations | Dessert |

If the meal is not specified, the skill asks first.

The skill can use the included default taste profile or interview the user for different preferences, budget, dietary needs, travel tolerance, and dining style.

## Availability is part of the research

A restaurant should not appear as an active recommendation simply because its normal weekly hours say it is open.

For date-specific guides, the skill checks current official hours and, when possible, same-day reservation inventory, closure notices, or other current signals. If a place appears closed or cannot be verified with reasonable confidence, it is removed or clearly flagged before the guide is produced.

This check is part of the recommendation process rather than a correction section added afterward.

## Example

The repository includes a complete Detroit dinner guide centered on a downtown hotel:

[`examples/detroit-dinner-example.html`](examples/detroit-dinner-example.html)

It demonstrates the intended output format, including restaurant rankings, map, images, source links, travel estimates, ordering advice, and a full dessert section.

## Included skills

### ChatGPT

`skills/chatgpt/where-id-eat/`

Includes:

- `SKILL.md`
- OpenAI agent metadata
- Default taste profile
- Shared report specification
- HTML validation script

### Claude

`skills/claude/where-id-eat/`

Includes:

- `SKILL.md`
- Default taste profile
- Shared report specification
- HTML validation script

The two versions are tuned for their respective agent environments while following the same research and report rules.

## Repository structure

```text
where-id-eat/
├── README.md
├── assets/
│   └── where-id-eat-banner.png
├── examples/
│   └── detroit-dinner-example.html
├── template/
│   └── where-id-eat-template.html
└── skills/
    ├── chatgpt/
    │   └── where-id-eat/
    │       ├── SKILL.md
    │       ├── agents/
    │       │   └── openai.yaml
    │       ├── references/
    │       │   ├── default-taste-profile.md
    │       │   └── report-spec.md
    │       └── scripts/
    │           └── validate_report.py
    └── claude/
        └── where-id-eat/
            ├── SKILL.md
            ├── references/
            │   ├── default-taste-profile.md
            │   └── report-spec.md
            └── scripts/
                └── validate_report.py
```

## Default taste profile

The included default profile is built for someone who:

- Cares more about execution than trendiness
- Likes restaurants with a clear point of view
- Values one exceptional dish more than a huge menu
- Wants food that feels specific to the city
- Uses Yelp as a useful signal, not the sole authority
- Gives strong weight to respected local writers and publications
- Is willing to travel a little for a meaningfully better meal
- Prefers good value over either cheapness or luxury for its own sake
- Wants practical information, not just restaurant descriptions

The profile is only a default. The skill can interview the user and replace it.

## Output format

The preferred output is a self-contained HTML guide with:

- Strong header image
- Fast comparison table
- Internal anchor navigation
- Interactive map centered on the trip anchor
- Detailed cards for each recommendation
- Clearly separated meal and dessert or coffee recommendations
- Mobile-friendly layout
- Print-friendly styles
- Image credits
- Source links

Use `template/where-id-eat-template.html` as the starting point when building a new report.

## Validation

Each skill includes `scripts/validate_report.py` to catch common report problems before delivery, including missing sections, broken internal anchors, malformed structure, and other output issues.

Example:

```bash
python skills/chatgpt/where-id-eat/scripts/validate_report.py examples/detroit-dinner-example.html
```

## Suggested repository description

> Personalized food guides centered on where you’re staying, with ranked picks, current availability, maps, photos, local sources, Yelp links, coffee, and dessert.

## Status

Early version. The core report format, default taste profile, ChatGPT skill, Claude skill, reusable template, and Detroit example are included.
