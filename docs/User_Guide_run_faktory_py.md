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

## Output
Success will generate a JSON sidecar file in the same directory as the source asset.
* **Input:** `D:\Diagrams\Mars_City_Full_Stack.png`
* **Output:** `D:\Diagrams\Mars_City_Full_Stack.png.engram.json`

The console will display:
```text
✅ Engram Generation Successful
   Path: D:\Diagrams\Mars_City_Full_Stack.png.engram.json
```
