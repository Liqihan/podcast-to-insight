# Podcast-to-Insight (Backend)

FastAPI backend that turns a Xiaoyuzhou episode page (or direct audio URL) into an AI text summary.

## Requirements

- Python 3.10+
- 百炼(Bailian) API key for both transcription and summarization
- 阿里云语音识别服务API key for ASR functionality

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export BAILIAN_API_KEY="your_bailian_key"
export BAILIAN_ASR_API_KEY="your_bailian_asr_key"
```

Optional environment variables:

- `BAILIAN_BASE_URL` (default: `https://bailian.aliyuncs.com/v1`)
- `BAILIAN_CHAT_MODEL` (default: `qwen-plus`)
- `BAILIAN_ASR_BASE_URL` (default: `https://nls-gateway-cn-shanghai.aliyuncs.com`)
- `BAILIAN_ASR_MODEL` (default: `paraformer-realtime-v2`)
- `BAILIAN_POLL_INTERVAL_S` (default: `2.0`)
- `BAILIAN_POLL_TIMEOUT_S` (default: `900.0`)
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
