# OpenClaw Skill Deployment Guide

Tai lieu nay huong dan cach dong goi va trien khai project thanh mot skill de OpenClaw co the goi lai on dinh.

## 1. Muc tieu

Bo skill nay giup OpenClaw:

- crawl 1 URL dong qua Cloudflare Browser Rendering API
- mac dinh tra ve bao cao text de doc nhanh
- van luu JSON va co the chuyen sang JSON output khi can
- cap nhat code tu Git bang 1 script rieng

## 2. Cac file da tao

### Shell wrappers

- `bin/openclaw-crawl.sh`
  - wrapper mac dinh de chay crawler
  - doi lenh dai `python main.py crawl ...` thanh 1 lenh ngan

- `bin/openclaw-discord.sh`
  - wrapper cho bot Discord
  - stdout chi tra ve noi dung text chinh de bot gui lai
  - ho tro gioi han so ky tu de tranh vuot muc Discord

- `bin/openclaw-update.sh`
  - cap nhat code tu Git bang `git fetch --tags` va `git pull --ff-only`
  - sau do refresh dependency neu `.venv` da ton tai

### Skill package

- `skills/openclaw-cafef-report/SKILL.md`
- `skills/openclaw-cafef-report/agents/openai.yaml`
- `skills/openclaw-cafef-report/scripts/run-skill.sh`
- `skills/openclaw-cafef-report/scripts/run-discord.sh`
- `skills/openclaw-cafef-report/scripts/update-project.sh`

## 3. Chuan bi moi truong

Chay trong repo:

```bash
cd /Users/toruwatanabe/workspace/AI/crawl_ai
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Tao `.env`:

```env
CF_ACCOUNT_ID=your_cloudflare_account_id
CF_API_TOKEN=your_cloudflare_api_token
```

## 4. Cach chay truc tiep

Lenh mac dinh:

```bash
./bin/openclaw-crawl.sh
```

Chay voi URL cu the:

```bash
./bin/openclaw-crawl.sh "https://cafef.vn/du-lieu.chn"
```

Lay JSON thay vi report:

```bash
./bin/openclaw-crawl.sh "https://cafef.vn/du-lieu.chn" json
```

Luu them HTML raw:

```bash
./bin/openclaw-crawl.sh "https://cafef.vn/du-lieu.chn" report --save-raw
```

Lenh danh cho Discord bot:

```bash
./bin/openclaw-discord.sh
```

Truyen URL cu the:

```bash
./bin/openclaw-discord.sh "https://cafef.vn/du-lieu.chn"
```

Truyen JSON neu bot can:

```bash
./bin/openclaw-discord.sh "https://cafef.vn/du-lieu.chn" json
```

Gioi han 1900 ky tu stdout cho Discord:

```bash
./bin/openclaw-discord.sh "https://cafef.vn/du-lieu.chn" report 1900
```

## 5. Cach update code

```bash
./bin/openclaw-update.sh
```

Script nay:

1. fetch tag va branch moi nhat tu `origin`
2. pull fast-forward cho branch hien tai
3. cai lai dependency neu `.venv` da ton tai

Neu co local changes khong the fast-forward, script se dung de tranh ghi de thay doi cua ban.

## 6. Cach dung skill voi OpenClaw / Codex skills

### Cach 1: Dung ngay trong repo

Neu OpenClaw/Codex co the truy cap workspace nay, chi can tro toi skill:

```text
/Users/toruwatanabe/workspace/AI/crawl_ai/skills/openclaw-cafef-report
```

### Cach 2: Copy skill vao kho skills rieng

Copy folder:

```bash
cp -R /Users/toruwatanabe/workspace/AI/crawl_ai/skills/openclaw-cafef-report \
  "$CODEX_HOME/skills/openclaw-cafef-report"
```

Neu skill khong nam ben trong repo goc, dat bien moi truong truoc khi chay:

```bash
export OPENCLAW_CRAWLER_REPO=/Users/toruwatanabe/workspace/AI/crawl_ai
```

Khi do:

```bash
"$CODEX_HOME/skills/openclaw-cafef-report/scripts/run-skill.sh"
"$CODEX_HOME/skills/openclaw-cafef-report/scripts/update-project.sh"
```

## 7. Entry points de OpenClaw goi

Lenh chinh:

```bash
./bin/openclaw-crawl.sh
```

Lenh danh cho Discord:

```bash
./bin/openclaw-discord.sh
```

Lenh update:

```bash
./bin/openclaw-update.sh
```

Skill wrapper:

```bash
./skills/openclaw-cafef-report/scripts/run-skill.sh
./skills/openclaw-cafef-report/scripts/run-discord.sh
./skills/openclaw-cafef-report/scripts/update-project.sh
```

## 8. Dau ra mac dinh

Mac dinh chuong trinh se:

1. in report text ra console
2. luu report vao `output/*.report.txt`
3. luu JSON vao `output/*.json`
4. chi luu HTML raw khi co `--save-raw`

Neu dung wrapper Discord:

1. stdout chi chua noi dung text chinh
2. khong in them dong `Saved ...` vao stdout
3. van luu report va JSON vao `output/`
4. co the cat ngan text bang tham so gioi han ky tu

## 9. Kiem tra sau trien khai

Chay test:

```bash
.venv/bin/pytest -q
```

Chay smoke test:

```bash
./bin/openclaw-crawl.sh "https://cafef.vn/du-lieu.chn"
```

Neu thanh cong, ban se thay:

- report text tren console
- file moi trong `output/`

## 10. Goi y tich hop cho OpenClaw

Default command nen cau hinh la:

```bash
./bin/openclaw-crawl.sh
```

Neu OpenClaw can truyen URL dong:

```bash
./bin/openclaw-crawl.sh "<TARGET_URL>"
```

Neu OpenClaw can output JSON:

```bash
./bin/openclaw-crawl.sh "<TARGET_URL>" json
```

Neu Discord bot can nhan thang noi dung text tu stdout:

```bash
./bin/openclaw-discord.sh "<TARGET_URL>"
```

Neu bot chi nhan toi da 1900 ky tu:

```bash
./bin/openclaw-discord.sh "<TARGET_URL>" report 1900
```
