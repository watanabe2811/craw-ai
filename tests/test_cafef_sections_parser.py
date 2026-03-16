from app.parsers.cafef_sections_parser import CafeFSectionsParser


def test_cafef_sections_parser_extracts_core_sections() -> None:
    html = """
    <html>
      <head><title>Toàn cảnh thị trường</title></head>
      <body>
        <div id="listNewHeaderNew">
          <ul>
            <li>
              <span class="time">08:00</span>
              <a href="/news-1.chn"><span class="inner">Tin 1</span></a>
            </li>
          </ul>
        </div>
        <div class="indexs_content">
          <div>
            <div class="price_indexs-ho">
              <div class="index_name">HOSE</div>
              <div class="index_index">1,200</div>
              <div class="index_change">-1.2</div>
              <div class="index_changePercent">-0.1 %</div>
            </div>
          </div>
        </div>
        <tbody class="topstock_contentdata">
          <tr>
            <td>1</td>
            <td><a href="/stock.chn">AAA</a></td>
            <td>1,000</td>
            <td>10.5</td>
            <td>+0.2 (+1.9%)</td>
          </tr>
        </tbody>
        <table id="dataBusiness">
          <tbody>
            <tr class="businessv2_content_top"><th>Header</th></tr>
            <tr>
              <th>1</th>
              <th><span>Vàng</span></th>
              <th>5000</th>
              <th><span class="down">-10 (-0.2%)</span></th>
            </tr>
          </tbody>
        </table>
        <div class="businessv2_content_bottom">
          <div class="timeUpdate">08:29 16/03/2026</div>
          <a class="showAll" href="/hang-hoa-tieu-bieu.chn">Xem thêm</a>
        </div>
        <div class="market__and__analysis__right__body__item">
          <div class="market__and__analysis__item__content">
            <div class="market__and__analysis__item__content__head">
              <div><a href="/report.chn">Bao cao A</a></div>
            </div>
            <div class="market__and__analysis__item__content__bottom">
              <div><p>16/03</p><span>AAA</span></div>
            </div>
          </div>
        </div>
        <div id="labelBottom">Lưu ý dữ liệu chỉ tham khảo.</div>
        <div id="refTTVN"><a href="http://example.com">Theo Trí thức trẻ</a></div>
      </body>
    </html>
    """

    result = CafeFSectionsParser().parse(html, "https://cafef.vn/du-lieu.chn")

    assert result["title"] == "Toàn cảnh thị trường"
    assert result["latest_news"] == [
        {
            "time": "08:00",
            "title": "Tin 1",
            "url": "https://cafef.vn/news-1.chn",
        }
    ]
    assert result["market_indices"] == [
        {
            "name": "HOSE",
            "value": "1,200",
            "change": "-1.2",
            "change_percent": "-0.1 %",
        }
    ]
    assert result["top_stocks"][0]["symbol"] == "AAA"
    assert result["commodities"]["items"][0]["name"] == "Vàng"
    assert result["analysis_reports"][0]["title"] == "Bao cao A"
    assert result["note"] == "Lưu ý dữ liệu chỉ tham khảo."
