# Podcast-to-Insight (Backend)

FastAPI backend that turns a Xiaoyuzhou episode page (or direct audio URL) into an AI text summary.

## Requirements

- Python 3.10+
- DashScope API key for transcription
- iFlow API key for summarization (OpenAI-compatible)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DASHSCOPE_API_KEY="your_dashscope_key"
export IFLOW_API_KEY="your_iflow_key"
```

Optional environment variables:

- `DASHSCOPE_BASE_URL` (default: `https://dashscope.aliyuncs.com/api/v1`)
- `DASHSCOPE_ASR_MODEL` (default: `fun-asr`)
- `IFLOW_BASE_URL` (default: `https://apis.iflow.cn/v1`)
- `IFLOW_SUMMARY_MODEL` (default: `TBStars2-200B-A13B`)
- `DASHSCOPE_POLL_INTERVAL_S` (default: `2.0`)
- `DASHSCOPE_POLL_TIMEOUT_S` (default: `900.0`)
- `MAX_AUDIO_BYTES` (default: `209715200`)
- `SUMMARY_CHUNK_CHARS` (default: `6000`)
- `SUMMARY_CHUNK_OVERLAP` (default: `300`)
- `SUMMARY_LANGUAGE` (default: `zh`)
- `SUMMARY_STYLE` (default: `bullet`)
- `SUMMARY_MAX_WORDS` (default: `200`)

## 启动

后端（FastAPI，默认 `http://localhost:8000`）：

```bash
uvicorn app.main:app --reload
```

前端（Next.js，默认 `http://localhost:3000`）：

```bash
cd web
npm install
npm run dev
```

可选前端环境变量（放到 `web/.env.local` 或启动前导出）：

- `NEXT_PUBLIC_API_BASE_URL`（默认: `http://localhost:8000`）
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## API

### `POST /api/v1/summarize`

Request body:

```json
{
  "url": "https://www.xiaoyuzhoufm.com/episode/xxxxx",
  "language": "zh",
  "summary_style": "bullet",
  "max_words": 200,
  "include_transcript": false
}
```

Response body:

```json
{
  "source_url": "https://www.xiaoyuzhoufm.com/episode/xxxxx",
  "audio_url": "https://...mp3",
  "summary": "- ...",
  "transcript": null
}
```
