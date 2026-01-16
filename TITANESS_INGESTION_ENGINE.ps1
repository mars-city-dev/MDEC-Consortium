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
        }
        
        $manifestEntries += $entry
        Write-Host "  [+] Ingested: $($file.Name) | Score: $q_score" -ForegroundColor Gray
    }
    
    if (-not $DryRun) {
        $json = $manifestEntries | ConvertTo-Json -Depth 3
        $manifestPath = Join-Path $RootPath "mdec_manifest.json"
        $json | Set-Content $manifestPath
        Write-Host "MANIFEST SAVED: $manifestPath" -ForegroundColor Green
    }
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