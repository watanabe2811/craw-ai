from __future__ import annotations


def render_cafef_report(data: dict[str, object]) -> str:
    lines: list[str] = []

    title = data.get("title") or "Bao cao CafeF"
    lines.append(str(title))
    lines.append("=" * len(str(title)))
    lines.append("")

    indices = data.get("market_indices", [])
    if isinstance(indices, list) and indices:
        lines.append("Chi so thi truong")
        lines.append("-" * 18)
        for item in indices:
            if not isinstance(item, dict):
                continue
            lines.append(
                f"- {item.get('name')}: {item.get('value')} | {item.get('change')} | {item.get('change_percent')}"
            )
        lines.append("")

    latest_news = data.get("latest_news", [])
    if isinstance(latest_news, list) and latest_news:
        lines.append("Tin moi")
        lines.append("-" * 7)
        for item in latest_news[:10]:
            if not isinstance(item, dict):
                continue
            lines.append(f"- [{item.get('time')}] {item.get('title')}\n  {item.get('url')}")
        lines.append("")

    top_stocks = data.get("top_stocks", [])
    if isinstance(top_stocks, list) and top_stocks:
        lines.append("Top co phieu")
        lines.append("-" * 12)
        for item in top_stocks[:10]:
            if not isinstance(item, dict):
                continue
            lines.append(
                f"- #{item.get('rank')} {item.get('symbol')}: gia {item.get('price')}, thay doi {item.get('change')}, KL {item.get('volume')}"
            )
        lines.append("")

    top_hits = data.get("top_hits", [])
    if isinstance(top_hits, list) and top_hits:
        lines.append("Top truy cap")
        lines.append("-" * 11)
        for item in top_hits[:10]:
            if not isinstance(item, dict):
                continue
            lines.append(
                f"- #{item.get('rank')} {item.get('symbol')}: gia {item.get('price')}, thay doi {item.get('change')}, KL {item.get('volume')}"
            )
        lines.append("")

    commodities = data.get("commodities", {})
    if isinstance(commodities, dict):
        items = commodities.get("items", [])
        updated_at = commodities.get("updated_at")
        if isinstance(items, list) and items:
            lines.append("Hang hoa")
            lines.append("-" * 8)
            if updated_at:
                lines.append(f"Cap nhat: {updated_at}")
            for item in items[:10]:
                if not isinstance(item, dict):
                    continue
                lines.append(
                    f"- #{item.get('rank')} {item.get('name')}: gia {item.get('price')}, thay doi {item.get('change')}"
                )
            if commodities.get("more_url"):
                lines.append(f"Xem them: {commodities.get('more_url')}")
            lines.append("")

    analysis_reports = data.get("analysis_reports", [])
    if isinstance(analysis_reports, list) and analysis_reports:
        lines.append("Bao cao phan tich")
        lines.append("-" * 17)
        for item in analysis_reports[:10]:
            if not isinstance(item, dict):
                continue
            lines.append(f"- [{item.get('date')}] {item.get('symbol')}: {item.get('title')}\n  {item.get('url')}")
        lines.append("")

    note = data.get("note")
    if note:
        lines.append("Ghi chu")
        lines.append("-" * 7)
        lines.append(str(note))
        lines.append("")

    source = data.get("source")
    if isinstance(source, dict):
        lines.append("Nguon")
        lines.append("-" * 5)
        lines.append(f"{source.get('title')}: {source.get('url')}")

    return "\n".join(lines).strip() + "\n"
