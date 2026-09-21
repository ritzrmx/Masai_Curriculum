$ansi = [System.Text.Encoding]::GetEncoding(1252)
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$files = Get-ChildItem -Path E:\Masai\SME\IITP-GenAI-TA-I2606 -Include "mental-map*.md", "pre-read*.md" -Recurse

foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    if ($content.Contains([char]0x00F0) -or $content.Contains([char]0x00E2) -or $content.Contains([char]0x00C3)) {
        Write-Host "Fixing $($file.Name)"
        $bytes = $ansi.GetBytes($content)
        $fixedContent = $utf8NoBom.GetString($bytes)
        [System.IO.File]::WriteAllText($file.FullName, $fixedContent, $utf8NoBom)
    }
}
