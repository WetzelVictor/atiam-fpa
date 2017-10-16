# Compile latex and makes bibliography
pdflatex main.tex
bibtex main
pdflatex main.tex
START-PROCESS main.pdf
