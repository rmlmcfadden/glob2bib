# simple install/uninstall instrunctions for *nix based systems

SRC = glob2bib.py
EXE = glob2bib
DIR = /usr/local/bin

install:
	cp $(SRC) $(DIR)/$(EXE)
	chmod +x $(DIR)/$(EXE)

uninstall:
	rm $(DIR)/$(EXE)
