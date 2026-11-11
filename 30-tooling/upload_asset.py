#!/usr/bin/env python3
"""Upload a binary file to a repo path via the contents API.

Runtime tool for putting generated images into the profile / org repos so READMEs
can reference them. Idempotent: updates if the path exists.

Usage:
    GH_PAT=... python3 tools/upload_asset.py --owner gadix-labs --repo gadix-labs \
        --path assets/banner-1280x320.png --file 10-profile/assets/banner-1280x320.png
"""
from __future__ import annotations

import argparse
import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghbrand as gh  # noqa: E402


def upload(owner, repo, path, file_path, message):
    with open(file_path, "rb") as fh:
        content = base64.b64encode(fh.read()).decode("ascii")
    existing, status = gh.try_get(f"/repos/{owner}/{repo}/contents/{path}")
    sha = existing.get("sha") if status is None and isinstance(existing, dict) else None
    body = {"message": message, "content": content}
    if sha:
        body["sha"] = sha
    _, st = gh.try_put(f"/repos/{owner}/{repo}/contents/{path}", body)
    if st is not None:
        raise gh.GitHubError(st, f"cannot upload {owner}/{repo}/{path}")
    return "updated" if sha else "created"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--path", required=True, help="destination path in the repo")
    ap.add_argument("--file", required=True, help="local file to upload")
    ap.add_argument("--message", default="Add brand asset")
    args = ap.parse_args()
    result = upload(args.owner, args.repo, args.path, args.file, args.message)
    print(f"{result}: {args.owner}/{args.repo}/{args.path}")


if __name__ == "__main__":
    main()
