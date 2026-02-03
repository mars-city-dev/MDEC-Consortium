import re

file_path = r"d:\Projects\MDEC-Consortium\docs\MDEC_CODEX.md"

print(f"Reading {file_path}...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# New Article Content
new_article = r"""
---

## Article X: Data Warehousing & Modern Telemetry

### Section 10.1: The Immutable M-ID (Metadata Identifier)
To maintain integrity across physical and digital realms, the **M-ID** is established as the absolute Primary Key.
- **Definition**: A globally unique, immutable identifier assigned to every distinct data asset.
- **Scope**: Sticks to the asset regardless of location (Vault, Cloud, NAS) or format.
- **Requirement**: No asset shall be moved, archived, or transformed without preserving its M-ID.

### Section 10.2: Data Activity Tracking (Modern Warehousing)
MDEC adopts modern telemetry standards to ensure "Smart Datum" are traceable.
- **Change Data Capture (CDC)**: Systems must log *deltas* (changes), not just snapshots. Every modification is an event.
- **The "Daily Delta" Report**: A standardized operational report generated every 24 hours summarizing:
    - **Ingress**: New assets entering the ecosystem.
    - **Egress**: Assets archived or deleted.
    - **Mutations**: Metadata updates or tag enhancements.
    - **Movement**: Physical transfers (e.g., Shelf A -> Shelf B).

### Section 10.3: Physical-Digital Bridging (The Vault Protocol)
For hybrid environments (Physical Media + Digital Twins):
- **Location Mapping**: Physical assets must be tracked via `Row` (X-axis) and `Bin` (Y-axis) coordinates linked to the M-ID.
- **Telemetry**: Automated scanners or logging tools must record physical movements as digital events.
- **Verification**: Periodic "Cycle Counts" (digital vs. physical audit) are required for Gold Certification.

"""

# Insertion Point: Before "## Appendices"
if "## Article X:" not in content:
    if "## Appendices" in content:
        print("Inserting Article X before Appendices...")
        content = content.replace("## Appendices", new_article.strip() + "\n\n## Appendices")
    else:
        print("Could not find Appendices section. Appending to end.")
        content += new_article
else:
    print("Article X already exists.")

print("Writing file...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done.")
