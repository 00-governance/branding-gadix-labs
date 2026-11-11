#!/usr/bin/env python3
"""Discover a GitHub account and the organizations it owns.

Reads the user profile, the orgs where the user is admin, and each org's profile,
logo, pinned repos, and settings. Writes a JSON inventory for the audit scorer.

Usage:
    GH_PAT=... python3 discover.py --user <login> [--out inventory.json]
"""

from __future__ import annotations

import argparse
import json
import sys

import ghbrand as gh


def discover(login: str) -> dict:
    inv: dict = {"login": login, "generated_by": "gh-branding-practice/1.0"}

    user = gh.user_profile(login)
    inv["user"] = {
        "login": user.get("login"),
        "name": user.get("name"),
        "bio": user.get("bio"),
        "company": user.get("company"),
        "blog": user.get("blog"),
        "email": user.get("email"),
        "location": user.get("location"),
        "twitter_username": user.get("twitter_username"),
        "avatar_url": user.get("avatar_url"),
        "avatar_is_default": gh.avatar_is_default(user.get("avatar_url")),
        "avatar_colors": gh.avatar_color_count(user.get("avatar_url")),
        "public_repos": user.get("public_repos"),
        "public_gists": user.get("public_gists"),
        "followers": user.get("followers"),
        "hireable": user.get("hireable"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at"),
    }
    inv["social_accounts"] = gh.user_social(login)
    inv["profile_readme_exists"] = gh.profile_readme_exists(login)
    inv["profile_readme_text"] = gh.repo_readme_text(login, login) if inv["profile_readme_exists"] else ""
    inv["profile_assets"] = gh.repo_file_list(login, login, "assets") if inv["profile_readme_exists"] else []
    inv["profile_repo_readme_text"] = inv["profile_readme_text"]

    try:
        inv["pinned"] = gh.user_pinned(login)
    except gh.GitHubError as e:
        inv["pinned"] = []
        inv["pinned_error"] = str(e)

    orgs = []
    for o in gh.owned_orgs():
        ologin = o["login"]
        try:
            prof = gh.org_profile(ologin)
        except gh.GitHubError as e:
            orgs.append({"login": ologin, "error": str(e)})
            continue
        entry = {
            "login": prof.get("login"),
            "name": prof.get("name"),
            "description": prof.get("description"),
            "company": prof.get("company"),
            "blog": prof.get("blog"),
            "location": prof.get("location"),
            "email": prof.get("email"),
            "twitter_username": prof.get("twitter_username"),
            "avatar_url": prof.get("avatar_url"),
            "avatar_is_default": gh.avatar_is_default(prof.get("avatar_url")),
            "avatar_colors": gh.avatar_color_count(prof.get("avatar_url")),
            "public_repos": prof.get("public_repos"),
            "verified": prof.get("is_verified"),
            "default_repository_permission": prof.get("default_repository_permission"),
            "two_factor_requirement_enabled": prof.get("two_factor_requirement_enabled"),
        }
        entry["profile_readme_exists"] = gh.org_profile_readme_exists(ologin)
        entry["profile_readme_text"] = (
            gh.org_profile_readme_text(ologin) if entry["profile_readme_exists"] else "")
        entry["profile_assets"] = (
            gh.repo_file_list(ologin, ".github", "profile/assets")
            if entry["profile_readme_exists"] else [])
        try:
            entry["pinned"] = gh.org_pinned(ologin)
        except gh.GitHubError as e:
            entry["pinned"] = []
            entry["pinned_error"] = str(e)
        domains, status = gh.try_get(f"/orgs/{ologin}/domains")
        entry["verified_domains"] = domains.get("domains", []) if isinstance(domains, dict) else []
        if status in (403, 404):
            entry["settings_access"] = "blocked" if status == 403 else "unavailable"
        orgs.append(entry)
    inv["orgs"] = orgs
    return inv


def summarize(inv: dict) -> str:
    u = inv["user"]
    lines = [
        f"login: {u['login']}",
        f"name:  {u.get('name') or '(unset)'}",
        f"bio:   {'(set)' if u.get('bio') else '(unset)'}",
        f"avatar: {'default' if u.get('avatar_is_default') else 'custom'}",
        f"profile readme: {'yes' if inv.get('profile_readme_exists') else 'no'}",
        f"pinned: {len(inv.get('pinned', []))}",
        f"owned orgs: {len(inv.get('orgs', []))}",
    ]
    for o in inv.get("orgs", []):
        if o.get("error"):
            lines.append(f"  - {o['login']}: ERROR {o['error']}")
            continue
        lines.append(
            f"  - {o['login']}: desc={'yes' if o.get('description') else 'no'}, "
            f"logo={'default' if o.get('avatar_is_default') else 'custom'}, "
            f"readme={'yes' if o.get('profile_readme_exists') else 'no'}, "
            f"pinned={len(o.get('pinned', []))}"
        )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Discover a GitHub account and its orgs.")
    ap.add_argument("--user", required=True, help="GitHub login to audit")
    ap.add_argument("--out", default="gh-inventory.json", help="output JSON path")
    args = ap.parse_args()

    rate = gh.rate_limit()
    if rate:
        sys.stderr.write(f"rate limit: {rate.get('remaining')}/{rate.get('limit')}\n")

    try:
        inv = discover(args.user)
    except gh.GitHubError as e:
        sys.stderr.write(f"error: {e}\n")
        return 1

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(inv, fh, indent=2, sort_keys=True)

    print(summarize(inv))
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
