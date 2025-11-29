# PowerShell helper to create and activate a virtual environment named .venv, upgrade pip, and install requirements
# Usage (PowerShell):
#   .\setup_venv.ps1

$venvPath = "$PWD\.venv"

Write-Host "Creating virtual environment at: $venvPath"
python -m venv $venvPath

# Activate the venv for the current session
$activateScript = Join-Path $venvPath 'Scripts\Activate.ps1'
if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment"
    & $activateScript
} else {
    Write-Warning "Activate script not found at $activateScript. You can activate manually: .\.venv\Scripts\Activate.ps1"
}

# Upgrade pip and install requirements
Write-Host "Upgrading pip and installing requirements"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "Virtual environment setup complete. To activate in a new session run: .\.venv\Scripts\Activate.ps1"
