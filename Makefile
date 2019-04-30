# Package details
CONTAINER_NAME = pycast
TAG_VERSION    = latest
PACKAGE_NAME   = pycast

# Directory structure
BUILD_DIR      = _build
DOC_DIR        = $(BUILD_DIR)/doc
DIST_DIR       = $(BUILD_DIR)/dist
PY_BUILD_DIR   = $(BUILD_DIR)/py_build

# Sphinx configuration
SPHINXOPTS     =
SPHINXBUILD    = sphinx-build -E
SPHINXAPIDOC   = sphinx-apidoc -fMP
ALLSPHINXOPTS   = -d $(DOC_DIR)/doctrees $(SPHINXOPTS) .

clean:
	rm -rf $(DIST_DIR)/*
	rm -rf $(DOC_DIR)/*
	rm -rf $(PY_BUILD_DIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

dist:
	python setup.py bdist_wheel --dist-dir=$(DIST_DIR) --bdist-dir=$(PY_BUILD_DIR)
	mv build $(PY_BUILD_DIR)
	mv $(PACKAGE_NAME).egg-info $(PY_BUILD_DIR)

install:
	python setup.py install

test:
	pytest

docker-build:
	docker build -t $(CONTAINER_NAME):$(TAG_VERSION) .

docker-run: docker-build
	docker run \
	    -it $(CONTAINER_NAME):$(TAG_VERSION)                                                        \
	    bash

dev: docker-build
	docker run \
	    -v $(CURDIR)/$(PACKAGE_NAME):/$(PACKAGE_NAME)/$(PACKAGE_NAME)   \
	    -v $(CURDIR)/tests:/$(PACKAGE_NAME)/tests                       \
	    -v $(CURDIR)/doc:/$(PACKAGE_NAME)/doc                           \
	    -v $(CURDIR)/conf.py:/$(PACKAGE_NAME)/conf.py                   \
	    -v $(CURDIR)/Makefile:/$(PACKAGE_NAME)/Makefile                 \
	    -v $(CURDIR)/readme.rst:/$(PACKAGE_NAME)/readme.rst             \
	    -v $(CURDIR)/requirements.txt:/$(PACKAGE_NAME)/requirements.txt \
	    -v $(CURDIR)/setup.py:/$(PACKAGE_NAME)/setup.py                 \
	    -it $(CONTAINER_NAME):$(TAG_VERSION)                            \
	    bash

#release: test
#	# only build a release, if all tests were sucessfull
#	if [ $$? -eq 0 ] ; then                        \
#		python setup.py bdist_egg upload          ;\
#	else                                           \
#		@echo "tests not successfull. exiting"    ;\
#		exit 70                                   ;\
#	fi
##	python setup.py sdist bdist bdist_egg upload  ;\
##	python setup.py build_sphinx                  ;\
##	python setup.py upload_sphinx                 ;\
#
#cbindings:
#	@echo "\nGenerating Python Bindings"
#	python bin/helper/generate-bindings.py > pycastC.c
#
#	@echo "\nBuilding C++ library"
#	g++ -Wall -fPIC -I/usr/include/python2.7 -c -o pycast.o pycast/main.cpp
#	g++ -Wall -shared -o libpycast.so -lpython pycast.o
#
#	@echo "\nBuilding Python bindings"
#	g++ -Wall -fPIC -I/usr/include/python2.7 -c -o pycastC.o pycastC.c
#	g++ -Wall -shared -I/usr/include/python2.7 -o pycastC.so -L. -lpycast -lpython pycastC.o
