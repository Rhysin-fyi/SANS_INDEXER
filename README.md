
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
    ├── FOR508 - Book 1_2538395.pdf
    ├── FOR508 - Book 2_2538395.pdf
    ├── FOR508 - Book 3_2538395.pdf
    ├── FOR508 - Book 4_2538395.pdf
    └── FOR508 - Book 5_2538395.pdf
```
## Usage
To run the parser, use the following command in your terminal:

```bash
python pdfparse.py -d <directory> -o <output_file> [options]
```

## Command Line Options:

- **`-m, --merge`**: Merge all PDFs into a single PDF. *(Note: This may be redundant as the tool processes recursively.)*

- **`-s, --scrape`**: Scrape all title slides from the PDFs.

- **`--labs`**: Specifically scrape Lab titles from the PDFs use with -s.

- **`--index <Book5>`**: Strip the specified book index (e.g., Book5) into search terms.

- **`--omega`**: Generate an OMGEA index.

- **`--dcrypt`**: Decrypt all PDFs in the specified directory. *(Note: Password must be enclosed in quotes.)*

- **`-p, --passwd <PASS>`**: Provide the password for PDF decryption. *(Password should be wrapped in quotes.)*

- **`-d, --dir <Dir>`**: Specify the directory containing the SANS PDFs.

- **`-o, --out <OutFile>`**: Define the output file name.

- **`--omit <Strings>`**: Provide a list of strings to omit during scraping (e.g., certain names or phrases).

- **`--format <FORMAT>`**: Specify the output format: `.txt`, `.csv`, or `.doc`.


## Examples

1. **Decrypting PDFs**: The SANS PASSWORD MUST BE IN QUOTES this will also create a new sub-folder called decrypt in the same directory as the Encryped PDFs, if using zsh use escape on unsafe characters or bash single quotes\
**RECOMMENDED**: Use default names after downloading from SANS, when using -o for dcrypt use SANS and course # followed by and underscore (ex. SANS508_)
   ```bash
   python pdfparse.py -d "D:\SANS\508\Encrypt" -o SANS508_ --dcrypt --pass "4$`s9....1-q=V"
   ```
   
2. **OMEGA INDEX**:
   ```bash
   python pdfparse.py -d "D:\SANS\508\Encrypt" -o omegaindex.txt --omega
   ```

2. **OMEGA INDEX formatted csv**:
   ```bash
   python pdfparse.py -d "D:\SANS\508\Encrypt" -o omegaindex.txt --omega --format csv
   ```

   
3. **Scraping Title Slides**:
   ```bash
   python pdfparse.py -s -d "D:\SANS\508\Encrypt\DECRYPT" -o Slidescrape.txt
   ```

4. **Scraping LAB Title Slides**:
   ```bash
   python pdfparse.py -s -d "D:\SANS\508\Encrypt\DECRYPT" -o Labscrape.txt --labs
   ```

5. **Merging PDFs**:
   ```bash
   python pdfparse.py -m -d "D:\SANS\508\Encrypt\DECRYPT" -o MERGED.PDF
   ```

6. **Stripping Index**:
   ```bash
   python pdfparse.py --index SANS508_Book5Dcrypt.pdf -d "D:\SANS\508\Encrypt\DECRYPT" -o index.txt --omit John Doe
   ```

## Contribution

Contributions are welcome! If you have suggestions for improvements or want to add new features, feel free to open an issue or submit a pull request.

