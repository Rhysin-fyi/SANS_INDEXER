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

        
