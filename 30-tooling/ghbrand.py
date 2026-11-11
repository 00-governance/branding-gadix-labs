#!/usr/bin/env python3
"""Shared GitHub API helpers for the branding practice.

Auth: reads the token from the GH_PAT environment variable. The token is never
printed, never written to disk, and never passed as an argument.

Uses only the Python standard library (urllib) so scripts run anywhere.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
GRAPHQL = "https://api.github.com/graphql"
USER_AGENT = "gh-branding-practice/1.0"


class GitHubError(RuntimeError):
    def __init__(self, status: int, message: str):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status


def token() -> str:
    tok = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    if not tok:
        sys.stderr.write("error: set GH_PAT (or GITHUB_TOKEN) before running.\n")
        raise SystemExit(2)
    return tok


def _request(method: str, url: str, body=None, params=None, token_value=None):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token_value or token()}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", USER_AGENT)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = resp.read().decode()
            return resp.status, (json.loads(payload) if payload else None), dict(resp.headers)
    except urllib.error.HTTPError as e:
        payload = e.read().decode()
        try:
            parsed = json.loads(payload)
            message = parsed.get("message", payload)
        except json.JSONDecodeError:
            message = payload
        raise GitHubError(e.code, str(message)) from None
    except urllib.error.URLError as e:
        raise GitHubError(0, f"network error: {e.reason}") from None


def get(path: str, params=None):
    _, data, _ = _request("GET", f"{API}{path}", params=params)
    return data


def patch(path: str, body):
    _, data, _ = _request("PATCH", f"{API}{path}", body=body)
    return data


def put(path: str, body):
    _, data, _ = _request("PUT", f"{API}{path}", body=body)
    return data


def post(path: str, body):
    _, data, _ = _request("POST", f"{API}{path}", body=body)
    return data


def graphql(query: str, variables: dict):
    _, data, _ = _request("POST", GRAPHQL, body={"query": query, "variables": variables})
    if data and data.get("errors"):
        raise GitHubError(200, f"GraphQL errors: {data['errors']}")
    return data.get("data", {}) if data else {}


def try_get(path: str, params=None):
    """Return (data, error_status). data is None on 404/403."""
    try:
        return get(path, params=params), None
    except GitHubError as e:
        return None, e.status


def try_post(path: str, body):
    """Return (data, error_status) for POST, never raising on HTTP errors."""
    try:
        return post(path, body), None
    except GitHubError as e:
        return None, e.status


def try_put(path: str, body):
    """Return (data, error_status) for PUT, never raising on HTTP errors."""
    try:
        return put(path, body), None
    except GitHubError as e:
        return None, e.status


def token_scopes() -> list[str]:
    """Read scopes from a HEAD request (classic tokens only)."""
    req = urllib.request.Request(f"{API}/user", method="GET")
    req.add_header("Authorization", f"Bearer {token()}")
    req.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.headers.get("x-oauth-scopes", "")
            return [s.strip() for s in raw.split(",") if s.strip()]
    except urllib.error.HTTPError:
        return []


def rate_limit() -> dict:
    try:
        return get("/rate_limit").get("rate", {})
    except GitHubError:
        return {}


# ---- domain helpers -------------------------------------------------------

def authed_user():
    return get("/user")


def user_profile(login: str):
    return get(f"/users/{login}")


def user_social(login: str):
    data, _ = try_get(f"/users/{login}/social_accounts")
    return data or []


def owned_orgs():
    """Orgs where the authenticated user has the admin role."""
    orgs = get("/user/orgs", params={"per_page": 100})
    owned = []
    for o in orgs:
        login = o["login"]
        m, status = try_get(f"/user/memberships/orgs/{login}")
        if m and m.get("role") == "admin" and m.get("state") == "active":
            owned.append(o)
    return owned


def org_profile(org: str):
    return get(f"/orgs/{org}")


def user_pinned(login: str):
    q = """
    query($login: String!) {
      user(login: $login) {
        pinnedItems(first: 6, types: [REPOSITORY]) {
          nodes { ... on Repository { nameWithOwner description stargazerCount forkCount
            repositoryTopics(first: 20) { nodes { topic { name } } } } }
        }
      }
    }"""
    data = graphql(q, {"login": login})
    nodes = (data.get("user") or {}).get("pinnedItems", {}).get("nodes", [])
    return [n for n in nodes if n]


def org_pinned(org: str):
    q = """
    query($login: String!) {
      organization(login: $login) {
        pinnedItems(first: 6, types: [REPOSITORY]) {
          nodes { ... on Repository { nameWithOwner description stargazerCount forkCount
            repositoryTopics(first: 20) { nodes { topic { name } } } } }
        }
      }
    }"""
    data = graphql(q, {"login": org})
    nodes = (data.get("organization") or {}).get("pinnedItems", {}).get("nodes", [])
    return [n for n in nodes if n]


def repo_readme_exists(owner: str, repo: str) -> bool:
    data, status = try_get(f"/repos/{owner}/{repo}/readme")
    return bool(data)


def profile_readme_exists(login: str) -> bool:
    return repo_readme_exists(login, login)


def org_profile_readme_exists(org: str) -> bool:
    return repo_readme_exists(org, ".github")


def list_repos(owner: str, is_org: bool, limit: int = 100):
    path = f"/orgs/{owner}/repos" if is_org else f"/users/{owner}/repos"
    return get(path, params={"per_page": min(limit, 100), "sort": "updated"})


# ---- avatar default detection (stdlib PNG colour count) -------------------

def _png_unique_colors(data: bytes) -> int:
    """Count unique RGB colours in an 8-bit PNG. Returns -1 if not decodable."""
    import struct, zlib
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return -1
    pos, w, h, bitd, ctype = 8, 0, 0, 0, 0
    idat = b""
    while pos + 8 <= len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, bitd, ctype = struct.unpack(">IIBB", chunk[:10])
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
        pos += 12 + ln
    if bitd != 8 or ctype not in (2, 6):
        return -1
    ch = 3 if ctype == 2 else 4
    raw = zlib.decompress(idat)
    stride = w * ch
    colors = set()
    prev = bytearray(stride)
    i = 0
    for _ in range(h):
        ft = raw[i]; i += 1
        line = bytearray(raw[i:i + stride]); i += stride
        for x in range(stride):
            a = line[x - ch] if x >= ch else 0
            b = prev[x]
            c = prev[x - ch] if x >= ch else 0
            if ft == 1:
                line[x] = (line[x] + a) & 0xFF
            elif ft == 2:
                line[x] = (line[x] + b) & 0xFF
            elif ft == 3:
                line[x] = (line[x] + ((a + b) >> 1)) & 0xFF
            elif ft == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        for x in range(0, stride, ch):
            colors.add(bytes(line[x:x + 3]))
        prev = line
    return len(colors)


def avatar_color_count(url: str) -> int:
    """Unique RGB colours in the avatar PNG, or -1 if it cannot be read.

    GitHub serves default avatars from avatars.githubusercontent.com without an
    'identicons' path, so a URL check is not enough; we inspect the pixels.
    """
    if not url:
        return 0
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
    except Exception:
        return -1
    return _png_unique_colors(data)


def avatar_is_default(url: str) -> bool:
    """True if the avatar is a generated identicon (2 flat colours)."""
    if not url or "identicons" in url:
        return True
    n = avatar_color_count(url)
    return n >= 0 and n <= 2


def is_default_avatar(avatar_url: str) -> bool:
    return "identicons" in (avatar_url or "") or not avatar_url


# ---- content helpers (for quality-aware scoring) --------------------------

def get_raw(path: str) -> str:
    """Fetch a file's raw text. Returns '' on 404."""
    req = urllib.request.Request(f"{API}{path}", method="GET")
    req.add_header("Authorization", f"Bearer {token()}")
    req.add_header("Accept", "application/vnd.github.raw")
    req.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return ""
        raise GitHubError(e.code, "raw fetch failed") from None


def repo_readme_text(owner: str, repo: str) -> str:
    return get_raw(f"/repos/{owner}/{repo}/readme")


def org_profile_readme_text(org: str) -> str:
    """Read the org profile README at .github/profile/README.md."""
    return get_raw(f"/repos/{org}/.github/contents/profile/README.md")


def repo_file_list(owner: str, repo: str, path: str = "") -> list:
    data, status = try_get(f"/repos/{owner}/{repo}/contents/{path}")
    if status is not None or not isinstance(data, list):
        return []
    return [d["path"] for d in data if isinstance(d, dict)]
