from src.chunking import chunk_text
from src.guardrails import screen_prompt


def test_chunks_cover_text_with_overlap() -> None:
    text = "a" * 1000
    chunks = chunk_text(text, size=400, overlap=50)
    assert len(chunks) == 3
    assert chunks[0][-50:] == chunks[1][:50]


def test_empty_text() -> None:
    assert chunk_text("   ") == []


def test_ssn_is_blocked() -> None:
    result = screen_prompt("customer ssn is 123-45-6789")
    assert result["allowed"] is False
    assert "ssn" in result["blocked_types"]


def test_clean_prompt_is_allowed() -> None:
    result = screen_prompt("What is the capital ratio trend for failed banks?")
    assert result == {"allowed": True, "blocked_types": []}
