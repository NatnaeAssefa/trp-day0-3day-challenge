# Skill: Download YouTube

Downloads video or audio from a YouTube URL for downstream processing (e.g. transcription, clipping). Used by Workers when a task requires fetching external video/audio.

## Input Contract

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `video_url` | str | Yes | Full YouTube URL (e.g. `https://www.youtube.com/watch?v=...`). |
| `format` | str | No | Requested format: `video` (default) or `audio`. When `audio`, the skill returns an audio-only asset (e.g. extracted or audio stream). |

**Example call:**

```python
download_youtube(video_url="https://www.youtube.com/watch?v=abc123", format="audio")
```

## Output Contract

Returns an object with at least:

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | True if download completed. |
| `local_path` | str \| None | Path to the downloaded file on the runtime filesystem, or None if not stored locally. |
| `blob_ref` | str \| None | Optional reference (e.g. storage URI) if the asset is stored in blob storage instead of local path. |
| `error` | str \| None | If success is False, a short error message. |

**Example (success):**

```json
{
  "success": true,
  "local_path": "/tmp/chimera/audio_abc123.m4a",
  "blob_ref": null,
  "error": null
}
```

Tests in `tests/test_skills_interface.py` assert that the skill module accepts `video_url` and optional `format` and returns an object with these fields.

## Implementation Status

Stub/structure only. Implementation may use yt-dlp or an MCP tool that wraps a download service.
