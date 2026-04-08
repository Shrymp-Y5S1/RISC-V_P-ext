param(
    [string]$Seed = "20260405",
    [int]$RandomPerSeed = 200,
    [string]$CasesOut = "cases/week1_seed20260405.json",
    [string]$ExpectedOut = "expected/week1_seed20260405.expected.json",
    [string]$RawActualIn = "",
    [string]$ActualIn = "actual/week1_seed20260405.actual.json",
    [string]$DiffOut = "reports/diff-week1.csv",
    [string]$DiffSummaryOut = "reports/diff-week1-summary.md"
)

Write-Host "[1/3] 生成样例"
python scripts/gen_cases.py --out $CasesOut --seeds $Seed --random-per-seed $RandomPerSeed
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[2/3] 生成期望"
python scripts/model_eval.py --cases $CasesOut --out $ExpectedOut
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (-not (Test-Path $ActualIn) -and $RawActualIn -and (Test-Path $RawActualIn)) {
    Write-Host "[3/4] 转换原始输出为 actual"
    python scripts/build_actual_from_raw.py --raw $RawActualIn --out $ActualIn
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

if (-not (Test-Path $ActualIn)) {
    Write-Host "[3/4] 跳过差分：未找到 actual 文件 -> $ActualIn"
    if ($RawActualIn) {
        Write-Host "RawActualIn 已提供但未找到 -> $RawActualIn"
    }
    Write-Host "请先导出 ISS/DUT 结果，或传入 -RawActualIn <raw.csv|raw.txt|raw.json>"
    exit 0
}

Write-Host "[4/4] 对拍差分 + 归因摘要"
python scripts/diff.py --expected $ExpectedOut --actual $ActualIn --out $DiffOut
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python scripts/summarize_diff.py --diff $DiffOut --out $DiffSummaryOut
exit $LASTEXITCODE
