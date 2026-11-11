#!/usr/bin/env python3
"""Score a GitHub branding inventory and emit an audit report.

Reads the JSON produced by discover.py and scores every dimension mechanically —
no judgment calls left as TBD. Quality is measured from real content: README text,
committed assets, alt text, and embed health.

Usage:
    python3 audit.py --inventory gh-inventory.json [--out audit-report.md]
    python3 audit.py --inventory gh-inventory.json --check-embeds   # network
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request

# dimension -> weight
WEIGHTS = {
    "A1": 2.0, "A2": 2.0, "A3": 1.5, "A4": 1.5, "A5": 1.0, "A6": 1.0,
    "O1": 2.0, "O2": 2.0, "O3": 1.5, "O4": 1.5, "O5": 1.0,
    "X1": 1.5, "E1": 1.0,
}

MD_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
HTML_IMG_RE = re.compile(r"<img[^>]*>", re.I)
SRC_RE = re.compile(r"src=[\"']([^\"']+)[\"']", re.I)
ALT_ATTR_RE = re.compile(r"alt=[\"']([^\"']*)[\"']", re.I)


# ---- readme helpers ---------------------------------------------------------

def image_sources(text: str) -> list[str]:
    out = [m.group(2) for m in MD_IMG_RE.finditer(text)]
    for tag in HTML_IMG_RE.findall(text):
        s = SRC_RE.search(tag)
        if s:
            out.append(s.group(1))
    return out


def images_missing_alt(text: str) -> int:
    missing = sum(1 for alt, _ in MD_IMG_RE.findall(text) if not alt.strip())
    missing += sum(1 for tag in HTML_IMG_RE.findall(text) if not ALT_ATTR_RE.search(tag))
    return missing


def is_external(url: str) -> bool:
    return url.startswith("http")


def relative_images(text: str) -> list[str]:
    return [u for u in image_sources(text) if not is_external(u)]


def external_images(text: str) -> list[str]:
    return [u for u in image_sources(text) if is_external(u)]


def embed_ok(url: str) -> bool:
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "Mozilla/5.0 gh-branding-audit")
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            return resp.status < 400
    except urllib.error.HTTPError as e:
        return e.code < 400
    except Exception:
        return False


# ---- user dimensions --------------------------------------------------------

def score_user_identity(u: dict):
    fields = ("name", "bio", "location", "company", "blog")
    present = sum(bool((u.get(k) or "").strip()) for k in fields)
    if present == 0:
        return 0, "no name, bio, location, company, or website"
    if not (u.get("bio") or "").strip():
        return 1, "bio missing"
    if not (u.get("name") or "").strip():
        return 1, "display name missing"
    if len((u.get("bio") or "").strip()) < 20:
        return 1, f"bio too short ({len(u['bio'].strip())} chars)"
    if present >= 4 and (u.get("blog") or "").strip():
        return 4, f"{present}/5 identity fields set incl. website"
    if present >= 3:
        return 3, f"{present}/5 identity fields set"
    return 2, f"only {present}/5 identity fields set"


def score_user_avatar(u: dict):
    if u.get("avatar_is_default"):
        return 0, "default identicon avatar"
    n = u.get("avatar_colors")
    if n is None:
        return 3, "custom avatar set (richness not measurable)"
    if n <= 64:
        return 2, f"custom avatar but low colour richness ({n} colours); may be a flat block"
    return 4, f"custom avatar, {n} colours (a real image)"


def score_user_readme(inv: dict):
    if not inv.get("profile_readme_exists"):
        return 0, "no profile README (repo <login>/<login> missing or empty)"
    text = inv.get("profile_readme_text") or ""
    if not text.strip():
        return 1, "README exists but is empty"
    assets = inv.get("profile_assets") or []
    imgs = image_sources(text)
    rel = relative_images(text)
    missing_alt = images_missing_alt(text)
    if not imgs:
        return 2, "README has content but no images/banner"
    if rel and not assets:
        return 2, f"README references {len(rel)} local image(s) but none committed under assets/"
    if missing_alt:
        return 3, f"{len(imgs)} image(s), {missing_alt} without alt text"
    if len(imgs) >= 2 and assets:
        return 4, f"{len(imgs)} images, all with alt text, {len(assets)} committed assets"
    return 3, f"{len(imgs)} image(s), all with alt text"


def _pins_score(pins: list, note: str):
    if not pins:
        return 0, f"no pinned repositories ({note})"
    undescribed = [p.get("nameWithOwner") for p in pins if not p.get("description")]
    if undescribed:
        return 1, f"{len(undescribed)} pinned repo(s) without a description"
    if len(pins) < 4:
        return 2, f"only {len(pins)} pinned repo(s); 6 slots available"
    def topics(p):
        return ((p.get("repositoryTopics") or {}).get("nodes") or [])
    no_topics = [p.get("nameWithOwner") for p in pins if not topics(p)]
    if no_topics:
        return 3, f"{len(pins)} pinned repos described; {len(no_topics)} without topics"
    return 4, f"{len(pins)} pinned repos, all described and tagged with topics"


def score_user_pins(inv: dict):
    return _pins_score(inv.get("pinned", []), "set in the web UI; no API")


def score_social(inv: dict):
    social = inv.get("social_accounts") or []
    u = inv["user"]
    has_contact = bool((u.get("blog") or "").strip()) or bool((u.get("email") or "").strip())
    readme = inv.get("profile_readme_text") or ""
    has_readme_contact = "mailto:" in readme.lower() or "linkedin.com" in readme.lower()
    if not social and not has_contact and not has_readme_contact:
        return 0, "no social accounts and no contact route"
    if social and has_contact:
        return 4, f"{len(social)} social account(s) and a contact route"
    if has_contact or has_readme_contact:
        return 3, "contact route present"
    return 2, f"{len(social)} social account(s), no direct contact route"


def score_account_settings(inv: dict):
    u = inv["user"]
    if not u.get("login"):
        return 0, "profile not readable"
    named = bool((u.get("name") or "").strip())
    has_bio = bool((u.get("bio") or "").strip())
    has_site = bool((u.get("blog") or "").strip())
    if not named:
        return 1, "public but display name unset (undiscoverable)"
    if named and has_bio and has_site:
        return 4, "public, named, bio and website set (discoverable)"
    if named and has_bio:
        return 3, "public, named, bio set"
    return 2, "public but settings left at defaults"


# ---- org dimensions ---------------------------------------------------------

def score_org_identity(o: dict):
    if o.get("error"):
        return 0, f"org not readable: {o['error']}"
    name = bool((o.get("name") or "").strip())
    desc = bool((o.get("description") or "").strip())
    blog = bool((o.get("blog") or "").strip())
    if not desc and not name:
        return 0, "no organization description or name"
    if desc and not name:
        return 1, "description set but display name missing"
    if desc and name and blog:
        return 4, "name, description, and website set"
    if desc and name:
        return 3, "display name and description set"
    return 2, "partially configured"


def score_org_logo(o: dict):
    if o.get("error"):
        return 0, "org not readable"
    if o.get("avatar_is_default"):
        return 0, "no custom organization logo (upload in the web UI)"
    n = o.get("avatar_colors")
    if n is None:
        return 3, "custom logo set (richness not measurable)"
    if n <= 64:
        return 2, f"custom logo but low colour richness ({n} colours); may be a flat block"
    return 4, f"custom logo, {n} colours (a real image)"


def score_org_readme(o: dict):
    if o.get("error"):
        return 0, "org not readable"
    if not o.get("profile_readme_exists"):
        return 0, "no organization profile README ({org}/.github/profile/README.md)"
    text = o.get("profile_readme_text") or ""
    if not text.strip():
        return 1, "org README exists but is empty"
    assets = o.get("profile_assets") or []
    imgs = image_sources(text)
    rel = relative_images(text)
    missing_alt = images_missing_alt(text)
    if not imgs:
        return 2, "org README has content but no images/banner"
    if rel and not assets:
        return 2, f"README references {len(rel)} local image(s) but none committed under profile/assets/"
    if missing_alt:
        return 3, f"{len(imgs)} image(s), {missing_alt} without alt text"
    if len(imgs) >= 2 and assets:
        return 4, f"{len(imgs)} images, all with alt text, {len(assets)} committed assets"
    return 3, f"{len(imgs)} image(s), all with alt text"


def score_org_pins(o: dict):
    if o.get("error"):
        return 0, "org not readable"
    return _pins_score(o.get("pinned", []), "set in the web UI; no API")


def score_org_settings(o: dict):
    if o.get("error"):
        return 0, "org not readable"
    perm = (o.get("default_repository_permission") or "").lower()
    twofa = o.get("two_factor_requirement_enabled")
    domains = o.get("verified_domains") or []
    if not perm:
        return 0, "settings not readable"
    if perm == "write":
        return 1, "default repository permission is write (not least privilege)"
    if perm in ("read", "none") and twofa and domains:
        return 4, "least-privilege permission, 2FA required, verified domain"
    if perm in ("read", "none") and twofa:
        return 3, "least-privilege permission and 2FA required"
    if perm in ("read", "none"):
        return 2, "least-privilege permission, 2FA not required"
    return 2, f"default repository permission is {perm or 'unknown'}"


def score_consistency(inv: dict):
    u = inv["user"]
    orgs = [o for o in inv.get("orgs", []) if not o.get("error")]
    if not orgs:
        return 3, "no owned orgs; single-surface account"
    if any(not (o.get("description") or "").strip() for o in orgs):
        return 1, "at least one org has no description; the story breaks"
    if any(not (o.get("name") or "").strip() for o in orgs):
        return 2, "an org is missing a display name"
    with_logo = all(not o.get("avatar_is_default") for o in orgs)
    with_readme = all(o.get("profile_readme_exists") for o in orgs)
    if with_logo and with_readme and (u.get("bio") or "").strip():
        return 4, "all orgs described, named, logos + READMEs, account bio set"
    return 3, "names, taglines, and tone match across account and orgs"


# ---- assembly ---------------------------------------------------------------

def check_embed_finding(inv: dict):
    urls = list(external_images(inv.get("profile_readme_text") or ""))
    for o in inv.get("orgs", []):
        urls += external_images(o.get("profile_readme_text") or "")
    urls = sorted(set(urls))
    if not urls:
        return {"dimension": "E1", "label": "Embed health", "surface": "readmes",
                "score": 4, "evidence": "no external embeds to check"}
    bad = [u for u in urls if not embed_ok(u)]
    if not bad:
        return {"dimension": "E1", "label": "Embed health", "surface": "readmes",
                "score": 4, "evidence": f"{len(urls)} external embed(s), all reachable"}
    return {"dimension": "E1", "label": "Embed health", "surface": "readmes",
            "score": 0, "evidence": f"{len(bad)}/{len(urls)} external embed(s) broken: {bad[:3]}"}


def build_findings(inv: dict, check_embeds: bool = False):
    findings = []
    u = inv["user"]

    def add(dim, label, result, surface):
        score, evidence = result
        findings.append({
            "dimension": dim, "label": label, "surface": surface,
            "score": score, "evidence": evidence,
        })

    add("A1", "Identity", score_user_identity(u), "user profile")
    add("A2", "Visual identity", score_user_avatar(u), "user avatar")
    add("A3", "Profile README", score_user_readme(inv), "profile README")
    add("A4", "Pinned repositories", score_user_pins(inv), "pinned repos")
    add("A5", "Social proof & links", score_social(inv), "social accounts")
    add("A6", "Account settings", score_account_settings(inv), "account settings")

    for o in inv.get("orgs", []):
        login = o.get("login")
        add("O1", f"Org identity ({login})", score_org_identity(o), f"org {login}")
        add("O2", f"Org logo ({login})", score_org_logo(o), f"org {login}")
        add("O3", f"Org README ({login})", score_org_readme(o), f"org {login}")
        add("O4", f"Org pinned ({login})", score_org_pins(o), f"org {login}")
        add("O5", f"Org settings ({login})", score_org_settings(o), f"org {login}")

    add("X1", "Consistency", score_consistency(inv), "account + orgs")

    if check_embeds:
        findings.append(check_embed_finding(inv))
    return findings


def maturity(findings):
    total_w = 0.0
    total = 0.0
    for f in findings:
        if f["score"] is None:
            continue
        w = WEIGHTS.get(f["dimension"], 1.0)
        total += f["score"] * w
        total_w += 4 * w
    if total_w == 0:
        return None
    return round(100 * total / total_w, 1)


def render(inv, findings):
    u = inv["user"]
    score = maturity(findings)
    tbd = [f for f in findings if f["score"] is None]
    low = sorted([f for f in findings if (f["score"] or 0) < 3],
                 key=lambda f: (f["score"] or 0))
    lines = [
        f"# Audit report — {u['login']}",
        "",
        "## Summary",
        f"- Maturity score (mechanical): {score if score is not None else 'n/a'}/100",
        f"- Surfaces audited: {len(findings)}",
        f"- Judgment calls remaining (TBD): {len(tbd)}",
        f"- Owned organizations: {len(inv.get('orgs', []))}",
        "",
        "## Findings",
        "| ID | Dimension | Surface | Score | Evidence |",
        "|----|-----------|---------|-------|----------|",
    ]
    for i, f in enumerate(findings, 1):
        s = "TBD" if f["score"] is None else str(f["score"])
        lines.append(
            f"| F{i} | {f['dimension']} {f['label']} | {f['surface']} | {s} | {f['evidence']}"
        )
    lines += ["", "## Improvement queue (score < 3)", ""]
    if low:
        for f in low:
            lines.append(f"- [{f['score']}] {f['dimension']} {f['label']} — {f['evidence']}")
    else:
        lines.append("- none; every surface scores 3 or better")
    lines += [
        "",
        "## Manual steps for the owner (no API)",
        "These cannot be automated; hand them to the owner. See the remediation skill's",
        "`30-manual-steps.md` for exact click paths.",
        "",
        "- [ ] Upload the avatar (A2) — Settings > Public profile > avatar.",
        "- [ ] Upload each org logo (O2) — Org settings > Profile > logo.",
        "- [ ] Pin repositories for the profile and each org (A4, O4) — Customize pins.",
        "- [ ] Turn on **Include private contributions on my profile** — Settings >",
        "      Public profile > Contributions & Activity. Shows private counts without",
        "      revealing repos or orgs.",
        "- [ ] Verify an org domain (O5) — Org settings > Domains.",
        "",
        "## Next step",
        "Turn each queued finding into a prioritized action (impact x cost) in the plan.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Score a GitHub branding inventory.")
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--out", default="audit-report.md")
    ap.add_argument("--check-embeds", action="store_true",
                    help="HTTP-check external embeds (adds an E1 finding)")
    args = ap.parse_args()

    with open(args.inventory, encoding="utf-8") as fh:
        inv = json.load(fh)

    findings = build_findings(inv, check_embeds=args.check_embeds)
    report = render(inv, findings)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(report)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
