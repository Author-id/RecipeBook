from pathlib import Path
from typing import Any
import uuid

from django.utils.deconstruct import deconstructible
from markdown import Markdown
from pymdownx import emoji


class Thumbnail:
    url: str


MD = Markdown(
    extensions=[
        "markdown.extensions.tables",
        "pymdownx.magiclink",
        "pymdownx.betterem",
        "pymdownx.tilde",
        "pymdownx.emoji",
        "pymdownx.tasklist",
        "pymdownx.superfences",
        "pymdownx.saneheaders",
    ],
    extension_configs={
        "pymdownx.magiclink": {
            "repo_url_shortener": True,
            "repo_url_shorthand": True,
        },
        "pymdownx.tilde": {"subscript": False},
        "pymdownx.emoji": {
            "emoji_index": emoji.twemoji,
            "emoji_generator": emoji.to_png,
            "alt": "short",
            "options": {
                "attributes": {
                    "align": "absmiddle",
                    "height": "20px",
                    "width": "20px",
                },
            },
        },
    },
)


def render_markdown(text: str) -> str:
    return MD.convert(text)


def make_admin_fieldsets(
    fields: list[str],
) -> list[tuple[None, dict[str, list[str]]]]:
    return [(None, {"fields": fields})]


@deconstructible
class RandomFileName(object):
    def __init__(self, path: str):
        self.path = Path(path)

    def __call__(self, instance: Any, filename: str):
        path = Path(filename)
        random_path = path.with_name(str(uuid.uuid4()))
        random_path = random_path.with_suffix(path.suffix)
        return self.path / random_path


__all__ = []
