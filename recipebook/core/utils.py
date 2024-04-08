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


def make_admin_fieldsets(fields: list[str]) -> list[tuple[None, dict[str, list[str]]]]:
    return [(None, {"fields": fields})]


__all__ = []
