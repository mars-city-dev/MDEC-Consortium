# MDEC v1.0.0 RFC Alignment & Compatibility Map

## 1. Abstract
The Meta Data Excellence Consortium (MDEC) standard is designed not to replace, but to **extend and enforce** the foundational internet standards established by the IETF. This document maps MDEC v1.0.0 core fields to their definitions in RFC 5013 (Dublin Core), RFC 4287 (Atom), and RFC 8941 (Structured Fields), ensuring immediate interoperability with existing internet infrastructure while introducing "Titaness" quality assurance mechanisms.

## 2. Core Field Mapping: MDEC to Dublin Core (RFC 5013)

MDEC adopts the definitions of RFC 5013 for semantic clarity but enforces stricter validation rules.

| MDEC Field | RFC 5013 (Dublin Core) | RFC Compliant? | Notes |
| :--- | :--- | :---: | :--- |
| **id** | `dc:identifier` | ✅ Yes | MDEC enforces **GUID/UUID** format for this field, acting as the primary key (Titaness M-ID). RFC 5013 allows any unique string; MDEC restricts it for uniqueness safety. |
| **name** | `dc:title` | ✅ Yes | Maps directly. MDEC usage: "Human-readable title". |
| **category** | `dc:type` | ✅ Yes | MDEC narrows `dc:type` to 8 Universal Categories (Documents, Media, etc.) to prevent taxonomy fragmentation. |
| **tags** | `dc:subject` | ✅ Yes | Used for descriptive keywords. MDEC typically serializes this as a List. |
| **created_at** | `dc:date` | ✅ Yes | MDEC enforces **ISO 8601** (RFC 3339) strict compliance, as recommended but not required by generic DC. |
| **path** | `dc:source` (loosely) | ⚠️ Partial | `dc:source` refers to a resource derivation. MDEC `path` refers to the *canonical storage location*. In Atom (RFC 4287), this maps closer to `atom:link rel="self"`. |

## 3. The "Excellence Layer": MDEC Extensions & RFC 8941

MDEC introduces fields specifically for **Quality Assurance** and **Provenance** that extend beyond descriptive metadata. These are defined using **RFC 8941 (Structured Field Values for HTTP)** types to ensure they are machine-parseable in modern headers.

| MDEC Extension | Type (RFC 8941) | Purpose |
| :--- | :--- | :--- |
| **quality_score** | `Decimal` (Section 3.3.2) | **The Core Utility.** A 0.00-100.00 score indicating metadata completeness. <br> *Example Header:* `MDEC-Quality: 98.50` |
| **checksum** | `Byte Sequence` (Section 3.3.5) | **Integrity.** SHA-256 hash to ensure asset hasn't suffered bit-rot. <br> *Example Header:* `MDEC-Integrity: :cHJldGVuZCB0aGlzIGlzIGJpbmFyeSBjb250ZW50Lg==:` |
| **SIGNET** | `String` (Section 3.3.3) | **Deep Provenance.** A structured string embedding Creator-DOB-Epoch-Vocation. <br> Maps to an enhanced `dc:creator` or `atom:author`. |

## 4. The TITANESS M-ID Protocol
*Alignment with RFC 4287 (Atom Syndication Format)*

In an Atom Feed/Entry, the **TITANESS M-ID** serves as the mandated `atom:id`:

```xml
<!-- MDEC Asset represented as Atom Entry -->
<entry>
  <title>MDEC_CODEX.md</title>
  <!-- MDEC ID: The Immutable M-ID -->
  <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
  <updated>2026-01-16T12:00:00Z</updated>
  <author>
    <!-- SIGNET Mapping -->
    <name>Christopher-Olds-07-14-1962-20xx-Engineer-Musician-Author-Poet-USA</name>
  </author>
  <!-- MDEC Quality Extension -->
  <mdec:quality value="98.5" certification="Gold" />
</entry>
```

## 5. Conclusion
MDEC is a **Strict Superset** of RFC 5013 (Dublin Core). Any MDEC-compliant system is automatically Dublin Core 1.1 compliant. The "Excellence" comes from the additional, mandatory fields (`quality_score`, `integrity`) that turn passive metadata into active, managed assets.
