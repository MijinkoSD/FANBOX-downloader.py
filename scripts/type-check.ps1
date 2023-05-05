Set-Location (Join-Path -Path $PSScriptRoot -ChildPath "/../")
python -m mypy --no-incremental --strict --show-column-numbers ./ --exclude "local_files/.+"
