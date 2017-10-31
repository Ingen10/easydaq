# build python files from ui files

PROJECT=easydaq
VERSION=$(shell python setup.py --version)
UI_FILES=$(wildcard ./easydaq/*.ui)
PY_FILES=$(UI_FILES:%.ui=%.py)

all: $(PY_FILES)

version:
	@echo $(VERSION)

executable: $(PY_FILES)
	pyinstaller /$(PROJECT)/main.py --onefile

%.py: %.ui
	pyuic5 -x $< -o $@

sdist: dist/$(PROJECT)-$(VERSION).tar.gz

dist/$(PROJECT)-$(VERSION).tar.gz: setup.py $(PY_FILES)
	python setup.py sdist

clean:
	rm -f dist/$(PROJECT)-$(VERSION).tar.gz
	rm -f $(PY_FILES)
