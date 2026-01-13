# MDEC Standards Validation Toolkit
Import-Module ".\Core\MDEC_Validation_Engine.psm1"

function Test-MDECCompliance {
    param([string]$MetadataPath)

    Write-Host "🔍 Validating MDEC Standards Compliance..." -ForegroundColor Cyan

    $results = Test-MetadataDatabase -MetadataPath $MetadataPath -ReportOnly

    $compliance = @{
        SchemaCompliance = ($results.invalid -eq 0)
        QualityScore = [math]::Round((($results.valid / ($results.valid + $results.invalid)) * 100), 1)
        TotalEntries = $results.valid + $results.invalid
        ValidEntries = $results.valid
        InvalidEntries = $results.invalid
    }

    # Determine certification level
    if ($compliance.QualityScore -ge 100 -and $compliance.SchemaCompliance) {
        $compliance.CertificationLevel = "Gold"
    } elseif ($compliance.QualityScore -ge 80 -and $compliance.SchemaCompliance) {
        $compliance.CertificationLevel = "Silver"
    } elseif ($compliance.QualityScore -ge 50) {
        $compliance.CertificationLevel = "Bronze"
    } else {
        $compliance.CertificationLevel = "Not Certified"
    }

    return $compliance
}

# Export function
Export-ModuleMember -Function Test-MDECCompliance
