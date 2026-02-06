"""
Asserts that skill modules accept the correct parameters and return the contract shape
defined in skills/*/README.md. Tests MUST fail until skills fulfil their contracts (TDD empty slot).
"""
import pytest


def test_download_youtube_accepts_parameters_and_returns_contract():
    """skill_download_youtube must accept video_url, optional format; return success, local_path/blob_ref, error."""
    from skills.skill_download_youtube import download_youtube

    result = download_youtube(video_url="https://www.youtube.com/watch?v=test", format="audio")
    assert isinstance(result, dict)
    assert "success" in result, "Contract: output must have 'success'"
    assert "error" in result, "Contract: output must have 'error'"
    assert "local_path" in result or "blob_ref" in result, "Contract: must have local_path or blob_ref"


def test_transcribe_audio_accepts_parameters_and_returns_contract():
    """skill_transcribe_audio must accept audio_url or audio_path, optional language_hint; return success, transcript, error."""
    from skills.skill_transcribe_audio import transcribe_audio

    result = transcribe_audio(audio_url="https://example.com/audio.mp3", language_hint="en")
    assert isinstance(result, dict)
    assert "success" in result, "Contract: output must have 'success'"
    assert "transcript" in result, "Contract: output must have 'transcript'"
    assert "error" in result, "Contract: output must have 'error'"
