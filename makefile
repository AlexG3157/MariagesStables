test:
	python -m unittest -v GaleShapley_test.py
rapport:
	pdflatex rapport
clean:
	rm *.aux *.out *.log *.fls *.fdb_latexmk *.synctex.gz