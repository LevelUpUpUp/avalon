#!/usr/bin/env python3
"""Check generated pages, internal links and publication readiness."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build import ROOT


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.errors = set(), [], []
        self.heading_count = 0
        self.language = None
        self.viewport = False
        self.title = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        if tag == "title":
            self.title = True
        if tag == "h1":
            self.heading_count += 1
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.errors.append("Duplicate id: " + attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "script" or tag in ("iframe", "form"):
            self.errors.append("Unexpected active or embedded content: " + tag)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "link" and attrs.get("rel") == "stylesheet":
            href = attrs.get("href", "")
            if urlsplit(href).scheme or href.startswith("//"):
                self.errors.append("External stylesheet: " + href)
            self.links.append(href)


def check(root, allow_draft=False):
    errors, pages = [], {}
    expected = ("index.html", "privacy/index.html", "privacy/en/index.html", "support/index.html", "support/en/index.html")
    root = root.resolve()
    for relative in expected:
        path = root / relative
        if not path.is_file():
            errors.append("Missing page: " + relative)
            continue
        source = path.read_text(encoding="utf-8")
        page = Page()
        page.feed(source)
        pages[path] = page
        if page.language not in ("zh-CN", "en") or not page.title or not page.viewport or page.heading_count != 1:
            errors.append(relative + ": missing language/title/viewport or invalid main heading")
        if "{{" in source or "}}" in source:
            errors.append(relative + ": unresolved template")
        if not allow_draft and any(token in source for token in ('class="draft"', "contact-pending@", "example.invalid", "名称待填写")):
            errors.append(relative + ": draft content cannot be published")
        errors.extend(relative + ": " + error for error in page.errors)
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme in ("https", "mailto"):
                continue
            if not link or url.scheme or link.startswith("/"):
                errors.append(str(path.relative_to(root)) + ": invalid or base-path-unsafe link " + link)
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(str(path.relative_to(root)) + ": broken link " + link)
            elif url.fragment and (target not in pages or unquote(url.fragment) not in pages[target].ids):
                errors.append(str(path.relative_to(root)) + ": broken fragment " + link)
    if errors:
        raise ValueError("\n".join(errors))
    print("Checked 5 pages: internal links, language switches, anchors, mobile metadata and passive content." + (" Draft preview allowed." if allow_draft else " Publication content complete."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=ROOT / "_site")
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()
    try:
        check(args.directory, args.allow_draft)
    except ValueError as exc:
        parser.exit(1, str(exc) + "\n")
