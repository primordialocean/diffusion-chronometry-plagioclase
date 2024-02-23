# Get the path to the Activate.ps1 script inside the venv directory
$venvPath = "~\venv\Scripts\Activate.ps1"

# Check if the Activate.ps1 script exists
if (Test-Path $venvPath) {
    . $venvPath
    Write-Host "Virtual environment activated."
} else {
    Write-Host "Virtual environment not found."
}
python interpolation.py
python preprocessor.py
python diffmodel.py
python fitting.py
python plotter.py

Write-Host "Calculation completed."