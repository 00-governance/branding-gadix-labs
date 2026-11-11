# branding-gadix-labs

Branding and settings record for the GitHub account **gadix-labs** (Mohamed Gad) and
the organizations it owns.

This repository is the single source of truth for how the account and its
organizations are configured and branded: identity text, profile and org READMEs,
image assets, settings snapshots, and the audit trail. It is generated and
maintained by the GitHub-branding practice; the practice itself lives separately.

## Layout

| Path | Contents |
|---|---|
| `00-account/` | Engagement record, inventory, audit reports, brand core, remediation plan, decision log, verification |
| `10-profile/` | The user profile README, profile settings, and the profile image assets |
| `20-organizations/<org>/` | One folder per organization: profile README, settings snapshot, and image assets |
| `30-tooling/` | Scripts that discover, audit, generate assets, and publish |
| `40-lab/` | Change ledger and backlog (tracking for the practice) |

## Account

- **User:** `gadix-labs`
- **Organizations owned:** 10 (see `20-organizations/`)
- **Maturity score:** see `00-account/80-audit-report-after.md`

## Regenerating

```bash
export GH_PAT=...                      # a token with read:user, read:org
python3 30-tooling/discover.py --user gadix-labs --out 00-account/70-inventory-after.json
python3 30-tooling/audit.py --inventory 00-account/70-inventory-after.json \
    --out 00-account/80-audit-report-after.md --check-embeds
```

Never commit a token. Assets are regenerated with `30-tooling/make_assets.py`.

## Owner-only steps

Some surfaces have no API (avatar, org logos, pinning, org rename, private
contributions). They are listed per folder and in the practice's manual-steps
runbook.
