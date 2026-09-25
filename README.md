# Where I’d Eat

![Where I’d Eat](assets/where-id-eat-banner.webp)

**Food worth leaving your hotel for.**

Where I’d Eat builds a ranked food guide around a hotel, Airbnb, venue, landmark, or address for a specific meal and date.

Version 2 uses a fixed pipeline so ChatGPT and Claude research the food, but do not improvise the report format:

```text
research -> strict JSON -> canonical renderer -> validators -> HTML
```

That keeps maps, tables, cards, photography, Yelp data, availability checks, coffee or dessert, and section order consistent from report to report.

## What it does

- Breakfast, lunch, or dinner centered on one anchor
- Default taste profile or a short preference interview
- Minimum 5 meal picks and 4 companion picks
- Dinner adds Dessert; breakfast and lunch add Coffee
- Official hours plus a second current availability signal
- Real restaurant/food/exterior photography with source credit whenever a usable photo can be verified
- Real location or destination-food photography for the hero
- Direct Yelp business links and verified ratings when available
- Official site, menu, directions, reservations, and local editorial sources
- Anchor-centered map using MapLibre + PMTiles when available, with a fully embedded offline proximity-map fallback for downloaded HTML
- No direct runtime requests to OpenStreetMap tile servers

Real photography remains the default. The image search ladder now explicitly requires the official restaurant site, Yelp, and at least one other independent current source before fallback. If Yelp blocks automated access, the attempted Yelp business or photo URL is still recorded as part of the search evidence. If a usable photo cannot be found after those checks, the report may use a simple generated SVG fallback for that recommendation. The fallback is allowed only when the research evidence is recorded in the JSON contract.

## Install

### Claude app (claude.ai, Claude Desktop, Claude mobile)

1. Download **[where-id-eat-claude.zip](https://github.com/BuggyButLearning/Where-Id-Eat/releases/latest/download/where-id-eat-claude.zip)**. Leave it zipped.
2. In Claude, open **Settings → Capabilities** and make sure **Code execution and file creation** is turned on. The skill needs it to build the report.
3. In the **Skills** section of the same page, click **Upload skill** and pick the zip.
4. Make sure the **where-id-eat** toggle is on.

Skills sync to your account, so uploading once on the web also covers the desktop and mobile apps. Nothing needs to be registered and no API key is required. If you do not see a Skills section, your plan or organization does not have Skills turned on. On Team and Enterprise plans, an owner may need to enable skills first, and can also provision this one for everyone.

To update, download the latest zip, delete the old skill, and upload again.

### Claude Code

Install it as a plugin straight from this repo:

```text
/plugin marketplace add BuggyButLearning/Where-Id-Eat
/plugin install where-id-eat@where-id-eat
```

Get updates with `/plugin marketplace update where-id-eat`.

Or, without the plugin system, unzip the same package into your skills folder:

```bash
mkdir -p ~/.claude/skills
unzip where-id-eat-claude.zip -d ~/.claude/skills
```

For a project-only install, unzip it under `.claude/skills` instead.

### ChatGPT

Download **[where-id-eat-chatgpt.zip](https://github.com/BuggyButLearning/Where-Id-Eat/releases/latest/download/where-id-eat-chatgpt.zip)** and upload it in the ChatGPT Skills UI.

### Build the packages yourself

```bash
git clone https://github.com/BuggyButLearning/Where-Id-Eat.git
cd Where-Id-Eat
python tools/package_skills.py
```

This creates `dist/claude/where-id-eat.zip` and `dist/chatgpt/where-id-eat.zip`. Pushing a `v*` tag builds the same zips and attaches them to a GitHub release.

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

The validators fail reports with missing required sections, too few recommendations, undocumented image fallbacks, missing links, unresolved anchors, incomplete availability evidence, map/card count mismatches, legacy Leaflet/OpenStreetMap runtime tile maps, missing offline map fallback, or invalid Yelp state. Even the `render` command validates input before rendering.

Do not use old generated HTML as the source for a new report or map experiment. Use schema-valid JSON or research again so legacy placeholders cannot leak into current output.

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
