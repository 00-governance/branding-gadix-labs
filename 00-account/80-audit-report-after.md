# Audit report — gadix-labs

## Summary
- Maturity score (mechanical): 51.2/100
- Surfaces audited: 57
- Judgment calls remaining (TBD): 0
- Owned organizations: 10

## Findings
| ID | Dimension | Surface | Score | Evidence |
|----|-----------|---------|-------|----------|
| F1 | A1 Identity | user profile | 4 | 4/5 identity fields set incl. website
| F2 | A2 Visual identity | user avatar | 0 | default identicon avatar
| F3 | A3 Profile README | profile README | 4 | 12 images, all with alt text, 3 committed assets
| F4 | A4 Pinned repositories | pinned repos | 0 | no pinned repositories (set in the web UI; no API)
| F5 | A5 Social proof & links | social accounts | 3 | contact route present
| F6 | A6 Account settings | account settings | 4 | public, named, bio and website set (discoverable)
| F7 | O1 Org identity (40-cluster-automation) | org 40-cluster-automation | 4 | name, description, and website set
| F8 | O2 Org logo (40-cluster-automation) | org 40-cluster-automation | 0 | no custom organization logo (upload in the web UI)
| F9 | O3 Org README (40-cluster-automation) | org 40-cluster-automation | 4 | 2 images, all with alt text, 1 committed assets
| F10 | O4 Org pinned (40-cluster-automation) | org 40-cluster-automation | 0 | no pinned repositories (set in the web UI; no API)
| F11 | O5 Org settings (40-cluster-automation) | org 40-cluster-automation | 2 | least-privilege permission, 2FA not required
| F12 | O1 Org identity (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | 4 | name, description, and website set
| F13 | O2 Org logo (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | 0 | no custom organization logo (upload in the web UI)
| F14 | O3 Org README (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | 4 | 2 images, all with alt text, 1 committed assets
| F15 | O4 Org pinned (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | 0 | no pinned repositories (set in the web UI; no API)
| F16 | O5 Org settings (30-gitops-argocd-flux) | org 30-gitops-argocd-flux | 2 | least-privilege permission, 2FA not required
| F17 | O1 Org identity (20-workload-deployments) | org 20-workload-deployments | 4 | name, description, and website set
| F18 | O2 Org logo (20-workload-deployments) | org 20-workload-deployments | 0 | no custom organization logo (upload in the web UI)
| F19 | O3 Org README (20-workload-deployments) | org 20-workload-deployments | 4 | 2 images, all with alt text, 1 committed assets
| F20 | O4 Org pinned (20-workload-deployments) | org 20-workload-deployments | 0 | no pinned repositories (set in the web UI; no API)
| F21 | O5 Org settings (20-workload-deployments) | org 20-workload-deployments | 2 | least-privilege permission, 2FA not required
| F22 | O1 Org identity (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | 4 | name, description, and website set
| F23 | O2 Org logo (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | 0 | no custom organization logo (upload in the web UI)
| F24 | O3 Org README (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | 4 | 2 images, all with alt text, 1 committed assets
| F25 | O4 Org pinned (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | 0 | no pinned repositories (set in the web UI; no API)
| F26 | O5 Org settings (10-vanilla-k8s-and-hardening) | org 10-vanilla-k8s-and-hardening | 2 | least-privilege permission, 2FA not required
| F27 | O1 Org identity (00-governance) | org 00-governance | 4 | name, description, and website set
| F28 | O2 Org logo (00-governance) | org 00-governance | 0 | no custom organization logo (upload in the web UI)
| F29 | O3 Org README (00-governance) | org 00-governance | 4 | 2 images, all with alt text, 1 committed assets
| F30 | O4 Org pinned (00-governance) | org 00-governance | 0 | no pinned repositories (set in the web UI; no API)
| F31 | O5 Org settings (00-governance) | org 00-governance | 2 | least-privilege permission, 2FA not required
| F32 | O1 Org identity (org-cheaper-inference) | org org-cheaper-inference | 4 | name, description, and website set
| F33 | O2 Org logo (org-cheaper-inference) | org org-cheaper-inference | 0 | no custom organization logo (upload in the web UI)
| F34 | O3 Org README (org-cheaper-inference) | org org-cheaper-inference | 4 | 2 images, all with alt text, 1 committed assets
| F35 | O4 Org pinned (org-cheaper-inference) | org org-cheaper-inference | 0 | no pinned repositories (set in the web UI; no API)
| F36 | O5 Org settings (org-cheaper-inference) | org org-cheaper-inference | 2 | least-privilege permission, 2FA not required
| F37 | O1 Org identity (org-omnilabs-ai) | org org-omnilabs-ai | 4 | name, description, and website set
| F38 | O2 Org logo (org-omnilabs-ai) | org org-omnilabs-ai | 0 | no custom organization logo (upload in the web UI)
| F39 | O3 Org README (org-omnilabs-ai) | org org-omnilabs-ai | 4 | 2 images, all with alt text, 1 committed assets
| F40 | O4 Org pinned (org-omnilabs-ai) | org org-omnilabs-ai | 0 | no pinned repositories (set in the web UI; no API)
| F41 | O5 Org settings (org-omnilabs-ai) | org org-omnilabs-ai | 2 | least-privilege permission, 2FA not required
| F42 | O1 Org identity (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | 4 | name, description, and website set
| F43 | O2 Org logo (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | 0 | no custom organization logo (upload in the web UI)
| F44 | O3 Org README (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | 4 | 2 images, all with alt text, 1 committed assets
| F45 | O4 Org pinned (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | 0 | no pinned repositories (set in the web UI; no API)
| F46 | O5 Org settings (org-cheaper-inference-analysis) | org org-cheaper-inference-analysis | 2 | least-privilege permission, 2FA not required
| F47 | O1 Org identity (org-ai-governance) | org org-ai-governance | 4 | name, description, and website set
| F48 | O2 Org logo (org-ai-governance) | org org-ai-governance | 0 | no custom organization logo (upload in the web UI)
| F49 | O3 Org README (org-ai-governance) | org org-ai-governance | 4 | 2 images, all with alt text, 1 committed assets
| F50 | O4 Org pinned (org-ai-governance) | org org-ai-governance | 0 | no pinned repositories (set in the web UI; no API)
| F51 | O5 Org settings (org-ai-governance) | org org-ai-governance | 2 | least-privilege permission, 2FA not required
| F52 | O1 Org identity (portfolio-git-hub-branding) | org portfolio-git-hub-branding | 4 | name, description, and website set
| F53 | O2 Org logo (portfolio-git-hub-branding) | org portfolio-git-hub-branding | 0 | no custom organization logo (upload in the web UI)
| F54 | O3 Org README (portfolio-git-hub-branding) | org portfolio-git-hub-branding | 4 | 2 images, all with alt text, 1 committed assets
| F55 | O4 Org pinned (portfolio-git-hub-branding) | org portfolio-git-hub-branding | 0 | no pinned repositories (set in the web UI; no API)
| F56 | O5 Org settings (portfolio-git-hub-branding) | org portfolio-git-hub-branding | 2 | least-privilege permission, 2FA not required
| F57 | X1 Consistency | account + orgs | 3 | names, taglines, and tone match across account and orgs

## Improvement queue (score < 3)

- [0] A2 Visual identity — default identicon avatar
- [0] A4 Pinned repositories — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (40-cluster-automation) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (40-cluster-automation) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (30-gitops-argocd-flux) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (30-gitops-argocd-flux) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (20-workload-deployments) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (20-workload-deployments) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (10-vanilla-k8s-and-hardening) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (10-vanilla-k8s-and-hardening) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (00-governance) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (00-governance) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (org-cheaper-inference) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (org-cheaper-inference) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (org-omnilabs-ai) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (org-omnilabs-ai) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (org-cheaper-inference-analysis) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (org-cheaper-inference-analysis) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (org-ai-governance) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (org-ai-governance) — no pinned repositories (set in the web UI; no API)
- [0] O2 Org logo (portfolio-git-hub-branding) — no custom organization logo (upload in the web UI)
- [0] O4 Org pinned (portfolio-git-hub-branding) — no pinned repositories (set in the web UI; no API)
- [2] O5 Org settings (40-cluster-automation) — least-privilege permission, 2FA not required
- [2] O5 Org settings (30-gitops-argocd-flux) — least-privilege permission, 2FA not required
- [2] O5 Org settings (20-workload-deployments) — least-privilege permission, 2FA not required
- [2] O5 Org settings (10-vanilla-k8s-and-hardening) — least-privilege permission, 2FA not required
- [2] O5 Org settings (00-governance) — least-privilege permission, 2FA not required
- [2] O5 Org settings (org-cheaper-inference) — least-privilege permission, 2FA not required
- [2] O5 Org settings (org-omnilabs-ai) — least-privilege permission, 2FA not required
- [2] O5 Org settings (org-cheaper-inference-analysis) — least-privilege permission, 2FA not required
- [2] O5 Org settings (org-ai-governance) — least-privilege permission, 2FA not required
- [2] O5 Org settings (portfolio-git-hub-branding) — least-privilege permission, 2FA not required

## Manual steps for the owner (no API)
These cannot be automated; hand them to the owner. See the remediation skill's
`30-manual-steps.md` for exact click paths.

- [ ] Upload the avatar (A2) — Settings > Public profile > avatar.
- [ ] Upload each org logo (O2) — Org settings > Profile > logo.
- [ ] Pin repositories for the profile and each org (A4, O4) — Customize pins.
- [ ] Turn on **Include private contributions on my profile** — Settings >
      Public profile > Contributions & Activity. Shows private counts without
      revealing repos or orgs.
- [ ] Verify an org domain (O5) — Org settings > Domains.

## Next step
Turn each queued finding into a prioritized action (impact x cost) in the plan.
