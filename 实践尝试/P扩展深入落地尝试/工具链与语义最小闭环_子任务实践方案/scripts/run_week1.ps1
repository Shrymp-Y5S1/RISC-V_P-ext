param(
    [string]$Seed = "20260405",
    [int]$RandomPerSeed = 200,
    [string]$CasesOut = "cases/week1_seed20260405.json",
    [string]$ExpectedOut = "expected/week1_seed20260405.expected.json",
    [string]$ActualIn = "actual/week1_seed20260405.actual.json",
    [string]$DiffOut = "reports/diff-week1.csv"
)

Write-Host "[1/3] 生成样例"
python scripts/gen_cases.py --out $CasesOut --seeds $Seed --random-per-seed $RandomPerSeed
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[2/3] 生成期望"
python scripts/model_eval.py --cases $CasesOut --out $ExpectedOut
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[3/3] 对拍差分"
python scripts/diff.py --expected $ExpectedOut --actual $ActualIn --out $DiffOut
exit $LASTEXITCODE
