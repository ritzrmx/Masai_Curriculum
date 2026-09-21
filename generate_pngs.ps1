$files = Get-ChildItem -Path . -Filter "mental-map*.md" -Recurse
foreach ($file in $files) {
    $outPng = $file.FullName -replace '\.md$', '.png'
    $outSvg = $file.FullName -replace '\.md$', '.svg'
    $tempPng = $file.FullName -replace '\.md$', '-1.png'
    $tempSvg = $file.FullName -replace '\.md$', '-1.svg'
    
    Write-Host "Generating PNG for $($file.Name)..."
    npx -y @mermaid-js/mermaid-cli@latest -i "$($file.FullName)" -o "$outPng" -s 5 -b white
    if (Test-Path $tempPng) {
        Move-Item -Path $tempPng -Destination $outPng -Force
    }
    
    Write-Host "Generating SVG for $($file.Name)..."
    npx -y @mermaid-js/mermaid-cli@latest -i "$($file.FullName)" -o "$outSvg" -b white
    if (Test-Path $tempSvg) {
        Move-Item -Path $tempSvg -Destination $outSvg -Force
    }
}
Write-Host "Done!"
