from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag


class CafeFSectionsParser:
    def parse(self, html: str, base_url: str) -> dict[str, object]:
        soup = BeautifulSoup(html, "html.parser")

        return {
            "title": self._extract_title(soup),
            "latest_news": self._extract_latest_news(soup, base_url),
            "market_indices": self._extract_market_indices(soup),
            "top_stocks": self._extract_ranked_table(soup, ".topstock_contentdata tr", base_url),
            "top_hits": self._extract_ranked_table(soup, ".stockhits_contentdata tr", base_url),
            "commodities": self._extract_commodities(soup),
            "analysis_reports": self._extract_analysis_reports(soup, base_url),
            "note": self._extract_note(soup),
            "source": self._extract_source(soup),
        }

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        if soup.title and soup.title.string:
            return " ".join(soup.title.string.split())
        return None

    def _extract_latest_news(self, soup: BeautifulSoup, base_url: str) -> list[dict[str, str | None]]:
        items: list[dict[str, str | None]] = []
        for li in soup.select("#listNewHeaderNew li"):
            anchor = li.find("a", href=True)
            if not anchor:
                continue

            time_node = li.find("span", class_="time")
            title = self._clean_text(anchor.get_text(" ", strip=True))
            items.append(
                {
                    "time": self._clean_text(time_node.get_text(" ", strip=True)) if time_node else None,
                    "title": title or None,
                    "url": urljoin(base_url, anchor["href"]),
                }
            )
        return items

    def _extract_market_indices(self, soup: BeautifulSoup) -> list[dict[str, str | None]]:
        items: list[dict[str, str | None]] = []
        seen: set[str] = set()

        for block in soup.select(".indexs_content > div > div[class^='price_indexs-']"):
            name_node = block.select_one(".index_name")
            value_node = block.select_one(".index_index")
            change_nodes = block.select(".index_change, .index_changePercent")
            if not name_node or not value_node:
                continue

            name = self._clean_text(name_node.get_text(" ", strip=True))
            if not name or name in seen:
                continue

            seen.add(name)
            change = self._clean_text(change_nodes[0].get_text(" ", strip=True)) if len(change_nodes) > 0 else None
            change_percent = (
                self._clean_text(change_nodes[1].get_text(" ", strip=True))
                if len(change_nodes) > 1
                else None
            )
            items.append(
                {
                    "name": name,
                    "value": self._clean_text(value_node.get_text(" ", strip=True)) or None,
                    "change": change or None,
                    "change_percent": change_percent or None,
                }
            )

        return items

    def _extract_ranked_table(
        self,
        soup: BeautifulSoup,
        selector: str,
        base_url: str,
    ) -> list[dict[str, str | None]]:
        rows: list[dict[str, str | None]] = []
        for row in soup.select(selector):
            cells = row.find_all(["td", "th"])
            if len(cells) < 5:
                continue

            anchor = row.find("a", href=True)
            symbol = self._clean_text(cells[1].get_text(" ", strip=True))
            if symbol == "Mã CK":
                continue

            rows.append(
                {
                    "rank": self._clean_text(cells[0].get_text(" ", strip=True)) or None,
                    "symbol": symbol or None,
                    "url": urljoin(base_url, anchor["href"]) if anchor else None,
                    "volume": self._clean_text(cells[2].get_text(" ", strip=True)) or None,
                    "price": self._clean_text(cells[3].get_text(" ", strip=True)) or None,
                    "change": self._clean_text(cells[4].get_text(" ", strip=True)) or None,
                }
            )
        return rows

    def _extract_commodities(self, soup: BeautifulSoup) -> dict[str, object]:
        rows: list[dict[str, str | None]] = []
        for row in soup.select("#dataBusiness tbody tr"):
            classes = row.get("class", [])
            if "businessv2_content_top" in classes:
                continue

            cells = row.find_all("th")
            if len(cells) < 4:
                continue

            rows.append(
                {
                    "rank": self._clean_text(cells[0].get_text(" ", strip=True)) or None,
                    "name": self._clean_text(cells[1].get_text(" ", strip=True)) or None,
                    "price": self._clean_text(cells[2].get_text(" ", strip=True)) or None,
                    "change": self._clean_text(cells[3].get_text(" ", strip=True)) or None,
                }
            )

        update_node = soup.select_one(".businessv2_content_bottom .timeUpdate")
        more_node = soup.select_one(".businessv2_content_bottom .showAll")
        return {
            "updated_at": self._clean_text(update_node.get_text(" ", strip=True)) if update_node else None,
            "items": rows,
            "more_url": urljoin("https://cafef.vn", more_node["href"]) if more_node and more_node.get("href") else None,
        }

    def _extract_analysis_reports(
        self,
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[dict[str, str | None]]:
        items: list[dict[str, str | None]] = []
        for card in soup.select(".market__and__analysis__right__body__item"):
            head_link = card.select_one(".market__and__analysis__item__content__head div a[href]")
            meta = card.select_one(".market__and__analysis__item__content__bottom div")
            if not head_link:
                continue

            date_node = meta.find("p") if meta else None
            symbol_node = meta.find("span") if meta else None
            items.append(
                {
                    "title": self._clean_text(head_link.get_text(" ", strip=True)) or None,
                    "url": urljoin(base_url, head_link["href"]),
                    "date": self._clean_text(date_node.get_text(" ", strip=True)) if date_node else None,
                    "symbol": self._clean_text(symbol_node.get_text(" ", strip=True)) if symbol_node else None,
                }
            )
        return items

    def _extract_note(self, soup: BeautifulSoup) -> str | None:
        note_node = soup.select_one("#labelBottom")
        if not note_node:
            return None
        return self._clean_text(note_node.get_text(" ", strip=True)) or None

    def _extract_source(self, soup: BeautifulSoup) -> dict[str, str | None] | None:
        source_node = soup.select_one("#refTTVN a[href]")
        if not source_node:
            return None
        return {
            "title": self._clean_text(source_node.get_text(" ", strip=True)) or None,
            "url": source_node.get("href"),
        }

    @staticmethod
    def _clean_text(value: str) -> str:
        return " ".join(value.split())

