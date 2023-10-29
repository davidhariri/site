## Develop

```
pyenv virtualenv 3.11.0 site
pyenv activate site
poetry install --sync
make run
```

## Deploy

```
fly deploy
```
