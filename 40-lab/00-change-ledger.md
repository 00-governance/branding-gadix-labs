# Branding change ledger — gadix-labs

Runtime log. Every branding decision, approach, rule, and concept we invent during
this engagement is recorded here so it can later be **folded back into the agnostic
practice** (`10-portfolio-github-branding/`). Nothing here is agnostic yet; this is
the raw material.

Legend: **APPLIED** = live on GitHub · **MANUAL** = needs the owner · **IDEA** = not
done yet · **FOLD** = ready to move into the practice.

## Iteration 1 — 2026-11-11

### Changes applied (API)

| # | Surface | Change | Status |
|---|---|---|---|
| 1 | User profile | bio + company | APPLIED |
| 2-11 | 10 org profiles | name + description | APPLIED |
| 12 | User profile README | `gadix-labs/gadix-labs/README.md` | APPLIED |
| 13-22 | 10 org profile READMEs | `{org}/.github/profile/README.md` | APPLIED |
| 23 | Workspace repo | description + 5 topics | APPLIED |

### Approaches discovered

- **A1 · Two-surface model.** A GitHub account has two independent branding
  surfaces: *fields* (name, bio, company, org name/description — set via API) and
  *files* (profile README, org profile README — set by publishing to a special
  repo). Any audit or remediation must treat them separately. → FOLD
- **A2 · Special repos are the README mechanism.** User profile README lives in
  `<login>/<login>` (public repo named after the login). Org profile README lives in
  `<org>/.github/profile/README.md`. This is not obvious and is the single biggest
  cause of "why is my profile blank". → FOLD
- **A3 · Derive the theme from the org names.** We did not ask for a brand; the org
  names (`k8s`, `gitops`, `ai`) already implied the theme (Kubernetes/GitOps/AI).
  Reading the portfolio is cheaper and truer than interviewing the owner. → FOLD

### Rules invented

- **R1 · Field vs file rule.** If a surface is a field, set it via API. If it is a
  file, publish it. Never try to PATCH a README.
- **R2 · Idempotent publish rule.** Publishing must create-or-update. A fresh repo
  (auto_init) can 404 until its default branch exists, so retry the first read.
- **R3 · Assets travel with the repo.** A README that references a local image
  (`assets/banner.png`) must have that image uploaded to the same repo first, or the
  image is broken. Relative paths + committed asset = portable.
- **R4 · Score, then re-score.** Every remediation ends with a fresh audit. We
  measured 1.5 → 29.1 → 41.6, which proves the changes landed.

### Concepts invented

- **C1 · Mechanical maturity score.** A 0-100 score computed from surface
  presence/quality, so progress is a number, not a feeling.
- **C2 · Dynamic profile.** A profile that *renders* live data (stats, streak,
  activity graph, profile views, typing header) reads as active and modern. Static
  text reads as abandoned.
- **C3 · Animated identity.** A static avatar looks like everyone else's. A subtle
  animated avatar/logo (moving glow) is memorable and costs nothing to host.
- **C4 · Asset family.** One generator emits avatar + logo + banner for every
  identity, from one palette, so the whole account looks like one family.

### Missions this suggests (portfolio backlog)

- **M1 · Image/asset generation mission.** Turn "make_assets.py" into a documented,
  agnostic mission: input = brand core, output = full asset family (PNG + GIF).
- **M2 · Dynamic README mission.** A reusable catalog of dynamic features (typing,
  badges, stats, streak, activity, skill icons) with exact embed snippets and a
  "pick N" rule so profiles do not become badge walls.
- **M3 · Manual-upload mission.** A checklist mission for the surfaces the API
  cannot touch (avatar, org logo, social, domain), with exact click paths.

### Open questions for the owner

- Avatars/logos need a web-UI upload (API cannot). Assets are ready in
  `assets/10-user/` and `assets/20-orgs/`. Which do you prefer: **static PNG** or
  **animated GIF**?
- Org names (`10-...`, `20-...`) sort well but read oddly in URLs. Rename later?

## Iteration 2 — 2026-11-11 (images + dynamic profiles)

### Changes applied (API)

| # | Surface | Change | Status |
|---|---|---|---|
| 24 | User profile README | rebuilt with banner + cards + typing + badges | APPLIED |
| 25 | Profile repo | uploaded `banner-1280x320.png`, `card-focus-1280x300.png`, `card-skills-1280x220.png` | APPLIED |
| 26-35 | 10 org profile READMEs | rebuilt with per-org banner + owner badge | APPLIED |
| 36-45 | 10 org `.github` repos | uploaded `profile/assets/banner-1280x240.png` each | APPLIED |
| 46 | 33 brand assets generated | avatars, logos, banners (PNG + animated GIF) | LOCAL |

### New approach discovered

- **A4 · Self-host beats third-party.** We embedded four third-party services and
  tested them. Two were **dead**: `github-readme-stats` returned `503
  DEPLOYMENT_PAUSED`, and `github-readme-activity-graph` returned `402
  DEPLOYMENT_DISABLED`. A broken image reads as neglect. We replaced both with
  self-hosted generated cards. Rule: **always HTTP-check an embed before shipping
  it; prefer an asset you control.** → FOLD
