Set-Location (Join-Path -Path $PSScriptRoot -ChildPath "/../")
python -m unittest discover -s test -p test_*.py
