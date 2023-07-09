Set-Location (Join-Path -Path $PSScriptRoot -ChildPath "/../")
Write-Host "-----------------------" -ForegroundColor Blue
Write-Host "venvを開始します。" -ForegroundColor Blue
Write-Host "-----------------------" -ForegroundColor Blue
. (Join-Path -Path $PSScriptRoot -ChildPath "/active-venv.ps1")

Write-Host "-----------------------" -ForegroundColor Blue
Write-Host "型チェックを開始します。" -ForegroundColor Blue
Write-Host "-----------------------" -ForegroundColor Blue
. (Join-Path -Path $PSScriptRoot -ChildPath "/type-check.ps1")

Write-Host "-----------------------" -ForegroundColor Blue
Write-Host "単体テストを開始します。" -ForegroundColor Blue
Write-Host "-----------------------" -ForegroundColor Blue
. (Join-Path -Path $PSScriptRoot -ChildPath "/run-test.ps1")

Write-Host "-----------------------" -ForegroundColor Blue
Write-Host "フォーマットチェックを開始します。" -ForegroundColor Blue
Write-Host "-----------------------" -ForegroundColor Blue
. (Join-Path -Path $PSScriptRoot -ChildPath "/format-check.ps1")

Write-Host "-----------------------" -ForegroundColor Blue
Write-Host "venvを終了します。" -ForegroundColor Blue
Write-Host "-----------------------" -ForegroundColor Blue
. (Join-Path -Path $PSScriptRoot -ChildPath "/deactive-venv.ps1")

Write-Host "-----------------------" -ForegroundColor Blue
Write-Host "終了しました。" -ForegroundColor Green
