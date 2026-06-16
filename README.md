# 📄 Axiom PDF Toolkit

> **Manipulate PDFs from terminal. No Adobe. No bullshit.**

One command to rule all your PDF needs.

## ✨ Features

| Command | What it does |
|---------|---------------|
| `axiom-pdf merge a.pdf b.pdf` | Merge PDFs |
| `axiom-pdf split doc.pdf -p 5,10,15` | Extract specific pages |
| `axiom-pdf compress heavy.pdf` | Reduce file size |
| `axiom-pdf protect secret.pdf -p 1234` | Add password protection |
| `axiom-pdf text document.pdf` | Extract all text |
| `axiom-pdf images document.pdf` | Extract all images |
| `axiom-pdf rotate twisted.pdf -d 90` | Rotate pages |

## 🚀 Install

```bash
pip install axiom-pdf-toolkit
```
## 💻 Usage Examples
# Merge two PDFs
axiom-pdf merge invoice1.pdf invoice2.pdf

# Extract pages 5, 10 and 15
axiom-pdf split report.pdf -p 5,10,15

# Compress a heavy PDF
axiom-pdf compress huge_document.pdf

# Password protect a PDF
axiom-pdf protect confidential.pdf -p mySecurePassword

# Extract all text
axiom-pdf text scanned_doc.pdf

# Extract all images
axiom-pdf images magazine.pdf

# Rotate all pages 90 degrees
axiom-pdf rotate sideways.pdf -d 90

## 📦 Requirements
-Python 3.8+
-Works on Linux, macOS, Windows

## 📄 License
MIT © Manuel Echepares / AXIOM Systems

