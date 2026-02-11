"""
Titaness Metadata Faktory - Minimal implementation
Provides TitanessSentientOS that ingests an asset and emits an engram sidecar
"""
import os
import json
import hashlib
import uuid
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='[TITANESS-OS-JENNIFER] %(levelname)s: %(message)s')
logger = logging.getLogger("JenniferCore")

class TitanessSentientOS:
    """The cognitive core (Jennifer) responsible for governing the Metadata Faktory."""
    def __init__(self, vault_path: str, org_name: str = "Mars City Unity", owner: str = None, owner_id: str = None, config_path: str = None):
        self.vault_path = vault_path
        self.org_name = org_name

        # Load optional JSON config (faktory.config.json)
        self.config = {}
        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as cf:
                    self.config = json.load(cf)
                    logger.info(f"Loaded config from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config {config_path}: {e}")

        # Owner resolution: CLI arg overrides config, config overrides default
        self.owner = owner or self.config.get('owner', 'The Architect')
        # Normalize owner id if not provided (machine-friendly URN)
        owner_slug = self.owner.lower().replace(" ", "-")
        self.owner_id = owner_id or self.config.get('owner_id') or f"urn:person:mars-city:{owner_slug}"

        self.mdec_version = "1.0.0"
        self.engram_schema_version = "2.1"
        self.os_identity = "Titaness Sentient Systems OS - Jennifer"
        
        # Valid MdEC Categories
        self.valid_categories = [
            "Neural_DevOps_Protocol", "Open_Data_Legacy", 
            "Architectures", "Deployments", "User_Guides", 
            "Protocols", "Technical_Reports", "unassigned"
        ]
        
    def generate_guid(self) -> str:
        return str(uuid.uuid4())

    def calculate_integrity_hash(self, file_path: str) -> str:
        """MdEC Standard Requirement: SHA256 Integrity."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(8192), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest().upper()
        except Exception as e:
            logger.error(f"Integrity check failed: {e}")
            return "ERROR_CALCULATING"

    def _evaluate_excellence(self, metadata: Dict) -> int:
        """
        MdEC Quality Scorer: Evaluates adherence to excellence standards.
        """
        score = 100
        required = ["id", "name", "path", "category", "created", "modified", "checksum"]
        
        # Check for missing essentials
        for field in required:
            if field not in metadata or not metadata[field] or metadata[field] == "unassigned":
                score -= 15
        
        # Sentience & Enrichment Bonuses
        if metadata.get("sentient_layer"): score += 10
        if metadata.get("neural_links") and len(metadata["neural_links"]) > 0: score += 5
        if metadata.get("tags") and len(metadata["tags"]) > 0: score += 5
        
        return min(100, max(0, score))

    def execute_faktory_run(self, source_path: str, category: str = "unassigned", context: str = "", preflight: bool = True, preflight_level: str = "warn", dry_run: bool = False, skip_checks: bool = False, strict: bool = False, quality_threshold: int = 50, auto_approve: bool = False, operator_mode: bool = False) -> Dict:
        """
        STAGES: Ingest -> Hash -> Cognitive Analysis -> Scoring -> Certification -> Engram Emission

        New runtime controls:
        - preflight: enable/disable pre-flight checks
        - preflight_level: 'required'|'warn'|'info' (how strict to treat warnings)
        - dry_run: perform analysis but do not write sidecar
        - skip_checks: skip all preflight checks
        - strict: treat warnings as errors
        - quality_threshold: minimum quality score allowed
        - auto_approve: non-interactive auto-continue on warnings
        - operator_mode: non-interactive (CI) defaults
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Asset missing: {source_path}")

        logger.info(f"Faktory Pipeline Started for: {os.path.basename(source_path)}")
        
        # Resolve runtime defaults from config if caller passed None
        if preflight is None:
            preflight = self.config.get('preflight', True)
        if preflight_level is None:
            preflight_level = self.config.get('preflight_level', 'warn')
        if quality_threshold is None:
            quality_threshold = self.config.get('quality_threshold', 50)
        if dry_run is None:
            dry_run = self.config.get('dry_run', False)

        asset_name = os.path.basename(source_path)
        checksum = self.calculate_integrity_hash(source_path)
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Initialize Engram v2.1
        engram = {
            "id": self.generate_guid(),
            "engram_version": self.engram_schema_version,
            "mdec_standards_version": self.mdec_version,
            "origin_vault": "DATA_LEGACY_VAULT_PERSONAL",
            "name": asset_name,
            "path": os.path.abspath(source_path),
            "owner": self.owner,
            "owner_id": self.owner_id,
            "category": category if category in self.valid_categories else "unassigned",
            "created": timestamp,
            "modified": timestamp,
            "checksum": checksum,
            "tags": [f"owner:{self.owner.lower().replace(' ', '-')}"] ,
            "neural_links": [], 
            "sentient_layer": {
                "os_authority": self.os_identity,
                "owner_identity": self.owner,
                "context": context or "Cognitive ingestion via Jennifer OS.",
                "legacy_grade": "PENDING_VERIFICATION",
                "cognitive_flags": ["faktory_processed"],
                "sentiment_vector": None
            }
        }

        # Evaluate quality early for preflight decisions
        quality_score = self._evaluate_excellence(engram)
        engram["quality_score"] = quality_score
        
        # Pre-flight checks
        if preflight and not skip_checks:
            issues = []  # tuple of (severity, message)

            # Integrity
            if checksum == "ERROR_CALCULATING":
                issues.append(("error", "Integrity hash calculation failed"))

            # Owner
            if not self.owner or not self.owner_id:
                issues.append(("warn", "Owner information missing or incomplete"))

            # Vault availability
            if not os.path.exists(self.vault_path):
                issues.append(("warn", f"Vault path does not exist: {self.vault_path}"))
            else:
                if not os.access(self.vault_path, os.W_OK):
                    issues.append(("warn", f"Vault path not writable: {self.vault_path}"))

            # Quality threshold
            if quality_score < quality_threshold:
                issues.append(("warn", f"Quality score {quality_score} below threshold {quality_threshold}"))

            # Promote warnings to errors if strict or required
            if strict or preflight_level == "required":
                issues = [("error" if s == "warn" else s, m) for (s, m) in issues]

            # Decide what to do
            errors = [m for (s, m) in issues if s == "error"]
            warns = [m for (s, m) in issues if s == "warn"]

            if errors:
                raise RuntimeError(f"Preflight failed: {errors[0]}")

            if warns:
                # Operator/CI: behave non-interactively
                if operator_mode or auto_approve:
                    logger.warning("Preflight warnings (auto-approved): %s", warns)
                else:
                    # Interactive: prompt user
                    print("Preflight detected warnings:")
                    for w in warns:
                        print(f" - {w}")
                    resp = input("Continue anyway? (y/N): ")
                    if resp.strip().lower() not in ("y","yes"):
                        raise RuntimeError("Aborted by user during preflight checks")

        # Certification Mapping
        if quality_score >= 95: engram["certification"] = "Gold"
        elif quality_score >= 80: engram["certification"] = "Silver"
        elif quality_score >= 50: engram["certification"] = "Bronze"
        else: engram["certification"] = "Uncertified"

        # Emit Engram to Sidecar unless dry-run
        engram_path = f"{source_path}.engram.json"
        if dry_run:
            logger.info(f"Dry-run enabled: no sidecar will be written. Certification: {engram['certification']}")
            return engram

        with open(engram_path, "w", encoding='utf-8') as f:
            json.dump(engram, f, indent=4)
        
        logger.info(f"Faktory Complete. [{engram['certification']}] Engram emitted: {engram_path}")
        return engram


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Titaness Metadata Faktory - quick runner')
    parser.add_argument('source', help='Path to source asset')
    parser.add_argument('--category', default='unassigned', help='Category for the asset')
    parser.add_argument('--context', default='', help='Context note')
    args = parser.parse_args()

    os_jennifer = TitanessSentientOS(vault_path=args.source, owner=args.owner, owner_id=args.owner_id)
    engram = os_jennifer.execute_faktory_run(args.source, category=args.category, context=args.context)
    print('--- ENGRAM ---')
    print(json.dumps(engram, indent=2))
