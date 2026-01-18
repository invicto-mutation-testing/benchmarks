[CmdletBinding()]
param(
    [ValidateRange(1, 1000000)]
    [int]$Count = 1,

    [string]$RepoRoot = ".",

    [string]$EnvPath = ".venv-invicto",

    [string]$Requirements = "requirements-invicto.txt",

    [string]$AggregatePattern = "benchmark_results_*.csv",

    [string]$AggregateStem = "benchmark_results",

    [string]$DatasetOutput = "benchmark_dataset.csv",

    [string]$AnalysisScript = "scripts/run_statistical_analysis.R",

    [int]$BootstrapSamples = 100000,

    [double]$Alpha = 0.05,

    [switch]$SkipInitialClean,

    [switch]$GenerateShapiroTable
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-FullPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BasePath,
        [Parameter(Mandatory = $true)]
        [string]$Path
    )
    if ([string]::IsNullOrWhiteSpace($Path)) {
        throw "Path parameter cannot be empty."
    }
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }
    return [System.IO.Path]::GetFullPath((Join-Path -Path $BasePath -ChildPath $Path))
}

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][scriptblock]$Action
    )
    Write-Host "=== $Name ===" -ForegroundColor Cyan
    & $Action
    Write-Host "=== Completed: $Name ===" -ForegroundColor Green
}

if ($RepoRoot -eq "." -and $PSScriptRoot) {
    $repoRootFull = $PSScriptRoot
} else {
    $repoRootFull = [System.IO.Path]::GetFullPath($RepoRoot)
}
if (-not (Test-Path -LiteralPath $repoRootFull -PathType Container)) {
    throw "Repository root '$repoRootFull' does not exist."
}

$scriptsRelativeRoot = "scripts"

$setupScript = Resolve-FullPath -BasePath $repoRootFull -Path (Join-Path -Path $scriptsRelativeRoot -ChildPath "create_python_venv.ps1")
$cleanScript = Resolve-FullPath -BasePath $repoRootFull -Path (Join-Path -Path $scriptsRelativeRoot -ChildPath "remove_mutation_caches.ps1")
$loopScript = Resolve-FullPath -BasePath $repoRootFull -Path (Join-Path -Path $scriptsRelativeRoot -ChildPath "run_mutmut_iterations.ps1")
$aggregateScript = Resolve-FullPath -BasePath $repoRootFull -Path (Join-Path -Path $scriptsRelativeRoot -ChildPath "compute_benchmark_statistics.py")
$analysisScriptFull = Resolve-FullPath -BasePath $repoRootFull -Path $AnalysisScript
$baselineCsv = Resolve-FullPath -BasePath $repoRootFull -Path "baseline.csv"

foreach ($required in @($setupScript, $cleanScript, $loopScript, $aggregateScript, $analysisScriptFull, $baselineCsv)) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Required file '$required' was not found."
    }
}

$envFullPath = Resolve-FullPath -BasePath $repoRootFull -Path $EnvPath
$requirementsFull = Resolve-FullPath -BasePath $repoRootFull -Path $Requirements
$tempResultsFull = Resolve-FullPath -BasePath $repoRootFull -Path "temp_results"
if (-not (Test-Path -LiteralPath $tempResultsFull)) {
    New-Item -Path $tempResultsFull -ItemType Directory | Out-Null
}
$datasetFull = Resolve-FullPath -BasePath $tempResultsFull -Path $DatasetOutput
$rscriptCommand = $null
try {
    $rscriptCommand = Get-Command -Name "Rscript" -ErrorAction Stop
} catch {
    throw "Rscript.exe was not found on the PATH. Install R for Windows (4.4.2 per manuscript) and ensure Rscript.exe is reachable."
}


