import json
import os
import sys
import datetime
import argparse

# PATHS
WORKSPACE_ROOT = r"D:\Projects\MDEC-Consortium"
LEDGER_PATH = os.path.join(WORKSPACE_ROOT, "TITANESS_CENTRAL_LEDGER_SSOT.json")
MANIFEST_PATH = os.path.join(WORKSPACE_ROOT, "mdec_manifest.json")
REPORT_PATH = os.path.join(WORKSPACE_ROOT, "TITANESS_INGEST_REPORT.html")

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def generate_html_report(new_entries):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <html>
    <head>
        <title>TITANESS Ingestion Report - {timestamp}</title>
        <style>
            body {{ font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }}
            h1 {{ color: #58a6ff; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #30363d; padding: 8px; text-align: left; }}
            th {{ background-color: #161b22; }}
            .m-id {{ color: #7ee787; }}
            .score {{ color: #d2a8ff; }}
        </style>
    </head>
    <body>
        <h1>TITANESS INGESTION REPORT</h1>
        <p>Generated: {timestamp}</p>
        <p>Total New Assets: {len(new_entries)}</p>
        <table>
            <tr>
                <th>File Name</th>
                <th>M-ID (Deterministic)</th>
                <th>Signet Creator</th>
                <th>Quality Score</th>
            </tr>
    """
    
    for entry in new_entries:
        html += f"""
            <tr>
                <td>{entry.get('file_name', 'N/A')}</td>
                <td class="m-id">{entry.get('m-id', 'PENDING')}</td>
                <td>{entry.get('signet_creator', 'Unknown')}</td>
                <td class="score">{entry.get('quality_score', '0.0')}</td>
            </tr>
        """
        
    html += """
        </table>
    </body>
    </html>
    """
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Report Generated: {REPORT_PATH}")

def main():
    print("------------------------------------------------")
    print("TITANESS BRIDGE: INGEST -> LEDGER")
    print("------------------------------------------------")
    
    # 1. Load Data
    manifest = load_json(MANIFEST_PATH)
    ledger = load_json(LEDGER_PATH)
    
    if not manifest:
        print("No manifest found. Run Ingestion Worker first.")
        sys.exit(1)
        
    # 2. Process Entries
    new_ledger_entries = 0
    processed_list = []
    
    # Ensure ledger structure
    if "entries" not in ledger:
        ledger["entries"] = {}
        
    # Manifest is usually a list
    if isinstance(manifest, list):
        items = manifest
    else:
        items = [manifest] # Handle single object edge case
        
    for item in items:
        mid = item.get("m-id")
        if mid and mid not in ledger["entries"]:
            # Commit to Ledger
            ledger["entries"][mid] = {
                "signet": item.get("signet_creator"),
                "timestamp": item.get("generated_at"),
                "file_ref": item.get("relative_path"),
                "provenance": "TITANESS_INGESTION_WORKER"
            }
            new_ledger_entries += 1
            processed_list.append(item)
            print(f"[+] LEDGER UPDATE: {mid} -> {item.get('file_name')}")
            
    # 3. Save Ledger
    save_json(LEDGER_PATH, ledger)
    print(f"Ledger Updated. {new_ledger_entries} new entries committed.")
    
    # 4. Generate Report
    generate_html_report(processed_list)

if __name__ == "__main__":
    main()
