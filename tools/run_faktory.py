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

import argparse

def main():
    parser = argparse.ArgumentParser(description="Titaness Metadata Faktory - Engram Generator")
    parser.add_argument("source", nargs="?", help="Path to the source asset file")
    parser.add_argument("--category", default="Architectures", help="MdEC Category (default: Architectures)")
    parser.add_argument("--context", default="Ops Execution: Manual Trigger", help="Context string for the engram")
    parser.add_argument("--vault", help="Override vault path")
    parser.add_argument("--owner", default=os.getenv('TITANESS_OWNER', "The Architect"), help="Human-friendly owner name (e.g., 'The Architect')")
    parser.add_argument("--owner-id", default=os.getenv('TITANESS_OWNER_ID', None), help="Machine-readable owner identifier (URN)")
    parser.add_argument("--config", default=os.getenv('TITANESS_CONFIG_PATH', None), help="Path to a JSON configuration file (e.g., faktory.config.json)")

    # Pre-flight / runtime controls
    parser.add_argument("--preflight", dest="preflight", action="store_true", help="Enable pre-flight checks (default: enabled for interactive runs)")
    parser.add_argument("--no-preflight", dest="preflight", action="store_false", help="Disable pre-flight checks")
    parser.set_defaults(preflight=True)
    parser.add_argument("--preflight-level", choices=['required','warn','info'], default=os.getenv('TITANESS_PREFLIGHT_LEVEL','warn'), help="How strictly to treat preflight issues")
    parser.add_argument("--dry-run", action="store_true", help="Run analysis but do not write engram sidecar")
    parser.add_argument("--skip-checks", action="store_true", help="Skip pre-flight checks entirely")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors (equivalent to --preflight-level=required)")
    parser.add_argument("--quality-threshold", type=int, default=int(os.getenv('TITANESS_QUALITY_THRESHOLD','50')), help="Minimum quality score required (0-100)")
    parser.add_argument("--yes", action="store_true", help="Auto-approve prompts (non-interactive)")
    parser.add_argument("--operator-mode", action="store_true", help="Non-interactive operator/CI mode (fail on errors, auto-approve warnings by default)")

    args = parser.parse_args()

    if args.source:
        source = args.source
    else:
        source = input('Path to asset: ')

    if not os.path.exists(source):
        print(f"Error: Asset not found at {source}")
        sys.exit(1)

    # Initialize the OS Wrapper
    # Note: Vault path should ideally come from env var or config, defaulting here for now
    vault_path = args.vault or os.getenv('TITANESS_VAULT_PATH', 'E:\\MDEC_VAULT_PROOF_CONCEPT')
    
    print(f"Initializing Titaness Sentient OS (Jennifer)... Vault: {vault_path}")
    os_j = TitanessSentientOS(vault_path=vault_path, owner=args.owner, owner_id=args.owner_id, config_path=args.config)

    print(f"Processing Asset: {source}")
    print(f"   Category: {args.category}")
    print(f"   Context:  {args.context}")

    try:
        en = os_j.execute_faktory_run(
            source,
            category=args.category,
            context=args.context,
            preflight=args.preflight,
            preflight_level=args.preflight_level,
            dry_run=args.dry_run,
            skip_checks=args.skip_checks,
            strict=args.strict,
            quality_threshold=args.quality_threshold,
            auto_approve=args.yes,
            operator_mode=args.operator_mode
        )
        print('✅ Engram Generation Successful')
        print('   Path:', f"{source}.engram.json")
    except Exception as e:
        print(f"❌ Pipeline Failure: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
