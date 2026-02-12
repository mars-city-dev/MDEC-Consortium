# APOLLO: The Metadata Muse
## Project Charter & Codification

**Status:** INITIATION
**Sponsor:** MDEC (Metadata Excellence Consortium)
**Codename:** APOLLO
**Date:** January 15, 2026

---

### 1. Vision & Mission
**"To lead the Muses."**

APOLLO is the reference implementation and "World Standard" tool for interacting with metadata. It serves as the bridge between raw data mining (Data) and human understanding (Knowledge). It transforms abstract JSON/YAML metadata into a tangible, interactive "MOSART-ID-Card" that provides immediate insight and governance capabilities.

### 2. Core Philosophy
*   **Human-in-the-Loop:** Automation mines the data, but Humans govern it.
*   **Lightweight & Elegant:** No heavy databases required for the view layer. It operates on pure text (Markdown/JSON).
*   **Visual First:** Metadata should be seen to be understood.

### 3. Key Capabilities

#### A. The MOSART-ID-Card
A visual representation of an asset's digital soul.
*   **Visualization:** Instantly renders key metadata (Tags, Category, MDEC Class, Description, Author, Checksum) in a concise "Card" format.
*   **Interaction:** "Hover to Reveal" or "Click to Inspect" paradigms.

#### B. The Universal Reader/Writer
*   **Bi-Directional:**
    *   **Reader:** Parses .md frontmatter, JSON sidecars, and embedded tags.
    *   **Writer:** Injects standard-compliant metadata back into assets without destroying content.
*   **Format:** Focus on `.md` (Markdown) as the universal carrier of light-weight metadata.

#### C. Manual Repair & Governance
*   **The "Fix It" Button:** Allow users to manually correct AI-generated tags or categories.
*   **Validation:** Immediate visual feedback if an asset fails MDEC standards (e.g., Red Border = Untagged).

### 4. Technical Architecture (Proposed)
*   **Backend:** TypeScript/Python (MDEC Core Tools).
*   **Frontend (The Face of Apollo):**
    *   **Phase 1:** An HTML5/JS "Card Viewer" consuming the `archive_metadata.json` index.
    *   **Phase 2:** A VS Code Extension to render metadata on hover/click within the editor.
*   **Storage:** Flat-file systems (`.md` and `.json sidecars`).

### 5. Roadmap
1.  **Codification (Current):** Define the standard.
2.  **Prototype (The Viewer):** Build a simple web-based viewer for the existing Vault Archive.
3.  **Integration (The Editor):** Enable "Edit" functionality in the viewer to update the source `.md`.
4.  **The Extension:** Native OS or IDE integration for the "Hover" effect.

---
*Signed,*
*On behalf of the MDEC Consortium*
Christopher Olds
Founder/Lead Architect