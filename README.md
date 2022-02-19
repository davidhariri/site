## Local
```
pyenv virtualenv 3.9.10 test-site
pyenv activate test-site
pip install -r requirements.txt
flask run
```

## Docker
```
docker build --tag test-site .
docker run -p 8000:8000 test-site
```