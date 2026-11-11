#!/usr/bin/env python3
"""Generate brand assets (avatars, org logos, banners) from the brand core.

Runtime tool. Pillow-based, no external binaries. Produces both static PNGs and
animated GIFs so profiles look modern and alive.

Writes into the repository layout: 10-profile/assets/ and
20-organizations/<org>/assets/.

Usage:
    python3 30-tooling/make_assets.py
"""
from __future__ import annotations

import os
import re

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(HERE, "00-account", "30-brand-core.yaml")
PROFILE = os.path.join(HERE, "10-profile", "assets")
ORGS = os.path.join(HERE, "20-organizations")
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# --- palette (defaults; overridden from the brand core where present) ---------
PALETTE = {
    "primary": "#0b2545",
    "accent": "#00b4d8",
    "background": "#f8f9fa",
    "text": "#1a1a1a",
}


def hex2rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# --- brand core parsing -------------------------------------------------------
def parse_core(path: str) -> dict:
    core = {"orgs": [], "owner": {}, "visual": {}}
    cur_org = None
    section = None
    for line in open(path, encoding="utf-8"):
        if re.match(r"^\s*#", line) or not line.strip():
            continue
        m = re.match(r"^  owner:\s*$", line)
        if m:
            section = "owner"
            continue
        if re.match(r"^  visual:\s*$", line):
            section = "visual"
            continue
        if re.match(r"^  orgs:\s*$", line):
            section = "orgs"
            continue
        if section == "owner":
            m = re.match(r"^    (\w+):\s*(.*?)\s*$", line)
            if m:
                core["owner"][m.group(1)] = m.group(2).strip('"')
        elif section == "visual":
            m = re.match(r"^      (\w+):\s*\"?(#[0-9a-fA-F]{6})\"?\s*$", line)
            if m:
                core["visual"][m.group(1)] = m.group(2)
            m = re.match(r"^    (typography):\s*(.+?)\s*$", line)
            if m:
                core["visual"][m.group(1)] = m.group(2)
        elif section == "orgs":
            m = re.match(r"^    - login:\s*(.+?)\s*$", line)
            if m:
                cur_org = {"login": m.group(1)}
                core["orgs"].append(cur_org)
                continue
            m = re.match(r"^      (display_name|one_liner|code|accent):\s*(.+?)\s*$", line)
            if m and cur_org is not None:
                cur_org[m.group(1)] = m.group(2).strip('"')
    return core


# --- drawing primitives -------------------------------------------------------
def linear_gradient(size, c1, c2, diagonal=True):
    w, h = size
    base = Image.new("RGB", (w, h))
    px = base.load()
    for y in range(h):
        for x in range(w):
            t = ((x / w) + (y / h)) / 2 if diagonal else (y / h)
            px[x, y] = mix(c1, c2, t)
    return base


def dot_grid(img, color, spacing=22, radius=1, alpha=40):
    w, h = img.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(spacing, h, spacing):
        for x in range(spacing, w, spacing):
            d.ellipse([x - radius, y - radius, x + radius, y + radius],
                      fill=(*color, alpha))
    return Image.alpha_composite(img.convert("RGBA"), layer)


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1],
                                           radius=radius, fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def spaced_text(draw, xy, text, font, fill, spacing=8, anchor_center=True):
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x, y = xy
    if anchor_center:
        x -= total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += w + spacing
    return total


def glow(base, center, radius, color, strength=90):
    w, h = base.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=(*color, strength))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.5))
    return Image.alpha_composite(base, layer)


# --- user avatar --------------------------------------------------------------
def make_avatar(size=460, accent="#00b4d8", monogram="GX", bg="#0b2545"):
    img = linear_gradient((size, size), hex2rgb(bg), mix(hex2rgb(bg), (0, 0, 0), 0.35))
    img = dot_grid(img, hex2rgb(accent), spacing=size // 14, radius=1, alpha=36)
    img = glow(img, (size * 0.72, size * 0.28), size * 0.45, hex2rgb(accent), 70)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, int(size * 0.34))
    spaced_text(d, (size / 2, size * 0.47), monogram, font, (255, 255, 255), spacing=size * 0.02)
    # accent underline
    d.rounded_rectangle([size * 0.34, size * 0.70, size * 0.66, size * 0.72],
                        radius=6, fill=hex2rgb(accent))
    return img


