#!/usr/bin/env python3
"""Apply an approved GitHub branding remediation plan.

Reads a plan (JSON), captures the current value of each surface, applies the
`auto` actions, and writes a JSON decision log. `manual` actions are skipped and
listed. Destructive or visibility-changing actions require an explicit consent
flag per action.

The token is read from GH_PAT and never written anywhere.

Usage:
    GH_PAT=... python3 apply.py --plan plan.json [--dry-run] [--log decision-log.json]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

import ghbrand as gh

# Actions that require an explicit per-action consent flag before applying.
CONSENT_REQUIRED = {
    "update_org_settings", "set_default_repository_permission",
    "require_two_factor", "set_member_visibility", "rename_org",
}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def current_value(action: dict, ctx: dict):
    """Best-effort read of the current value for the before/after log."""
    try:
        kind = action["action"]
        if kind == "update_user_profile":
            return {k: ctx["user"].get(k) for k in action.get("fields", {})}
        if kind == "update_org_profile":
            org = ctx["orgs"].get(action["org"], {})
            return {k: org.get(k) for k in action.get("fields", {})}
        if kind == "update_repo":
            repo = gh.get(f"/repos/{action['owner']}/{action['repo']}")
            return {k: repo.get(k) for k in action.get("fields", {})}
        if kind == "set_social_accounts":
            return {"social_accounts": gh.user_social(ctx["user"]["login"])}
    except gh.GitHubError as e:
        return {"error": str(e)}
    return None


def apply_action(action: dict, ctx: dict):
    """Apply one action. Returns (result, before, after)."""
    kind = action["action"]

    if kind == "update_user_profile":
        before = {k: ctx["user"].get(k) for k in action["fields"]}
        gh.patch("/user", action["fields"])
        after = gh.get("/user")
        return "applied", before, {k: after.get(k) for k in action["fields"]}

    if kind == "update_org_profile":
        org = action["org"]
        before = {k: ctx["orgs"].get(org, {}).get(k) for k in action["fields"]}
        gh.patch(f"/orgs/{org}", action["fields"])
        after = gh.get(f"/orgs/{org}")
        return "applied", before, {k: after.get(k) for k in action["fields"]}

    if kind == "update_repo":
        path = f"/repos/{action['owner']}/{action['repo']}"
        before = {k: gh.get(path).get(k) for k in action["fields"]}
        gh.patch(path, action["fields"])
        after = gh.get(path)
        return "applied", before, {k: after.get(k) for k in action["fields"]}

    if kind == "set_social_accounts":
        before = {"social_accounts": gh.user_social(ctx["user"]["login"])}
        gh.put("/user/social_accounts", {"account_urls": action["urls"]})
        after = {"social_accounts": gh.user_social(ctx["user"]["login"])}
        return "applied", before, after

    raise gh.GitHubError(0, f"unknown action: {kind}")


def load_context(plan: dict):
    user = gh.get("/user")
    orgs = {}
    for action in plan.get("actions", []):
        org = action.get("org")
        if org and org not in orgs:
            try:
                orgs[org] = gh.get(f"/orgs/{org}")
            except gh.GitHubError as e:
                orgs[org] = {"error": str(e)}
    return {"user": user, "orgs": orgs}


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply a GitHub branding remediation plan.")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--log", default="decision-log.json")
    args = ap.parse_args()

    with open(args.plan, encoding="utf-8") as fh:
        plan = json.load(fh)

    rate = gh.rate_limit()
    if rate:
        sys.stderr.write(f"rate limit: {rate.get('remaining')}/{rate.get('limit')}\n")

    ctx = load_context(plan)
    print(f"token: <set>  acting as: {ctx['user']['login']}")

    log = {"started": now(), "dry_run": args.dry_run, "entries": []}
    applied = 0
    for i, action in enumerate(plan.get("actions", []), 1):
        kind = action["action"]
        mode = action.get("mode", "auto")

        if mode == "manual":
            log["entries"].append({"index": i, "action": kind, "result": "skipped_manual",
                                   "note": action.get("owner_step", "")})
            print(f"[{i}] SKIP (manual) {kind} — {action.get('owner_step', '')}")
            continue

        if kind in CONSENT_REQUIRED and not action.get("consent", False):
            log["entries"].append({"index": i, "action": kind, "result": "skipped_no_consent"})
            print(f"[{i}] SKIP (needs consent) {kind}")
            continue

        before = current_value(action, ctx)
        if args.dry_run:
            log["entries"].append({"index": i, "action": kind, "result": "dry_run",
                                   "before": before, "after": action.get("fields", action.get("urls"))})
            print(f"[{i}] DRY-RUN {kind}")
            print(f"      before: {before}")
            print(f"      after:  {action.get('fields', action.get('urls'))}")
            continue

        try:
            result, before, after = apply_action(action, ctx)
            log["entries"].append({"index": i, "action": kind, "result": result,
                                   "before": before, "after": after})
            applied += 1
            print(f"[{i}] APPLIED {kind}")
        except gh.GitHubError as e:
            status = "blocked" if e.status in (401, 403) else "failed"
            log["entries"].append({"index": i, "action": kind, "result": status, "error": str(e)})
            print(f"[{i}] {status.upper()} {kind}: {e}")
            if e.status == 403 and "rate limit" in str(e).lower():
                print("rate limited — stopping cleanly; rerun to continue.")
                break

    log["finished"] = now()
    log["applied_count"] = applied
    if not args.dry_run:
        with open(args.log, "w", encoding="utf-8") as fh:
            json.dump(log, fh, indent=2)
        print(f"\nwrote {args.log}")
    else:
        print("\ndry-run complete; nothing written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
