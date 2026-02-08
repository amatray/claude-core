#!/usr/bin/env python3
"""Extract text from a PDF, chunking automatically if large.

Usage:
    python extract_pdf.py <pdf_path> [--output <output_path>] [--chunk-size <pages>]

Output: writes extracted text to a .txt file (default: same name as input, .txt extension).
Prints the output file path to stdout on success.
"""

import argparse
import sys
import os

def extract_pdf(pdf_path, output_path=None, chunk_size=12):
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber not installed. Run: pip install pdfplumber", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        output_path = os.path.splitext(pdf_path)[0] + ".txt"

    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"PDF has {total_pages} pages. Processing in chunks of {chunk_size}...", file=sys.stderr)

        for start in range(0, total_pages, chunk_size):
            end = min(start + chunk_size, total_pages)
            print(f"  Processing pages {start + 1}-{end}...", file=sys.stderr)
            for page in pdf.pages[start:end]:
                text = page.extract_text()
                if text:
                    all_text.append(f"--- PAGE {page.page_number} ---\n{text}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))

    print(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from PDF with automatic chunking")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output", "-o", help="Output text file path (default: <input>.txt)")
    parser.add_argument("--chunk-size", "-c", type=int, default=12, help="Pages per chunk (default: 12)")
    args = parser.parse_args()
    extract_pdf(args.pdf_path, args.output, args.chunk_size)
