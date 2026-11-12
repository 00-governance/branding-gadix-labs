# Portfolio backlog — from the gadix-labs engagement

Runtime working document. Everything below is a candidate to fold into the
**agnostic** practice under `10-portfolio-github-branding/`. Nothing here is
agnostic yet; each item names the artifact it should become.

Status: **FOLDED** = moved into the practice · **READY** = proven in this engagement
· **DRAFT** = partial · **IDEA** = not started.

> Fold-back completed 2026-11-11. The table below records where each item landed.
> See the ledger's "Iteration 7" for the full mapping.

## Approaches → practice principles

| ID | Approach | Became | Status |
|---|---|---|---|
| A1 | Field vs file surfaces | `20-github-branding-principles.md` §1.3 + rule R1 | **FOLDED** |
| A2 | Special repos carry READMEs | `70-github-api-reference.md` §4.1 + glossary "Special repo" | **FOLDED** |
| A3 | Derive theme from org names | playbook Phase 2 (infer from existing content) | **FOLDED** |
| A4 | Self-host beats third-party | principle P11 | **FOLDED** |
| A5 | Fit branding to real maturity | principle P12 | **FOLDED** |

## Rules → practice standards

| ID | Rule | Became | Status |
|---|---|---|---|
| R1 | Field vs file rule | `60-rules-and-guardrails.md` §4a (R1) | **FOLDED** |
| R2 | Idempotent publish rule | §4a (R2) | **FOLDED** |
| R3 | Assets travel with the repo | §4a (R3) | **FOLDED** |
| R4 | Score, then re-score | playbook Phase 6 (already present) | **FOLDED** |
| R5 | Verify embeds before publish | §4b (R5) + E1 dimension | **FOLDED** |
| R6 | Relative asset paths | §4a (R6) | **FOLDED** |
| R7 | Animation optional and explicit | §4a (R7) | **FOLDED** |
| R8 | Verify a surface before trusting it | §4b (R8) | **FOLDED** |
| R9 | Never invent identity facts | §4b (R9) | **FOLDED** |

## Concepts → practice reference

| ID | Concept | Became | Status |
|---|---|---|---|
| C1 | Mechanical maturity score | `10-dimensions-and-scoring.md` (rewritten) | **FOLDED** |
| C2 | Dynamic profile | `50-content-style-guide.md` (README guidance) | **FOLDED** |
| C3 | Animated identity | rule R7 + assets guidance | **FOLDED** |
| C4 | Asset family | `40-brand-core-guide.md` (asset map) | **FOLDED** |
| C5 | Self-hosted card system | principle P11 + glossary "Card" | **FOLDED** |
| C6 | Identity family | `40-brand-core-guide.md` | **FOLDED** |
| C7 | Honest score (measure content, not presence) | `10-dimensions-and-scoring.md` §1, §5 | **FOLDED** |
| C8 | API vs owner split | `70-github-api-reference.md` + `30-manual-steps.md` | **FOLDED** |

## Missions → practice missions

| ID | Mission | Scope | Status |
|---|---|---|---|
| M1 | Asset generation | brand core → full asset family (PNG + GIF) | **FOLDED** (script exists) |
| M2 | Dynamic README | catalog of dynamic features + "pick N" rule | **FOLDED** (style guide) |
| M3 | Manual upload | checklist for avatar/logo/social/domain | **FOLDED** (`30-manual-steps.md`) |
| M4 | Embed verification | fetch every README image, fail if not 200 | **FOLDED** (E1, `--check-embeds`) |
| M5 | Self-hosted cards | document card generators | **FOLDED** (P11) |
| M6 | Brand core authoring | how to fill the brand core from an account | **FOLDED** (`40-brand-core-guide.md`) |

## Skills to update when folding

- `10-github-account-audit` — **DONE.** `--check-embeds` scores E1; the reference
  `10-dimensions-and-scoring.md` now documents the exact test behind every score.
- `20-github-brand-remediation` — `publish_readme.py` folded; asset pipeline
  (`make_assets.py`, `upload_asset.py`) remains runtime-only (gap 2).
- `30-github-brand-verify` — **DONE.** Embed-health and asset-reachability checks
  added to `10-verification-checklist.md`.

## Known gaps to close before folding

1. ~~Scorer ignores quality.~~ **CLOSED** — `audit.py` is fully mechanical and
   quality-aware (README content, assets, alt text, embed health); 100.0 is reachable.
2. **Asset pipeline is runtime-only.** `make_assets.py` and `upload_asset.py` live
   in `runtime/`. Generalize (no hardcoded orgs) and move to the practice. Still open.
3. **Pillow is a new dependency.** The practice was stdlib-only. Decide: vendor a
   pure-Python path, or document Pillow as an optional dependency of the assets
   mission. Still open.
4. **Owner-only surfaces have no API.** Avatars, org logos, org rename, and pinning
   are web-UI only. **CLOSED** — the manual runbook (`30-manual-steps.md`) ships and
   the audit never assumes they are set.

## Iteration 3 additions to fold

| ID | Item | Became | Status |
|---|---|---|---|
| A6 | Self-host beats third-party | principle P11 | **FOLDED** |
| R8 | Verify a surface before trusting it | §4b (R8) | **FOLDED** |
| R9 | Never invent identity facts | §4b (R9) + P12 | **FOLDED** |
| C7 | Honest score (measure content, not presence) | scoring reference §1, §5 | **FOLDED** |
| C8 | API vs owner split | API reference + manual steps | **FOLDED** |
| M7 | Manual-steps runbook | remediation reference | **FOLDED** |
| M8 | Embed-health check | audit flag (`--check-embeds`), E1 | **FOLDED** |

