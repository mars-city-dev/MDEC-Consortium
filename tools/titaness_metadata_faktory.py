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
    def __init__(self, vault_path: str, org_name: str = "Mars City Unity"):
        self.vault_path = vault_path
        self.org_name = org_name
        self.mdec_version = "1.0.0"
        self.engram_schema_version = "2.1"
        self.os_name = "Titaness Sentient Systems OS - Jennifer"
        
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

    def compute_quality_metrics(self, metadata: Dict) -> int:
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

    def run_faktory_pipeline(self, source_path: str, category: str = "unassigned", context: str = "") -> Dict:
        """
        STAGES: Ingest -> Hash -> Cognitive Analysis -> Scoring -> Certification -> Engram Emission
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Asset missing: {source_path}")

        logger.info(f"Faktory Pipeline Started for: {os.path.basename(source_path)}")
        
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
            "category": category if category in self.valid_categories else "unassigned",
            "created": timestamp,
            "modified": timestamp,
            "checksum": checksum,
            "tags": [],
            "neural_links": [], 
            "sentient_layer": {
                "os_authority": self.os_name,
                "context": context or "Cognitive ingestion via Jennifer OS.",
                "legacy_grade": "PENDING_VERIFICATION",
                "cognitive_flags": ["faktory_processed"],
                "sentiment_vector": None
            }
        }

        # Quality & Certification Pass
        quality_score = self.compute_quality_metrics(engram)
        engram["quality_score"] = quality_score
        
        # Certification Mapping
        if quality_score >= 95: engram["certification"] = "Gold"
        elif quality_score >= 80: engram["certification"] = "Silver"
        elif quality_score >= 50: engram["certification"] = "Bronze"
        else: engram["certification"] = "Uncertified"

        # Emit Engram to Sidecar
        engram_path = f"{source_path}.engram.json"
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

    os_jennifer = TitanessSentientOS(vault_path=args.source)
    engram = os_jennifer.run_faktory_pipeline(args.source, category=args.category, context=args.context)
    print('--- ENGRAM ---')
    print(json.dumps(engram, indent=2))
