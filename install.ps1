# Install asci on Windows (no admin needed):
#
#   irm https://raw.githubusercontent.com/wetpant000/asci/main/install.ps1 | iex
#
# or from a clone of the repo:   powershell -ExecutionPolicy Bypass -File install.ps1
#
# Uses Python if it is installed; otherwise downloads the standalone asci.exe.
# Installs the commands `asci` and `asi` into %LOCALAPPDATA%\Programs\asci
# and adds that folder to your user PATH.
$ErrorActionPreference = 'Stop'
$repo = 'wetpant000/asci'
$dest = Join-Path $env:LOCALAPPDATA 'Programs\asci'
New-Item -ItemType Directory -Force -Path $dest | Out-Null

function Find-Python {
    # The Microsoft Store "python" stub doesn't run code, so test each candidate.
    $candidates = @(@('py', '-3'), @('python'), @('python3'))
    foreach ($c in $candidates) {
        if (-not (Get-Command $c[0] -ErrorAction SilentlyContinue)) { continue }
        try {
            $exe = $c[0]
            $pyArgs = @($c | Select-Object -Skip 1) + @('-c', 'import sys; print(sys.version_info[0])')
            $out = & $exe @pyArgs 2>$null
            if ($LASTEXITCODE -eq 0 -and "$out".Trim() -eq '3') { return ($c -join ' ') }
        } catch { }
    }
    return $null
}

# Remove any previous install so the .exe and .cmd versions never clash.
Remove-Item -Force -ErrorAction SilentlyContinue `
    (Join-Path $dest 'asci.exe'), (Join-Path $dest 'asi.exe'),
    (Join-Path $dest 'asci.cmd'), (Join-Path $dest 'asi.cmd'), (Join-Path $dest 'asci.py')

$python = Find-Python
if ($python) {
    $script = Join-Path $dest 'asci.py'
    if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot 'asci.py'))) {
        Copy-Item (Join-Path $PSScriptRoot 'asci.py') $script
    } else {
        Invoke-WebRequest "https://raw.githubusercontent.com/$repo/main/asci.py" -OutFile $script -UseBasicParsing
    }
    $launcher = "@echo off`r`n$python `"%~dp0asci.py`" %*`r`n"
    foreach ($name in 'asci', 'asi') {
        [IO.File]::WriteAllText((Join-Path $dest "$name.cmd"), $launcher)
    }
    Write-Host "Installed asci (using $python) to $dest"
} else {
    Write-Host 'Python not found - downloading standalone asci.exe ...'
    $exe = Join-Path $dest 'asci.exe'
    Invoke-WebRequest "https://github.com/$repo/releases/latest/download/asci.exe" -OutFile $exe -UseBasicParsing
    Copy-Item $exe (Join-Path $dest 'asi.exe')
    Write-Host "Installed asci.exe to $dest"
}

$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if (-not $userPath) { $userPath = '' }
if (($userPath -split ';') -notcontains $dest) {
    $newPath = (($userPath.TrimEnd(';'), $dest) | Where-Object { $_ }) -join ';'
    [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
    Write-Host 'Added to your PATH. Open a new terminal if the command is not found.'
}
if (($env:Path -split ';') -notcontains $dest) { $env:Path += ";$dest" }

Write-Host 'Try:  asci cat   or   asi dog'
