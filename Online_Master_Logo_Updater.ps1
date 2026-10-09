# Master Logo/Icon Library Online Updater
# Run from inside Master_Logo_Icon_Library.
# Adds/updates files; does NOT delete your existing files.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Brand = Join-Path $Root "Brand_Logos"

$Dirs = @{
  Raw = Join-Path $Brand "00_Raw_Source"
  Black = Join-Path $Brand "01_Transparent_Black"
  White = Join-Path $Brand "02_Transparent_White"
  CircleBlue = Join-Path $Brand "03_Circle_Blue"
  CircleDark = Join-Path $Brand "04_Circle_Dark"
  SquareBlue = Join-Path $Brand "05_Rounded_Square_Blue"
  SquareDark = Join-Path $Brand "06_Rounded_Square_Dark"
}
$Dirs.Values | ForEach-Object { New-Item -ItemType Directory -Force -Path $_ | Out-Null }

$Blue = "#0B63CE"
$Dark = "#082B62"
$Temp = Join-Path $env:TEMP ("MasterLogoUpdate_" + [guid]::NewGuid())
New-Item -ItemType Directory -Force -Path $Temp | Out-Null

function Get-ViewBox([string]$Svg) {
  $m = [regex]::Match($Svg, 'viewBox\s*=\s*["'']([^"'']+)["'']', 'IgnoreCase')
  if ($m.Success) { return $m.Groups[1].Value }
  return "0 0 24 24"
}
function Get-Inner([string]$Svg) {
  $s = [regex]::Replace($Svg, '^\s*<\?xml[^>]*\?>\s*', '', 'IgnoreCase')
  $m = [regex]::Match($s, '<svg\b[^>]*>(.*)</svg>\s*$', 'IgnoreCase,Singleline')
  if ($m.Success) { return $m.Groups[1].Value }
  return $s
}
function Recolor-Inner([string]$Inner,[string]$Color) {
  $style = "<style>path,rect,circle,ellipse,polygon,polyline,line{fill:$Color!important;stroke:$Color!important}[fill=`"none`"]{fill:none!important}</style>"
  return $style + $Inner
}
function Make-Transparent([string]$Svg,[string]$Color) {
  $vb=Get-ViewBox $Svg; $inner=Recolor-Inner (Get-Inner $Svg) $Color
  return "<svg xmlns=`"http://www.w3.org/2000/svg`" viewBox=`"$vb`">$inner</svg>"
}
function Make-Framed([string]$Svg,[string]$Bg,[string]$Shape) {
  $vb=Get-ViewBox $Svg; $inner=Recolor-Inner (Get-Inner $Svg) "#FFFFFF"
  if($Shape -eq "circle"){$base="<circle cx=`"32`" cy=`"32`" r=`"30`" fill=`"$Bg`"/>"}
  else{$base="<rect x=`"2`" y=`"2`" width=`"60`" height=`"60`" rx=`"12`" fill=`"$Bg`"/>"}
  return "<svg xmlns=`"http://www.w3.org/2000/svg`" viewBox=`"0 0 64 64`">$base<svg x=`"14`" y=`"14`" width=`"36`" height=`"36`" viewBox=`"$vb`">$inner</svg></svg>"
}
function Save-Logo([string]$Slug,[string]$Svg) {
  $Slug = $Slug.ToLower() -replace '[^a-z0-9]+','-'
  $Slug = $Slug.Trim('-')
  Set-Content -LiteralPath (Join-Path $Dirs.Raw "${Slug}__logo__raw-source.svg") -Value $Svg -Encoding UTF8
  Set-Content -LiteralPath (Join-Path $Dirs.Black "${Slug}__logo__transparent-black.svg") -Value (Make-Transparent $Svg "#000000") -Encoding UTF8
  Set-Content -LiteralPath (Join-Path $Dirs.White "${Slug}__logo__transparent-white.svg") -Value (Make-Transparent $Svg "#FFFFFF") -Encoding UTF8
  Set-Content -LiteralPath (Join-Path $Dirs.CircleBlue "${Slug}__logo__circle-blue.svg") -Value (Make-Framed $Svg $Blue "circle") -Encoding UTF8
  Set-Content -LiteralPath (Join-Path $Dirs.CircleDark "${Slug}__logo__circle-dark.svg") -Value (Make-Framed $Svg $Dark "circle") -Encoding UTF8
  Set-Content -LiteralPath (Join-Path $Dirs.SquareBlue "${Slug}__logo__square-blue.svg") -Value (Make-Framed $Svg $Blue "square") -Encoding UTF8
  Set-Content -LiteralPath (Join-Path $Dirs.SquareDark "${Slug}__logo__square-dark.svg") -Value (Make-Framed $Svg $Dark "square") -Encoding UTF8
}

try {
  Write-Host ""
  Write-Host "=== 1/3: Downloading latest Simple Icons collection ===" -ForegroundColor Cyan
  $siZip = Join-Path $Temp "simple-icons.zip"
  Invoke-WebRequest -Uri "https://github.com/simple-icons/simple-icons/archive/refs/heads/develop.zip" -OutFile $siZip
  $siOut = Join-Path $Temp "simple-icons"
  Expand-Archive -LiteralPath $siZip -DestinationPath $siOut -Force
  $iconDir = Get-ChildItem $siOut -Directory -Recurse | Where-Object { $_.Name -eq "icons" } | Select-Object -First 1
  if(-not $iconDir){ throw "Could not find Simple Icons 'icons' folder." }
  $icons = Get-ChildItem $iconDir.FullName -Filter *.svg
  $i=0
  foreach($f in $icons){
    $i++
    if(($i % 200) -eq 0){Write-Host "  Processed $i / $($icons.Count) brand logos..."}
    $svg = Get-Content -LiteralPath $f.FullName -Raw
    Save-Logo $f.BaseName $svg
  }
  Write-Host "  Added/updated $($icons.Count) searchable brand logos." -ForegroundColor Green

  Write-Host ""
  Write-Host "=== 2/3: Updating exact Microsoft Power BI / Power Automate / Power Query vectors ===" -ForegroundColor Cyan
  $msZip = Join-Path $Temp "PowerBI-Icons.zip"
  Invoke-WebRequest -Uri "https://github.com/microsoft/PowerBI-Icons/archive/refs/heads/main.zip" -OutFile $msZip
  $msOut = Join-Path $Temp "PowerBI-Icons"
  Expand-Archive -LiteralPath $msZip -DestinationPath $msOut -Force
  $wanted = @{
    "Power-BI.svg"=@("power-bi","powerbi","microsoft-power-bi");
    "Power-Automate-Colored.svg"=@("power-automate","powerautomate","microsoft-power-automate");
    "Power-Query-Colored.svg"=@("power-query","powerquery","microsoft-power-query")
  }
  foreach($pair in $wanted.GetEnumerator()){
    $file = Get-ChildItem $msOut -Filter $pair.Key -Recurse | Select-Object -First 1
    if($file){
      $svg = Get-Content -LiteralPath $file.FullName -Raw
      foreach($alias in $pair.Value){ Save-Logo $alias $svg }
      Write-Host "  Updated $($pair.Key)"
    }
  }

  Write-Host ""
  Write-Host "=== 3/3: Updating Google Apps Script vector ===" -ForegroundColor Cyan
  try {
    $gas = Join-Path $Temp "Google_Apps_Script.svg"
    Invoke-WebRequest -Uri "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_Apps_Script.svg" -OutFile $gas
    $svg = Get-Content -LiteralPath $gas -Raw
    @("google-apps-script","googleappsscript","apps-script") | ForEach-Object { Save-Logo $_ $svg }
    Write-Host "  Updated Google Apps Script." -ForegroundColor Green
  } catch {
    Write-Warning "Google Apps Script direct download skipped: $($_.Exception.Message)"
  }

  # Refresh CSV index as a convenience. The new Search_Icons.html does not depend on it.
  $rows = Get-ChildItem $Root -Recurse -File | Where-Object { $_.Extension -match '^\.(svg|png|webp|jpg|jpeg)$' } | ForEach-Object {
    [pscustomobject]@{
      Name=$_.BaseName
      FileName=$_.Name
      RelativePath=$_.FullName.Substring($Root.Length+1)
      Extension=$_.Extension.TrimStart('.')
    }
  }
  $rows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path (Join-Path $Root "Icon_Index.csv")
  Write-Host ""
  Write-Host "DONE. Search page will discover the new files after Refresh Library." -ForegroundColor Green
  Write-Host "Total image files now: $($rows.Count)"
}
finally {
  Remove-Item -LiteralPath $Temp -Recurse -Force -ErrorAction SilentlyContinue
}
