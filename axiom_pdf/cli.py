#!/usr/bin/env python3
"""
Axiom PDF Toolkit - Manipulate PDFs from terminal
"""

import sys
import argparse
import os
from pathlib import Path

try:
    from PyPDF2 import PdfReader, PdfWriter
    from pypdf import PdfReader as PdfReader4, PdfWriter as PdfWriter4
    from pdf2image import convert_from_path
    from PIL import Image
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


class AxiomPDF:
    """PDF manipulation toolkit"""
    
    @staticmethod
    def merge(pdfs: list, output: str = "merged.pdf"):
        """Merge multiple PDFs into one"""
        writer = PdfWriter()
        
        for pdf_path in pdfs:
            if not os.path.exists(pdf_path):
                print(f"❌ File not found: {pdf_path}")
                return False
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        
        with open(output, 'wb') as f:
            writer.write(f)
        
        print(f"✅ Merged {len(pdfs)} PDFs into {output}")
        return True
    
    @staticmethod
    def split(pdf_path: str, pages: str):
        """Extract specific pages from PDF"""
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return False
        
        page_numbers = [int(p.strip()) for p in pages.split(',')]
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page_num in page_numbers:
            if 1 <= page_num <= len(reader.pages):
                writer.add_page(reader.pages[page_num - 1])
            else:
                print(f"⚠️ Page {page_num} doesn't exist")
        
        output = f"extracted_{os.path.basename(pdf_path)}"
        with open(output, 'wb') as f:
            writer.write(f)
        
        print(f"✅ Extracted pages {pages} to {output}")
        return True
    
    @staticmethod
    def compress(pdf_path: str):
        """Compress PDF (simple mode)"""
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return False
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)
        
        output = f"compressed_{os.path.basename(pdf_path)}"
        with open(output, 'wb') as f:
            writer.write(f)
        
        original_size = os.path.getsize(pdf_path) / 1024
        new_size = os.path.getsize(output) / 1024
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"✅ Compressed: {original_size:.1f}KB → {new_size:.1f}KB ({reduction:.1f}% reduction)")
        return True
    
    @staticmethod
    def protect(pdf_path: str, password: str):
        """Add password protection to PDF"""
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return False
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        writer.encrypt(password)
        
        output = f"protected_{os.path.basename(pdf_path)}"
        with open(output, 'wb') as f:
            writer.write(f)
        
        print(f"✅ Password protected: {output}")
        return True
    
    @staticmethod
    def extract_text(pdf_path: str):
        """Extract all text from PDF"""
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return False
        
        reader = PdfReader(pdf_path)
        text = ""
        
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            text += f"\n--- Page {page_num} ---\n{page_text}\n"
        
        output = f"{os.path.splitext(pdf_path)[0]}_text.txt"
        with open(output, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ Text extracted to {output}")
        return True
    
    @staticmethod
    def extract_images(pdf_path: str):
        """Extract all images from PDF"""
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return False
        
        try:
            images = convert_from_path(pdf_path)
            output_dir = f"{os.path.splitext(pdf_path)[0]}_images"
            os.makedirs(output_dir, exist_ok=True)
            
            for i, image in enumerate(images):
                image_path = os.path.join(output_dir, f"page_{i+1}.png")
                image.save(image_path, 'PNG')
            
            print(f"✅ Extracted {len(images)} images to {output_dir}/")
            return True
        except Exception as e:
            print(f"❌ Image extraction failed: {e}")
            print("📌 Note: Some PDFs don't have extractable images")
            return False
    
    @staticmethod
    def rotate(pdf_path: str, degrees: int):
        """Rotate all pages of PDF"""
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            return False
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.rotate(degrees)
            writer.add_page(page)
        
        output = f"rotated_{os.path.basename(pdf_path)}"
        with open(output, 'wb') as f:
            writer.write(f)
        
        print(f"✅ Rotated {degrees}°: {output}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Axiom PDF Toolkit - Manipulate PDFs from terminal",
        epilog="Examples:\n  axiom-pdf merge a.pdf b.pdf\n  axiom-pdf split doc.pdf -p 5,10,15\n  axiom-pdf compress big.pdf"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge multiple PDFs')
    merge_parser.add_argument('pdfs', nargs='+', help='PDF files to merge')
    merge_parser.add_argument('-o', '--output', default='merged.pdf', help='Output filename')
    
    # Split command
    split_parser = subparsers.add_parser('split', help='Extract specific pages')
    split_parser.add_argument('pdf', help='PDF file to split')
    split_parser.add_argument('-p', '--pages', required=True, help='Page numbers (e.g., 5,10,15)')
    
    # Compress command
    compress_parser = subparsers.add_parser('compress', help='Compress PDF')
    compress_parser.add_argument('pdf', help='PDF file to compress')
    
    # Protect command
    protect_parser = subparsers.add_parser('protect', help='Add password protection')
    protect_parser.add_argument('pdf', help='PDF file to protect')
    protect_parser.add_argument('-p', '--password', required=True, help='Password to set')
    
    # Text command
    text_parser = subparsers.add_parser('text', help='Extract all text')
    text_parser.add_argument('pdf', help='PDF file to extract text from')
    
    # Images command
    images_parser = subparsers.add_parser('images', help='Extract all images')
    images_parser.add_argument('pdf', help='PDF file to extract images from')
    
    # Rotate command
    rotate_parser = subparsers.add_parser('rotate', help='Rotate PDF pages')
    rotate_parser.add_argument('pdf', help='PDF file to rotate')
    rotate_parser.add_argument('-d', '--degrees', type=int, required=True, choices=[90, 180, 270], help='Rotation degrees (90, 180, 270)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    toolkit = AxiomPDF()
    
    if args.command == 'merge':
        toolkit.merge(args.pdfs, args.output)
    elif args.command == 'split':
        toolkit.split(args.pdf, args.pages)
    elif args.command == 'compress':
        toolkit.compress(args.pdf)
    elif args.command == 'protect':
        toolkit.protect(args.pdf, args.password)
    elif args.command == 'text':
        toolkit.extract_text(args.pdf)
    elif args.command == 'images':
        toolkit.extract_images(args.pdf)
    elif args.command == 'rotate':
        toolkit.rotate(args.pdf, args.degrees)


if __name__ == "__main__":
    main()
