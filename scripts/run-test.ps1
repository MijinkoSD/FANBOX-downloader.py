Set-Location (Join-Path -Path $PSScriptRoot -ChildPath "/../")
python -m unittest discover -s src/test_py -p test_*.py
