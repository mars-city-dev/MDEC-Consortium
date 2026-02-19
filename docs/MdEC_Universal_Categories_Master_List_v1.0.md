# MdEC Universal Categories Master List v1.0
**Status:** RATIFIED  
**Date:** 2026-02-18  
**Codex:** TITANESS-MDEC-CORE-CAT-V1  
**Scope:** Global (All Nodes / All Filesystems)

## 1. The Philosophy of the 10
To prevent metadata fragmentation and ensure universal compatibility across the Titaness Neural Network, all digital assets MUST be sorted into one of the following 10 High-Level Categories.

These categories are **Immutable** at the root level. Sub-taxonomies (tags) usually handle specific details, but the "Folder 01-99" structure remains constant.

## 2. The Universal Categories

| ID | Category Name | Description | Examples |
| :--- | :--- | :--- | :--- |
| **01** | **Documents** | Text-based information, knowledge, and written records. | `.h`, `.c`, `.txt`, `.md`, `.pdf`, `.docx`, `.epub` |
| **02** | **Media** | Visual, Audio, and Sensory inputs. | `.jpg`, `.png`, `.mp4`, `.wav`, `.flac` |
| **03** | **Data** | Structured data, databases, and configuration arrays. | `.json`, `.csv`, `.sql`, `.yaml`, `.xml` |
| **04** | **Code** | Executable logic, scripts, and source code. | `.py`, `.js`, `.ts`, `.ps1`, `.sh` |
| **05** | **Archives** | Compressed containers and disk images. | `.zip`, `.tar.gz`, `.iso`, `.rar` |
| **06** | **Assets** | Creative building blocks, 3D models, and raw design files. | `.psd`, `.ai`, `.obj`, `.fbx`, `.unitypackage` |
| **07** | **Communications** | Interaction records, emails, and contacts. | `.eml`, `.msg`, `.vcf` |
| **08** | **References** | Pointers to other locations (Shortcuts). | `.lnk`, `.url` |
| **09** | **Uncategorized** | The "Catch-All" for unidentified anomalies. Usage should be minimized. | `_mdec_catchall` |
| **99** | **System** | OS Artifacts, Logs, and Protected System Files. (DO NOT TOUCH) | `.dll`, `.sys`, `.dat`, `thumbs.db` |

## 3. Implementation Rules

1.  **Orphan Rule:** Any file extension NOT found in Categories 01-08 or 99 is automatically moved to **09_Uncategorized**.
2.  **System Protection:** Category **99_System** is considered "Radioactive." Automated tools should generally skip deep scanning of these folders unless specifically auditing OS integrity.
3.  **Expansion:** Future Categories (10-98) are reserved for domain-specific expansion (e.g., "10_Medical_Imaging" for a hospital node), but the **Core 10** must remain standard across all MdEC nodes.
