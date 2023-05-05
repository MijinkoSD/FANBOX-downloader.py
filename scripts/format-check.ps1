Set-Location (Join-Path -Path $PSScriptRoot -ChildPath "/../")
python -m flake8 --extend-exclude ".venv, .mypy_cache"
