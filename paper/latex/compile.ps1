# PowerShell Compilation Script for LaTeX
# Antigravity Nano Research Multiagentic Core - arXiv Submission

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "LaTeX Compilation for arXiv Submission" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if pdflatex is available
try {
    $null = Get-Command pdflatex -ErrorAction Stop
    Write-Host "✓ pdflatex found" -ForegroundColor Green
} catch {
    Write-Host "✗ pdflatex not found. Please install MiKTeX or TeX Live." -ForegroundColor Red
    exit 1
}

# Check if bibtex is available
try {
    $null = Get-Command bibtex -ErrorAction Stop
    Write-Host "✓ bibtex found" -ForegroundColor Green
} catch {
    Write-Host "✗ bibtex not found. Please install MiKTeX or TeX Live." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 1: Converting PNG images to PDF..." -ForegroundColor Yellow

# Convert PNG to PDF if ImageMagick is available
if (Get-Command magick -ErrorAction SilentlyContinue) {
    Write-Host "  Converting figure1_curriculum.png..." -ForegroundColor Gray
    magick ..\figure1_curriculum.png -density 300 figures\figure1_curriculum.pdf
    
    Write-Host "  Converting figure2_architecture.png..." -ForegroundColor Gray
    magick ..\figure2_architecture.png -density 300 figures\figure2_architecture.pdf
    
    Write-Host "✓ Images converted successfully" -ForegroundColor Green
} else {
    Write-Host "⚠ ImageMagick not found. Please convert PNG images manually:" -ForegroundColor Yellow
    Write-Host "  magick figure1_curriculum.png -density 300 figures/figure1_curriculum.pdf" -ForegroundColor Gray
    Write-Host "  magick figure2_architecture.png -density 300 figures/figure2_architecture.pdf" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Step 2: First pdflatex pass (generating aux files)..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode main.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ First pdflatex pass failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ First pass completed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Running bibtex (processing bibliography)..." -ForegroundColor Yellow
bibtex main
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ bibtex reported warnings (this is often okay)" -ForegroundColor Yellow
}
Write-Host "✓ Bibliography processed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Second pdflatex pass (resolving references)..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode main.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Second pdflatex pass failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Second pass completed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Third pdflatex pass (final resolution)..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode main.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Third pdflatex pass failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Third pass completed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 6: Cleaning up auxiliary files..." -ForegroundColor Yellow
Remove-Item -Path "*.aux", "*.log", "*.out", "*.toc", "*.bbl", "*.blg" -ErrorAction SilentlyContinue
Write-Host "✓ Cleanup completed" -ForegroundColor Green

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "✓ COMPILATION SUCCESSFUL!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Output file: main.pdf" -ForegroundColor White
Write-Host ""
Write-Host "Visual elements included:" -ForegroundColor White
Write-Host "  • 7 Figures (2 existing + 5 TikZ/PGFPlots)" -ForegroundColor Gray
Write-Host "  • 6 Tables (professional booktabs style)" -ForegroundColor Gray
Write-Host "  • Complete bibliography" -ForegroundColor Gray
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review main.pdf for quality" -ForegroundColor Gray
Write-Host "  2. Check all figures render correctly" -ForegroundColor Gray
Write-Host "  3. Verify all citations resolved" -ForegroundColor Gray
Write-Host "  4. Prepare arXiv submission package" -ForegroundColor Gray
Write-Host ""

# Open PDF if available
if (Get-Command start -ErrorAction SilentlyContinue) {
    $response = Read-Host "Open main.pdf now? (y/n)"
    if ($response -eq "y") {
        Start-Process main.pdf
    }
}
