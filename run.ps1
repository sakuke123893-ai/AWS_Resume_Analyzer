# ============================================================
# AI Resume Intelligence — Quick Start Script
# Run this from the project root: .\run.ps1
# ============================================================

$envFile = Join-Path $PSScriptRoot ".env"

if (-not (Test-Path $envFile)) {
    Write-Host ""
    Write-Host "⚠️  No .env file found!" -ForegroundColor Yellow
    Write-Host "   Creating one now..." -ForegroundColor Gray
    Copy-Item (Join-Path $PSScriptRoot ".env.example") $envFile
    Write-Host ""
    Write-Host "👉  Please edit .env and add your GROQ_API_KEY:" -ForegroundColor Cyan
    Write-Host "   $envFile" -ForegroundColor White
    Write-Host ""
    Write-Host "   Get a free key at: https://console.groq.com" -ForegroundColor Green
    Write-Host ""
    exit 1
}

# Check if key is still the placeholder
$envContent = Get-Content $envFile -Raw
if ($envContent -match "your_groq_api_key_here") {
    Write-Host ""
    Write-Host "❌  GROQ_API_KEY is still set to the placeholder value." -ForegroundColor Red
    Write-Host "   Edit .env and paste your real API key." -ForegroundColor Yellow
    Write-Host "   Get a free key at: https://console.groq.com" -ForegroundColor Green
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "⚡  Starting AI Resume Intelligence..." -ForegroundColor Cyan
Write-Host "   Open your browser at: http://localhost:5000" -ForegroundColor Green
Write-Host "   Press Ctrl+C to stop." -ForegroundColor Gray
Write-Host ""

Set-Location (Join-Path $PSScriptRoot "backend")
python -m pip install -q -r requirements.txt
python app.py
