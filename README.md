
# SANS PDF Parser

A command-line tool for parsing and manipulating SANS PDFs. This tool provides functionalities such as merging, scraping title slides, creating indices, decrypting, and stripping content for easier searching and navigation.

## Features

- **Merge PDFs**: Combine multiple PDFs into a single document.
- **Scrape Title Slides**: Extract title slides from all PDFs.
- **Create Omega Index**: Generate an OMEGA index for efficient searching.
- **Decrypt PDFs**: Decrypt password-protected PDFs.
- **Strip Index**: Strip the specified book index into searchable terms.

## Installation

To use the SANS PDF parser, you'll need python installed on your machine along with the necessary libraries. You can install the required libraries using:

```pip
pip install -r requirements.txt
```
## PREREQUISITE
PLEASE make a folder with ONLY the PDFs downloaded from SANS present I do not want any adverse effects to other files on your computer
```
508
└── ENCRYPTED
    ├── file1.pdf
    ├── file2.pdf
    ├── file3.pdf
    ├── file4.pdf
    └── file5.pdf
```
## Usage
To run the parser, use the following command in your terminal:

```bash
python pdfparse.py -d <directory> -o <output_file> [options]
```

## Command-Line Arguments

- `-m`, `--merge`: Merge all PDFs into a single PDF (kinda useless as this tool is recursive but ¯\(ツ)/¯ ).
- `-s`, `--scrape`: Scrape all title slides across all PDFs.
- `--strip <Book5>`: Strips the specified book index into search terms.
- `--omega`: Make an OMGEA index.
- `--dcrypt`: Decrypt all PDFs in the specified directory. **Enclose the password in quotes.**
- `--omit`, `--omit <Strings>`: Specify strings to omit during scrape.
- `-p`, `--passwd <PASS>`: Specify the password to use with decryption. **Wrap the password in quotes.**
- `-d`, `--dir <Dir>`: Specify which directory the SANS PDFs are located in.
- `-o`, `--out <OutFile>`: Specify the output file name.
- `-b`, `--book <OutFile>`: Specify book5 name to index.

## Examples

1. **Decrypting PDFs**: The SANS PASSWORD MUST BE IN QUOTES this will also create a new sub-folder called decrypt in the same directory as the Encryped PDFs
   ```bash
   python pdfparse.py -d D:\SANS\508\Encrypt -o SANS508_ --dcrypt --pass "4$`s9....1-q=V"
   ```
   
2. **OMEGA INDEX**:
   ```bash
   python pdfparse.py -d D:\SANS\508\Encrypt -o omegaindex.txt --omega
   ```
   
3. **Scraping Title Slides**:
   ```bash
   python pdfparse.py -s -d "D:\SANS\508\Encrypt\DECRYPT" -o Slidescrape.txt
   ```

4. **Merging PDFs**:
   ```bash
   python pdfparse.py -m -d "D:\SANS\508\Encrypt\DECRYPT" -o MERGED.PDF
   ```

5. **Stripping Index**:
   ```bash
   python pdfparse.py --index SANS508_Book5Dcrypt.pdf -d "D:\SANS\508\Encrypt\DECRYPT" -o index.txt --omit John Doe
   ```

## Contribution

Contributions are welcome! If you have suggestions for improvements or want to add new features, feel free to open an issue or submit a pull request.

