start:
	poetry run uvicorn main:mmr --reload

spellcheck:
	./scripts/spellcheck.sh

test:
	poetry run pytest

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report -m

doc:
	cd docs/tex/; \
	pdflatex proyecto.tex; \
	bibtex proyecto; \
	pdflatex proyecto.tex;
	mv docs/tex/proyecto.pdf .

cleandoc:
	rm proyecto.pdf docs/tex/*.log docs/tex/*.aux docs/tex/*.bbl docs/tex/*.blg docs/tex/*.lof docs/tex/*.lot docs/tex/*.out docs/tex/*.toc

clean: cleandoc
