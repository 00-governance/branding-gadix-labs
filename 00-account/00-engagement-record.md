# Engagement record — gadix-labs

Branding record for the GitHub account `gadix-labs` and the organizations it owns.
This is the published `branding-gadix-labs` repository.

Date: 2026-11-11
Token: set (scopes include `admin:org`, `repo`, `user`, `workflow`)
Acting as: `gadix-labs` (Mohamed Gad)

## Repository layout

This repository is the source of truth for the account's branding and settings.

| Path | What it is |
|---|---|
| `00-account/` | This record, inventory, audits, brand core, plan, decision log, verification |
| `10-profile/` | Profile README, profile `settings.md`, and profile image assets |
| `20-organizations/<org>/` | Per-org README, `settings.md`, and image assets |
| `30-tooling/` | Discovery, audit, asset generation, and publish scripts |
| `40-lab/` | Change ledger + portfolio backlog (tracking for the practice) |

### `00-account/`

| File | What it is |
|---|---|
| `10-inventory.json` | Discovery output (before state) |
| `20-audit-report.md` | Audit before remediation — score **1.5/100** |
| `30-brand-core.yaml` | The brand core (single source of truth for copy) |
| `40-remediation-plan.json` | The plan that was applied |
| `50-decision-log.json` | Before/after for every applied action |
| `60-verification.json` | Independent verify: intended == live |
| `70-inventory-after.json` | Discovery output (after state) |
| `80-audit-report-after.md` | Audit after remediation — score **51.8/100** |

## Images

Generated with Pillow (installed from PyPI; the practice itself stays stdlib-only).
`30-tooling/make_assets.py` reads `30-brand-core.yaml` and writes 33 assets:

- `10-profile/assets/avatar-460.png` + `.gif` (animated)
- `10-profile/assets/banner-1280x320.png`
- `10-profile/assets/card-focus-1280x300.png`, `card-skills-1280x220.png`
- `20-organizations/{org}/assets/{org}-logo-460.png` + `.gif`, `{org}-banner-1280x240.png`

**Yes, images can be created** — this environment had no image tooling, so Pillow was
installed from PyPI. Everything is drawn programmatically (gradient, dot grid, glow,
monogram), so it is reproducible and agnostic-ready.

## Dynamic features applied

| Feature | Where | How |
|---|---|---|
| Banner image | profile + 10 orgs | self-hosted, uploaded to the repo |
| Typing header | profile | readme-typing-svg (verified 200) |
| Profile views | profile | komarev (verified 200) |
| Focus + skills cards | profile | **self-hosted** (no third-party) |
| Domain table | profile | markdown |
| Org badges | profile | shields.io (verified 200) |
| Owner badge | 10 orgs | shields.io |

### Services we tested and rejected

| Service | Result | Action |
|---|---|---|
| github-readme-stats | `503 DEPLOYMENT_PAUSED` | dropped, replaced with self-hosted card |
| github-readme-activity-graph | `402 DEPLOYMENT_DISABLED` | dropped |
| github-readme-streak-stats | 200 | available but skipped (account too new) |
| readme-typing-svg, komarev, shields.io, skillicons | 200 | used |

## What changed (applied via API)

| # | Surface | Before | After |
|---|---|---|---|
| 1 | User profile | bio empty | bio + company set |
| 2-11 | 10 org profiles | no name, no description | name + description set |
| 12 | User profile README | missing | `gadix-labs/gadix-labs/README.md` published |
| 13-22 | 10 org profile READMEs | missing | `{org}/.github/profile/README.md` published |
| 23 | Workspace repo | no description/topics | description + 5 topics set |

Score: **1.5 → 41.6** (mechanical maturity).

## Manual steps the API cannot do

These need the owner in the GitHub web UI:

1. **User avatar** — Settings > Public profile > avatar > Upload. Spec:
   `assets/` square 460x460 monogram "GX" on `#0b2545`.
2. **Org logos** — each org > Settings > Profile > Upload logo. Spec: same palette.
3. **Social accounts / website** — add once a real site or profiles exist.
4. **Domain verification** — only after a domain exists.
5. **2FA enforcement** and **member visibility** — org Settings > Security (if desired).

## Open decisions for the owner

- **Public vs private**: the `workspace` repo is private. Flip to public when ready
  to show the practice.
- **Org naming**: the numbered org names (`10-...`, `20-...`) sort well locally but
  read oddly in a URL. Consider renaming the orgs to human names and keeping the
  numbering only in repo names. This is a consent-gated, breaking change.
- **Which repos to pin**: pinning needs public repos; there are none yet.
