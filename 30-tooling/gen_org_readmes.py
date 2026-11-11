#!/usr/bin/env python3
"""Generate one org profile README per org, from the brand core.

Reads 00-account/30-brand-core.yaml and writes 20-organizations/<org>/README.md
for each org. Then publish each with publish_readme.py.

Usage:
    python3 30-tooling/gen_org_readmes.py
"""
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(HERE, "00-account", "30-brand-core.yaml")
ORGS = os.path.join(HERE, "20-organizations")

# Minimal parse of the orgs: list under brand_core.orgs. Each entry has
# login, display_name, one_liner.
def parse_orgs(path):
    orgs, cur = [], None
    in_orgs = False
    for line in open(path, encoding="utf-8"):
        if re.match(r"^\s{2}orgs:\s*$", line):
            in_orgs = True
            continue
        if in_orgs:
            if re.match(r"^\s{2}\w", line) and "orgs:" not in line:
                break
            m = re.match(r"^\s{4}- login:\s*(.+?)\s*$", line)
            if m:
                cur = {"login": m.group(1)}
                orgs.append(cur)
                continue
            m = re.match(r"^\s{6}(display_name|one_liner):\s*(.+?)\s*$", line)
            if m and cur is not None:
                cur[m.group(1)] = m.group(2)
    return orgs


TEMPLATE = """<div align="center">

<img src="assets/banner-1280x240.png" alt="{display_name}" width="100%" />

# {display_name}

{one_liner}

<img src="https://img.shields.io/badge/owner-gadix--labs-0b2545?style=flat&logo=github" alt="Owner" />

</div>

## About

**{display_name}** is part of a cloud-native platform practice: Kubernetes, GitOps,
and AI infrastructure. This organization groups repositories for one clear domain.

## Explore

Browse the repositories below, or see the full list in the organization's
repository tab.

<div align="center">
<sub>Maintained by <a href="https://github.com/gadix-labs">gadix-labs</a></sub>
</div>
"""


def main():
    orgs = parse_orgs(CORE)
    written = []
    for o in orgs:
        if "login" not in o:
            continue
        body = TEMPLATE.format(
            display_name=o.get("display_name", o["login"]),
            one_liner=o.get("one_liner", ""),
        )
        out_dir = os.path.join(ORGS, o["login"])
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "README.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        written.append(path)
    print(f"wrote {len(written)} org READMEs")
    for w in written:
        print("  ", os.path.relpath(w, HERE))


if __name__ == "__main__":
    main()
