#!/bin/bash
################################################################################
# Beamer Presentation Compilation Script
#
# This script compiles Beamer presentations with proper LaTeX build sequence:
# 1. xelatex (first pass)
# 2. bibtex (if bibliography present)
# 3. xelatex (second pass)
# 4. xelatex (third pass - resolve references)
#
# Usage:
#   ./compile_beamer.sh main.tex              # Compile master file
#   ./compile_beamer.sh main.tex --clean      # Compile and clean aux files
#   ./compile_beamer.sh main.tex --quiet      # Quiet mode
#
# Note: For modular presentations with sections/, always compile main.tex
#       (which contains \input{sections/...} statements)
################################################################################

set -e  # Exit on error

# Default options
QUIET=false
CLEAN=false
TEXFILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN=true
            shift
            ;;
        --quiet|-q)
            QUIET=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS] <file.tex>"
            echo ""
            echo "Options:"
            echo "  --clean     Remove auxiliary files after compilation"
            echo "  --quiet     Suppress detailed output"
            echo "  --help      Show this help message"
            exit 0
            ;;
        *.tex)
            TEXFILE="$1"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate input
if [ -z "$TEXFILE" ]; then
    echo "Error: No .tex file specified"
    echo "Usage: $0 <file.tex>"
    exit 1
fi

if [ ! -f "$TEXFILE" ]; then
    echo "Error: File not found: $TEXFILE"
    exit 1
fi

# Extract base name (without .tex extension)
BASENAME="${TEXFILE%.tex}"

# Function to print section headers
print_section() {
    if [ "$QUIET" = false ]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "$1"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi
}

# Function to compile with xelatex
compile_xelatex() {
    local pass_num=$1
    print_section "Pass $pass_num/3: Running xelatex..."

    if [ "$QUIET" = true ]; then
        xelatex -interaction=batchmode "$TEXFILE" > /dev/null 2>&1
    else
        xelatex -interaction=nonstopmode "$TEXFILE"
    fi

    if [ $? -ne 0 ]; then
        echo "✗ Error during xelatex pass $pass_num"
        echo "Check ${BASENAME}.log for details"
        exit 1
    fi
}

# Function to run bibtex
run_bibtex() {
    print_section "Processing bibliography..."

    if [ "$QUIET" = true ]; then
        bibtex "$BASENAME" > /dev/null 2>&1
    else
        bibtex "$BASENAME"
    fi

    # bibtex may "fail" if no citations, but that's ok
}

# Function to clean auxiliary files
clean_aux_files() {
    print_section "Cleaning auxiliary files..."

    local extensions=("aux" "log" "nav" "out" "snm" "toc" "bbl" "blg" "synctex.gz")

    for ext in "${extensions[@]}"; do
        if [ -f "${BASENAME}.${ext}" ]; then
            rm "${BASENAME}.${ext}"
            if [ "$QUIET" = false ]; then
                echo "  Removed: ${BASENAME}.${ext}"
            fi
        fi
    done
}

# Function to check output
check_output() {
    print_section "Checking output..."

    if [ ! -f "${BASENAME}.pdf" ]; then
        echo "✗ PDF file not generated!"
        echo "Compilation may have failed. Check ${BASENAME}.log"
        exit 1
    fi

    # Get PDF info
    local pages=$(pdfinfo "${BASENAME}.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}')
    local size=$(ls -lh "${BASENAME}.pdf" | awk '{print $5}')

    echo "✓ Compilation successful!"
    echo "  Output: ${BASENAME}.pdf"
    echo "  Pages: ${pages}"
    echo "  Size: ${size}"

    # Check for warnings in log
    if [ -f "${BASENAME}.log" ]; then
        local warnings=$(grep -c "Warning" "${BASENAME}.log" 2>/dev/null || echo "0")
        local overfull=$(grep -c "Overfull" "${BASENAME}.log" 2>/dev/null || echo "0")

        echo "  Warnings: ${warnings}"
        echo "  Overfull boxes: ${overfull}"

        if [ "$overfull" -gt 5 ]; then
            echo "  ⚠  Multiple overfull boxes detected!"
            echo "     Consider reviewing table/figure sizing"
        fi

        # Check for undefined references
        local undef=$(grep -c "undefined" "${BASENAME}.log" 2>/dev/null || echo "0")
        if [ "$undef" -gt 0 ]; then
            echo "  ⚠  Undefined references detected!"
            echo "     Check hyperlinks and labels"
        fi
    fi
}

################################################################################
# Main compilation workflow
################################################################################

print_section "Compiling: $TEXFILE"

# First pass
compile_xelatex 1

# Check if bibliography needed
if grep -q "\\\\bibliography" "$TEXFILE"; then
    run_bibtex
fi

# Second pass
compile_xelatex 2

# Third pass (resolve references)
compile_xelatex 3

# Check output
check_output

# Clean if requested
if [ "$CLEAN" = true ]; then
    clean_aux_files
fi

print_section "Done!"

exit 0
