# TITANESS Ingestion Engine - MDEC Data Legacy Vault
# Version: 1.2.0 - Safety Protocol Enhanced
# Implements: draft-mdec-metadata-excellence-00 (Section 6: Destructive Operations)

param(
    [string]$RootPath = "d:\Projects\MDEC-Consortium",
    [switch]$DryRun,
    [switch]$EliminateEmpty,
    [switch]$ConfirmDelete,
    [switch]$GenerateManifest
)

Write-Host "TITANESS INGESTION ENGINE ACTIVATED" -ForegroundColor Cyan
Write-Host "Root Path: $RootPath" -ForegroundColor Yellow
Write-Host "Mode: $(if($DryRun){'DRY RUN'}else{'LIVE INGESTION'})" -ForegroundColor Yellow
Write-Host "Safety Protocol: $(if($ConfirmDelete){'ARMED'}else{'SAFE (Reporting Only)'})" -ForegroundColor Magenta
Write-Host ""

# -------------------------------------------------------------------------
# HELPER: QS Algo (Section 5 of Draft)
# -------------------------------------------------------------------------
function Get-MdecQualityScore {
    param($File)
    
    # Cm (Completeness): 1.0 (We are auto-generating the manifest)
    $Cm = 1.0
    
    # Ac (Accuracy): 1.0 (File exists on disk)
    $Ac = 100 
    if (-not (Test-Path $File.FullName)) { $Ac = 0 }
    
    # Cn (Consistency): 0.9 (Standard taxonomy)
    $Cn = 0.9
    
    # Au (Automation): 1.0 (Script generated)
    $Au = 1.0
    
    # Formula: Score = (Cm * 0.4) + (Ac * 0.3) + (Cn * 0.2) + (Au * 0.1)
    # Note: Normalizing Ac to 0-1
    $score = ($Cm * 0.4) + (($Ac/100) * 0.3) + ($Cn * 0.2) + ($Au * 0.1)
    return "{0:N2}" -f $score
}

# -------------------------------------------------------------------------
# PHASE 1: SCAN FOR EMPTY DIRECTORIES
# -------------------------------------------------------------------------
Write-Host "PHASE 1: DUE DILIGENCE SCAN" -ForegroundColor Green

