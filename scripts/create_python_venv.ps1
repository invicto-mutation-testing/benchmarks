[CmdletBinding()]
param(
    [string]$EnvPath = ".venv-invicto",
    [string]$Requirements = "requirements-invicto.txt"
)

$ErrorActionPreference = "Stop"

$pythonVersion = (python --version 2>$null).Split()[1]
if (-not $pythonVersion.StartsWith('3.10')) {
    throw "Python 3.10 is required. Detected: $pythonVersion"
}

if (-not (Test-Path -LiteralPath $Requirements)) {
    throw "Requirements file '$Requirements' was not found."
}

python -m venv $EnvPath

$venvPython = Join-Path $EnvPath "Scripts/python.exe"
$venvPip = Join-Path $EnvPath "Scripts/pip.exe"

& $venvPython -m pip install --upgrade pip
& $venvPip install --requirement $Requirements

Write-Host "Environment created at $EnvPath" -ForegroundColor Green
Write-Host "Activate it with:`n`t& `"$EnvPath\Scripts\Activate.ps1`"" -ForegroundColor Yellow
