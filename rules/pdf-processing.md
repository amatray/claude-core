# PDF Processing Protocol

## MANDATORY FIRST STEP FOR ANY PDF

**When ANY task involves a PDF file** (reading, analyzing, summarizing, reviewing, extracting content), you MUST use the chunked extraction method below. This applies to:

- Any PDF input regardless of size
- All PDF reading tasks
- PDF content analysis
- PDF summarization
- PDF review or comparison

**Do NOT attempt to read PDFs directly** using the Read tool or any other method. Always extract first.

## Extraction Workflow

### Step 1: Extract PDF to Text

Run the extraction script:

```bash
python ~/claude-workflows/claude-core/scripts/extract_pdf.py <pdf_path> --output /tmp/extracted.txt
```

**Parameters:**
- `pdf_path` - Path to the PDF file
- `--output` - Output text file path (default: same name as input with .txt extension)
- `--chunk-size` - Pages per chunk (default: 12)

### Step 2: Read Extracted Text

After extraction completes, read the extracted text file:

```bash
cat /tmp/extracted.txt
```

Use the Read tool on `/tmp/extracted.txt` for all subsequent analysis.

## Why This Approach

1. **Reliability** - Avoids PDF parsing issues in large documents
2. **Performance** - Chunked processing prevents memory issues
3. **Consistency** - Uniform text extraction across all PDFs
4. **Context Management** - Extracted text is easier to work with than raw PDF

## Requirements

The extraction script requires `pdfplumber`:

```bash
pip install pdfplumber
```

If the package is not installed, the script will print an error message with installation instructions.

## Output Format

Extracted text includes page markers:

```
--- PAGE 1 ---
[Page 1 content]

--- PAGE 2 ---
[Page 2 content]
```

This allows you to reference specific pages in your analysis.

## Never Skip This Step

Even for small PDFs, always use the extraction workflow. The overhead is minimal, and it ensures consistent behavior across all PDF processing tasks.
