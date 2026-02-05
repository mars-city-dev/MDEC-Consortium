# Titaness - Metadata Faktory > User Guide: run_faktory.py

**Project:** MdEC Consortium
**Tool:** Titaness Metadata Faktory CLI (`tools/run_faktory.py`)
**Status:** Production

## Overview
The `run_faktory.py` utility is the standard command-line interface for the Titaness Metadata Faktory. It triggers the MdEC Engram Generation Pipeline to produce certified metadata sidecars (`.engram.json`) for digital assets.

## Usage Syntax
Run the script from the root of the repository:

```powershell
python tools/run_faktory.py [source] [options]
```

## Arguments

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `source` | Positional | (Prompt) | The absolute or relative path to the asset file you want to process. |
| `--category` | Optional | `Architectures` | The MdEC Category for the asset. See valid categories below. |
| `--context` | Optional | `Ops Execution...` | A descriptive string explaining *why* this asset is being processed or its origin. |
| `--vault` | Optional | (Env Var) | Override the default `TITANESS_VAULT_PATH` environment variable. |
| `--owner` | Optional | `The Architect` | Human-friendly owner name to embed in the engram (e.g., "The Architect"). |
| `--owner-id` | Optional | (Env Var) | Machine-readable owner identifier (URN), e.g., `urn:person:mars-city:the-architect`. |
| `--config` | Optional | (Env Var) | Path to a JSON configuration file (e.g., `faktory.config.json`) to set defaults for preflight, quality thresholds and owner. |
| `--preflight` | Flag | Enabled (interactive) | Run pre-flight checks before the Faktory executes. |
| `--no-preflight` | Flag | N/A | Disable pre-flight checks. |
| `--preflight-level` | Option | `warn` | How to handle findings: `required` (treat warnings as errors), `warn`, `info`. |
| `--dry-run` | Flag | N/A | Perform analysis but do not write engram sidecar. |
| `--skip-checks` | Flag | N/A | Skip pre-flight checks entirely. |
| `--strict` | Flag | N/A | Treat warnings as errors (alias for `--preflight-level required`). |
| `--quality-threshold` | Option | `50` | Minimum quality score required to avoid warning/failure. |
| `--yes` | Flag | N/A | Auto-approve prompts for non-interactive runs. |
| `--operator-mode` | Flag | N/A | Non-interactive operator/CI mode (fail on errors, auto-approve warnings). |
| `--help` | Flag | N/A | Show help message and exit. |

### Valid Categories
* `Neural_DevOps_Protocol`
* `Open_Data_Legacy`
* `Architectures`
* `Deployments`
* `User_Guides`
* `Protocols`
* `Technical_Reports`
* `unassigned` (fallback)

## Examples

### 1. Basic Usage (Interactive)
The script will prompt for the asset path if not provided.
```powershell
python tools/run_faktory.py
# Enter path when prompted: D:\Assets\my_contract.pdf
```

### 2. Standard Production Run
Specifying all metadata flags for a deployment architecture diagram.
```powershell
python tools/run_faktory.py "D:\Diagrams\Mars_City_Full_Stack.png" --category "Architectures" --context "Production Deployment Vagus Release"
```

### 3. Protocol Ingestion
Ingesting a new operational protocol document.
```powershell
python tools/run_faktory.py "docs/SOP_Log_Rotation.md" --category "Protocols" --context "Ops Team Handoff"
```

### 4. Owner Override (Explicit)
When you want the engram to record a specific owner identity (human-friendly and machine-readable), pass `--owner` and optionally `--owner-id`:
```powershell
python tools/run_faktory.py "D:\Diagrams\Mars_City_Full_Stack.png" --category "Architectures" --context "Production Deployment Vagus Release" --owner "The Architect" --owner-id "urn:person:mars-city:the-architect"
```

### 5. Preflight & Dry-run Example
Run pre-flight checks and show results without writing the engram (useful for operators and CI):
```powershell
python tools/run_faktory.py "D:\Diagrams\Mars_City_Full_Stack.png" --category "Architectures" --preflight --dry-run --preflight-level warn
```

Run in non-interactive operator mode (CI):
```powershell
python tools/run_faktory.py "D:\Diagrams\Mars_City_Full_Stack.png" --category "Architectures" --operator-mode --yes --quality-threshold 80
```

### 6. Config File Example
You can provide a JSON config file (e.g., `faktory.config.json`) to set repository-wide defaults and policies. The runner supports `--config` or the `TITANESS_CONFIG_PATH` environment variable:
```powershell
python tools/run_faktory.py "D:\Diagrams\Mars_City_Full_Stack.png" --config faktory.config.json
```

## Output
Success will generate a JSON sidecar file in the same directory as the source asset.
* **Input:** `D:\Diagrams\Mars_City_Full_Stack.png`
* **Output:** `D:\Diagrams\Mars_City_Full_Stack.png.engram.json`

The console will display:
```text
✅ Engram Generation Successful
   Path: D:\Diagrams\Mars_City_Full_Stack.png.engram.json
```
