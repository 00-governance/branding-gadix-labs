# Portfolio backlog — from the gadix-labs engagement

Runtime working document. Everything below is a candidate to fold into the
**agnostic** practice under `10-portfolio-github-branding/`. Nothing here is
agnostic yet; each item names the artifact it should become.

Status: **READY** = proven in this engagement · **DRAFT** = partial · **IDEA** = not
started.

## Approaches → practice principles

| ID | Approach | Becomes | Status |
|---|---|---|---|
| A1 | Field vs file surfaces | a principle in `20-principles` | READY |
| A2 | Special repos carry READMEs | API reference note | READY |
| A3 | Derive theme from org names | playbook step (discovery) | READY |
| A4 | Self-host beats third-party | principle + embed-verify rule | READY |
| A5 | Fit branding to real maturity | principle (honesty) | READY |

## Rules → practice standards

| ID | Rule | Becomes | Status |
|---|---|---|---|
| R1 | Field vs file rule | standard | READY |
| R2 | Idempotent publish rule | standard | READY |
| R3 | Assets travel with the repo | standard | READY |
| R4 | Score, then re-score | standard | READY |
| R5 | Verify embeds before publish | standard | READY |
| R6 | Relative asset paths | standard | READY |
| R7 | Animation optional and explicit | standard | READY |

## Concepts → practice reference

| ID | Concept | Becomes | Status |
|---|---|---|---|
| C1 | Mechanical maturity score | audit reference | READY |
| C2 | Dynamic profile | remediation reference | READY |
| C3 | Animated identity | assets reference | READY |
| C4 | Asset family | assets reference | READY |
| C5 | Self-hosted card system | assets reference | READY |
| C6 | Identity family | assets reference | READY |

## Missions → practice missions

| ID | Mission | Scope | Status |
|---|---|---|---|
| M1 | Asset generation | brand core → full asset family (PNG + GIF) | READY (script exists) |
| M2 | Dynamic README | catalog of dynamic features + "pick N" rule | DRAFT |
| M3 | Manual upload | checklist for avatar/logo/social/domain | DRAFT |
| M4 | Embed verification | fetch every README image, fail if not 200 | IDEA |
| M5 | Self-hosted cards | document card generators | READY (script exists) |
| M6 | Brand core authoring | how to fill the brand core from an account | DRAFT |

## Skills to update when folding

- `10-github-account-audit` — add "dynamic README quality" and "embed health" to the
  score. Today the score did not move when we added the dynamic profile, because the
  scorer only checks presence, not quality. This is a known gap.
- `20-github-brand-remediation` — fold in `publish_readme.py` (done) and the asset
  pipeline (`make_assets.py`, `upload_asset.py`).
- `30-github-brand-verify` — add the embed-health check and an asset-reachability
  check.

## Known gaps to close before folding

1. ~~Scorer ignores quality.~~ **CLOSED** — `audit.py` is now fully mechanical and
   quality-aware (README content, assets, alt text, embed health); 100.0 is reachable.
2. **Asset pipeline is runtime-only.** `make_assets.py` and `upload_asset.py` live
   in `runtime/`. Generalize (no hardcoded orgs) and move to the practice.
3. **Pillow is a new dependency.** The practice was stdlib-only. Decide: vendor a
   pure-Python path, or document Pillow as an optional dependency of the assets
   mission.
4. **Owner-only surfaces have no API.** Avatars, org logos, org rename, and pinning
   are web-UI only. The practice must ship the manual runbook
   (`30-manual-steps.md`, done) and the audit must never assume they are set.

## Iteration 3 additions to fold

| ID | Item | Becomes | Status |
|---|---|---|---|
| A6 | Self-host beats third-party | principle | READY |
| R8 | Verify a surface before trusting it | standard | READY |
| R9 | Never invent identity facts | standard | READY |
| C7 | Honest score (measure content, not presence) | audit reference | READY |
| C8 | API vs owner split | remediation reference | READY |
| M7 | Manual-steps runbook | remediation reference | READY |
| M8 | Embed-health check | audit flag (`--check-embeds`) | READY |

