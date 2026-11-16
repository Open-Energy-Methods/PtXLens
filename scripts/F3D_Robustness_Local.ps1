# F3-D observed-year controlled robustness / independent LP cost-bound research.
# PowerShell 5.1; all provider original hourly arrays and counterfactual
# 8760/8784-hour primal witnesses are PRIVATE outside both Git repositories.
# No Actions minutes, Copernicus or ENTSO-E network downloads required.
[CmdletBinding()]
param(
 [ValidateSet("Test","Status","IndependentLP","SolvePair","ReviewPair","Consolidate","IndependentWindFeasibility")]
 [string]$Phase="Test",
 [ValidateSet(2022,2024)]
 [int]$Year=2022,
 [ValidateSet("max_inventory","usable_service")]
 [string]$Mode="max_inventory",
 [ValidateSet("price_roll_168h","price_spread_150pct",
              "wind_power_090","wind_power_110_capped")]
 [string]$Variant="price_roll_168h",
 [ValidateRange(30,14400)]
 [int]$DispatchTimeLimit=3600,
 [ValidateRange(10,7200)]
 [int]$LPTimeLimit=900,
 [string]$FlexRoot=(Join-Path $PSScriptRoot "..\..\PtXFlex"),
 [string]$PrivateRoot=(Join-Path $HOME "PtX_PRIVATE_RESEARCH")
)
Set-StrictMode -Version Latest
$ErrorActionPreference="Stop"
$LensRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$FlexRoot=[IO.Path]::GetFullPath($FlexRoot)
$PrivateRoot=[IO.Path]::GetFullPath($PrivateRoot)
$python=Join-Path $FlexRoot ".venv\Scripts\python.exe"
$publicSource=Join-Path $FlexRoot "research\F3D_ARCO_2022_2024_PUBLIC_VERIFIED_AGGREGATES_v1.json"
$publicResults=Join-Path $LensRoot "data\results"
$lpOutput=Join-Path $publicResults ("F3D_LP_{0}_{1}_independent_relaxed_cost_KKT_NOT_mip_tree.json" -f $Year,$Mode)
$pairOutput=Join-Path $publicResults ("F3D_CF_{0}_{1}_{2}_INDEPENDENT_PUBLIC_REPLAY.json" -f $Year,$Mode,$Variant)
$windLPOutput=Join-Path $publicResults ("F3D_WIND_090_{0}_{1}_INDEPENDENT_SOURCE_LP_FEASIBILITY_v1.json" -f $Year,$Mode)
function Need([bool]$ok,[string]$errorMessage) {
  if(-not $ok){ throw $errorMessage }
}
function Run([string]$exe,[string[]]$argumentList) {
  & $exe @argumentList
  if($LASTEXITCODE -ne 0){ throw ("F3D robustness local command failed with exit {0}" -f $LASTEXITCODE) }
}
Need (Test-Path -LiteralPath $python -PathType Leaf) "PtXFlex virtualenv Python missing"
Need (Test-Path -LiteralPath $publicSource -PathType Leaf) "PtXFlex public source-verified year model JSON missing"
Need (Test-Path -LiteralPath $publicResults -PathType Container) "PtXLens public data/results directory missing"
if($Phase -eq "Status") {
  Write-Host ("Original local private research archive present: {0}" -f (Test-Path -LiteralPath $PrivateRoot -PathType Container))
  Write-Host ("Source-year LP review output exists: {0}" -f (Test-Path -LiteralPath $lpOutput -PathType Leaf))
  Write-Host ("Controlled pair independently reviewed output exists: {0}" -f (Test-Path -LiteralPath $pairOutput -PathType Leaf))
  Write-Host ("Independent wind-power feasibility review exists: {0}" -f (Test-Path -LiteralPath $windLPOutput -PathType Leaf))
  foreach($case in @("E","E_plus_S")){
    $p=Join-Path $PrivateRoot ("results\counterfactuals\PRIVATE_F3D_CF_{0}_{1}_{2}_{3}.json" -f $Year,$Mode,$Variant,$case)
    Write-Host ("PRIVATE source model {0} result exists: {1}" -f $case,(Test-Path -LiteralPath $p -PathType Leaf))
  }
  Write-Host "Status lists file presence ONLY; it is not a valid mathematical/physical acceptance certificate"
  return
}
if($Phase -eq "Test") {
  Run $python @("-m","pytest","-q",
    (Join-Path $FlexRoot "tests\test_f3d_external_year_controlled_counterfactual.py"),
    (Join-Path $LensRoot "tests\test_f3d_source_year_independent_cost_lp_dual.py"),
    (Join-Path $LensRoot "tests\test_f3d_lp_cf_public_consolidation.py"),
    (Join-Path $LensRoot "tests\test_f3d_wind_reduction_independent_feasibility.py"))
  Write-Host "Hermetic scientific regression tests completed; original provider-year MILPs NOT run"
  return
}
Need (Test-Path -LiteralPath $PrivateRoot -PathType Container) "Original private source archive missing"
if($Phase -eq "IndependentLP"){
  # Locally reconstruct independently from scratch the original price/wind/H2
  # physical LP relaxation. KKT pass is NOT a HiGHS integer search proof.
  Run $python @("-m","ptxlens.f3d_source_year_independent_cost_lp_dual",
    "--year","$Year","--mode",$Mode,
    "--private-root",$PrivateRoot,
    "--public-source",$publicSource,
    "--LP-time-limit","$LPTimeLimit",
    "--output",$lpOutput)
  Write-Host ("Independent source-year relaxed LP result saved: {0}" -f $lpOutput)
  return
}
if($Phase -eq "IndependentWindFeasibility"){
  Need ($Variant -eq "wind_power_090") "IndependentWindFeasibility is only preregistered for wind_power_090; use -Variant wind_power_090"
  Need (Test-Path -LiteralPath $pairOutput -PathType Leaf) "Run -Phase SolvePair and -Phase ReviewPair on wind_power_090 before independent feasibility"
  Run $python @("-m","ptxlens.f3d_wind_reduction_independent_feasibility",
    "--year","$Year","--mode",$Mode,
    "--private-root",$PrivateRoot,
    "--public-source",$publicSource,
    "--LP-time-limit","$LPTimeLimit",
    "--output",$windLPOutput)
  Write-Host ("Independently reconstructed E infeasible LP / E+S feasible constraint audit saved: {0}" -f $windLPOutput)
  Write-Host "SOURCE ORIGINAL E/E+S MATCHED SERVICE COST SAVING IS NULL, not 0"
  return
}
if($Phase -eq "Consolidate"){
  Need (Test-Path -LiteralPath $lpOutput -PathType Leaf) "Independent KKT LP review JSON missing; run -Phase IndependentLP"
  Need (Test-Path -LiteralPath $pairOutput -PathType Leaf) "Independent original-hour price/wind reviewer JSON missing; run -Phase ReviewPair"
  Run $python @("-m","ptxlens.f3d_lp_cf_public_consolidation",
    "--original-public-source",$publicSource,
    "--lp-review",$lpOutput,
    "--counterfactual-review",$pairOutput,
    "--output-dir",$publicResults)
  Write-Host "Original independent KKT-LP saving interval and controlled price/wind result condensed into public 2-file report"
  Write-Host "Inspect generated F3D_*_LP_CF_PUBLIC_v1 JSON+MD; DO NOT stage private source/witness folders"
  return
}
if($Phase -eq "SolvePair"){
  foreach($case in @("E","E_plus_S")){
    # Independent PRIVATE source/checks. A crash/non-certified MILP does not
    # overwrite successful prior individual case. Two modes/years are separate.
    Run $python @("-m","ptxflex.f3d_external_year_controlled_counterfactual",
      "--year","$Year","--mode",$Mode,"--variant",$Variant,
      "--case",$case,"--private-root",$PrivateRoot,
      "--source",$publicSource,"--time-limit","$DispatchTimeLimit")
  }
  Write-Host "Both original modeled source cases are saved PRIVATELY; NOT YET independent PtXLens-reviewed"
  return
}
if($Phase -eq "ReviewPair"){
  Run $python @("-m","ptxlens.f3d_external_year_counterfactual_independent_review",
    "--year","$Year","--mode",$Mode,"--variant",$Variant,
    "--private-root",$PrivateRoot,
    "--public-source",$publicSource,"--output",$pairOutput)
  Write-Host ("Only sanitized independently physically replayed pair result saved: {0}" -f $pairOutput)
  Write-Host "Do not publish private hourly source or witness archives"
  return
}
throw "unrecognized F3-D local robustness phase"
