"""
Transcribe audio skill — stub. Contract: skills/skill_transcribe_audio/README.md.
Implement to return dict with success, transcript, error.
"""


def transcribe_audio(
    audio_url: str | None = None,
    audio_path: str | None = None,
    language_hint: str | None = None,
) -> dict:
    """Stub: returns wrong shape so tests fail until implementation fulfils contract."""
    # Deliberately wrong structure so test_skills_interface.py fails (TDD "empty slot").
    return {"result": "not_implemented"}
