import pdfplumber
import os
import re
import PyPDF2
import argparse
import pikepdf
import pikepdf.models

pattern = r"(^[a-zA-Z0-9]{32}$)"

def create_parser():
    parser = argparse.ArgumentParser(description="Command Line SANS PDF parser")
    parser.add_argument("-m", "--merge", action="store_true", help="Merge all PDFs into a single PDF")
    parser.add_argument("-s", "--scrape", action="store_true", help="Scrape all title slides accross all PDFs")
    parser.add_argument("--omega", action="store_true", help="Make an OMGEA index")
    parser.add_argument("--dcrypt", action="store_true", help="Decrypt all PDFs in directory")
    parser.add_argument("-p", "--passwd", metavar="PASS", type=str, help="Password to use with decryption")
    parser.add_argument("-d", "--dir", metavar="Dir", type=str, help="Specify which directory SANS PDFs live in")
    parser.add_argument("-o", "--out", metavar="OutFile", type=str, help="Specify output file name")
    return parser

def extract_slides_from_pdf(file_path,outputfile,filename):

    with pdfplumber.open(file_path) as pdf:
        counter = 1
        for pages in pdf.pages:
            text = pages.extract_text()
            page = pages.page_number
            

            text = text.split('\n')
            clean = text[1].replace(",", "")
            if(re.search(pattern, clean)):
                continue
            else:
                outputfile.write(f"{clean}, {filename}:{page-2}\n")


def pdf_merger(directory):
    files = os.listdir(directory)

    mergeFile = PyPDF2.PdfMerger()

    for names in files:
        if(names.endswith("pdf")):
            mergeFile.append(PyPDF2.PdfReader(f'{directory}\\{names}', 'rb'))
        
    mergeFile.write("SANSmerged.pdf")


def scrape_titles(directory, outputfile):    
    files = os.listdir(directory)
    
    output = open(outputfile, "w")
    counter = 1
    for file in files:
        if(file.endswith("pdf")):
            extract_slides_from_pdf(f"{directory}\\{file}",output,counter)
            counter += 1

    output.close()

def decrypt_pdfs(directory, outfile, passwd):
    files = os.listdir(directory)
    counter = 1
    print(passwd)
    for file in files:
        pdf = pikepdf.open(filename_or_stream=f"{directory}\\{file}", password=rf"4$`s9SLdsAPqt#To.~MYg!aW1-q=V")
        #print(pikepdf.models.EncryptionInfo.file_method)
        pdf.save(f"{outfile}DECRYPT{counter}.pdf")
        
        counter += 1
    return

import pdfplumber
import os
import re
import PyPDF2
import requests as rq

pattern = r"(^[a-zA-Z0-9]{32}$)"
wordspattern = r"^(?!.*[^\x20-\x7E])(?=[^\d:])[^\d:\n]{3,}(?: [^\d:\n]+)*"
exclude = ["� SANS Institute","Edwinsberry","This page intentionally left blank.","Edwin ","Edwin Berry","Berry","ohNrhAfzA","live","lia","Licensed To","� SANS Institute  ","Index","� SANS Institute "]

common_words = rq.get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt").text.split("\n")
lower_common = []
for lowercommon in common_words:
    lower_common.append(lowercommon.lower()) 


def extract_slides_from_pdf(file_path,outputfile):

    with pdfplumber.open(file_path) as pdf:
        for pages in pdf.pages:
            text = pages.extract_text()
            page = pages.page_number

            text = text.split('\n')
            clean = text[1].replace(",", "")
            if(re.search(pattern, clean)):
                continue

            else:
                outputfile.write(f"{clean}, {page-2}\n")


def pdf_merger(directory):
    files = os.listdir(directory)

    mergeFile = PyPDF2.PdfMerger()

    for names in files:
        if(names.endswith("pdf")):
            mergeFile.append(PyPDF2.PdfReader(f'{directory}\\{names}', 'rb'))
        
    mergeFile.write("SANSmerged.pdf")


def scrape_titles():
    directory = r'C:\Users\wynnb\OneDrive\Documents\SANS\508_FA\Resources\DECRYPT'
    files = os.listdir(directory)
    outputfile = input("Enter Output Filename: ")
    output = open(outputfile, "w")

    for file in files:
        if(file.endswith("pdf")):
            extract_slides_from_pdf(f"{directory}\\{file}",output)

    output.close()


def check_if_good(word:str):
    # Length check
    word = str(word).strip()
    if len(word) < 3:
        return False
    # Starts with number
    if word[0].isdigit():
        return False
    # Not common english word
    if word.lower() in lower_common or word.lower() + "s" in lower_common:
        return False
    if word.endswith((',',':','.','!')):
        return False
    # Not SANS url
    if word.startswith("http://") or word.startswith("https://"):
        return False
    if(re.match(pattern, word)):
        return False
    if(re.match(r'.*@.*', word)):
        return False
    return True
    

def split_index():
    directory = r'C:\Users\wynnb\OneDrive\Documents\SANS\508_FA\Resources\DECRYPT'
    files = os.listdir(directory)
    output = open("testomega.txt", "w")
    fullIndex = []
    with pdfplumber.open(f"{directory}\\{files[4]}") as pdf:
        totalpages = pdf.pages
        for index in totalpages[119:]:
            mal = index.extract_text()
            mal = mal.split('\n')
            for words in mal:
                if(re.search(wordspattern,words)):
                    words = re.findall(wordspattern,words,re.MULTILINE)
                    for text in words:
                        stripped_text = text.lower().strip()
                        # Check if the found text is in the exclude list
                        if stripped_text not in (excl.lower() for excl in exclude) and check_if_good(stripped_text):  # Case-insensitive check
                            fullIndex.append(text)
                            output.write(text + '\n') 
                else:
                    continue    


                   
    return fullIndex

def strip_all_pdfs(fullIndex:list[str]):
    directory = r'C:\Users\wynnb\OneDrive\Documents\SANS\508_FA\Resources\DECRYPT'
    files = os.listdir(directory)
    output = open("STRIPALL.txt", "w")
    counter = 1
    for name in files:
        if name.endswith("pdf"):
            with pdfplumber.open(f"{directory}\\{name}") as pdf:
                for pages in pdf.pages:
                    text = pages.extract_text()
                    page = pages.page_number

                    text = text.split()
                    for everything in fullIndex:
                        for testing in text:
                            if everything.lower().split() == testing.lower().split():
                                print(f"FOUND {everything} On PAGE: {page - 2} Book: {counter}")
                    #for data in text:
                    #    if(check_if_good(data)):
                    #        #print(f"{data} BOOK: {counter} PAGE: {page - 2}")
                    #        continue
                    #    else:
                    #        continue
                    #print(f"{text[2]} PAGE: {page-2}")
        counter += 1
    return

def omega_index():
    fullIndex = split_index()
    strip_all_pdfs(fullIndex)

    return


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.dir and args.out:
        directory = args.dir
        outfile = args.out
        if args.merge:
            pdf_merger(directory, outfile)
            return
        elif args.scrape:
            scrape_titles(directory, outfile)
            return
        elif args.omega:
            return
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

        
