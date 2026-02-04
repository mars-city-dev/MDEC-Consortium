# MDEC Implementation Example
# This script demonstrates how to implement MDEC standards in your organization

# Step 1: Import MDEC Toolkit
Import-Module ".\Core\MDEC_Metadata_Extractor.psm1"
Import-Module ".\Validation\MDEC_Validation_Toolkit.psm1"

# Step 2: Extract metadata from your files
$metadataPath = ".\metadata_database.json"
Extract-Metadata -Path "C:\Your\Documents" -OutputPath $metadataPath

# Step 3: Validate compliance
$compliance = Test-MDECCompliance -MetadataPath $metadataPath

Write-Host "MDEC Compliance Results:" -ForegroundColor Cyan
Write-Host "Schema Compliance: $($compliance.SchemaCompliance)"
Write-Host "Quality Score: $($compliance.QualityScore)%"
Write-Host "Certification Level: $($compliance.CertificationLevel)"

# Step 4: Apply AI automation (if available)
if (Test-Path ".\Core\MDEC_Phase3_Orchestrator.psm1") {
    Import-Module ".\Core\MDEC_Phase3_Orchestrator.psm1"
    Start-MDECAIAutomation -MetadataPath $metadataPath -FullCycle
}
