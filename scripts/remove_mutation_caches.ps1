param(
    [switch]$DryRun,
    [switch]$Force
)

# Remove cache directories from assistant/ and completions/ trees.
# Safety check: requires baseline.csv in repo root unless -Force is provided.
# Usage: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\remove_mutation_caches.ps1 [-DryRun] [-Force]

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$repoRoot = Resolve-Path (Join-Path -Path $scriptRoot -ChildPath "..")

$markerFile = Join-Path -Path $repoRoot -ChildPath "baseline.csv"
if (-not (Test-Path -LiteralPath $markerFile) -and -not $Force) {
    throw "Safety check failed: baseline.csv not found under '$repoRoot'. Re-run with -Force to override."
}

$roots = @(
    (Join-Path -Path $repoRoot -ChildPath "assistant"),
    (Join-Path -Path $repoRoot -ChildPath "completions")
)

# Mirror bash script behavior: fail if any root is missing.
foreach ($r in $roots) {
    if (-not (Test-Path -LiteralPath $r)) {
        throw "Root not found: $r"
    }
}

function Test-IsUnderRoots {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string[]]$RootPrefixes
    )
    foreach ($root in $RootPrefixes) {
        if ($Path.StartsWith($root, [StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }
    return $false
}

function Get-CacheTargets {
    param(
        [Parameter(Mandatory = $true)][string[]]$RootPaths
    )
    $targets = New-Object System.Collections.Generic.List[System.IO.FileSystemInfo]
    $stack = New-Object System.Collections.Generic.Stack[string]
    foreach ($root in $RootPaths) {
        $rootItem = Get-Item -LiteralPath $root -Force -ErrorAction Stop
        if ($rootItem.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            Write-Warning ("Skipping reparse-point root: {0}" -f $rootItem.FullName)
            continue
        }
        $stack.Push($root)
    }

    while ($stack.Count -gt 0) {
        $current = $stack.Pop()
        $entries = Get-ChildItem -LiteralPath $current -Force -ErrorAction Stop
        foreach ($entry in $entries) {
            if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                continue
            }
            if ($entry.PSIsContainer) {
                if ($entry.Name -eq '.pytest_cache' -or $entry.Name -eq '__pycache__') {
                    $targets.Add($entry)
                } else {
                    $stack.Push($entry.FullName)
                }
            } elseif ($entry.Name -eq '.mutmut-cache') {
                $targets.Add($entry)
            }
        }
    }
    return $targets
}

$rootPrefixes = foreach ($root in $roots) {
    $full = (Resolve-Path -LiteralPath $root).Path
    if ($full.EndsWith([IO.Path]::DirectorySeparatorChar)) {
        $full
    } else {
        $full + [IO.Path]::DirectorySeparatorChar
    }
}

# Find targets:
#  - files named '.mutmut-cache'
#  - directories named '.pytest_cache' or '__pycache__'
$items = Get-CacheTargets -RootPaths $roots

if ($DryRun) {
    if (-not $items) {
        Write-Host '[DRY-RUN] No matching cache files/directories found.'
    } else {
        foreach ($it in $items) {
            if (-not (Test-IsUnderRoots -Path $it.FullName -RootPrefixes $rootPrefixes)) {
                Write-Warning ("[DRY-RUN] Skipping unexpected path outside roots: {0}" -f $it.FullName)
                continue
            }
            Write-Host ("[DRY-RUN] Would remove: {0}" -f $it.FullName)
        }
    }
} else {
    # Remove them (equivalent to: xargs -0r rm -rf). If none matched, do nothing and exit 0.
    foreach ($it in $items) {
        if (-not (Test-IsUnderRoots -Path $it.FullName -RootPrefixes $rootPrefixes)) {
            Write-Warning ("Skipping unexpected path outside roots: {0}" -f $it.FullName)
            continue
        }
        Remove-Item -LiteralPath $it.FullName -Recurse -Force -ErrorAction Stop
    }
}

exit 0
