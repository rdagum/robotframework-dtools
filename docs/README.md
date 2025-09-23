# Robot Framework DTools Documentation

This folder contains the generated Robot Framework documentation for the DTools library.

## Generated Files

- `dtools_keywords.html` - Main library documentation with all utility keywords
- `dtools_encryption_keywords.html` - Encryption module documentation

## Generating Documentation

To regenerate the documentation files, run:

```bash
make docs
```

Or manually:

```bash
python -m robot.libdoc dtools.DTools docs/dtools_keywords.html
python -m robot.libdoc dtools.encryption.Encryption docs/dtools_encryption_keywords.html
```

## Viewing Documentation

Open the HTML files in any web browser to view the formatted documentation with examples and detailed parameter descriptions.