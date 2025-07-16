# CSC2103 Data Structure and Algorithm Assignment

## Recommedned Python Version Manager

1. Use pyenv to manage your Python versions

To install [pyenv](https://github.com/pyenv-win/pyenv-win) on Windows use in Powershell:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

On other Operating Systems, follow the [guide here](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).

2. Download version 3.12.9

```bash
pyenv install 3.12.9
```

3. Use the installed python version

```bash
pyenv global 3.12.9
```

4. Test your python version

```bash
python --version
```

## Setup

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
