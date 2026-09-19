# Downloads the images and CV from the current WordPress site into assets/.
# Run once from this folder in PowerShell:  .\fetch-assets.ps1
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path "assets\img" | Out-Null
$files = @{
  "assets\img\livermore.jpg"    = "https://michaellivermore.com/wp-content/uploads/2025/12/livermore.jpg?w=1600"
  "assets\img\reviving.png"     = "https://michaellivermore.com/wp-content/uploads/2020/08/9780197539446.png"
  "assets\img\lawasdata.png"    = "https://michaellivermore.com/wp-content/uploads/2020/08/030619_lad_paperback_front.png"
  "assets\img\globalization.png"= "https://michaellivermore.com/wp-content/uploads/2020/08/9780199934386.png"
  "assets\img\retaking.png"     = "https://michaellivermore.com/wp-content/uploads/2020/08/9780195368574.png"
  "assets\img\podcast.jpg"      = "https://michaellivermore.com/wp-content/uploads/2021/12/podcastlogo3.jpg?w=800"
  "assets\livermore-cv.pdf"     = "https://michaellivermore.com/wp-content/uploads/2025/12/livermore-cv-20252.pdf"
}
foreach ($k in $files.Keys) { Invoke-WebRequest -Uri $files[$k] -OutFile $k; Write-Host "saved $k" }
