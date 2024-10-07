import pdfplumber
import os
import re
import PyPDF2
import argparse
import pikepdf
import pikepdf.models
import requests as rq
from tqdm import tqdm

pattern = r"(^[a-zA-Z0-9]{32}$)"
wordspattern = r"^(?!.*[^\x20-\x7E])(?=[^\d:])[^\d:\n]{3,}(?: [^\d:\n]+)*"
HARD_CODED_OMIT = ["� SANS Institute","this page intentionally left blank.","ohNrhAfzA","live","lia","Licensed To","� SANS Institute  ","Index","� SANS Institute "]
characters_to_strip = "()'\":,”“‘?;-•’—…[]!"
phrases_to_strip = ["'s", "'re", "'ve", "'t", "[0]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]"]
delimeter = "Licensed To: "

def get_wordlist():
    common_words = rq.get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt").text.split("\n")
    lower_common = []
    for lowercommon in common_words:
        lower_common.append(lowercommon.lower())
    return lower_common


def create_parser():
    parser = argparse.ArgumentParser(description="Command Line SANS PDF parser")
    parser.add_argument("-m", "--merge", action="store_true", help="Merge all PDFs into a single PDF (kinda useless but ¯\(ツ)/¯ )")
    parser.add_argument("-s", "--scrape", action="store_true", help="Scrape all title slides accross all PDFs")
    parser.add_argument("--index", metavar="Book5",type=str, help="This strips the book five index into search terms")
    parser.add_argument("--omega", action="store_true", help="Make an OMGEA index")
    parser.add_argument("--dcrypt", action="store_true", help="Decrypt all PDFs in directory ENCLOSE PASSWORD IN QUOTES")
    parser.add_argument("-p", "--passwd", metavar="PASS", type=str, help="Password to use with decryption WRAP PASSWORD IN QUOTES")
    parser.add_argument("-d", "--dir", metavar="Dir", type=str, help="Specify which directory SANS PDFs live in")
    parser.add_argument("-o", "--out", metavar="OutFile", type=str, help="Specify output file name")
    parser.add_argument("--omit", metavar="NAME", type=str, nargs='*', help="Specify a list of strings to omit from the scrape")
    return parser

def strip_characters(word):
    word_length = len(word)
    word = word.replace("’", "'")
    while True:
        for phrase in phrases_to_strip:
            if word.endswith(phrase):
                word = word[:len(phrase)]
        word = word.strip(characters_to_strip).rstrip(".")
        if len(word) == word_length:
            return word
        else:
            word_length = len(word)


def decrypt_pdfs(directory, outfile, passwd):
    files = os.listdir(directory)
    counter = 1
    decrypting = "DECRYPT"
    decrypt_path = os.path.join(directory,decrypting)
    try:
        os.mkdir(decrypt_path)
    except Exception as e:
        print(e)
        print("ATTEMPTING TO ACCESS/REMOVE SUBDIR")
        os.rmdir(decrypt_path)
        os.mkdir(decrypt_path)

    for file in files:
        pdf_file = os.path.join(directory, file)
        try:
            pdf = pikepdf.open(filename_or_stream=pdf_file, password=passwd)
            
            pdf.save(f"{os.path.join(decrypt_path,outfile)}Book{counter}_Dcrypt.pdf")
        except pikepdf.PasswordError:
            print(f"FAILED TO DECRYPT using pikepdf: {pdf_file}")
            print("TRYING WITH QPDF")

            try:
                os.system(f'qpdf --password={passwd} --decrypt --remove-restrictions "{pdf_file}" "{os.path.join(directory,decrypting)}{outfile}{counter}.pdf"')
            except Exception as e:
                print(f"FAILED TO DECRYPT using qpdf on file {pdf_file}: {str(e)}")
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
        
        counter += 1

    return

def pdf_merger(directory):
    files = os.listdir(directory)

    mergeFile = PyPDF2.PdfMerger()

    for names in files:
        if(names.endswith("pdf")):
            pdf_name = os.path.join(directory,names)
            mergeFile.append(PyPDF2.PdfReader(pdf_name, 'rb'))
        
    mergeFile.write("SANSmerged.pdf")
    
def scrape_titles(directory,outputfile):
    files = os.listdir(directory)
    outputfile = open(outputfile, "w")
    counter = 1
    for file in files:
        if(file.endswith("pdf")):
            pdf_name = os.path.join(directory,file)
            with pdfplumber.open(pdf_name) as pdf:
                for pages in tqdm(pdf.pages, desc="Processing Title Slides"):
                    text = pages.extract_text()
                    page = pages.page_number

                    text = text.split('\n')
                    clean = text[1].replace(",", "")
                    if(re.search(pattern, clean)):
                        continue
                    else:
                        outputfile.write(f"{clean}, BOOK: {counter} Page: {page-2}\n") 
        counter += 1

    outputfile.close()


