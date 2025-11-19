param(
  [string[]]$Branches = @("main"),
  [int]$IntervalSeconds = 120,
  [switch]$NotifyOnly
)

$inside = git rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not a git repo"; exit 1 }

function GetCurrentBranch {
  git rev-parse --abbrev-ref HEAD
}

while ($true) {
  git fetch --prune origin | Out-Null
  $current = GetCurrentBranch
  foreach ($b in $Branches) {
    $counts = git rev-list --left-right --count "$b...origin/$b"
    $parts = $counts -split "\s+"
    $localAhead = [int]$parts[0]
    $remoteAhead = [int]$parts[1]
    if ($remoteAhead -gt 0) {
      if ($NotifyOnly -or $b -ne $current) {
        Write-Host "origin/$b ahead by $remoteAhead commit(s)"
      } else {
        Write-Host "origin/$b ahead by $remoteAhead commit(s). Pulling..."
        git pull --rebase --autostash
      }
    } else {
      Write-Host "No remote changes for $b"
    }
  }
  Start-Sleep -Seconds $IntervalSeconds
}