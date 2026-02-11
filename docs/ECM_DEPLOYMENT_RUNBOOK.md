# ECM Deployment Runbook (MDEC Consortium)

This runbook summarizes the safe ECM workflow for MDEC assets.

## Steps
1. Develop and test on Stargazer (D:).
2. Update `neural_map.json` if an infra state change is required.
3. Copy artifacts to Infrastructure (C:) and commit from the Infrastructure repo.
4. Push to `master` on the Infrastructure repo — Vagus/Watcher handles deployment.
5. Verify NIaC and Vagus status: run `VERIFY_NIAC_SYSTEM.ps1` and `python vagus_controller.py --status`.

## Verification
- Confirm remote health endpoints and Git hashes.
- If deployment fails, fix on D:, re-sync, push again.

---

This file is a lightweight, community-friendly copy of the primary runbook in `Mars-City-Infrastructure` and is intended to provide immediate operational guidance for MDEC contributors.
