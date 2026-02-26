# Podcast-to-Insight (Backend)

FastAPI backend that turns a Xiaoyuzhou episode page (or direct audio URL) into an AI text summary.

## Requirements

- Python 3.10+
- OpenAI API key for transcription + summarization

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_key"
```

Optional environment variables:

- `OPENAI_BASE_URL` (default: `https://api.openai.com/v1`)
- `OPENAI_AUDIO_MODEL` (default: `whisper-1`)
- `OPENAI_SUMMARY_MODEL` (default: `gpt-4o-mini`)
- `MAX_AUDIO_BYTES` (default: `209715200`)
- `SUMMARY_CHUNK_CHARS` (default: `6000`)
- `SUMMARY_CHUNK_OVERLAP` (default: `300`)
- `SUMMARY_LANGUAGE` (default: `zh`)
- `SUMMARY_STYLE` (default: `bullet`)
- `SUMMARY_MAX_WORDS` (default: `200`)

## Run

```bash
uvicorn app.main:app --reload
```

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
