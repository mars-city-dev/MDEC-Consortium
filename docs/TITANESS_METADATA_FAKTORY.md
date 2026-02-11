# TITANESS METADATA FAKTORY (Faktory Edition)  — v2.5

**TITANESS METADATA FAKTORY** — Powered by Titaness Sentient Systems OS — *Jennifer*

Project: Data Legacy Vault (DLV)
Consortium: Meta Data Excellence Consortium (MdEC)
Version: 2.5 (Faktory Edition)

This engine is the authoritative toolchain for generating MdEC Gold-Certified Engrams within the Titaness Metadata Faktory ecosystem. It provides a deterministic pipeline to ingest an asset and produce a certified engram sidecar (`*.engram.json`) that records integrity, provenance, and quality scoring according to MdEC standards.

---

## Overview
- Name: Titaness Metadata Faktory
- Owner: Titaness Sentient Systems mars-city-dev COlds The Architect
- Purpose: Ingest, verify, score, and emit certified engrams for archival
- Primary outputs: `<asset>.engram.json` (engram v2.1)

## Capabilities
- SHA256 integrity hashing for every asset
- MdEC quality scoring and certification (Gold/Silver/Bronze/Uncertified)
- Sidecar engram emission with stencil metadata (sentient_layer info)
- Simple Python API for programmatic and CLI usage

## Files added
- `docs/TITANESS_METADATA_FAKTORY.md` — this overview
- `tools/titaness_metadata_faktory.py` — implementation module with the `TitanessSentientOS` class
- `tools/run_faktory.py` — production execution script

## Usage Instructions
```bash
# Run a Faktory pass on a single file
python tools/titaness_metadata_faktory.py "D:/path/to/my_asset.mp4" --category Media --context "Event: Mars Launch"

# Programmatic
from tools.titaness_metadata_faktory import TitanessSentientOS
os_jennifer = TitanessSentientOS(vault_path="E:/MDEC_VAULT_PROOF_CONCEPT")
engram = os_jennifer.run_faktory_pipeline("D:/path/to/my_asset.mp4", category="Architectures", context="Ingest test")
print(engram['certification'])
```

## Conformance
- Engram schema version: `2.1`
- MdEC toolkit compatibility: `1.x` exports

## Notes & Next Steps
- Added: preflight configuration support via `faktory.config.json` and `--config` flag.
- Added: CI lint workflow to check formatting and lints on PRs (`.github/workflows/ci-lint.yml`).
- Added: `AGENTS.md` and `MAINTENANCE_PLAYBOOK.md` to define agent responsibilities and governance.
- Next: add CI smoke checks and deploy-time validation (follow-up step), and consider a UI integration to the Titaness Observability Platform to trigger the pipeline and show certification results in real-time.

---

*Generated and committed on feature branch `feat/titaness-metadata-faktory`.*