Push-Location -LiteralPath $repoRootFull
try {
    Invoke-Step "Create/refresh .venv-invicto environment" {
        & $setupScript -EnvPath $EnvPath -Requirements $Requirements
    }

    $venvPython = Resolve-FullPath -BasePath $repoRootFull -Path (Join-Path -Path $EnvPath -ChildPath "Scripts/python.exe")
    $venvPip = Resolve-FullPath -BasePath $repoRootFull -Path (Join-Path -Path $EnvPath -ChildPath "Scripts/pip.exe")

    foreach ($exe in @($venvPython, $venvPip)) {
        if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) {
            throw "Expected executable '$exe' was not found."
        }
    }

    Invoke-Step "Install aggregation dependencies (numpy, pandas)" {
        & $venvPip install --upgrade numpy pandas
    }

    if (-not $SkipInitialClean) {
        Invoke-Step "Initial cache clean" {
            & $cleanScript
        }
    }

    Invoke-Step "Run replicated mutmut benchmark loop ($Count iteration(s))" {
        & $loopScript -Count $Count -OutputDir $tempResultsFull
    }

    Invoke-Step "Aggregate replicated CSVs" {
        Push-Location $tempResultsFull
        try {
            & $venvPython $aggregateScript --pattern $AggregatePattern --out-stem $AggregateStem
        } finally {
            Pop-Location
        }
        
        # Move the final median CSV to the project root as requested
        $medianFile = Join-Path $tempResultsFull "${AggregateStem}_medians.csv"
        if (Test-Path $medianFile) {
            Move-Item -Path $medianFile -Destination $repoRootFull -Force
        }
    }

    $medianFileRoot = Resolve-FullPath -BasePath $repoRootFull -Path "${AggregateStem}_medians.csv"
    if (-not (Test-Path -LiteralPath $medianFileRoot)) {
        throw "Median benchmark CSV '$medianFileRoot' was not found."
    }

    $datasetColumns = @(
        "put",
        "api_mode",
        "temperature",
        "repetition_id",
        "duration_seconds",
        "file_size_bytes",
        "killed_mutations",
        "all_mutations",
        "score",
        "actual_test_path"
    )

    $requiredMedianColumns = @(
        "put",
        "api_mode",
        "temperature",
        "repetition_id",
        "duration_seconds",
        "file_size_bytes",
        "killed_medians",
        "all_medians",
        "score_medians",
        "actual_test_path"
    )

    Invoke-Step "Build semicolon-delimited dataset ($DatasetOutput)" {
        $medianRows = Import-Csv -LiteralPath $medianFileRoot

        foreach ($col in $requiredMedianColumns) {
            if (-not ($medianRows | Get-Member -Name $col)) {
                throw "Column '$col' is missing from $medianFileRoot. Ensure it was produced by compute_benchmark_statistics.py."
            }
        }

        $medianRows = $medianRows | ForEach-Object {
            if ($_.put) { $_.put = $_.put.ToUpperInvariant() }
            $_
        }

        $datasetRows = $medianRows | Select-Object `
            put, api_mode, temperature, repetition_id, duration_seconds, file_size_bytes, `
            @{Name = "killed_mutations"; Expression = { [double]$_.killed_medians } }, `
            @{Name = "all_mutations"; Expression = { [double]$_.all_medians } }, `
            @{Name = "score"; Expression = { [double]$_.score_medians } }, `
            actual_test_path

        $datasetRows | Select-Object $datasetColumns |
            Export-Csv -LiteralPath $datasetFull -Delimiter ';' -NoTypeInformation -Encoding UTF8
    }

    Invoke-Step "Run statistical analysis (run_statistical_analysis.R)" {
        $datasetArg = "--data=$datasetFull"
        $nbootArg = "--nboot=$BootstrapSamples"
        $alphaArg = "--alpha=$Alpha"
        $argsList = @($datasetArg, $nbootArg, $alphaArg)
        if (-not $GenerateShapiroTable) {
            $argsList += "--no-shapiro-tex"
        }
        & $rscriptCommand.Source $analysisScriptFull $argsList
    }

    Write-Host "`nPipeline completed successfully." -ForegroundColor Green
    Write-Host "Key outputs:" -ForegroundColor Green
    Write-Host " - Raw benchmark CSVs: temp_results\${AggregateStem}_<iteration>.csv"
    Write-Host " - Intermediate Aggregations: temp_results\${AggregateStem}_{means,stds,aggregated}.csv"
    Write-Host " - Final Median Scores: ${AggregateStem}_medians.csv"
    Write-Host " - Dataset for R: temp_results\$DatasetOutput"

    $artifacts = "statistical_analysis.json"
    if ($GenerateShapiroTable) {
        $artifacts += ", generated\tbl_shapiro.tex"
    }
    Write-Host " - Analysis artifacts: $artifacts"
}
finally {
    Pop-Location
}
