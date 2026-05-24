# Compile Instructions

This package is aligned to PLOS ONE as closely as possible using the official PLOS LaTeX template conventions and `plos2025.bst`.

Recommended compile command from the `latex/` directory:

```bash
latexmk -pdf main.tex
```

Equivalent manual sequence:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Important PLOS upload note: PLOS initial LaTeX submission uses the compiled PDF as the manuscript file and requires figures to be uploaded separately. This package includes figures inside the PDF for local quality assurance and also includes separate files under `figures/`.
