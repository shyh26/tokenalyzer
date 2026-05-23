import json
import tempfile
from pathlib import Path

from tokenalyzer.core import _parse_session_log, SessionStats


def test_parse_session_log_with_usage():
    log_content = json.dumps({
        "message": {
            "role": "assistant",
            "model": "claude-sonnet-4-6",
            "usage": {
                "input_tokens": 1000,
                "output_tokens": 200,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 500,
                "server_tool_use": {"web_search_requests": 0, "web_fetch_requests": 0}
            }
        }
    })

    path = Path("_test_log.jsonl")
    path.write_text(log_content)
    try:
        stats = _parse_session_log(path)
        assert stats is not None
        assert stats.input_tokens == 1000
        assert stats.output_tokens == 200
        assert stats.cache_read == 500
        assert stats.api_calls == 1
        assert stats.model == "claude-sonnet-4-6"
    finally:
        path.unlink()


def test_parse_session_log_multiple_calls():
    lines = [
        json.dumps({"message": {"role": "assistant", "model": "claude-4", "usage": {"input_tokens": 100, "output_tokens": 50, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}}}),
        json.dumps({"message": {"role": "assistant", "model": "claude-4", "usage": {"input_tokens": 200, "output_tokens": 75, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}}}),
    ]

    path = Path("_test_log.jsonl")
    path.write_text("\n".join(lines))
    try:
        stats = _parse_session_log(path)
        assert stats is not None
        assert stats.api_calls == 2
        assert stats.input_tokens == 300
        assert stats.output_tokens == 125
    finally:
        path.unlink()


def test_parse_session_log_empty_file():
    path = Path("_empty.jsonl")
    path.write_text("")
    try:
        stats = _parse_session_log(path)
        assert stats is not None
        assert stats.api_calls == 0
    finally:
        path.unlink()