def check_if_good(word:str,lower_common):
    word = str(word).strip()
    if len(word) < 3:
        return False
    if word[0].isdigit():
        return False
    if word.lower() in lower_common or word.lower() + "s" in lower_common:
        return False
    if word.endswith((',',':','.','!')):
        return False
    if word.startswith("http://") or word.startswith("https://"):
        return False
    if word in HARD_CODED_OMIT:
        return False
    if(re.match(pattern, word)):
        return False
    if(re.match(r'.*@.*', word)):
        return False
    return True
    

def split_index(directory, book, outfile, omit):
    with open(outfile, "w") as output:
        full_index = []
        book_path = os.path.join(directory, book)
        with pdfplumber.open(book_path) as pdf:
            total_pages = pdf.pages
            index_page = input("Enter the last page number before the index starts: ")
            index_page = int(index_page) + 2

            normalized_omit = [omit_word.lower() for omit_word in omit]
            normalized_hardcoded_omit = [omit_word.lower() for omit_word in HARD_CODED_OMIT]

            combined_omit = normalized_omit + normalized_hardcoded_omit

            for index in total_pages[index_page:]:
                mal = index.extract_text()
                if mal: 
                    mal_lines = mal.split('\n')
                    for words in mal_lines:
                        if re.search(wordspattern, words):
                            found_words = re.findall(wordspattern, words, re.MULTILINE)
                            for text in found_words:
                                stripped_text = text.lower().strip()
                                if not any(omit_phrase in stripped_text for omit_phrase in combined_omit):
                                    full_index.append(stripped_text)
                                    output.write(stripped_text + '\n')

    return full_index

def strip_all_pdfs(directory, outfile, giant_exclude):
    files = os.listdir(directory)
    counter = 1  
    index = {}  
    total_words = []

    for name in files:
        if name.endswith("pdf"):
            pdf_path = os.path.join(directory, name)
            with pdfplumber.open(pdf_path) as pdf:
                for pages in tqdm(pdf.pages, desc=f"Processing Pages in {name}", leave=False):
                    text = pages.extract_text().split()
                    pagenum = pages.page_number - 2
                    
                    long_words = [] 
                    for page in text:
                        page = page.replace("\n", " ").replace("\t", " ")
                        page_len = len(page)
                        while True:
                            page = page.replace("  ", " ")
                            if len(page) == page_len:
                                break
                            else:
                                page_len = len(page)
                        page = page.strip()
                        words = page.split(" ")
                        for word in words:
                            word = strip_characters(word).lower()
                            if check_if_good(word, giant_exclude):
                                total_words.append(word)
                                long_words.append(word)
                    
                    if counter not in index:
                        index[counter] = {}
                    if pagenum not in index[counter]:
                        index[counter][pagenum] = long_words
                    else:
                        index[counter][pagenum].extend(long_words) 

        counter += 1

    results = []
    
   
    for word in set(total_words):
        occurrences = []
        
        for book_num, pages in index.items():
            for pagenum, words_on_page in pages.items():
                if word in words_on_page:
                    occurrences.append(f"({book_num}){pagenum}")

        if len(occurrences) < 15:
            joined_occurrences = ', '.join(occurrences)
            results.append(f"{word}: {joined_occurrences}")

    results.sort(key=str.casefold)

    with open(outfile, "w", encoding="utf-8", errors="ignore") as f:
        f.write("\n".join(results))

def omega_index(directory,outfile):
    giant_exclude = get_wordlist()
    strip_all_pdfs(directory,outfile,giant_exclude)

    return

def main():
    wordlist = get_wordlist()
    parser = create_parser()
    args = parser.parse_args()
    omitted_strings = args.omit if args.omit else []

    if args.dir and args.out:
        directory = args.dir
        outfile = args.out
        book = args.index
        if args.merge:
            pdf_merger(directory, outfile)
            return
        elif args.scrape:
            scrape_titles(directory, outfile)
            return
        elif args.omega:
            omega_index(directory,outfile)
            return
        elif args.index:
            split_index(directory,book,outfile,omitted_strings)
        elif args.dcrypt:
            if args.passwd:
                password = args.passwd
                decrypt_pdfs(directory, outfile, password)
            else:
                print("Please specify a password with --pass")
        else:
            parser.print_help()
    else:
        print("Please specify a directory with -d and out file -o")

if __name__ == "__main__":
    main()

        