- **A5 · Empty account + stat cards = empty cards.** The account has 2 public repos
  and 0 followers. Third-party stat cards would render zeros or blanks, which is
  worse than no card. Branding must fit the account's real maturity, not a template.

### New rules invented

- **R5 · Verify embeds.** Every external image URL in a README must be fetched and
  confirmed `200` before publish. Record the check.
- **R6 · Relative asset paths.** Reference repo-local images with a relative path
  (`assets/x.png`) and commit the asset to the same repo. No absolute
  `raw.githubusercontent` URLs that break on rename.
- **R7 · Animation is optional and explicit.** Ship both a static PNG and an
  animated GIF for avatars/logos; the owner chooses. Never make the only option one
  the API cannot install.

### New concepts invented

- **C5 · Card system.** Self-hosted "focus" and "skills" cards in the brand palette
  replace third-party stat widgets with content we fully control.
- **C6 · Identity family.** Avatar, logo, and banner are generated from one palette
  and one motif (dot grid + moving glow + spaced monogram) so every surface looks
  related.

### Missions added to the backlog

- **M4 · Embed-verification mission.** A mission that fetches every external image
  in a README and fails the run if any is not `200`. (See M2.)
- **M5 · Self-hosted card mission.** Document `make_focus_card` / `make_skill_card`
  as the agnostic replacement for stat widgets.

## Iteration 3 — 2026-11-11 (scorer to max, GIFs, org rename)

### Requests and outcomes

| # | Request | Outcome |
|---|---|---|
| R1 | Increase the scorer to the maximum | DONE — scorer is now fully mechanical (0 TBD) and 100.0 is reachable |
| R2 | Animated GIFs | DONE — GIFs exist and are valid; upload needs the web UI (runbook written) |
| R3 | Rename orgs now | BLOCKED — no API; only an owner can do it in the web UI |

### R1 — the scorer

The old scorer left 35 of 57 surfaces as `TBD`, so the score could never reach 100.
Rewrote `scripts/audit.py` so every dimension is scored from real content:

- **Quality-aware README scoring.** A3/O3 now read the README text and the committed
  assets. A README with images, alt text, and committed assets scores 4; one with no
  images scores 2.
- **Honest avatar/logo detection (a real bug fixed).** GitHub no longer puts
  `identicons` in the avatar URL, so the old check reported every default as
  "custom". Added a stdlib PNG decoder that counts unique colours: 2 colours =
  default identicon. This **dropped the score from 63.5 to 44.9** by removing a false
  positive — the honest number.
- **Embed health (E1).** `--check-embeds` HTTP-checks every external image and fails
  the run if any is not < 400.
- **Reachable ceiling.** Fixed three dimensions (A4/O4 pins, A6 settings) that could
  never reach 4. A simulated fully-branded account now scores **100.0** (verified).
- **No TBD.** 0 judgment calls remain.

Score path: 41.6 (old, 35 TBD) → 63.5 (first pass) → 44.9 (honest avatars) → 51.8
(after API improvements).

### R1 — API improvements applied

| # | Surface | Change | Status |
|---|---|---|---|
| 47 | User profile | website set to the profile URL | APPLIED |
| 48-57 | 10 orgs | website set to each org's GitHub page | APPLIED |

Reverted two fabricated values: I briefly set a location ("Cairo, Egypt") and
`hireable: true`. Neither is in the brand core, so I removed them rather than invent
personal facts.

### R2 — animated GIFs

Confirmed valid: `avatar-460.gif` = 24 frames, each `logo-460.gif` = 20 frames, all
looping. GitHub accepts animated GIF for avatars and org logos. Upload is web-UI only
→ see the new `30-manual-steps.md` in the remediation skill.

### R3 — org rename is not possible via API

Evidence:

- `PATCH /orgs/org-omnilabs-ai {"login":"omnilabs-ai"}` returned the **unchanged**
  login — the field is silently ignored.
- No `updateOrganization` mutation exists in the GraphQL schema (268 mutations
  checked).
- The browser has no GitHub session (logged out), so the web UI is not reachable
  from here either.

The official path is: org **Settings → Danger zone → Rename organization**, owner
only. That is now step 3 of `30-manual-steps.md`.

Availability check for shorter names (bare names are mostly taken):

| Proposed | Available? |
|---|---|
| vanilla-k8s, workload-deployments, inference-analysis, github-branding | AVAILABLE |
| governance, gitops, cluster-automation, ai-governance, cheaper-inference, omnilabs-ai | TAKEN |
| gadix-governance, gadix-gitops, gadix-k8s, gadix-ai | AVAILABLE |

A fully available, on-brand set exists (`gadix-*`), but a rename is destructive (the
old name becomes claimable, links break) and owner-only. It needs explicit approval
and the owner's hands.

### New rules and concepts

- **R8 · Verify a surface before trusting it.** The avatar check was wrong for weeks
  of API changes; a "custom" flag that is not measured is a lie. Measure pixels.
