
# SANS PDF Parser

A command-line tool for parsing and manipulating SANS PDFs. This tool provides functionalities such as merging, scraping title slides, creating indices, decrypting, and stripping content for easier searching and navigation.

## Features

- **Merge PDFs**: Combine multiple PDFs into a single document.
- **Scrape Title Slides**: Extract title slides from all PDFs.
- **Create Omega Index**: Generate an OMGEA index for efficient searching.
- **Decrypt PDFs**: Decrypt password-protected PDFs.
- **Strip Index**: Strip the specified book index into searchable terms.

## Installation

To use the SANS PDF parser, you'll need Python installed on your machine along with the necessary libraries. You can install the required libraries using:

```bash
pip install pikepdf pdfplumber
```

## Usage

To run the parser, use the following command in your terminal:

```bash
python your_script_name.py -d <directory> -o <output_file> [options]
```

## Command-Line Arguments

- `-m`, `--merge`: Merge all PDFs into a single PDF (kinda useless but ¯\(ツ)/¯ ).
- `-s`, `--scrape`: Scrape all title slides across all PDFs.
- `--strip <Book5>`: Strips the specified book index into search terms.
- `--omega`: Make an OMGEA index.
- `--dcrypt`: Decrypt all PDFs in the specified directory. **Enclose the password in quotes.**
- `-p`, `--passwd <PASS>`: Specify the password to use with decryption. **Wrap the password in quotes.**
- `-d`, `--dir <Dir>`: Specify which directory the SANS PDFs are located in.
- `-o`, `--out <OutFile>`: Specify the output file name.
- `-b`, `--book <OutFile>`: Specify the output file name for the book index.

## Examples

1. **Decrypting PDFs**:
   ```bash
   python your_script_name.py --dcrypt -p "4$`s9SLdsAPqt#T^o.~MYg!aW1-q=V" -d "path/to/pdfs" -o "output/"
   ```

2. **Scraping Title Slides**:
   ```bash
   python your_script_name.py -s -d "path/to/pdfs" -o "output/"
   ```

3. **Merging PDFs**:
   ```bash
   python your_script_name.py -m -d "path/to/pdfs" -o "merged.pdf"
   ```

4. **Stripping Index**:
   ```bash
   python your_script_name.py --strip Book5 -d "path/to/pdfs" -o "output/"
   ```

## Contribution

Contributions are welcome! If you have suggestions for improvements or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
