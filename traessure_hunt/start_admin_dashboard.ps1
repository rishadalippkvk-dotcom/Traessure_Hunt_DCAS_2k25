# Admin Dashboard Startup Script
# Starts the admin monitoring dashboard

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   FOSS Treasure Hunt - Admin Dashboard" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if required packages are installed
Write-Host "Checking dependencies..." -ForegroundColor Green

# Install all required packages from requirements file
if (Test-Path "streamlit_requirements.txt") {
    Write-Host "Installing packages from streamlit_requirements.txt..." -ForegroundColor Yellow
    pip install -r streamlit_requirements.txt
} else {
    # Fallback to individual package installation
    $packages = @("streamlit", "pandas", "plotly")
    $missing = @()

    foreach ($package in $packages) {
        $installed = pip show $package 2>$null
        if (-not $installed) {
            $missing += $package
        }
    }

    if ($missing.Count -gt 0) {
        Write-Host "Missing packages: $($missing -join ', ')" -ForegroundColor Red
        Write-Host "Installing required packages..." -ForegroundColor Yellow
        pip install $missing
    }
}

Write-Host "All dependencies installed!" -ForegroundColor Green
Write-Host ""

# Check if users.json exists
if (-not (Test-Path "users.json")) {
    Write-Host "Warning: users.json not found!" -ForegroundColor Yellow
    Write-Host "Creating empty users.json..." -ForegroundColor Yellow
    '{"users": []}' | Out-File -FilePath "users.json" -Encoding utf8
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Admin Dashboard..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default Admin Password: admin123" -ForegroundColor Yellow
Write-Host "Please change this in production!" -ForegroundColor Red
Write-Host ""
Write-Host "Dashboard will open at: http://localhost:8503" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the dashboard" -ForegroundColor Gray
Write-Host ""

# Get the full path to the admin dashboard file
$dashboardPath = Join-Path $PSScriptRoot "admin_dashboard.py"

# Start the dashboard on port 8503 (to avoid conflict with main game and other services)
streamlit run $dashboardPath --server.port 8503