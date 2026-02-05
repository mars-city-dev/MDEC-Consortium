# Maintenance Playbook — Titaness Metadata Faktory

## Goals
- Maintain deterministic, auditable engram generation
- Ensure preflight checks run by default and are reproducible
- Keep CI linting green and documentation current

## Roles
- **Operator**: Non-interactive runs, CI integration, auto-approve minor lint fixes
- **End-User**: Interactive runs, guided prompts, human-in-the-loop approval for risky ops
- **Owner**: `The Architect` (see CODEOWNERS)

## Daily/Weekly Tasks
- Monitor CI runs and fix linting issues
- Review open PRs and accept agent-suggested fixes when safe
- Verify vault accessibility and backups

## Release Checklist
1. Ensure CI lint passes
2. Run a full preflight with `--preflight-level required` and ensure no errors
3. Confirm `quality_threshold` meets release policy
4. Tag and create release notes

## Neural DevOps Protocol (Overview)
- Agents run scheduled preflight checks and propose fixes as PRs
- Human owners approve changes for sensitive files
- Agents may run `--dry-run` to show intended changes before creating PRs
