from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SessionStats:
    session_id: str
    model: str = "unknown"
    input_tokens: int = 0
    output_tokens: int = 0
    cache_created: int = 0
    cache_read: int = 0
    api_calls: int = 0
    project_name: str = ""

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.cache_created


@dataclass
class ProjectSummary:
    path: str
    sessions: list[SessionStats] = field(default_factory=list)

    @property
    def total_input(self) -> int:
        return sum(s.input_tokens for s in self.sessions)

    @property
    def total_output(self) -> int:
        return sum(s.output_tokens for s in self.sessions)

    @property
    def total_cache_read(self) -> int:
        return sum(s.cache_read for s in self.sessions)

    @property
    def total_api_calls(self) -> int:
        return sum(s.api_calls for s in self.sessions)


def scan_claude_dir(claude_dir: Path) -> list[ProjectSummary]:
    """Scan ~/.claude/projects/ for session logs and extract token usage."""
    projects_dir = claude_dir / "projects"
    if not projects_dir.exists():
        return []

    results: list[ProjectSummary] = []

    for project_dir in sorted(projects_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        summary = ProjectSummary(path=project_dir.name)
        for log_file in sorted(project_dir.glob("*.jsonl")):
            stats = _parse_session_log(log_file)
            if stats and stats.api_calls > 0:
                stats.project_name = project_dir.name
                summary.sessions.append(stats)
        if summary.sessions:
            results.append(summary)

    return results


def _parse_session_log(path: Path) -> SessionStats | None:
    session_id = path.stem
    stats = SessionStats(session_id=session_id)

    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg = entry.get("message", {})
                if msg.get("role") == "assistant":
                    stats.model = msg.get("model", stats.model)
                    usage = msg.get("usage")
                    if usage:
                        stats.input_tokens += usage.get("input_tokens", 0)
                        stats.output_tokens += usage.get("output_tokens", 0)
                        stats.cache_created += usage.get("cache_creation_input_tokens", 0)
                        stats.cache_read += usage.get("cache_read_input_tokens", 0)
                        stats.api_calls += 1
    except OSError:
        return None

    return stats
