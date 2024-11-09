import click
import requests
from config import settings

POST_CONTENT = """
# Coding with LLMs on the Weekend: A Family Affair

Most people spend their weekends unwinding, but for me, it's about firing up the laptop and diving into some late-night coding with LLMs—with my family in the mix, of course. Coding has always been a deeply rewarding escape, and these days, even my weekends are a little more interesting thanks to the creative potential of language models.

My wife might not dive into the syntax like I do, but she's got this knack for brainstorming wild prompt ideas—things I'd never consider alone. And then there's my baby, who obviously isn't coding just yet, but her background babbling adds a certain charm to the vibe, making my work sessions feel somehow playful and profound at the same time. It reminds me of why I got into programming: to build things that add meaning, even if it's just in small doses.

From building quick prototypes to testing new ideas for Ada, LLMs have become my digital playground for exploring concepts that don’t always make it to Monday morning. Watching these ideas unfold in real-time while being surrounded by the people I love brings a different kind of satisfaction. Coding on weekends has become a little tradition for us—one that's not just about algorithms, but about creating and exploring together. \n\nIn the end, it's a reminder that no matter the project, coding is best when it's shared.
"""

@click.command()
@click.option("--title", prompt="Enter the title of the new post", help="Title of the new post")
def create_new_post(title):
    url = f"{settings.FQD}/micropub"
    headers = {
        "Authorization": f"Bearer {settings.MICROPUB_SECRET}",
        "Content-Type": "application/json"
    }
    data = {
        "type": ["h-entry"],
        "properties": {
            "name": [title],
            "content": [POST_CONTENT]
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        click.echo(f"New post created at {response.json().get('url')}")
    else:
        click.echo(f"Failed to create post: {response.status_code} {response.text}")

if __name__ == "__main__":
    create_new_post()
