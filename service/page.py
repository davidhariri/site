from dataclasses import dataclass
from io import TextIOWrapper
import markdown # type: ignore


@dataclass
class Page:
    path: str
    title: str
    html_content: str

    @classmethod
    def from_file(cls, file_name: str, file: TextIOWrapper) -> "Page":
        file_name = file_name.split(".")[0]
        title = file_name.replace("-", " ")
        html_content = markdown.markdown(file.read())
        return cls(file_name.lower(), title, html_content)
