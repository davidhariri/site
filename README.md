## Develop

```
pyenv virtualenv 3.11.0 site
pyenv activate site
pip install -r requirements.txt
pip install -r requirements-dev.txt
make run
```

## Deploy

```
fly deploy
```
