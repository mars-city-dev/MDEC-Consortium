import os
import json
import hashlib
import datetime
import sys
from pathlib import Path
import zipfile
import time
#        Identifies Primary/Secondary/Tertiary duplicates and sorts by age.

# CONFIGURATION
# ------------------------------------------------------------------------------
WORKSPACE_ROOT = r"D:\Projects" # Scanning the whole workspace for intelligence
LEDGER_PATH = r"D:\Projects\MDEC-Consortium\TITANESS_CENTRAL_LEDGER_SSOT.json"

# MdEC UNIVERSAL CATEGORIES (The 10 Core Pillars)
CATEGORIES = {
    "01": "Documents",
    "02": "Media",
    "03": "Data",
    "04": "Code",
    "05": "Archives",
    "06": "Assets",
    "07": "Communications",
    "08": "References",
    "09": "Uncategorized",
    "99": "System"
}

# EXTENSION MAP (Simplified for the Inspector - The Organizer has the full list)
EXT_MAP = {
    "01": [".txt", ".md", ".pdf", ".doc", ".docx", ".epub", ".h", ".c"],
    "02": [".jpg", ".png", ".gif", ".mp4", ".wav", ".mp3", ".flac"],
    "03": [".json", ".csv", ".xml", ".yaml", ".sql"],
    "04": [".py", ".js", ".ts", ".ps1", ".sh", ".bat", ".html", ".css"],
    "05": [".zip", ".tar", ".gz", ".rar", ".7z", ".iso"],
    "06": [".psd", ".ai", ".obj", ".fbx", ".blend", ".unitypackage"],
    "07": [".eml", ".msg", ".vcf"],
    "08": [".lnk", ".url"],
    "99": [".dll", ".sys", ".dat", ".db", ".exe", ".bin"]
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("================================================================")
    print("      TITANESS METADATA FAKTORY  --  MdEC INSPECTOR v1.0        ")
    print("================================================================")
    print("      \"Intelligence over Replication\"                           ")
    print("----------------------------------------------------------------")

def get_file_hash(filepath):
    """Calculates SHA-256 hash of a file for identification."""
    try:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None

def get_file_category(extension):
    """Determines category ID based on extension."""
    ext = extension.lower()
    for cat_id, extensions in EXT_MAP.items():
        if ext in extensions:
            return cat_id
    if ext == "":
        return "09" # No extension
    return "09" # Uncategorized

def scan_zip_archive(zip_path, target_category_id):
    """
    Gently scans a .zip archive without extracting everything to disk.
    Reads file headers and streams content for hashing.
    """
    print(f"\n[SCANNING] Initiating Neural Rover (Gentle Mode) on: {zip_path} ...")
    print(f"[FILTER]   Looking for Category: {CATEGORIES.get(target_category_id, 'Unknown')}")
    
    found_files = {} 
    file_count = 0
    start_time = datetime.datetime.now()
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            file_list = z.namelist()
            print(f"[ARCHIVE]  {len(file_list)} files detected in archive.")
            
            for file in file_list:
                # Gentle processing - slight delay every 500 files to avoid CPU spikes
                if file_count > 0 and file_count % 500 == 0:
                    time.sleep(0.1)

                if file.endswith('/'): continue # Skip directories
                
                name = os.path.basename(file)
                _, ext = os.path.splitext(name)
                ext = ext.lower()
                
                # Category Logic
                current_cat = get_file_category(ext)
                if target_category_id == "09":
                    if current_cat != "09": continue
                elif current_cat != target_category_id:
                    continue
                
                # Metadata (from ZipInfo)
                info = z.getinfo(file)
                # Zip timestamps are tuples (Y,M,D,H,M,S)
                try:
                    dt = datetime.datetime(*info.date_time)
                except:
                    dt = datetime.datetime.now()
                
                # Hash Content (Streamed from memory)
                with z.open(file) as f:
                    sha256_hash = hashlib.sha256()
                    while chunk := f.read(4096):
                        sha256_hash.update(chunk)
                    f_hash = sha256_hash.hexdigest()
                
                file_info = {
                    "path": f"{zip_path} :: {file}",
                    "name": name,
                    "created": dt, # Zips only keep one timestamp usually
                    "modified": dt,
                    "size": info.file_size
                }

                if f_hash in found_files:
                    found_files[f_hash].append(file_info)
                else:
                    found_files[f_hash] = [file_info]
                    
                file_count += 1
                if file_count % 100 == 0:
                    print(f"\r[SCANNING] Found {file_count} items...", end="")
                    
    except zipfile.BadZipFile:
        print("\n[ERROR] The file is not a valid zip archive or is corrupted.")
    except Exception as e:
        print(f"\n[ERROR] An error occurred during zip scanning: {str(e)}")

    print(f"\r[COMPLETE] Found {file_count} items in {(datetime.datetime.now() - start_time).total_seconds():.2f}s.")
    return found_files

def scan_workspace(root_path, target_category_id):
    """
    Scans the workspace for files matching the target category.
    Returns a dictionary of found files organized by Hash (to find duplicates).
    """
    print(f"\n[SCANNING] Initiating Neural Rover scan on: {root_path} ...")
    print(f"[FILTER]   Looking for Category: {CATEGORIES.get(target_category_id, 'Unknown')}")

    found_files = {} # Key: Hash, Value: List of file info dicts
    file_count = 0
    start_time = datetime.datetime.now()

    target_extensions = EXT_MAP.get(target_category_id, [])
    # If category 09, we look for anything NOT in the other lists (simplified)

    for root, dirs, files in os.walk(root_path):
        # Skip safe zones or heavy folders if needed
        if "node_modules" in dirs: dirs.remove("node_modules")
        if ".git" in dirs: dirs.remove(".git")
        if "venv" in dirs: dirs.remove("venv")

        for file in files:
            name, ext = os.path.splitext(file)
            ext = ext.lower()

            # Category Filtering Logic
            current_cat = get_file_category(ext)

            # Special handling for "Uncategorized" (09) - catch everything else
            if target_category_id == "09":
                if current_cat != "09": continue
            elif current_cat != target_category_id:
                continue

            # We found a match!
            full_path = os.path.join(root, file)
            try:
                stat = os.stat(full_path)
                created = datetime.datetime.fromtimestamp(stat.st_ctime)
                modified = datetime.datetime.fromtimestamp(stat.st_mtime)
                size = stat.st_size

                # Get Hash to identify uniqueness
                f_hash = get_file_hash(full_path)
                if not f_hash: continue

                file_info = {
                    "path": full_path,
                    "name": file,
                    "created": created,
                    "modified": modified,
                    "size": size
                }

                if f_hash in found_files:
                    found_files[f_hash].append(file_info)
                else:
                    found_files[f_hash] = [file_info]

                file_count += 1
                if file_count % 100 == 0:
                    print(f"\r[SCANNING] Found {file_count} items...", end="")

            except Exception as e:
                # Permission errors, etc.
                continue

    print(f"\r[COMPLETE] Found {file_count} items in {(datetime.datetime.now() - start_time).total_seconds():.2f}s.")
    return found_files

def analyze_results(found_files):
    """
    Analyzes the scan results to find Primary/Secondary copies.
    """
    print("\n----------------------------------------------------------------")
    print("      INTELLIGENCE REPORT: DUPLICATE ANALYSIS                   ")
    print("----------------------------------------------------------------")

    total_unique = len(found_files)
    total_files = sum(len(v) for v in found_files.values())
    duplicates = total_files - total_unique

    print(f"TOTAL OBJECTS DETECTED: {total_files}")
    print(f"UNIQUE SIGNATURES:      {total_unique}")
    print(f"REDUNDANT COPIES:       {duplicates}")
    print("----------------------------------------------------------------\n")

    # Sort hashes by the creation date of their OLDEST file (Primary)
    sorted_hashes = []
    for f_hash, file_list in found_files.items():
        # Sort files in this group by creation date (Oldest first)
        file_list.sort(key=lambda x: x['created'])
        primary = file_list[0]
        sorted_hashes.append((primary['created'], f_hash, file_list))

    # Sort the global list by date of origin
    sorted_hashes.sort(key=lambda x: x[0])

    # Display Top 20 Oldest / Most Important
    count = 0
    for created, f_hash, file_list in sorted_hashes:
        count += 1
        primary = file_list[0]
        date_str = created.strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{count:03}] PRIMARY: {primary['name']} ({date_str})")
        print(f"      Location: {primary['path']}")

        if len(file_list) > 1:
            print(f"      COPIES DETECTED ({len(file_list)-1}):")
            for i, copy in enumerate(file_list[1:]):
                copy_date = copy['created'].strftime("%Y-%m-%d %H:%M:%S")
                print(f"        -> Copy {i+1}: {copy['path']} ({copy_date})")

        print("")
        if count >= 50: # Limit output for sanity
            print("... (Listing truncated for brevity) ...")
            break

