$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$passwordFile = Join-Path $projectRoot '.tools/db-password.local'
if (-not (Test-Path -LiteralPath $passwordFile)) {
    throw 'Run scripts/setup-local-database.ps1 first to configure your local database.'
}
$jdk = Get-ChildItem -LiteralPath (Join-Path $projectRoot '.tools') -Directory -Filter 'jdk-*' | Select-Object -First 1
if (-not $jdk) { throw 'The project-local Java toolchain is missing.' }
$env:JAVA_HOME = $jdk.FullName
$env:DB_USER = 'foodbridge'
$env:DB_URL = 'jdbc:mysql://127.0.0.1:3306/foodbridge?connectionTimeZone=UTC'
$passwordBytes = [Security.Cryptography.ProtectedData]::Unprotect(
    [Convert]::FromBase64String([IO.File]::ReadAllText($passwordFile)), $null,
    [Security.Cryptography.DataProtectionScope]::CurrentUser)
try {
    $env:DB_PASSWORD = [Text.Encoding]::UTF8.GetString($passwordBytes)
    Write-Host 'Starting FoodBridge backend. Keep this window open.' -ForegroundColor Green
    & (Join-Path $projectRoot '.tools/apache-maven-3.9.11/bin/mvn.cmd') -f backend/pom.xml "-Dmaven.repo.local=$projectRoot/.tools/m2" spring-boot:run
    if ($LASTEXITCODE -ne 0) { throw 'Backend startup failed. See the message above.' }
} finally {
    Remove-Item Env:DB_PASSWORD -ErrorAction SilentlyContinue
    [Array]::Clear($passwordBytes, 0, $passwordBytes.Length)
}
