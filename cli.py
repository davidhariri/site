import click
import requests
from config import settings

@click.command()
@click.option("--title", prompt="Enter the title of the new post", help="Title of the new post")
@click.option("--content", prompt="Enter the content of the new post", help="Content of the new post")
def create_new_post(title, content):
    url = f"{settings.FQD}/micropub"
    headers = {
        "Authorization": f"Bearer {settings.MICROPUB_SECRET}",
        "Content-Type": "application/json"
    }
    data = {
        "type": ["h-entry"],
        "properties": {
            "name": [title],
            "content": [content]
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        click.echo(f"New post created at {response.json().get('url')}")
    else:
        click.echo(f"Failed to create post: {response.status_code} {response.text}")

if __name__ == "__main__":
    create_new_post()
