"""
Execution Script for Titaness Metadata Faktory
Purpose: Triggers the MdEC Engram Generation Pipeline (Standardized)
"""
import sys
import os

# Ensure we can import the adjacent module whether running from root or tools dir
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from titaness_metadata_faktory import TitanessSentientOS
except ImportError:
    # If running from root as 'python -m tools.run_faktory', relative import might be needed 
    # but the sys.path hack above handles the direct execution case.
    # Fallback for other contexts:
    from tools.titaness_metadata_faktory import TitanessSentientOS

def main():
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        source = input('Path to asset: ')

    if not os.path.exists(source):
        print(f"Error: Asset not found at {source}")
        sys.exit(1)

    # Initialize the OS Wrapper
    # Note: Vault path should ideally come from env var or config, defaulting here for now
    vault_path = os.getenv('TITANESS_VAULT_PATH', 'E:\\MDEC_VAULT_PROOF_CONCEPT')
    
    print(f"Initializing Titaness Sentient OS (Jennifer)... Vault: {vault_path}")
    os_j = TitanessSentientOS(vault_path=vault_path)

    print(f"Processing Asset: {source}")
    try:
        en = os_j.run_faktory_pipeline(
            source, 
            category='Architectures', 
            context='Ops Execution: Manual Trigger'
        )
        print('✅ Engram Generation Successful')
        print('   Path:', f"{source}.engram.json")
    except Exception as e:
        print(f"❌ Pipeline Failure: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
