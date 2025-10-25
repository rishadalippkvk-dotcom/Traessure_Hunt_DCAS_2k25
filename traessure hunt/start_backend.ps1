# 🚀 Start Django Backend Server
# This script starts the Django backend for FOSS Treasure Hunt

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "     🎮 FOSS TREASURE HUNT - Backend Server" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Change to backend directory
Write-Host "📁 Navigating to backend directory..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\backend"

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "❌ Virtual environment not found at .\venv\" -ForegroundColor Red
    Write-Host "💡 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install django djangorestframework django-cors-headers
}

# Check if database exists
if (Test-Path ".\treasure_hunt.db") {
    Write-Host "✅ Database found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database not found - running migrations..." -ForegroundColor Yellow
    python manage.py migrate
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "     🌐 Starting Django Server on http://localhost:8000" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "💡 Open http://localhost:8000/admin to access admin panel" -ForegroundColor Yellow
Write-Host ""

# Start Django server
python manage.py runserver
