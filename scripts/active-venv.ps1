if (!(Test-Path ".\.venv\Scripts\activate")) {
    python3.11 -m venv .venv
}
&".\.venv\Scripts\activate"

python -m pip install -U pip
pip install -r .\requirements.txt
