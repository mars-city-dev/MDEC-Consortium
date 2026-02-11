# Canonical Agent & Network Map (MDEC Consortium)

This canonical map is derived from `neural_map.json` and provides a quick reference for agents (Vagus, NIaC, ECM) and service endpoints used by the consortium.

---

*(abridged — reference the authoritative `d:\Projects\Mars-City-Infrastructure\neural_map.json` for the source of truth)*

- MARSTHREE_DEVICE — 192.168.1.228 — Vagus Analytics (8084), Host Kernel API (8888)
- UNITY_DEVICE   — 192.168.1.244 — Unity Home Server (8080), Axon Gateway (8002)
- STARGAZER_DEVICE — 192.168.1.199 — Archive Engine (8004), Tri-Cortex Orchestrator (8082)

---

## Agent quick reference

- **Vagus**: monitoring and healing (controller: `vagus_controller.py` on STARGAZER). Ports 8083/8084.
- **NIaC**: `neural_map.json` is the infra source of truth; use NIaC workflows for infra state changes only.
- **ECM (Obelisk)**: authoritative guide at `docs/NEURAL_DEVOPS_OBELISK_ECM.md` (Stargazer); use the two-drive workflow (D:→C:→push→watcher).

---

Use this file for quick lookups and automation references. If you want, I can add a small script (`scripts/generate-canonical-map.py`) to parse `neural_map.json` and output this file automatically.
