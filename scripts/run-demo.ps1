# Run demo - backend and frontend (Windows PowerShell)
# Access from this machine: http://localhost:3000
# Access from Ubuntu laptop: http://<this-machine-ip>:3000

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Write-Host "Starting Construction AI Suite Demo..."
Write-Host "Backend: http://0.0.0.0:8000"
Write-Host "Frontend: http://0.0.0.0:3000"
Write-Host ""

# Backend
$backend = Start-Process -FilePath "python" -ArgumentList "run.py" -WorkingDirectory "$Root\backend" -PassThru -NoNewWindow
Start-Sleep -Seconds 3

# Frontend
$frontend = Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory "$Root\frontend" -PassThru -NoNewWindow

Write-Host "Demo running. Press Ctrl+C to stop."
Write-Host "From Ubuntu: http://$(hostname):3000 or your Windows IP"
try { $backend.WaitForExit() } catch { }
try { $frontend.WaitForExit() } catch { }
