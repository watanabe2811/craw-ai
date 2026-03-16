# Cloudflare Browser Rendering Single-URL Crawler

Project Python 3.11 nay thu thap noi dung tu mot URL dong bang Cloudflare Browser Rendering API thay vi chay Playwright hoac Selenium. Ung dung goi endpoint `/browser-rendering/content`, nhan HTML da render, parse noi dung chinh, chuan hoa du lieu thanh JSON, va luu ra file trong `output/`.

## Kien truc

```text
URL
 ↓
Cloudflare Browser Rendering API (/content)
 ↓
HTML rendered
 ↓
HTML parser
 ↓
JSON normalization
 ↓
Export file
```

## Cau truc thu muc

```text
project_root/
  app/
    clients/
      cloudflare_client.py
    parsers/
      html_parser.py
    models/
      response_models.py
    exporters/
      json_exporter.py
    services/
      crawl_service.py
    utils/
      config_loader.py
      logger.py
  config/
    config.yaml
  output/
  logs/
  tests/
  main.py
  requirements.txt
  README.md
  .env.example
```

## Cai dat

1. Tao virtual environment Python 3.11.
2. Cai dependencies:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Tao file `.env` tu `.env.example`.

## Tao Cloudflare API token

1. Dang nhap Cloudflare dashboard.
2. Tao API token co quyen goi Browser Rendering API cho account cua ban.
3. Lay `Account ID` tu Cloudflare dashboard.
4. Dien thong tin vao file `.env`:

```env
CF_ACCOUNT_ID=your_cloudflare_account_id
CF_API_TOKEN=your_cloudflare_api_token
```

Khong commit file `.env` hoac token that vao git.

## Cau hinh

File `config/config.yaml`:

```yaml
base_url: "https://api.cloudflare.com/client/v4"
default_target_url: "https://cafef.vn/du-lieu.chn"
timeout: 60000
retry: 3
output_dir: "output"
```

## Cach chay CLI

Lenh co san:

```bash
python main.py crawl --url https://cafef.vn/du-lieu.chn
```

Tuy chon:

- `--url`: URL dich can render.
- `--save-raw`: luu them file HTML da render.
- `--debug`: bat DEBUG logging.

Vi du:

```bash
python main.py crawl --url https://cafef.vn/du-lieu.chn --save-raw --debug
```

Doc file HTML cuc bo va tra ve noi dung dang text:

```bash
python main.py extract-text --html-file output/cafef.vn_du-lieu.chn_20260316T081119Z.html
```

Luu text ra file:

```bash
python main.py extract-text \
  --html-file output/cafef.vn_du-lieu.chn_20260316T081119Z.html \
  --output-file output/cafef.vn_du-lieu.chn.txt
```

## JSON output schema

```json
{
  "source": "cloudflare_render",
  "url": "https://example.com/page",
  "collected_at": "2026-03-16T08:00:00Z",
  "title": "Example title",
  "main_text": "Main page content",
  "links": [
    {
      "title": "About",
      "url": "https://example.com/about"
    }
  ]
}
```

## Logging

- Console logging
- File logging tai `logs/app.log`
- Muc log: `INFO`, `DEBUG`, `ERROR`

## Parser notes

- Loai bo `script`, `style`, `nav`, `footer`, `aside`, form, iframe va cac khoi co class/id goi y la noise.
- Uu tien lay noi dung tu `main`, `article`, `[role="main"]`, `.content`, `#content`.
- Neu khong tim thay vung ro rang, parser cham diem cac khoi HTML theo do dai text, so doan van, heading va mat do link de chon `main_text` hop ly hon cho cac trang tin/ajax.

## Testing

Chay test:

```bash
pytest
```

Bao gom test cho:

- `html_parser`
- `normalizer`

## Luu y bao mat

- Khong hardcode Cloudflare token trong source code.
- Su dung bien moi truong `CF_ACCOUNT_ID` va `CF_API_TOKEN`.
- Su dung `.env.example` de chia se mau cau hinh an toan.
