site:
	uv run make_site.py --with-drafts

clean:
	rm -rf public

run:
	python -m http.server --directory=public 8000

watch:
	uv run -m watchfiles "make site" posts pages templates static drafts