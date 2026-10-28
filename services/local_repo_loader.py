
from pathlib import Path

from services.github_analyzer import (
    is_allowed_file,
    MAX_FILES,
    MAX_FILE_BYTES,
    MAX_TOTAL_CHARS,
)


PRIORITY_FILES = {
    "app.py": 0,
    "graph/workflow.py": 1,
    "agents/router.py": 2,
    "llm/groq_client.py": 3,
    "config.py": 4,
    "README.md": 5,
}


def fetch_local_repository(folder="."):
    root = Path(folder).resolve()

    if not root.is_dir():
        raise ValueError("Repository folder not found.")

    candidates = []

    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue

        relative = path.relative_to(root).as_posix()

        if not is_allowed_file(relative):
            continue

        if path.stat().st_size > MAX_FILE_BYTES:
            continue

        candidates.append((relative, path))

    candidates.sort(
        key=lambda item: (
            PRIORITY_FILES.get(item[0], 100),
            item[0].count("/"),
            item[0].lower(),
        )
    )

    files = []
    total_chars = 0

    for relative, path in candidates[:MAX_FILES]:
        remaining = MAX_TOTAL_CHARS - total_chars

        if remaining <= 0:
            break

        content = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        content = content[:min(remaining, 4000)]

        files.append({
            "path": relative,
            "content": content,
        })

        total_chars += len(content)

    return {
        "name": root.name,
        "description": "Local repository analysis",
        "language": "Python",
        "stars": 0,
        "files": files,
        "total_candidates": len(candidates),
    }
