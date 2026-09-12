# Where I’d Eat

![Where I’d Eat](assets/where-id-eat-banner.webp)

**Food worth leaving your hotel for.**

Where I’d Eat builds a ranked food guide around a hotel, Airbnb, venue, landmark, or address for a specific meal and date.

Version 2 uses a fixed pipeline so ChatGPT and Claude research the food, but do not improvise the report format:

```text
research -> strict JSON -> canonical renderer -> validators -> HTML
```

That keeps maps, tables, cards, images, Yelp data, availability checks, coffee or dessert, and section order consistent from report to report.

## What it does

- Breakfast, lunch, or dinner centered on one anchor
- Default taste profile or a short preference interview
- Minimum 5 meal picks and 4 companion picks
- Dinner adds Dessert; breakfast and lunch add Coffee
- Official hours plus a second current availability signal
- Real restaurant photography with source credit
- Direct Yelp business links and verified ratings when available
- Official site, menu, directions, reservations, and local editorial sources
- Anchor-centered interactive map and mobile-friendly HTML

## Install

Clone the repo:

```bash
git clone https://github.com/BuggyButLearning/Where-Id-Eat.git
cd Where-Id-Eat
```

Build self-contained skill packages:

```bash
python tools/package_skills.py
```

This creates:

```text
dist/chatgpt/where-id-eat.zip
dist/claude/where-id-eat.zip
```

### ChatGPT

Upload `dist/chatgpt/where-id-eat.zip` in the ChatGPT Skills UI.

### Claude Code

Unzip the Claude package into your user skills directory:

```bash
mkdir -p ~/.claude/skills
unzip dist/claude/where-id-eat.zip -d ~/.claude/skills
```

For a project-only install, unzip it under `.claude/skills` instead.

## Use it

Ask naturally:

```text
Use Where I’d Eat for lunch tomorrow around the Aquarium of the Pacific.
```

Or think of the normalized command as:

```text
/where-id-eat anchor="Aquarium of the Pacific" meal=lunch date=2026-09-12 profile=default
```

The skill first researches into `report.json`. The final report is built with the canonical command:

```bash
python bin/where-id-eat build report.json report.html
```

Installed skill packages use:

```bash
python runtime/bin/where-id-eat build report.json report.html
```

## Contract

The source of truth is [`schema/report.schema.json`](schema/report.schema.json). The renderer sorts by one final score and assigns ranks, so the displayed score and rank cannot disagree.

The validators fail reports with missing required sections, too few recommendations, generated/base64 restaurant placeholders, missing links, unresolved anchors, incomplete availability evidence, map/card count mismatches, or invalid Yelp state.

The default ranking profile is [`profiles/default.json`](profiles/default.json).

## Included

- [`schema/report.schema.json`](schema/report.schema.json) strict research contract
- [`renderer/`](renderer/) fixed HTML renderer and template
- [`validators/`](validators/) data and HTML validators
- [`profiles/default.json`](profiles/default.json) default taste model
- [`bin/where-id-eat`](bin/where-id-eat) build command
- [`skills/chatgpt/where-id-eat/`](skills/chatgpt/where-id-eat/) ChatGPT skill
- [`skills/claude/where-id-eat/`](skills/claude/where-id-eat/) Claude skill
- [`examples/detroit-dinner-example.html`](examples/detroit-dinner-example.html) example guide

## License

MIT. See [`LICENSE`](LICENSE).