def make_avatar_anim(size=460, frames=24, accent="#00b4d8", monogram="GX", bg="#0b2545"):
    out = []
    for i in range(frames):
        t = i / frames
        img = linear_gradient((size, size), hex2rgb(bg), mix(hex2rgb(bg), (0, 0, 0), 0.35))
        img = dot_grid(img, hex2rgb(accent), spacing=size // 14, radius=1, alpha=36)
        # moving glow
        cx = size * (0.5 + 0.28 * __import__("math").cos(2 * 3.14159 * t))
        cy = size * (0.5 + 0.28 * __import__("math").sin(2 * 3.14159 * t))
        img = glow(img, (cx, cy), size * 0.42, hex2rgb(accent), 80)
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_BOLD, int(size * 0.34))
        spaced_text(d, (size / 2, size * 0.47), monogram, font, (255, 255, 255), spacing=size * 0.02)
        d.rounded_rectangle([size * 0.34, size * 0.70, size * 0.66, size * 0.72],
                            radius=6, fill=hex2rgb(accent))
        out.append(img.convert("P", palette=Image.ADAPTIVE, colors=128))
    return out


# --- org logo -----------------------------------------------------------------
def make_logo(code, size=460, accent="#00b4d8", bg="#0b2545"):
    img = linear_gradient((size, size), hex2rgb(bg), mix(hex2rgb(bg), (0, 0, 0), 0.3))
    img = dot_grid(img, hex2rgb(accent), spacing=size // 16, radius=1, alpha=30)
    img = glow(img, (size * 0.3, size * 0.7), size * 0.4, hex2rgb(accent), 60)
    d = ImageDraw.Draw(img)
    # ring
    m = size * 0.10
    d.ellipse([m, m, size - m, size - m], outline=(*hex2rgb(accent), 255), width=max(3, size // 90))
    font = ImageFont.truetype(FONT_BOLD, int(size * 0.26))
    spaced_text(d, (size / 2, size / 2), code, font, (255, 255, 255), spacing=size * 0.015)
    return img


def make_logo_anim(code, size=460, frames=20, accent="#00b4d8", bg="#0b2545"):
    out = []
    for i in range(frames):
        t = i / frames
        img = linear_gradient((size, size), hex2rgb(bg), mix(hex2rgb(bg), (0, 0, 0), 0.3))
        img = dot_grid(img, hex2rgb(accent), spacing=size // 16, radius=1, alpha=30)
        cx = size * (0.5 + 0.3 * __import__("math").cos(2 * 3.14159 * t))
        cy = size * (0.5 + 0.3 * __import__("math").sin(2 * 3.14159 * t))
        img = glow(img, (cx, cy), size * 0.4, hex2rgb(accent), 70)
        d = ImageDraw.Draw(img)
        m = size * 0.10
        d.ellipse([m, m, size - m, size - m], outline=(*hex2rgb(accent), 255), width=max(3, size // 90))
        font = ImageFont.truetype(FONT_BOLD, int(size * 0.26))
        spaced_text(d, (size / 2, size / 2), code, font, (255, 255, 255), spacing=size * 0.015)
        out.append(img.convert("P", palette=Image.ADAPTIVE, colors=128))
    return out


# --- banners ------------------------------------------------------------------
def make_banner(title, subtitle, size=(1280, 320), accent="#00b4d8", bg="#0b2545"):
    w, h = size
    img = linear_gradient(size, mix(hex2rgb(bg), (0, 0, 0), 0.1), hex2rgb(bg), diagonal=False)
    img = dot_grid(img, hex2rgb(accent), spacing=26, radius=1, alpha=30)
    img = glow(img, (w * 0.82, h * 0.2), h * 0.6, hex2rgb(accent), 70)
    d = ImageDraw.Draw(img)
    tf = ImageFont.truetype(FONT_BOLD, int(h * 0.28))
    sf = ImageFont.truetype(FONT_REG, int(h * 0.115))
    d.text((w * 0.06, h * 0.36), title, font=tf, fill=(255, 255, 255), anchor="lm")
    d.text((w * 0.06, h * 0.62), subtitle, font=sf, fill=(*hex2rgb(accent), 255), anchor="lm")
    d.rounded_rectangle([w * 0.06, h * 0.74, w * 0.06 + 90, h * 0.74 + 5], radius=4,
                        fill=hex2rgb(accent))
    return img


# --- cards (self-hosted, no third-party service) ------------------------------
def make_focus_card(items, size=(1280, 300), accent="#00b4d8", bg="#0b2545"):
    """items: list of (label, value) pairs, e.g. ('Domains','4')."""
    w, h = size
    img = linear_gradient(size, hex2rgb(bg), mix(hex2rgb(bg), (0, 0, 0), 0.3), diagonal=False)
    img = dot_grid(img, hex2rgb(accent), spacing=28, radius=1, alpha=24)
    img = glow(img, (w * 0.5, h * 1.05), h * 0.9, hex2rgb(accent), 60)
    d = ImageDraw.Draw(img)
    lf = ImageFont.truetype(FONT_REG, 26)
    vf = ImageFont.truetype(FONT_BOLD, 64)
    n = len(items)
    slot = w / n
    for i, (label, value) in enumerate(items):
        cx = slot * (i + 0.5)
        d.text((cx, h * 0.42), str(value), font=vf, fill=(255, 255, 255), anchor="mm")
        d.text((cx, h * 0.66), label, font=lf, fill=(*hex2rgb(accent), 255), anchor="mm")
        if i:
            d.line([(slot * i, h * 0.25), (slot * i, h * 0.75)], fill=(*hex2rgb(accent), 90), width=2)
    return img


def make_skill_card(skills, size=(1280, 220), accent="#00b4d8", bg="#0b2545"):
    """skills: list of strings rendered as pill chips."""
    w, h = size
    img = linear_gradient(size, hex2rgb(bg), mix(hex2rgb(bg), (0, 0, 0), 0.3), diagonal=False)
    img = dot_grid(img, hex2rgb(accent), spacing=26, radius=1, alpha=22)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, 30)
    gap, pad, x, y = 18, 22, 40, h / 2
    for s in skills:
        tw = d.textlength(s, font=font)
        bw = tw + pad * 2
        if x + bw > w - 40:
            break
        d.rounded_rectangle([x, y - 28, x + bw, y + 28], radius=28,
                            outline=(*hex2rgb(accent), 255), width=3,
                            fill=mix(hex2rgb(bg), hex2rgb(accent), 0.18))
        d.text((x + pad, y), s, font=font, fill=(255, 255, 255), anchor="lm")
        x += bw + gap
    return img


def main():
    core = parse_core(CORE)
    vis = core["visual"] or PALETTE
    accent = vis.get("accent", PALETTE["accent"])
    bg = vis.get("primary", PALETTE["primary"])

    os.makedirs(PROFILE, exist_ok=True)
    written = []

    # user avatar
    a = make_avatar(accent=accent, bg=bg)
    p = os.path.join(PROFILE, "avatar-460.png")
    a.save(p)
    written.append(p)
    frames = make_avatar_anim(accent=accent, bg=bg)
    p = os.path.join(PROFILE, "avatar-460.gif")
    frames[0].save(p, save_all=True, append_images=frames[1:], duration=80, loop=0, disposal=2)
    written.append(p)

    # user banner
    name = core["owner"].get("display_name", "Profile")
    tagline = core["owner"].get("tagline", "")
    b = make_banner(name, tagline, accent=accent, bg=bg)
    p = os.path.join(PROFILE, "banner-1280x320.png")
    b.save(p)
    written.append(p)

    # self-hosted cards (no third-party service, so nothing can break)
    focus = make_focus_card([("Domains", 4), ("Organizations", len(core["orgs"])),
                             ("Focus", "K8s"), ("Approach", "GitOps")], accent=accent, bg=bg)
    p = os.path.join(PROFILE, "card-focus-1280x300.png")
    focus.save(p)
    written.append(p)

    skills = make_skill_card(["Kubernetes", "Docker", "Terraform", "Argo CD",
                              "Flux", "GitOps", "Linux", "Go", "Python", "Bash",
                              "Prometheus", "Grafana"], accent=accent, bg=bg)
    p = os.path.join(PROFILE, "card-skills-1280x220.png")
    skills.save(p)
    written.append(p)

    # org logos + banners
    for o in core["orgs"]:
        login = o["login"]
        org_dir = os.path.join(ORGS, login, "assets")
        os.makedirs(org_dir, exist_ok=True)
        code = o.get("code", login[:3].upper())
        oaccent = o.get("accent", accent)
        logo = make_logo(code, accent=oaccent, bg=bg)
        p = os.path.join(org_dir, f"{login}-logo-460.png")
        logo.save(p)
        written.append(p)
        fr = make_logo_anim(code, accent=oaccent, bg=bg)
        p = os.path.join(org_dir, f"{login}-logo-460.gif")
        fr[0].save(p, save_all=True, append_images=fr[1:], duration=90, loop=0, disposal=2)
        written.append(p)
        banner = make_banner(o.get("display_name", login), o.get("one_liner", ""),
                             size=(1280, 240), accent=oaccent, bg=bg)
        p = os.path.join(org_dir, f"{login}-banner-1280x240.png")
        banner.save(p)
        written.append(p)

    print(f"wrote {len(written)} assets")
    for w in written:
        print("  ", os.path.relpath(w, HERE))


if __name__ == "__main__":
    main()
