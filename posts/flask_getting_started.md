---
title: Getting Started with Flask in 2023
date: 2023-07-30 20:06:44+00
tags:
- code
description: All you need to get started using Flask for your next web application project.
---
There are probably hundreds of blog posts about how to get started using [Flask](https://flask.palletsprojects.com/en/2.3.x/), but Flask and the python ecosystem has improved a lot in recent years. So here's a quick guide to getting started with Flask in 2023.

## Set Up

First, let's create a new directory for our project.

```bash
mkdir flask-getting-started && cd flask-getting-started
```

Next, let's use [pyenv](https://github.com/pyenv/pyenv#unixmacos) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installing-with-homebrew-for-macos-users) to create a new virtual environment for our project. Virtual environments are a way to isolate your project's dependencies from other projects on your system. This is especially useful if you're working on multiple projects that use different versions of the same library or Python itself.

```bash
pyenv virtualenv 3.11.0 flask-getting-started
pyenv activate flask-getting-started
```

Finally, let's install Flask and save it to our requirements.txt file.

```bash
pip install flask
pip freeze > requirements.txt
```

Great, we just created a new project and installed Flask. Now, let's create a new file called app.py and start writing some code.

## Defining our Application

Now, let's create a new file called app.py and start writing some code in our favorite text editor (I like [VSCode](https://code.visualstudio.com)). Add the following code and save it:

```python
from flask import Flask

app = Flask(__name__) # __name__ is a special variable that gets the name of the module. This is needed so that Flask knows where to look for templates and static files.

@app.route("/") # This is a decorator. It tells Flask's router what path ('/') should trigger the function (home()) that follows.
def home():
    return "Hello, World!"
```

## Run It!

Now, let's run the app and see what happens.

```bash
flask run
```

You should see the following:

```bash
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

If you navigate to http://localhost:5000/ in your browser, you should see:

```
Hello, World!
```

That's it! You've created your first Flask app. From here you could add more routes, create templates and deploy it to a production server.
