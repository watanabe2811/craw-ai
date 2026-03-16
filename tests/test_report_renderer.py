from app.exporters.report_renderer import render_cafef_report


def test_render_cafef_report_omits_news_and_analysis_sections() -> None:
    report = render_cafef_report(
        {
            "title": "Bao cao mau",
            "market_indices": [
                {
                    "name": "HOSE",
                    "value": "1200",
                    "change": "-1.2",
                    "change_percent": "-0.1 %",
                }
            ],
            "latest_news": [
                {
                    "time": "08:00",
                    "title": "Tin 1",
                    "url": "https://example.com/news-1",
                }
            ],
            "analysis_reports": [
                {
                    "date": "16/03",
                    "symbol": "AAA",
                    "title": "Phan tich 1",
                    "url": "https://example.com/report-1",
                }
            ],
            "top_stocks": [
                {
                    "rank": "1",
                    "symbol": "AAA",
                    "price": "10.5",
                    "change": "+0.2",
                    "volume": "1000",
                }
            ],
        }
    )

    assert "Bao cao mau" in report
    assert "Chi so thi truong" in report
    assert "#1 AAA" in report
    assert "Tin moi" not in report
    assert "Bao cao phan tich" not in report
