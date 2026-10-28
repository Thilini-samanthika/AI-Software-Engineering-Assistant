
import io
import zipfile
import requests

from services.github_analyzer import (
    parse_github_url,
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
    "requirements.txt": 5,
    "README.md": 6,
}


def fetch_repository_zip(url):
    owner, repo = parse_github_url(url)

    archive_url = (
        f"https://github.com/{owner}/{repo}/archive/HEAD.zip"
    )

    response = requests.get(
        archive_url,
        timeout=60,
    )
    response.raise_for_status()

    # Limit compressed archive size.
    if len(response.content) > 20 * 1024 * 1024:
        raise ValueError("Repository ZIP is too large.")

    with zipfile.ZipFile(
        io.BytesIO(response.content)
    ) as archive:

        candidates = []

        for info in archive.infolist():
            if info.is_dir():
                continue

            parts = info.filename.split("/", 1)

            if len(parts) != 2:
                continue

            relative_path = parts[1]

            if not is_allowed_file(relative_path):
                continue

            if info.file_size > MAX_FILE_BYTES:
                continue

            candidates.append(
                (relative_path, info)
            )

        candidates.sort(
            key=lambda item: (
                PRIORITY_FILES.get(item[0], 100),
                item[0].count("/"),
                item[0].lower(),
            )
        )

        files = []
        total_chars = 0

        for path, info in candidates[:MAX_FILES]:
            remaining = MAX_TOTAL_CHARS - total_chars

            if remaining <= 0:
                break

            content = archive.read(info).decode(
                "utf-8",
                errors="replace",
            )

            content = content[:min(remaining, 4000)]

            files.append({
                "path": path,
                "content": content,
            })

            total_chars += len(content)

    return {
        "name": f"{owner}/{repo}",
        "description": "",
        "language": "Unknown",
        "stars": 0,
        "files": files,
        "total_candidates": len(candidates),
    }
