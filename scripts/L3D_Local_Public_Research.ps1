# Windows PowerShell 5.1/7, no GitHub Actions minutes or private market inputs.
# Run inside PtXLens sibling checkout with PtXFlex installed Python env.
[CmdletBinding()]
param(
 [ValidateSet("Test","Produce","Status")]
 [string]$Phase="Test",
 [string]$LensRoot=(Join-Path $PSScriptRoot ".."),
 [string]$FlexRoot=(Join-Path $PSScriptRoot "..\..\PtXFlex")
)
Set-StrictMode -Version Latest
$ErrorActionPreference="Stop"
$LensRoot=[IO.Path]::GetFullPath($LensRoot)
$FlexRoot=[IO.Path]::GetFullPath($FlexRoot)
$python=Join-Path $FlexRoot ".venv\Scripts\python.exe"
function Need([bool]$ok,[string]$message) {
  if(-not $ok){throw $message}
}
function Run([string]$exe,[string[]]$arguments) {
  & $exe @arguments
  if($LASTEXITCODE -ne 0){throw "L3D local scientific job failed (exit $LASTEXITCODE)"}
}
$source=Join-Path $FlexRoot "research\F3D_ARCO_2022_2024_PUBLIC_VERIFIED_AGGREGATES_v1.json"
$out=Join-Path $LensRoot "data\results"
$dcf=Join-Path $out "L3_D_2022_2024_historical_DCF_frontiers_NOT_site_NPV.json"
$report=Join-Path $out "L3_D_2022_2024_historical_DCF_frontiers_NOT_site_NPV.md"
$bafu=Join-Path $out "L3_D_BAFU2026_native_incremental_stationary_TypeI_MAPPING_BLOCKED_v1.json"
Need (Test-Path $python -PathType Leaf) "PtXFlex local venv missing: install PtXFlex+PtXLens editable first"
Need (Test-Path $source -PathType Leaf) "PtXFlex verified public 2022/2024 JSON missing: git pull both repositories"
Need (Test-Path $out -PathType Container) "PtXLens data/results folder missing; do not create arbitrary output paths"
if($Phase -eq "Status") {
  Write-Host "PtXFlex public original aggregate available: $([bool](Test-Path $source))"
  Write-Host "Source-year conditional L3D DCF output exists: $([bool](Test-Path $dcf))"
  Write-Host "L3D BAFU native inventory NEGATIVE admission ledger exists: $([bool](Test-Path $bafu))"
  Write-Host "DCF output markdown exists: $([bool](Test-Path $report))"
  Write-Host "These existence flags DO NOT certify native LCIA, model dual proof or commercial v1"
  return
}
Run $python @("-m","pytest","-q",
  (Join-Path $FlexRoot "tests\test_f3d_historical_source_report.py"),
  (Join-Path $LensRoot "tests\test_l3d_historical_source_dcf.py"),
  (Join-Path $LensRoot "tests\test_l3d_bafu_incremental_inventory_gate.py"))
Write-Host "LOCAL HERMETIC SCIENTIFIC TESTS PASSED; source Git SHA, equations and scope gates verified"
if($Phase -eq "Test"){return}
Run $python @("-m","ptxlens.l3d_historical_source_dcf",
  "--source",$source,"--output-dir",$out)
Run $python @("-m","ptxlens.l3d_bafu_incremental_inventory_gate",
  "--output",$bafu)
Write-Host "L3-D four source-year scenario results + 324 parameter cells EXPORTED; native BAFU provider LCIA STILL BLOCKED"
Write-Host "Inspect only these three files before explicit git add:"
Write-Host $dcf
Write-Host $report
Write-Host $bafu
