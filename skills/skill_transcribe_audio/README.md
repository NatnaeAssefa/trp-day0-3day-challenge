# Skill: Transcribe Audio

Converts audio (from URL or local path) into text transcript. Used by Workers for content that originates from video/audio (e.g. after skill_download_youtube).

## Input Contract

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio_url` | str | No* | URL of the audio file. *One of `audio_url` or `audio_path` must be provided. |
| `audio_path` | str | No* | Local filesystem path to the audio file. *One of `audio_url` or `audio_path` must be provided. |
| `language_hint` | str | No | Optional language code (e.g. `en`, `am`) for better accuracy. |

**Example calls:**

```python
transcribe_audio(audio_url="https://example.com/clip.mp3")
transcribe_audio(audio_path="/tmp/chimera/audio_abc123.m4a", language_hint="en")
```

## Output Contract

Returns an object with at least:

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | True if transcription completed. |
| `transcript` | str | The full transcript text. Empty string if success is False. |
| `error` | str \| None | If success is False, a short error message. |

**Example (success):**

```json
{
  "success": true,
  "transcript": "Hello, this is the transcribed text...",
  "error": null
}
```

Tests in `tests/test_skills_interface.py` assert that the skill module accepts `audio_url` and/or `audio_path` and optional `language_hint`, and returns an object with `success`, `transcript`, and `error`.

## Implementation Status

Stub/structure only. Implementation may use an MCP tool or external ASR API (e.g. Whisper, platform-specific).
