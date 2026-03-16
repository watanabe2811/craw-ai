from app.parsers.html_parser import HtmlParser


def test_html_parser_extracts_title_text_and_links() -> None:
    html = """
    <html>
      <head>
        <title> Demo Page </title>
        <style>.hidden { display: none; }</style>
      </head>
      <body>
        <main>
          <h1>Hello world</h1>
          <p>This is AJAX content.</p>
          <a href="/news"> News </a>
          <a href="https://example.org/about"> About </a>
        </main>
        <script>console.log("ignore");</script>
      </body>
    </html>
    """

    parser = HtmlParser()
    result = parser.parse(html, "https://example.org/root")

    assert result["title"] == "Demo Page"
    assert result["main_text"] == "Hello world This is AJAX content. News About"
    assert result["links"] == [
        {"title": "News", "url": "https://example.org/news"},
        {"title": "About", "url": "https://example.org/about"},
    ]


def test_html_parser_handles_missing_fields() -> None:
    parser = HtmlParser()
    result = parser.parse("<html><body><div>No title here</div></body></html>", "https://x.test")

    assert result["title"] is None
    assert result["links"] == []
    assert result["main_text"] == "No title here"


def test_html_parser_prefers_main_content_over_navigation_blocks() -> None:
    html = """
    <html>
      <body>
        <div class="top-nav">
          <a href="/home">Home</a>
          <a href="/market">Market</a>
          <a href="/watchlist">Watchlist</a>
        </div>
        <div class="article-detail">
          <h1>Market overview</h1>
          <p>Stocks rose after strong banking and industrial results.</p>
          <p>Liquidity improved in the afternoon session.</p>
        </div>
        <div class="related-news">
          <a href="/related-1">Related one</a>
          <a href="/related-2">Related two</a>
        </div>
      </body>
    </html>
    """

    parser = HtmlParser()
    result = parser.parse(html, "https://example.com")

    assert result["main_text"] == (
        "Market overview Stocks rose after strong banking and industrial results. "
        "Liquidity improved in the afternoon session."
    )
