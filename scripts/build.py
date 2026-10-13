#!/usr/bin/env python3
"""Build accessible static policy pages using only the Python standard library."""
import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    ("privacy", "zh-CN", "privacy/index.html", "隐私政策", "privacy/en/index.html"),
    ("privacy", "en", "privacy/en/index.html", "Privacy policy", "privacy/index.html"),
    ("support", "zh-CN", "support/index.html", "支持", "support/en/index.html"),
    ("support", "en", "support/en/index.html", "Support", "support/index.html"),
)


def validate_config(config):
    errors = []
    name = config.get("developer_name", "").strip()
    email = config.get("contact_email", "").strip()
    if not name or any(token in name.lower() for token in ("todo", "placeholder", "待填写")):
        errors.append("Set developer_name in site.json to the actual developer or legal entity.")
    if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", email):
        errors.append("Set contact_email in site.json to a monitored public contact email.")
    elif email.lower().endswith(("@example.com", ".invalid", ".test")):
        errors.append("A placeholder email cannot be published.")
    try:
        date.fromisoformat(config.get("last_updated", ""))
    except (ValueError, TypeError):
        errors.append("Set last_updated to an ISO date (YYYY-MM-DD).")
    return errors


def inline(value):
    """Render the small, controlled Markdown subset used by the policy sources."""
    token = re.compile(r"\[([^\]]+)\]\(([^\s)]+)\)|\*\*([^*]+)\*\*")
    parts, pos = [], 0
    for match in token.finditer(value):
        parts.append(escape(value[pos:match.start()]))
        if match.group(3) is not None:
            parts.append("<strong>" + escape(match.group(3)) + "</strong>")
        else:
            label, href = match.group(1), match.group(2)
            if not (href.startswith(("https://", "mailto:", "../", "./", "#")) or ":" not in href):
                raise ValueError("Unsupported link scheme: " + href)
            parts.append('<a href="' + escape(href, quote=True) + '">' + escape(label) + "</a>")
        pos = match.end()
    parts.append(escape(value[pos:]))
    return "".join(parts)


def markdown(source):
    blocks, toc, paragraph = [], [], []
    in_list = False

    def flush():
        if paragraph:
            blocks.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    for line in source.splitlines() + [""]:
        if not line.startswith("- ") and in_list:
            blocks.append("</ul>")
            in_list = False
        if not line.strip():
            flush()
        elif line.startswith("# "):
            flush()
            blocks.append("<h1>" + inline(line[2:]) + "</h1>")
        elif line.startswith("## "):
            flush()
            section_id = "section-" + str(len(toc) + 1)
            heading = line[3:]
            toc.append((section_id, heading))
            blocks.append('<h2 id="' + section_id + '">' + inline(heading) + "</h2>")
        elif line.startswith("- "):
            flush()
            if not in_list:
                blocks.append("<ul>")
                in_list = True
            blocks.append("<li>" + inline(line[2:]) + "</li>")
        else:
            paragraph.append(line)
    return "\n".join(blocks), toc


def shell(title, language, output_path, content, toc, alternate, draft):
    prefix = "../" * (len(Path(output_path).parts) - 1)
    english = language == "en"
    privacy = "Privacy" if english else "隐私政策"
    support = "Support" if english else "支持"
    skip = "Skip to content" if english else "跳转到正文"
    note = "Privacy and support" if english else "隐私与支持"
    links = prefix + ("privacy/en/" if english else "privacy/")
    support_link = prefix + ("support/en/" if english else "support/")
    language_link = ""
    if alternate:
        language_link = '<a href="' + prefix + alternate.removesuffix("index.html") + '">' + ("简体中文" if english else "English") + "</a>"
    navigation = ""
    if toc:
        items = "".join('<li><a href="#' + ident + '">' + escape(label) + "</a></li>" for ident, label in toc)
        navigation = '<nav class="toc" aria-label="' + ("On this page" if english else "本页目录") + '"><p>' + ("On this page" if english else "本页目录") + "</p><ol>" + items + "</ol></nav>"
    banner = ""
    if draft:
        banner = '<aside class="draft">' + ("Draft preview — developer identity and contact details must be completed before publication." if english else "草稿预览：发布前需填写真实开发者名称及联系邮箱。") + "</aside>"
    robots = '<meta name="robots" content="noindex,nofollow">' if draft else ""
    return f'''<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(title + ' · Avalon', quote=True)}">
  <meta name="referrer" content="no-referrer">
  {robots}
  <title>{escape(title)} · Avalon</title>
  <link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
  <a class="skip" href="#main">{skip}</a>
  <header class="site-header"><a class="brand" href="{prefix}index.html">Avalon<span>{note}</span></a>
    <nav aria-label="{'Main navigation' if english else '主导航'}"><a href="{links}">{privacy}</a><a href="{support_link}">{support}</a>{language_link}</nav>
  </header>
  {banner}
  <div class="layout">{navigation}<main id="main" tabindex="-1">{content}</main></div>
  <footer>Avalon · {'Local photos. Your control.' if english else '本地照片，由你掌控。'}</footer>
</body>
</html>
'''


def build(output, allow_draft):
    config = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    errors = validate_config(config)
    if errors and not allow_draft:
        raise ValueError("Publication blocked:\n" + "\n".join(errors))
    output.mkdir(parents=True, exist_ok=True)
    (output / "assets").mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "assets/style.css", output / "assets/style.css")
    for kind, language, path, title, alternate in PAGES:
        source = (ROOT / "content" / f"{kind}.{language}.md").read_text(encoding="utf-8")
        values = {key: str(value).strip() for key, value in config.items()}
        if errors:
            values["developer_name"] = values.get("developer_name") or ("[Developer name pending]" if language == "en" else "[开发者名称待填写]")
            values["contact_email"] = values.get("contact_email") or "contact-pending@example.invalid"
        source = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], source)
        if "{{" in source or "}}" in source:
            raise ValueError("Unresolved template in " + path)
        content, toc = markdown(source)
        target = output / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(shell(title, language, path, content, toc, alternate, bool(errors)), encoding="utf-8")
    home = '''<p class="eyebrow">AVALON</p><h1>隐私与支持<br><span lang="en">Privacy &amp; support</span></h1>
<p>了解 Avalon 如何在你的设备上处理照片与视频，以及如何联系我们。</p>
<p lang="en">Learn how Avalon handles photos and videos on your devices, and how to contact us.</p>
<div class="cards"><section><h2>隐私政策 <span lang="en">Privacy policy</span></h2><p>本机处理、权限、分享与数据删除。</p><p><a href="privacy/">简体中文 →</a> <a href="privacy/en/" lang="en">English →</a></p></section>
<section><h2>支持 <span lang="en">Support</span></h2><p>联系方式与常见问题。</p><p><a href="support/">简体中文 →</a> <a href="support/en/" lang="en">English →</a></p></section></div>'''
    (output / "index.html").write_text(shell("隐私与支持 / Privacy & support", "zh-CN", "index.html", home, [], None, bool(errors)), encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built 5 pages in {output}" + (" (DRAFT; not ready to publish)" if errors else ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    parser.add_argument("--allow-draft", action="store_true", help="Local preview only; never used by the deployment workflow.")
    args = parser.parse_args()
    try:
        build(args.output, args.allow_draft)
    except (ValueError, KeyError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
