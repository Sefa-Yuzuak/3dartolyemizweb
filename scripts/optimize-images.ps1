# Bir kerelik dev script: assets/img/_raw icindeki ham Instagram medyalarini
# WebP'e cevirir (max 1200px genislik, kalite ~80, EXIF temizlenir, sRGB).
# Siteye dahil degildir; sadece bu donusumu calistirmak icin kullanilir.
# Video dosyalari (.mp4/.mov) atlanir.

$ErrorActionPreference = "Stop"
$magick = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
$root = Split-Path -Parent $PSScriptRoot
$rawDir = Join-Path $root "assets\img\_raw"
$outDir = Join-Path $root "assets\img"
$manifestPath = Join-Path $root "scripts\image-manifest.csv"

$files = Get-ChildItem -Path $rawDir -File |
    Where-Object { $_.Extension -match '(?i)^\.(jpg|jpeg|png|heic|webp)$' } |
    Sort-Object Name

$rows = @()
$i = 0
foreach ($f in $files) {
    $i++
    $outName = "is-{0:D2}.webp" -f $i
    $outPath = Join-Path $outDir $outName

    & $magick $f.FullName -auto-orient -strip -colorspace sRGB -resize "1200x1200>" -quality 80 $outPath
    if ($LASTEXITCODE -ne 0) { throw "magick failed on $($f.Name)" }

    $dims = & $magick identify -format "%wx%h" $outPath
    $w, $h = $dims -split "x"

    $rows += [PSCustomObject]@{ index = $i; out = $outName; raw = $f.Name; w = [int]$w; h = [int]$h }
    Write-Output "$($f.Name) -> $outName ($($w)x$($h))"
}

$rows | Export-Csv -Path $manifestPath -NoTypeInformation -Encoding UTF8
Write-Output "Manifest: $manifestPath ($($rows.Count) gorsel)"
