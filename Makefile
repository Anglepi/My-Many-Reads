start:
	POETRY_DOTENV_LOCATION="$(shell pwd)/prod.env" poetry run uvicorn api:mmr --reload

spellcheck:
	./scripts/spellcheck.sh

test:
	POETRY_DOTENV_LOCATION="$(shell pwd)/test.env" poetry run pytest
	POETRY_DOTENV_LOCATION="$(shell pwd)/test.env" poetry run python scripts/clean_test_db.py


test-nodb:
	TEST="test" poetry run pytest

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report -m

doc:
	cd docs/tex/; \
	pdflatex proyecto.tex; \
	bibtex proyecto; \
	pdflatex proyecto.tex;
	mv docs/tex/proyecto.pdf .

docs: doc

cleandoc:
	rm proyecto.pdf docs/tex/*.log docs/tex/*.aux docs/tex/*.bbl docs/tex/*.blg docs/tex/*.lof docs/tex/*.lot docs/tex/*.out docs/tex/*.toc

clean: cleandoc
