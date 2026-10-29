# Remove asci from Windows:
#   irm https://raw.githubusercontent.com/wetpant000/asci/main/uninstall.ps1 | iex
$ErrorActionPreference = 'Stop'
$dest = Join-Path $env:LOCALAPPDATA 'Programs\asci'
if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }

$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($userPath) {
    $kept = ($userPath -split ';') | Where-Object { $_ -and $_ -ne $dest }
    [Environment]::SetEnvironmentVariable('Path', ($kept -join ';'), 'User')
}
Write-Host 'asci removed.'