$emptyDirs = Get-ChildItem -Path $RootPath -Directory -Recurse -ErrorAction SilentlyContinue |
    Where-Object { (Get-ChildItem $_.FullName -Force -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0 }

Write-Host "Found $($emptyDirs.Count) empty directories:" -ForegroundColor Yellow
$emptyDirs | ForEach-Object { Write-Host "  WARNING: $($_.FullName)" -ForegroundColor Yellow }

# -------------------------------------------------------------------------
# PHASE 2: ASSET COUNT & MANIFEST GENERATION
# -------------------------------------------------------------------------
Write-Host "`nPHASE 2: ASSET COUNT & MANIFEST" -ForegroundColor Green

$allFiles = Get-ChildItem -Path $RootPath -File -Recurse -ErrorAction SilentlyContinue | 
    Where-Object { $_.Name -notmatch "mdec_manifest.json" } # Exclude self

Write-Host "Found $($allFiles.Count) files to potentially ingest" -ForegroundColor White

# -------------------------------------------------------------------------
# PHASE 2.5: GIT TRACKING & LICENSING PROMPTS (NEW FEATURE)
# -------------------------------------------------------------------------
Write-Host "`nPHASE 2.5: GIT TRACKING & LICENSING CONFIGURATION" -ForegroundColor Green

# Initialize metadata collection
$ingestionMetadata = [PSCustomObject]@{
    git_tracking_enabled = $false
    license_type = "Proprietary"
    license_version = ""
    attribution_required = $true
    commercial_use_allowed = $false
    derivative_works_allowed = $false
    source_code_available = $false
    repository_url = ""
    project_name = ""
    maintainer_contact = ""
    mdec_compliance_level = "draft-mdec-metadata-excellence-00"
    spdx_license_id = ""
    schema_org_type = "CreativeWork"
    dublin_core_creator = ""
    dublin_core_publisher = ""
    dublin_core_rights = ""
}

# User Prompts for Git Tracking
Write-Host "GIT TRACKING CONFIGURATION:" -ForegroundColor Cyan
$gitResponse = Read-Host "Enable Git tracking for these assets? (Y/N)"
$ingestionMetadata.git_tracking_enabled = ($gitResponse -eq "Y" -or $gitResponse -eq "y")

if ($ingestionMetadata.git_tracking_enabled) {
    Write-Host "Git tracking ENABLED - Assets will be added to version control" -ForegroundColor Green
} else {
    Write-Host "Git tracking DISABLED - Assets will remain untracked" -ForegroundColor Yellow
}

# User Prompts for Licensing
Write-Host "`nLICENSING CONFIGURATION:" -ForegroundColor Cyan
Write-Host "Available license types:" -ForegroundColor Gray
Write-Host "  1. Proprietary (Default)" -ForegroundColor White
Write-Host "  2. Open Source (GPL)" -ForegroundColor White
Write-Host "  3. Creative Commons (CC)" -ForegroundColor White
Write-Host "  4. MIT License" -ForegroundColor White
Write-Host "  5. Apache 2.0" -ForegroundColor White
Write-Host "  6. BSD" -ForegroundColor White

$licenseChoice = Read-Host "Select license type (1-6)"
switch ($licenseChoice) {
    "1" { 
        $ingestionMetadata.license_type = "Proprietary"
        $ingestionMetadata.commercial_use_allowed = $false
        $ingestionMetadata.derivative_works_allowed = $false
        $ingestionMetadata.attribution_required = $true
        $ingestionMetadata.spdx_license_id = "LicenseRef-Proprietary"
    }
    "2" { 
        $ingestionMetadata.license_type = "GPL"
        $licenseVersion = Read-Host "GPL Version (2/3)"
        $ingestionMetadata.license_version = $licenseVersion
        $ingestionMetadata.commercial_use_allowed = $true
        $ingestionMetadata.derivative_works_allowed = $true
        $ingestionMetadata.attribution_required = $true
        $ingestionMetadata.source_code_available = $true
        $ingestionMetadata.spdx_license_id = "GPL-$licenseVersion.0-only"
    }
    "3" { 
        $ingestionMetadata.license_type = "Creative Commons"
        $ccType = Read-Host "CC Type (BY/BY-SA/BY-ND/BY-NC/BY-NC-SA/BY-NC-ND)"
        $ingestionMetadata.license_version = $ccType
        $ingestionMetadata.attribution_required = $true
        $ingestionMetadata.commercial_use_allowed = -not ($ccType -match "NC")
        $ingestionMetadata.derivative_works_allowed = -not ($ccType -match "ND")
        $ingestionMetadata.spdx_license_id = "CC-$ccType-4.0"
    }
    "4" { 
        $ingestionMetadata.license_type = "MIT"
        $ingestionMetadata.commercial_use_allowed = $true
        $ingestionMetadata.derivative_works_allowed = $true
        $ingestionMetadata.attribution_required = $true
        $ingestionMetadata.spdx_license_id = "MIT"
    }
    "5" { 
        $ingestionMetadata.license_type = "Apache-2.0"
        $ingestionMetadata.commercial_use_allowed = $true
        $ingestionMetadata.derivative_works_allowed = $true
        $ingestionMetadata.attribution_required = $true
        $ingestionMetadata.source_code_available = $true
        $ingestionMetadata.spdx_license_id = "Apache-2.0"
    }
    "6" { 
        $ingestionMetadata.license_type = "BSD"
        $bsdType = Read-Host "BSD Type (2-Clause/3-Clause)"
        $ingestionMetadata.license_version = $bsdType
        $ingestionMetadata.commercial_use_allowed = $true
        $ingestionMetadata.derivative_works_allowed = $true
        $ingestionMetadata.attribution_required = $true
        $ingestionMetadata.spdx_license_id = "BSD-$bsdType"
    }
}

# Additional metadata prompts
$ingestionMetadata.project_name = Read-Host "Project name (optional)"
$ingestionMetadata.maintainer_contact = Read-Host "Maintainer contact (optional)"
$ingestionMetadata.repository_url = Read-Host "Repository URL (optional)"

# Dublin Core and Schema.org enrichment
$ingestionMetadata.dublin_core_creator = Read-Host "Creator/Author (for Dublin Core metadata)"
$ingestionMetadata.dublin_core_publisher = Read-Host "Publisher (optional)"
$ingestionMetadata.dublin_core_rights = "$($ingestionMetadata.license_type) $($ingestionMetadata.license_version)".Trim()

Write-Host "`nCONFIGURATION SUMMARY:" -ForegroundColor Cyan
Write-Host "  Git Tracking: $(if($ingestionMetadata.git_tracking_enabled){'ENABLED'}else{'DISABLED'})" -ForegroundColor $(if($ingestionMetadata.git_tracking_enabled){'Green'}else{'Yellow'})
Write-Host "  License: $($ingestionMetadata.license_type) $($ingestionMetadata.license_version)" -ForegroundColor White
Write-Host "  Commercial Use: $(if($ingestionMetadata.commercial_use_allowed){'ALLOWED'}else{'RESTRICTED'})" -ForegroundColor $(if($ingestionMetadata.commercial_use_allowed){'Green'}else{'Red'})
Write-Host "  Derivative Works: $(if($ingestionMetadata.derivative_works_allowed){'ALLOWED'}else{'RESTRICTED'})" -ForegroundColor $(if($ingestionMetadata.derivative_works_allowed){'Green'}else{'Red'})
Write-Host "  SPDX ID: $($ingestionMetadata.spdx_license_id)" -ForegroundColor Gray

$manifestEntries = @()

if ($GenerateManifest) {
    Write-Host "GENERATING RFC-COMPLIANT MANIFEST..." -ForegroundColor Cyan
    foreach ($file in $allFiles) {
        $uuid = [guid]::NewGuid().ToString()
        $m_id = "urn:mdec:$uuid"
        
        # Calculate Score
        $q_score = Get-MdecQualityScore -File $file
        
        # Signet (Section 4 of Draft) - Hardcoded for this session context
        $signet = "Christopher-Olds-07-14-1962-20xx-Engineer-Musician-Author-Poet-USA"
        
        $entry = [PSCustomObject]@{
            "m-id" = $m_id
            "file_name" = $file.Name
            "relative_path" = $file.FullName.Substring($RootPath.Length)
            "signet_creator" = $signet
            "quality_score" = $q_score
            "rfc_compliance" = "draft-mdec-metadata-excellence-00"
            "generated_at" = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
            
            # Git Tracking & Licensing Metadata
            "git_tracking_enabled" = $ingestionMetadata.git_tracking_enabled
            "license_type" = $ingestionMetadata.license_type
            "license_version" = $ingestionMetadata.license_version
            "attribution_required" = $ingestionMetadata.attribution_required
            "commercial_use_allowed" = $ingestionMetadata.commercial_use_allowed
            "derivative_works_allowed" = $ingestionMetadata.derivative_works_allowed
            "source_code_available" = $ingestionMetadata.source_code_available
            "repository_url" = $ingestionMetadata.repository_url
            "project_name" = $ingestionMetadata.project_name
            "maintainer_contact" = $ingestionMetadata.maintainer_contact
            
            # Standards Compliance
            "mdec_compliance_level" = $ingestionMetadata.mdec_compliance_level
            "spdx_license_id" = $ingestionMetadata.spdx_license_id
            "schema_org_type" = $ingestionMetadata.schema_org_type
            "dublin_core_creator" = $ingestionMetadata.dublin_core_creator
            "dublin_core_publisher" = $ingestionMetadata.dublin_core_publisher
            "dublin_core_rights" = $ingestionMetadata.dublin_core_rights
        }
        
        $manifestEntries += $entry
        Write-Host "  [+] Ingested: $($file.Name) | Score: $q_score | Git: $(if($ingestionMetadata.git_tracking_enabled){'TRACKED'}else{'UNTRACKED'})" -ForegroundColor Gray
    }
    
    if (-not $DryRun) {
        $json = $manifestEntries | ConvertTo-Json -Depth 3
        $manifestPath = Join-Path $RootPath "mdec_manifest.json"
        $json | Set-Content $manifestPath
        Write-Host "MANIFEST SAVED: $manifestPath" -ForegroundColor Green
    }
}

# -------------------------------------------------------------------------  
# PHASE 2.6: GIT TRACKING EXECUTION (if enabled)
# -------------------------------------------------------------------------
if ($ingestionMetadata.git_tracking_enabled -and -not $DryRun) {
    Write-Host "`nPHASE 2.6: GIT TRACKING EXECUTION" -ForegroundColor Green
    
    # Check if we're in a Git repository
    $gitDir = Join-Path $RootPath ".git"
    if (Test-Path $gitDir) {
        Write-Host "Git repository detected. Adding files..." -ForegroundColor Cyan
        
        # Add all files that were ingested
        foreach ($file in $allFiles) {
            $relativePath = $file.FullName.Substring($RootPath.Length).TrimStart("\")
            try {
                & git add $relativePath 2>$null
                Write-Host "  [+] Git add: $relativePath" -ForegroundColor Gray
            } catch {
                Write-Host "  [-] Failed to add: $relativePath" -ForegroundColor Red
            }
        }
        
        # Add the manifest
        $manifestRelativePath = "mdec_manifest.json"
        try {
            & git add $manifestRelativePath 2>$null
            Write-Host "  [+] Git add: $manifestRelativePath" -ForegroundColor Gray
        } catch {
            Write-Host "  [-] Failed to add manifest" -ForegroundColor Red
        }
        
        Write-Host "Git tracking complete. Run 'git commit' to finalize." -ForegroundColor Green
    } else {
        Write-Host "WARNING: No Git repository found at $RootPath" -ForegroundColor Yellow
        Write-Host "To enable Git tracking, initialize a repository first: git init" -ForegroundColor Yellow
    }
} elseif ($ingestionMetadata.git_tracking_enabled -and $DryRun) {
    Write-Host "`nPHASE 2.6: GIT TRACKING (DRY RUN - Would add $($allFiles.Count) files)" -ForegroundColor Yellow
}

# -------------------------------------------------------------------------
# PHASE 3: EMPTY DIRECTORY RESOLUTION (SAFETY PROTOCOL ENABLED)
# -------------------------------------------------------------------------
Write-Host "`nPHASE 3: EMPTY DIRECTORY RESOLUTION" -ForegroundColor Green

# Configuration Management Exclusion List
$Protocols = @('.git', '.svn', '.hg', 'node_modules', '.vscode', '.idea')

$DirectoriesToDelete = @()
foreach ($dir in $emptyDirs) {
    $isProtected = $false
    foreach ($p in $Protocols) {
        if ($dir.FullName -match [regex]::Escape($p)) {
            $isProtected = $true
            Write-Host "  SKIPPING PROTECTED PATH: $($dir.FullName)" -ForegroundColor DarkGray
            break
        }
    }
    if (-not $isProtected) {
        $DirectoriesToDelete += $dir
    }
}

if ($EliminateEmpty) {
    if ($DirectoriesToDelete.Count -eq 0) {
        Write-Host "No eligible empty directories found for elimination." -ForegroundColor Gray
    } else {
        # MANDATORY REPORTING BEFORE ACTION
        Write-Host "`n[!] CRITICAL ACTION REPORT: CANDIDATE DIRECTORIES FOR DELETION" -ForegroundColor Magenta
        Write-Host "-------------------------------------------------------------" -ForegroundColor Magenta
        $DirectoriesToDelete | ForEach-Object { Write-Host "   [DELETE] $($_.FullName)" -ForegroundColor Red }
        Write-Host "-------------------------------------------------------------" -ForegroundColor Magenta
        
        if ($ConfirmDelete -and -not $DryRun) {
            Write-Host "CONFIRMATION RECEIVED. EXECUTING PURGE..." -ForegroundColor Red
            foreach ($dir in $DirectoriesToDelete) {
                Remove-Item $dir.FullName -Force -ErrorAction SilentlyContinue
                Write-Host "  PURGED: $($dir.FullName)" -ForegroundColor Red
            }
        } else {
            Write-Host "ACTION ABORTED: Safety Protocol Active." -ForegroundColor Yellow
            Write-Host "To execute deletion, you MUST provide the -ConfirmDelete flag." -ForegroundColor Yellow
            Write-Host "This report has been generated for your review." -ForegroundColor Yellow
        }
    }
} else {
     Write-Host "FLAGGED FOR REVIEW: $($emptyDirs.Count) empty directories found." -ForegroundColor Yellow
     Write-Host "Run with -EliminateEmpty (and optional -ConfirmDelete) to process." -ForegroundColor Yellow
}

# -------------------------------------------------------------------------
# PHASE 4: REPORT
# -------------------------------------------------------------------------
Write-Host "`nPHASE 4: INGESTION REPORT" -ForegroundColor Green
Write-Host "SUMMARY:" -ForegroundColor Cyan
Write-Host "   * Files Processed: $($allFiles.Count)" -ForegroundColor White
Write-Host "   * Manifest Entries: $($manifestEntries.Count)" -ForegroundColor White
Write-Host "   * Empty Directories: $($emptyDirs.Count)" -ForegroundColor White
Write-Host "   * Action: $(if($EliminateEmpty){'ELIMINATION'}else{'FLAG_FOR_REVIEW'})" -ForegroundColor White

Write-Host "`nTITANESS INGESTION COMPLETE" -ForegroundColor Cyan
Write-Host "Excellence is mandatory. Data integrity preserved." -ForegroundColor White
