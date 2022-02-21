from datetime import datetime

from flask import Flask, render_template
import markdown

app = Flask(__name__)

@app.context_processor
def inject_now():
    return { "now": datetime.utcnow() }

@app.route("/")
def render_home():
    return render_template("home.html")

@app.route("/<page_name>/")
def render_page(page_name):
    try:
        with open(f"pages/{page_name}.md", "r") as page:
            page_html = markdown.markdown(page.read())
    except FileNotFoundError:
        return render_template("404.html")

    return render_template(
        "page.html",
        content=page_html,
        title=page_name
    )