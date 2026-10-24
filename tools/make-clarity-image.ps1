# Draws images\clarity.png (920x430) in the same style as the other store images: a diagonal gradient, the plugin
# name in Segoe UI Semibold and one line underneath. Uses the in-box System.Drawing.
Add-Type -AssemblyName System.Drawing
$root = Split-Path -Parent $PSScriptRoot
$w, $h = 920, 430
$bmp = New-Object System.Drawing.Bitmap $w, $h
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = 'AntiAlias'
$g.TextRenderingHint = 'AntiAliasGridFit'
$rect = New-Object System.Drawing.Rectangle 0, 0, $w, $h
$brush = New-Object System.Drawing.Drawing2D.LinearGradientBrush $rect, ([System.Drawing.Color]::FromArgb(18, 20, 26)), ([System.Drawing.Color]::FromArgb(20, 120, 170)), 25.0
$g.FillRectangle($brush, $rect)
$fmt = New-Object System.Drawing.StringFormat
$fmt.Alignment = 'Center'
$title = New-Object System.Drawing.Font 'Segoe UI Semibold', 54
$sub = New-Object System.Drawing.Font 'Segoe UI', 25
$g.DrawString('Clarity', $title, [System.Drawing.Brushes]::White, (New-Object System.Drawing.RectangleF 0, 140, $w, 100), $fmt)
$subBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(215, 225, 232))
$g.DrawString('FSR 4 Lite and frame generation', $sub, $subBrush, (New-Object System.Drawing.RectangleF 0, 245, $w, 50), $fmt)
$out = Join-Path $root 'images\clarity.png'
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
$out
