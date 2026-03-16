from __future__ import annotations

from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin


class HtmlParser:
    NOISE_SELECTORS = (
        "script",
        "style",
        "noscript",
        "iframe",
        "svg",
        "canvas",
        "button",
        "input",
        "select",
        "textarea",
        "nav",
        "footer",
        "aside",
    )
    CONTENT_CANDIDATES = ("main", "article", "[role='main']", ".content", "#content")
    NOISE_HINTS = (
        "menu",
        "nav",
        "footer",
        "header",
        "sidebar",
        "aside",
        "banner",
        "ads",
        "advert",
        "social",
        "breadcrumb",
        "comment",
        "related",
        "recommend",
        "popup",
        "subscribe",
        "widget",
        "share",
        "tool",
    )

    def parse(self, html: str, base_url: str) -> dict[str, object]:
        soup = BeautifulSoup(html, "html.parser")

        self._remove_noise(soup)

        title = self._extract_title(soup)
        links = self._extract_links(soup, base_url)
        main_text = self._extract_main_text(soup)

        return {
            "title": title,
            "main_text": main_text,
            "links": links,
        }

    def extract_full_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        self._remove_noise(soup)
        container = soup.body or soup
        return self._clean_whitespace(container.get_text(" ", strip=True))

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        if soup.title and soup.title.string:
            return self._clean_whitespace(soup.title.string)

        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            return self._clean_whitespace(og_title["content"])

        return None

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> list[dict[str, str | None]]:
        extracted_links: list[dict[str, str | None]] = []
        seen: set[str] = set()

        for anchor in soup.find_all("a", href=True):
            href = anchor.get("href", "").strip()
            if not href:
                continue

            absolute_url = urljoin(base_url, href)
            if absolute_url in seen:
                continue

            seen.add(absolute_url)
            title = self._clean_whitespace(anchor.get_text(" ", strip=True)) or None
            extracted_links.append(
                {
                    "title": title,
                    "url": absolute_url,
                }
            )

        return extracted_links

    def _extract_main_text(self, soup: BeautifulSoup) -> str:
        container = self._find_best_content_container(soup)
        return self._clean_whitespace(container.get_text(" ", strip=True))

    def _remove_noise(self, soup: BeautifulSoup) -> None:
        for tag in soup.select(",".join(self.NOISE_SELECTORS)):
            tag.decompose()

        for tag in soup.find_all(self._is_noise_block):
            tag.decompose()

    def _find_best_content_container(self, soup: BeautifulSoup) -> Tag:
        for selector in self.CONTENT_CANDIDATES:
            found = soup.select_one(selector)
            if found and self._text_length(found) > 100:
                return found

        candidates = soup.find_all(["article", "main", "section", "div"])
        scored_candidates = [
            (self._score_candidate(candidate), candidate)
            for candidate in candidates
            if self._text_length(candidate) > 80
        ]

        if scored_candidates:
            scored_candidates.sort(key=lambda item: item[0], reverse=True)
            return scored_candidates[0][1]

        return soup.body or soup

    def _score_candidate(self, tag: Tag) -> float:
        text_length = self._text_length(tag)
        link_text_length = sum(len(link.get_text(" ", strip=True)) for link in tag.find_all("a"))
        paragraph_count = len(tag.find_all(["p", "li"]))
        heading_bonus = len(tag.find_all(["h1", "h2", "h3"])) * 20
        penalty = 0

        attrs = " ".join(
            filter(
                None,
                [
                    tag.get("id", ""),
                    " ".join(tag.get("class", [])),
                ],
            )
        ).lower()
        if any(hint in attrs for hint in self.NOISE_HINTS):
            penalty += 200

        return text_length + paragraph_count * 40 + heading_bonus - link_text_length - penalty

    def _text_length(self, tag: Tag) -> int:
        return len(self._clean_whitespace(tag.get_text(" ", strip=True)))

    def _is_noise_block(self, tag: Tag) -> bool:
        if not isinstance(tag, Tag):
            return False

        if tag.name in {"html", "body", "main", "article", "form"}:
            return False

        attrs = " ".join(
            filter(
                None,
                [
                    tag.get("id", ""),
                    " ".join(tag.get("class", [])),
                ],
            )
        ).lower()
        if not any(hint in attrs for hint in self.NOISE_HINTS):
            return False

        return self._text_length(tag) < 1500

    @staticmethod
    def _clean_whitespace(value: str) -> str:
        return " ".join(value.split())
