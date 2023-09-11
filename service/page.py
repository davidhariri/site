import os
from dataclasses import dataclass
from io import TextIOWrapper
import markdown # type: ignore

PAGE_DIR = "pages"


@dataclass
class Page:
    path: str
    title: str
    html_content: str

    @classmethod
    def from_file(cls, file_name: str, file: TextIOWrapper) -> "Page":
        file_name = file_name.split(".")[0]
        title = file_name.replace("-", " ")
        html_content = markdown.markdown(file.read(), extensions=[
            "fenced_code",
            "codehilite",
            "toc",
        ])
        return cls(file_name.lower(), title, html_content)


def get_all_page_paths_and_pages() -> dict[str, Page]:
    """
    Get all the page paths and Page objects from the /pages directory

    e.g. "about" -> Page(...)
    """
    page_content = {}

    for file_name in os.listdir(PAGE_DIR):
        with open(f"{PAGE_DIR}/{file_name}", "r") as post_file:
            content = Page.from_file(file_name, post_file)

            if content is not None:
                page_content[content.path] = content

    return page_content

def get_all_pages_sorted() -> list[Page]:
    """
    Get all the Page objects from the /pages directory
    """
    return sorted(list(get_all_page_paths_and_pages().values()), key=lambda page: page.title)
