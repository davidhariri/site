from dataclasses import dataclass
from datetime import datetime
from io import TextIOWrapper
import markdown # type: ignore


@dataclass
class BlogPost:
    path: str
    title: str
    date: datetime
    html_content: str

    @classmethod
    def from_file(cls, file_name: str, file: TextIOWrapper) -> "BlogPost":
        file_name = file_name.split(".")[0]
        title = file_name.split("_")[1].replace("-", " ")
        date = datetime.strptime(file_name.split("_")[0], "%Y-%m-%d")
        html_content = markdown.markdown(file.read())
        return cls(file_name.lower(), title, date, html_content)
