# Audit report — gadix-labs

## Summary
- Maturity score (mechanical): 1.5/100
- Surfaces audited: 57
- Judgment calls remaining (TBD): 23
- Owned organizations: 10

## Findings
| ID | Dimension | Surface | Score | Evidence |
|----|-----------|---------|-------|----------|
| F1 | A1 Identity | user profile | 1 | bio missing |
| F2 | A2 Visual identity | user avatar | TBD | avatar is custom; judge legibility at 32px and brand fit |
| F3 | A3 Profile README | profile README | 0 | no profile README (repo <login>/<login> missing or empty) |
| F4 | A4 Pinned repositories | pinned repos | 0 | no pinned repositories |
| F5 | A5 Social proof & links | social accounts | TBD | judge social accounts and contactability |
| F6 | A6 Account settings | account settings | TBD | judge visibility and discoverability |
| F7 | O1 Org identity (40-cluster-automation) | org 40-cluster-automation | 0 | no organization description |
| F8 | O2 Org logo (40-cluster-automation) | org 40-cluster-automation | TBD | logo is custom; judge legibility and brand fit |
| F9 | O3 Org README (40-cluster-automation) | org 40-cluster-automation | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F10 | O4 Org pinned (40-cluster-automation) | org 40-cluster-automation | 0 | no pinned repositories |
| F11 | O5 Org settings (40-cluster-automation) | org 40-cluster-automation | TBD | judge domains, member visibility, default permissions, 2FA |
| F12 | O1 Org identity (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | 0 | no organization description |
| F13 | O2 Org logo (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | TBD | logo is custom; judge legibility and brand fit |
| F14 | O3 Org README (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F15 | O4 Org pinned (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | 0 | no pinned repositories |
| F16 | O5 Org settings (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | TBD | judge domains, member visibility, default permissions, 2FA |
| F17 | O1 Org identity (20-workload-deployments) | org 20-workload-deployments | 0 | no organization description |
| F18 | O2 Org logo (20-workload-deployments) | org 20-workload-deployments | TBD | logo is custom; judge legibility and brand fit |
| F19 | O3 Org README (20-workload-deployments) | org 20-workload-deployments | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F20 | O4 Org pinned (20-workload-deployments) | org 20-workload-deployments | 0 | no pinned repositories |
| F21 | O5 Org settings (20-workload-deployments) | org 20-workload-deployments | TBD | judge domains, member visibility, default permissions, 2FA |
| F22 | O1 Org identity (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | 0 | no organization description |
| F23 | O2 Org logo (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | TBD | logo is custom; judge legibility and brand fit |
| F24 | O3 Org README (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F25 | O4 Org pinned (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | 0 | no pinned repositories |
| F26 | O5 Org settings (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | TBD | judge domains, member visibility, default permissions, 2FA |
| F27 | O1 Org identity (00-governance) | org 00-governance | 0 | no organization description |
| F28 | O2 Org logo (00-governance) | org 00-governance | TBD | logo is custom; judge legibility and brand fit |
| F29 | O3 Org README (00-governance) | org 00-governance | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F30 | O4 Org pinned (00-governance) | org 00-governance | 0 | no pinned repositories |
| F31 | O5 Org settings (00-governance) | org 00-governance | TBD | judge domains, member visibility, default permissions, 2FA |
| F32 | O1 Org identity (org-cheaper-inference) | org org-cheaper-inference | 0 | no organization description |
| F33 | O2 Org logo (org-cheaper-inference) | org org-cheaper-inference | TBD | logo is custom; judge legibility and brand fit |
| F34 | O3 Org README (org-cheaper-inference) | org org-cheaper-inference | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F35 | O4 Org pinned (org-cheaper-inference) | org org-cheaper-inference | 0 | no pinned repositories |
| F36 | O5 Org settings (org-cheaper-inference) | org org-cheaper-inference | TBD | judge domains, member visibility, default permissions, 2FA |
| F37 | O1 Org identity (org-omnilabs-ai) | org org-omnilabs-ai | 0 | no organization description |
| F38 | O2 Org logo (org-omnilabs-ai) | org org-omnilabs-ai | TBD | logo is custom; judge legibility and brand fit |
| F39 | O3 Org README (org-omnilabs-ai) | org org-omnilabs-ai | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F40 | O4 Org pinned (org-omnilabs-ai) | org org-omnilabs-ai | 0 | no pinned repositories |
| F41 | O5 Org settings (org-omnilabs-ai) | org org-omnilabs-ai | TBD | judge domains, member visibility, default permissions, 2FA |
| F42 | O1 Org identity (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | 0 | no organization description |
| F43 | O2 Org logo (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | TBD | logo is custom; judge legibility and brand fit |
| F44 | O3 Org README (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F45 | O4 Org pinned (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | 0 | no pinned repositories |
| F46 | O5 Org settings (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | TBD | judge domains, member visibility, default permissions, 2FA |
| F47 | O1 Org identity (org-ai-governance) | org org-ai-governance | 0 | no organization description |
| F48 | O2 Org logo (org-ai-governance) | org org-ai-governance | TBD | logo is custom; judge legibility and brand fit |
| F49 | O3 Org README (org-ai-governance) | org org-ai-governance | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F50 | O4 Org pinned (org-ai-governance) | org org-ai-governance | 0 | no pinned repositories |
| F51 | O5 Org settings (org-ai-governance) | org org-ai-governance | TBD | judge domains, member visibility, default permissions, 2FA |
| F52 | O1 Org identity (portfolio-git-hub-branding) | org portfolio-git-hub-branding | 0 | no organization description |
| F53 | O2 Org logo (portfolio-git-hub-branding) | org portfolio-git-hub-branding | TBD | logo is custom; judge legibility and brand fit |
| F54 | O3 Org README (portfolio-git-hub-branding) | org portfolio-git-hub-branding | 0 | no organization profile README ({org}/.github/profile/README.md) |
| F55 | O4 Org pinned (portfolio-git-hub-branding) | org portfolio-git-hub-branding | 0 | no pinned repositories |
| F56 | O5 Org settings (portfolio-git-hub-branding) | org portfolio-git-hub-branding | TBD | judge domains, member visibility, default permissions, 2FA |
| F57 | X1 Consistency | account + orgs | 1 | at least one org has no description; story breaks at handoff |

## Judgment calls to complete
Score each TBD 0–4 against the rubric in
`references/dimensions-and-scoring.md`, then recompute the maturity score.

- [ ] A2 Visual identity — avatar is custom; judge legibility at 32px and brand fit
- [ ] A5 Social proof & links — judge social accounts and contactability
- [ ] A6 Account settings — judge visibility and discoverability
- [ ] O2 Org logo (40-cluster-automation) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (40-cluster-automation) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (30-gitops-argocd-flux) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (30-gitops-argocd-flux) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (20-workload-deployments) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (20-workload-deployments) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (10-vanilla-k8s-and-hardening) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (10-vanilla-k8s-and-hardening) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (00-governance) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (00-governance) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (org-cheaper-inference) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (org-cheaper-inference) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (org-omnilabs-ai) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (org-omnilabs-ai) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (org-cheaper-inference-analysis) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (org-cheaper-inference-analysis) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (org-ai-governance) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (org-ai-governance) — judge domains, member visibility, default permissions, 2FA
- [ ] O2 Org logo (portfolio-git-hub-branding) — logo is custom; judge legibility and brand fit
- [ ] O5 Org settings (portfolio-git-hub-branding) — judge domains, member visibility, default permissions, 2FA

## Next step
Turn each finding into a prioritized action (impact × cost) in the plan.
