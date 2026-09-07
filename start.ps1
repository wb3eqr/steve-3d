# Steve Minecraft PNG — PowerShell запуск
$port = 8000
$dir = $PSScriptRoot
Set-Location $dir
Write-Host "=== Steve Minecraft PNG — локалка ===" -ForegroundColor Green

# Проверка python
$py = $null
if (Get-Command python -ErrorAction SilentlyContinue) { $py = "python" }
elseif (Get-Command py -ErrorAction SilentlyContinue) { $py = "py" }
else { Write-Host "Python не найден!" -ForegroundColor Red; pause; exit 1 }

# Проверка порта
$busy = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($busy) {
  Write-Host "Порт $port уже занят — открываю сайт..." -ForegroundColor Yellow
} else {
  Write-Host "[1/3] Запускаю $py -m http.server $port ..."
  Start-Process $py -ArgumentList "-m","http.server","$port" -WindowStyle Normal
  Start-Sleep -Seconds 2
}

Write-Host "[3/3] Открываю браузер..."
Start-Process "http://localhost:$port/3d.html"
Start-Process "http://localhost:$port/index.html"

Write-Host "ГОТОВО! http://localhost:$port/3d.html" -ForegroundColor Green
Write-Host "Для остановки закрой окно сервера"
