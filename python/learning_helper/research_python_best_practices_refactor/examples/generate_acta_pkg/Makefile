# Convenience targets for the refactored generate_acta_pkg.
#
# IMPORTANT: every target `cd`s up to the project root (the directory that
# CONTAINS generate_acta_pkg/) before invoking python, because
# `python -m generate_acta_pkg` only finds the package when its parent
# directory is on sys.path. That's a quirk of how `python -m <package>`
# resolves sys.path.

PYTHON ?= python3
PKG    := generate_acta_pkg
HERE   := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ROOT   := $(abspath $(HERE)/..)

.PHONY: help
help:  ## Show this help.
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} \
	     /^[a-zA-Z_-]+:.*##/ \
	       { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' \
	    $(MAKEFILE_LIST)

.PHONY: install
install:  ## Install the package in editable mode.
	cd $(ROOT) && $(PYTHON) -m pip install -e .

.PHONY: simulate
simulate:  ## Run the full pipeline in --simulate mode (no Google calls).
	cd $(ROOT) && $(PYTHON) -m $(PKG) generate \
	  --title "ACTA No. TEST-DRYRUN" \
	  --field ACTA_NO=01-01-2026 \
	  --field TIPO_REUNION=Ordinaria \
	  --field FECHA_INICIO="01/01/2026 09:00:00" \
	  --field FECHA_FIN="01/01/2026 11:00:00" \
	  --field HORA_CIERRE="11:00 A.M." \
	  --field PRESIDENTE="GLADYS AMADO T." \
	  --field SECRETARIO="JEFFERSON S. SOTO M." \
	  --field ORDEN_DIA="1. Tema A\n2. Tema B" \
	  --field ORDEN_DIA_DESCRIPTIVO="1. Tema A — descripción.\n2. Tema B — descripción." \
	  --simulate

.PHONY: fields
fields:  ## Print the fields.json schema.
	cd $(ROOT) && $(PYTHON) -m $(PKG) fields

.PHONY: inject-simulate
inject-simulate:  ## Simulate the inject-tags step (no Google calls).
	cd $(ROOT) && ACTA_BASE_DOC_ID=fake-id-12345 $(PYTHON) -m $(PKG) inject-tags --simulate

.PHONY: comments-simulate
comments-simulate:  ## Simulate the inject-comments step (no Google calls).
	cd $(ROOT) && ACTA_BASE_DOC_ID=fake-id-12345 $(PYTHON) -m $(PKG) inject-comments --simulate --yes

.PHONY: lint
lint:  ## Run ruff against the package (if installed).
	cd $(ROOT) && $(PYTHON) -m ruff check $(PKG)

.PHONY: clean
clean:  ## Remove __pycache__ directories and any generated outputs.
	find $(PKG) -type d -name __pycache__ -exec rm -rf {} +
	rm -rf $(PKG)/baseActaReunion/outputs

.PHONY: test
test:  ## Run the test suite (placeholder — no tests yet).
	@echo "No tests yet. See Next Steps in the parent README.md."