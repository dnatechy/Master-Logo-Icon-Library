$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$rows = Get-ChildItem $Root -Recurse -File | Where-Object { $_.Extension -match '^\.(svg|png|webp|jpg|jpeg)$' } | ForEach-Object {
  [pscustomobject]@{
    Name=$_.BaseName
    FileName=$_.Name
    RelativePath=$_.FullName.Substring($Root.Length+1)
    Extension=$_.Extension.TrimStart('.')
  }
}
$rows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path (Join-Path $Root "Icon_Index.csv")
Write-Host "Index refreshed: $($rows.Count) files"
