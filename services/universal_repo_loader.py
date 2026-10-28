
import requests

from services.github_analyzer import (
    fetch_repository,
    parse_github_url,
)
from services.github_zip_loader import fetch_repository_zip


def fetch_any_repository(url):
    parse_github_url(url)

    try:
        return fetch_repository(url)

    except requests.exceptions.HTTPError as error:
        response = error.response

        # Do not use "if response" here.
        # requests.Response is falsy for 4xx/5xx.
        status = (
            response.status_code
            if response is not None
            else None
        )

        if status in (403, 429):
            print(
                "GitHub API unavailable. "
                "Trying ZIP fallback..."
            )
            return fetch_repository_zip(url)

        raise