def main():
    clear_screen()
    print_header()

    print("Which Universal Category would you like to inspect?")
    print("---------------------------------------------------")
    for cat_id, name in CATEGORIES.items():
        print(f" [{cat_id}] {name}")
    print("---------------------------------------------------")

    choice = input("Enter Category ID (01-99) or 'ALL': ").strip()

    target_id = choice
    if choice.upper() == 'ALL':
        print("Feature 'ALL' coming in v2.0. Please select a specific category.")
        return

    if target_id not in CATEGORIES:
        print("Invalid Selection. Defaulting to '09' (Uncategorized)")
        target_id = "09"
    
    print("\n---------------------------------------------------")
    print("TARGET LOCATION")
    print("---------------------------------------------------")
    print("[1] Scan Entire Workspace (Default)")
    print("[2] Scan Specific Folder")
    print("[3] Scan .ZIP Archive (Gentle Mode)")
    
    loc_choice = input("Select Option [1-3]: ").strip()
    
    scan_root = WORKSPACE_ROOT
    is_zip = False
    
    if loc_choice == '2':
        custom_path = input("Enter full folder path: ").strip().strip('"')
        if os.path.exists(custom_path) and os.path.isdir(custom_path):
            scan_root = custom_path
        else:
            print("Invalid folder. Reverting to Workspace Root.")
            
    elif loc_choice == '3':
        zip_path = input("Enter full .zip path: ").strip().strip('"')
        if os.path.exists(zip_path) and zip_path.lower().endswith('.zip'):
            scan_root = zip_path
            is_zip = True
        else:
            print("Invalid zip file. Reverting to Workspace Root.")

    print(f"\n[INIT] Inspector loaded. Target: [{target_id}] {CATEGORIES[target_id]}")
    print(f"[MODE] Scanning: {scan_root} {'(ZIP ARCHIVE)' if is_zip else ''}")
    
    # Run the Scan
    if is_zip:
        found_data = scan_zip_archive(scan_root, target_id)
    else:
        found_data = scan_workspace(scan_root, target_id)
