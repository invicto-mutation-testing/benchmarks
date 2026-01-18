Param(
  [Parameter(Mandatory = $true, Position = 0)]
  [ValidateRange(1, 1000000)]
  [int]$Count,

  [string]$OutputDir = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Running mutmut benchmark $Count time(s) ..." -ForegroundColor Cyan

# Prefer venv python if available
$RepoRoot = (Get-Item $PSScriptRoot).Parent.FullName
$VenvPython = Join-Path -Path $RepoRoot -ChildPath ".venv-invicto\Scripts\python.exe"
$PythonExe = if (Test-Path -LiteralPath $VenvPython) { $VenvPython } else { "python" }

for ($i = 1; $i -le $Count; $i++) {
  $outFile = Join-Path -Path $OutputDir -ChildPath "benchmark_results_$i.csv"
  Write-Host "[$i/$Count] Building $outFile" -ForegroundColor Green

  $argList = @(
    "$PSScriptRoot\run_single_mutation_test.py",
    "--python-hash-seed", "0",
    "--repo-root", ".",
    "--venv-path", ".venv-invicto",
    "--output-path", $outFile,
    "--mutmut-timeout-seconds", "300",
    "-j", "8"
  )

  Write-Host "[$i/$Count] Start-Process: $PythonExe $($argList -join ' ')" -ForegroundColor DarkGray
  $proc = Start-Process -FilePath $PythonExe -ArgumentList $argList -NoNewWindow -Wait -PassThru
  if ($null -eq $proc) { throw "Failed to start python process at iteration $i" }
  $exitCode = $proc.ExitCode
  if ($null -eq $exitCode) { $exitCode = 0 }
  if ($exitCode -ne 0) {
    throw "run_single_mutation_test.py failed with exit code $exitCode at iteration $i"
  }

  Write-Host "[$i/$Count] Cleaning caches ..." -ForegroundColor Yellow
  & "$PSScriptRoot\remove_mutation_caches.ps1"
  if ($LASTEXITCODE -ne 0) {
    throw "remove_mutation_caches.ps1 failed with exit code $LASTEXITCODE at iteration $i"
  }
}

Write-Host "Done. Created $Count CSV file(s)." -ForegroundColor Cyan
