# simple install/uninstall instrunctions for *nix based systems

SRC = glob2bib.py
EXE = glob2bib
DIR = /usr/local/bin

install:
	cp $(SRC) $(DIR)/$(EXE)
	chmod +x $(DIR)/$(EXE)

avatar:
	latexmk -pdf logo.tex
	latexmk -c
	convert -quality 100 -density 600 -flatten logo.pdf logo.png

uninstall:
	rm $(DIR)/$(EXE)
