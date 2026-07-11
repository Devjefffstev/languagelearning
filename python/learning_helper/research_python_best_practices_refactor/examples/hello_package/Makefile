# Convenience targets for the hello_package demo.
#
# IMPORTANT: every target `cd`s up one directory before invoking python,
# because `python -m hello_package` only finds the package when the cwd
# is the directory that CONTAINS hello_package/, not hello_package/ itself.
# That's a quirk of how `python -m <package>` resolves sys.path.

PYTHON ?= python3
PKG    := hello_package
# $(CURDIR) is where make was invoked; $(dir ...) is the directory of this
# Makefile. Using both lets the targets work no matter where you are.
HERE := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ROOT := $(abspath $(HERE)/..)

.PHONY: help
help:  ## Show this help message.
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} \
	     /^[a-zA-Z_-]+:.*##/ \
	       { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' \
	    $(MAKEFILE_LIST)

.PHONY: run
run:  ## Run the package with a default name (World).
	cd $(ROOT) && $(PYTHON) -m $(PKG)

.PHONY: greet
greet:  ## Run the package with a custom name: make greet NAME=Jefferson
	cd $(ROOT) && $(PYTHON) -m $(PKG) $(NAME)

.PHONY: install
install:  ## Install the package in editable mode (`pip install -e .`).
	cd $(ROOT) && $(PYTHON) -m pip install -e hello_package

.PHONY: uninstall
uninstall:  ## Uninstall the package.
	$(PYTHON) -m pip uninstall -y hello-package

.PHONY: clean
clean:  ## Remove __pycache__ directories.
	find . -type d -name __pycache__ -exec rm -rf {} +