#!/usr/bin/env python3
"""Publish a user profile README or an org profile README.

A user profile README is the file `README.md` in the repo named exactly after the
login (`<login>/<login>`), which must be public. An org profile README is the file
`profile/README.md` in the org's special `.github` repo.

This script creates the repo if missing and creates or updates the README, so the
same command is idempotent on re-run.

Usage:
    GH_PAT=... python3 publish_readme.py --owner <login> --kind user --file README-profile.md
    GH_PAT=... python3 publish_readme.py --owner <org>   --kind org  --file README-org.md
"""

from __future__ import annotations

import argparse
import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import time

import ghbrand as gh


def ensure_repo(owner: str, repo: str, description: str, private: bool = False) -> None:
    data, status = gh.try_get(f"/repos/{owner}/{repo}")
    if status is None:
        return
    # Try user endpoint first, then org endpoint. try_post returns (data, None)
    # on success, or (None, status) on HTTP error.
    body = {"name": repo, "description": description, "private": private,
            "auto_init": True, "has_issues": False, "has_wiki": False}
    for endpoint in (f"/user/repos", f"/orgs/{owner}/repos"):
        _, st = gh.try_post(endpoint, body)
        if st is None:
            return
    # The create may have raced or the repo may already exist; re-check.
    data, status = gh.try_get(f"/repos/{owner}/{repo}")
    if status is None:
        return
    raise gh.GitHubError(status, f"cannot create repo {owner}/{repo}")


def put_file(owner: str, repo: str, path: str, content: str, message: str) -> str:
    """Create or update a file. Returns 'created' or 'updated'.

    A freshly created repo (auto_init) can 404 briefly until its default branch
    exists, so retry the first read a few times.
    """
    existing, status = None, 404
    for _ in range(5):
        existing, status = gh.try_get(f"/repos/{owner}/{repo}/contents/{path}")
        if status != 404 or _ == 4:
            break
        time.sleep(1)
    sha = existing.get("sha") if status is None and isinstance(existing, dict) else None
    body = {"message": message,
            "content": base64.b64encode(content.encode("utf-8")).decode("ascii")}
    if sha:
        body["sha"] = sha
    _, st = gh.try_put(f"/repos/{owner}/{repo}/contents/{path}", body)
    if st is not None:
        raise gh.GitHubError(st, f"cannot write {owner}/{repo}/{path}")
    return "updated" if sha else "created"


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish a profile README.")
    ap.add_argument("--owner", required=True, help="user login or org login")
    ap.add_argument("--kind", required=True, choices=["user", "org"])
    ap.add_argument("--file", required=True, help="local markdown file to publish")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as fh:
        content = fh.read()

    if args.kind == "user":
        repo, path = args.owner, "README.md"
        ensure_repo(args.owner, repo, "Profile README")
    else:
        repo, path = ".github", "profile/README.md"
        ensure_repo(args.owner, repo, "Organization profile")

    result = put_file(args.owner, repo, path, content,
                      f"Publish {args.kind} profile README")
    print(f"{result}: {args.owner}/{repo}/{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
