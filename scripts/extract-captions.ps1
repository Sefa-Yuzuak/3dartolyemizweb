# Bir kerelik dev script: Instagram veri export JSON'undan (content/aciklamar.txt.json)
# medya dosya adi -> gonderi metni (caption) eslemesini cikarir ve mojibake (UTF-8 -> Latin1
# cift kodlama) hatasini duzeltir. Siteye dahil degildir, sadece gallery.js uretiminde
# yardimci veri olarak kullanilir.

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$jsonPath = Join-Path $root "content\aciklamar.txt.json"
$outPath = Join-Path $root "scripts\captions-report.txt"

function Fix-Mojibake([string]$s) {
    if ([string]::IsNullOrEmpty($s)) { return $s }
    $bytes = New-Object byte[] $s.Length
    for ($i = 0; $i -lt $s.Length; $i++) {
        $bytes[$i] = [byte]([int]$s[$i] -band 0xFF)
    }
    return [System.Text.Encoding]::UTF8.GetString($bytes)
}

$data = Get-Content -Raw -Path $jsonPath | ConvertFrom-Json
$posts = $data.organic_insights_posts

$rows = @()
foreach ($post in $posts) {
    foreach ($prop in $post.media_map_data.PSObject.Properties) {
        $media = $prop.Value
        $uri = $media.uri
        $file = Split-Path -Leaf $uri
        $captionRaw = $media.title
        $caption = Fix-Mojibake $captionRaw
        $rows += [PSCustomObject]@{ file = $file; caption = $caption; ts = $media.creation_timestamp }
    }
}

$sb = New-Object System.Text.StringBuilder
foreach ($r in ($rows | Sort-Object ts)) {
    [void]$sb.AppendLine("FILE: $($r.file)")
    [void]$sb.AppendLine("CAPTION: $($r.caption)")
    [void]$sb.AppendLine("---")
}
[System.IO.File]::WriteAllText($outPath, $sb.ToString(), (New-Object System.Text.UTF8Encoding($false)))
Write-Output "Yazildi: $outPath ($($rows.Count) kayit)"
