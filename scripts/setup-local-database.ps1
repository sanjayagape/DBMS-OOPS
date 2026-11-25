$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$mysql = 'C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe'
$passwordFile = Join-Path $projectRoot '.tools/db-password.local'
if (Test-Path -LiteralPath $passwordFile) {
    Write-Host 'Local database credentials already exist. Starting the backend.'
    & (Join-Path $PSScriptRoot 'start-backend.ps1')
    exit
}
Write-Host 'FoodBridge database setup' -ForegroundColor Green
Write-Host 'Enter the MySQL ROOT password you chose during installation at the prompt below.'
Write-Host 'The root password will not be saved. Typing may be hidden.'
$randomBytes = New-Object byte[] 32
$rng = [Security.Cryptography.RandomNumberGenerator]::Create()
try { $rng.GetBytes($randomBytes) } finally { $rng.Dispose() }
$appPassword = -join ($randomBytes | ForEach-Object { $_.ToString('x2') })
$protectedPassword = [Security.Cryptography.ProtectedData]::Protect(
    [Text.Encoding]::UTF8.GetBytes($appPassword), $null,
    [Security.Cryptography.DataProtectionScope]::CurrentUser)
$pendingPasswordFile = Join-Path $projectRoot '.tools/db-password.pending.local'
[IO.File]::WriteAllText($pendingPasswordFile, [Convert]::ToBase64String($protectedPassword))
$sql = @"
CREATE DATABASE IF NOT EXISTS foodbridge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'foodbridge'@'localhost' IDENTIFIED BY '$appPassword';
ALTER USER 'foodbridge'@'localhost' IDENTIFIED BY '$appPassword';
GRANT ALL PRIVILEGES ON foodbridge.* TO 'foodbridge'@'localhost';
"@
$sql | & $mysql -u root -p --connect-timeout=10
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Database setup did not complete. Send the error message to Codex, without your password.' -ForegroundColor Red
    exit 1
}
Move-Item -LiteralPath $pendingPasswordFile -Destination $passwordFile -Force
$appPassword = $null
$sql = $null
$frontendEnv = Join-Path $projectRoot '.env.local'
if (Test-Path -LiteralPath $frontendEnv) {
    $content = Get-Content -LiteralPath $frontendEnv -Raw
    if ($content -match '(?m)^VITE_API_MODE=') { $content = $content -replace '(?m)^VITE_API_MODE=.*$', 'VITE_API_MODE=backend' }
    else { $content += "`r`nVITE_API_MODE=backend`r`n" }
    Set-Content -LiteralPath $frontendEnv -Value $content
} else { Set-Content -LiteralPath $frontendEnv -Value 'VITE_API_MODE=backend' }
Write-Host 'Database created. App credentials are encrypted for your Windows account.' -ForegroundColor Green
& (Join-Path $PSScriptRoot 'start-backend.ps1')
