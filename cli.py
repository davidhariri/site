import datetime
import os
import click
from werkzeug.utils import secure_filename

POST_TEMPLATE = """---
title: {title}
date: {date}
tags:
    - 
description: 
---

"""

@click.command()
@click.option("--title", prompt="Enter the title of the new post", help="Title of the new post")
def create_new_post(title):
    date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).isoformat()
    filename = secure_filename(title).replace("_", "-").lower() + ".md"
    filepath = os.path.join("posts", filename)

    if os.path.exists(filepath):
        click.echo("A post with the same title already exists. Please choose a different title.")
        return

    with open(filepath, "w") as file:
        file.write(POST_TEMPLATE.format(title=title, date=date))

    click.echo(f"New post created at {filepath}")

if __name__ == "__main__":
    create_new_post()