- **R9 · Never invent identity facts.** Location and hireable were reverted; they are
  the owner's to state.
- **C7 · Honest score.** A score that only measures presence inflates; a score that
  measures content tells the truth. The honest number is lower and more useful.
- **C8 · API vs owner split.** Every surface is either API-settable or owner-only.
  The runbook names which, so nothing is silently skipped.

### Still blocked on the owner

- Upload the GIF avatar and 10 GIF logos (steps 1-2 of the runbook).
- Pin repos for the profile and each org (step 4).
- Rename orgs, if wanted (step 3) — approve the `gadix-*` set or another.
- Verify an org domain (step 5) — the only path to O5 = 4.
- Turn on **Include private contributions on my profile** (new step 6) — shows
  private contribution counts without revealing repos or orgs.

## Iteration 4 — 2026-11-11 (private contributions rule + API-reference corrections)

### Request

Add a branding rule: set **Include private contributions on my profile** to true
(profile contribution graph, achievements, and activity overview show private
contributions without revealing any repository or organization).

### Investigation

Confirmed there is **no API** for this setting:

- Not present in any field of `GET /user`.
- `PATCH /user {"include_private_contributions": true}` returns 200 but does not
  apply the field.
- No matching mutation in the GraphQL schema (`updateUserProfile`, no
  contributions/privacy mutation).

So it is web-UI only, and the practice must treat it as a manual owner step.

### Changes

| File | Change |
|---|---|
| `00-practice/documentation/60-rules-and-guardrails.md` | New section 8 "Discoverability rules": MUST recommend the setting; MUST NOT claim it is on (unreadable). Sections renumbered; one-page summary gained R9. |
| `skills/20-github-brand-remediation/references/30-manual-steps.md` | New section 6 with the exact click path; consent section renumbered to 7. |
| `skills/20-github-brand-remediation/references/10-plan-schema.md` | Added the setting to the manual-actions list. |
| `skills/20-github-brand-remediation/references/20-endpoints-and-fields.md` | New "Include private contributions — manual" section. |
| `skills/30-github-brand-verify/references/10-verification-checklist.md` | New "Private contributions" check (confirm with owner). |
| `skills/10-github-account-audit/scripts/audit.py` | Report now ends with "Manual steps for the owner" including this setting. |
| `00-practice/documentation/70-github-api-reference.md` | Corrected the dimension table and pin/avatar sections. |

### Errors found and fixed while editing

The API reference claimed two GraphQL mutations that **do not exist**:
`updateUserPins` and `updateOrganizationPins`. Both were confirmed absent from the
schema. Repository pinning has **no API at all** — corrected in
`70-github-api-reference.md` and `20-endpoints-and-fields.md`. Also fixed the org
README read path (was `repos/{org}/.github/readme`, the repo-root README; the org
profile README is at `repos/{org}/.github/contents/profile/README.md`).

### Reverted test writes

While probing org fields I set `twitter_username` on `00-governance` as a test;
reverted to `null`. No other test values left behind.




## Iteration 5 — 2026-11-11 (publish the branding repo)

### Request

From now on, each account gets a git repo in `runtime/` named
`branding-<github-account>` and pushed to a designated organization. Do this for
`gadix-labs` and push it to `00-governance`.

### What was built

`runtime/branding-gadix-labs/`, pushed to `00-governance/branding-gadix-labs`.

| Path | Contents |
|---|---|
| `00-account/` | Engagement record, inventory, both audits, brand core, plan, decision log, verification |
| `10-profile/` | Profile README, profile `settings.md`, profile assets (avatar, banner, cards) |
| `20-organizations/<org>/` | One folder per org: `README.md`, `settings.md`, `assets/` |
| `30-tooling/` | discover, audit, ghbrand, make_assets, gen_org_readmes, upload_asset, publish_readme |
| `40-lab/` | Change ledger + portfolio backlog |

### Tooling refactor

The scripts assumed the old flat layout (`assets/10-user`, `assets/20-orgs`,
`30-brand-core.yaml` at the repo root). Refactored to be self-locating:

- `make_assets.py` → `00-account/30-brand-core.yaml`, `10-profile/assets/`,
  `20-organizations/<org>/assets/`. Removed the `--out` flag.
- `gen_org_readmes.py` → reads the core, writes `20-organizations/<org>/README.md`.
- `upload_asset.py` / `publish_readme.py` → import `ghbrand` from beside themselves
  (previously reached into the practice tree by relative path).

Verified: `make_assets.py` reproduces **byte-identical** assets in the new layout,
and `gen_org_readmes.py` reproduces the **published** org READMEs exactly. The
discover → audit toolchain runs end-to-end from the new layout.

### Safety

- Repo `.gitignore` excludes credentials and transient output.
- Scanned for leaks: no private repo names, no members list, no tokens. The only
  email present is the owner's public contact address (already public on the profile).

### Naming convention adopted

`branding-<github-account>` for the repo, `branding-<github-account>` folder under
`runtime/`. Next planned convention: a `governance-<account>` organization holding
the branding repo plus settings docs for all orgs, repos, profile, and preferences.
