# Where I’d Eat

![Where I’d Eat](assets/where-id-eat-banner.webp)

**Food worth leaving your hotel for.**

Where I’d Eat turns a hotel, Airbnb, venue, or address into a ranked food guide for a specific meal and date.

## What it does

- Asks whether you want **breakfast, lunch, or dinner**
- Uses the included taste profile by default, or interviews you to customize it
- Ranks places by food quality, distinctiveness, local credibility, value, and travel payoff
- Checks current hours and a second live signal when practical before recommending a place
- Produces a mobile-friendly HTML guide with maps, photos, prices, what to order, Yelp, official sites, menus, reservations, directions, and local editorial sources

| Meal | Companion section |
| --- | --- |
| Breakfast | Coffee |
| Lunch | Coffee |
| Dinner | Dessert |

The coffee or dessert section is researched and ranked with the same standards as the main meal guide.

## Install

Clone the repo first:

```bash
git clone https://github.com/BuggyButLearning/Where-Id-Eat.git
cd Where-Id-Eat
```

### ChatGPT

Where ChatGPT Skills are available, OpenAI supports uploading a skill from **Plugins → Skills → Create → Upload from your computer**.

Package the ChatGPT version:

```bash
cd skills/chatgpt
zip -r where-id-eat.zip where-id-eat
```

Upload `skills/chatgpt/where-id-eat.zip` in the Skills UI.

### Claude Code

Install for your user account:

```bash
mkdir -p ~/.claude/skills
cp -R skills/claude/where-id-eat ~/.claude/skills/
```

Or install only for the current project:

```bash
mkdir -p .claude/skills
cp -R skills/claude/where-id-eat .claude/skills/
```

## Use it

Ask naturally. For example:

```text
Use Where I’d Eat for dinner tomorrow near my hotel in Portland.
```

```text
Build me a lunch guide around the convention center. Interview me about my tastes first.
```

The skill will resolve the anchor location, date, meal, and preference mode before researching.

## What’s included

- [`skills/chatgpt/where-id-eat/`](skills/chatgpt/where-id-eat/) — ChatGPT version
- [`skills/claude/where-id-eat/`](skills/claude/where-id-eat/) — Claude version
- [`template/where-id-eat-template.html`](template/where-id-eat-template.html) — reusable report template
- [`examples/detroit-dinner-example.html`](examples/detroit-dinner-example.html) — example dinner guide

The default taste profile favors focused restaurants, standout dishes, food specific to the destination, current local critical support, good value, and places worth a short trip. The skill can replace that profile with a short preference interview.

## Validation

Before delivery, generated reports should pass the included validator:

```bash
python skills/chatgpt/where-id-eat/scripts/validate_report.py examples/detroit-dinner-example.html
```

## License

MIT. See [`LICENSE`](LICENSE).
