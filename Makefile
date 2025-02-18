site:
	uv run make_site.py

clean:
	rm -rf public

run:
	python -m http.server --directory=public 8000