# 🎨 Start Streamlit Frontend
# This script starts the Streamlit frontend for FOSS Treasure Hunt

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "     🎮 FOSS TREASURE HUNT - Frontend App" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if Streamlit is installed
Write-Host "🔍 Checking for Streamlit..." -ForegroundColor Yellow
$streamlitCheck = python -c "import streamlit" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Streamlit not found" -ForegroundColor Red
    Write-Host "📦 Installing Streamlit..." -ForegroundColor Yellow
    pip install streamlit requests
} else {
    Write-Host "✅ Streamlit is installed" -ForegroundColor Green
}

# Check if final2.py exists
if (Test-Path ".\final2.py") {
    Write-Host "✅ Application file found" -ForegroundColor Green
} else {
    Write-Host "❌ final2.py not found in current directory!" -ForegroundColor Red
    Write-Host "💡 Make sure you're in the correct directory" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "     🌐 Starting Streamlit App on http://localhost:8501" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Make sure Django backend is running on port 8000!" -ForegroundColor Yellow
Write-Host "💡 Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host "💡 The app will open automatically in your browser" -ForegroundColor Yellow
Write-Host ""

# Start Streamlit
streamlit run final2.py
