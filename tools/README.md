# 🛠️ MDEC Tools & Global Standards Toolkit

**Practical tools for metadata excellence**

---

## 🚀 NEW: Core Python Tools (READY TO USE!)

### 1. MDEC Quality Scorer ✅
**File:** `Core/mdec_quality_scorer.py`

**What it does:** Analyzes any file and gives it a quality score (0-100) based on MDEC standards

**Usage:**
```bash
python Core/mdec_quality_scorer.py myfile.json
python Core/mdec_quality_scorer.py myfile.md --json
```

**Output Example:**
```
MDEC METADATA QUALITY SCORE
Overall Score: 87/100 ✅ GOOD

Detailed Scores:
  • Completeness: 95/100 ✅
  • Consistency:  75/100 ⚠️
  • Accuracy:     92/100 ✅
  • Richness:     85/100 ✅

Recommendations:
  ⚠️  Fix date format inconsistencies (use ISO8601)
  💡 Add more descriptive tags (aim for 3-5 tags)
```

---

### 2. MDEC Auto-Validator ✅
**File:** `Core/mdec_auto_validator.py`

**What it does:** Automatically validates metadata against MDEC standards and FIXES issues

**Three Modes:**

1. **Validate Mode** (check only):
```bash
python Core/mdec_auto_validator.py /path/to/files
```

2. **Fix Mode** (auto-correct issues):
```bash
python Core/mdec_auto_validator.py /path/to/files --fix
```

3. **Watch Mode** (continuous monitoring):
```bash
python Core/mdec_auto_validator.py /path/to/files --watch --fix
```

**What it fixes automatically:**
- ✅ Missing required fields (adds them)
- ✅ Invalid date formats (converts to ISO8601)
- ✅ Incorrect tag formats (converts to arrays)
- ✅ Weak IDs (generates proper UUIDs)
- ⚠️  Generic categories (flags for manual review)

---

## 🎯 Quick Start Guide

### Test Both Tools on a Sample File

```bash
# 1. Create a test file
echo '{"name": "test", "category": "misc"}' > test.json

# 2. Score it (will show low score)
python Core/mdec_quality_scorer.py test.json

# 3. Auto-fix issues
python Core/mdec_auto_validator.py test.json --fix

# 4. Score again (improved!)
python Core/mdec_quality_scorer.py test.json
```

---

## 📦 PowerShell Toolkit (Existing)

## What is MDEC?
The Meta Data Excellence Consortium (MDEC) is revolutionizing metadata management worldwide by establishing global standards that eliminate "shitty metadata practices" and ensure data integrity, discoverability, and automation.

## Quick Start

1. **Install the Toolkit**
   `powershell
   .\MDEC_Global_Standards_Toolkit.ps1 -Install
   `

2. **Run the Example**
   `powershell
   .\Examples\MDEC_Implementation_Example.ps1
   `

3. **Get Certified**
   - Achieve Bronze: Basic compliance (50% quality)
   - Achieve Silver: Full compliance (80% quality)
   - Achieve Gold: Perfect automation (100% quality)

## Toolkit Components

- **Core/**: Core MDEC modules and automation
- **Validation/**: Compliance testing and certification
- **AI/**: Intelligent automation tools
- **Standards/**: Official MDEC specifications
- **Certification/**: Certification programs and badges
- **Documentation/**: Guides and best practices
- **Examples/**: Implementation examples

## Community

Join the global MDEC community:
- Website: https://mdec.global
- Standards: https://standards.mdec.global
- Community: https://community.mdec.global

## License

MDEC Global Standards are open source and freely available for adoption worldwide.

---
*Eliminating shitty metadata practices, one organization at a time.*
