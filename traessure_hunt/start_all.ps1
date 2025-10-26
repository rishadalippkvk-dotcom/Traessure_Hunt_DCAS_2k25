# 🚀 Start Both Backend and Frontend Servers
# This script starts both the Django backend and Streamlit frontend

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "     🎮 FOSS TREASURE HUNT - Complete Setup" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Start backend in background
Write-Host "🔄 Starting Django Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python manage.py runserver" -WindowStyle Normal

# Wait a few seconds for backend to start
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start frontend
Write-Host "🎨 Starting Streamlit Frontend..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot"
streamlit run final2.py

Write-Host ""
Write-Host "✅ Both servers should now be running!" -ForegroundColor Green
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""