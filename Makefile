install:
	poetry install

start:
	POETRY_DOTENV_LOCATION="$(shell pwd)/prod.env" poetry run uvicorn api:mmr --reload

spellcheck:
	./scripts/spellcheck.sh

test: clean-test
	POETRY_DOTENV_LOCATION="$(shell pwd)/test.env" poetry run pytest
	
clean-test:
	POETRY_DOTENV_LOCATION="$(shell pwd)/test.env" poetry run python scripts/clean_test_db.py	

import-data:
	POETRY_DOTENV_LOCATION="$(shell pwd)/test.env" poetry run python scripts/import_data.py	

test-nodb:
	TEST="test" poetry run pytest

coverage: clean-test
	POETRY_DOTENV_LOCATION="$(shell pwd)/test.env" poetry run coverage run -m pytest
	poetry run coverage report -m

doc:
	cd docs/tex/; \
	pdflatex proyecto.tex; \
	bibtex proyecto; \
	pdflatex proyecto.tex; \
	pdflatex proyecto.tex;
	mv docs/tex/proyecto.pdf .

docs: doc

cleandoc:
	rm proyecto.pdf docs/tex/*.log docs/tex/*.aux docs/tex/*.bbl docs/tex/*.blg docs/tex/*.lof docs/tex/*.lot docs/tex/*.out docs/tex/*.toc

clean: cleandoc
