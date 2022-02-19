dev:
	flask run

prod:
	gunicorn app:app -w 3