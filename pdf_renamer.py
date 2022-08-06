#import required libraries
import re
import os
from PyPDF2 import PdfFileReader
from datetime import datetime

def read_pdf(pdf_path):
    # reading pdffile
    pdf_obj = open(pdf_path, 'rb')
    # creating pdf reader  object
    pdf_reader = PdfFileReader(pdf_obj)
    # getting total no. of pages present
    total_pages = pdf_reader.numPages
    # extracting pdf data
    pdf_data = "\n\n".join([pdf_reader.getPage(i).extractText() for i in range(total_pages)])
    # closing file object
    pdf_obj.close()
    return pdf_data
    
    
def format_filename(pdf_path):
    # checking file existence as well as extension
    if not os.path.isfile(pdf_path):
        print('File not existing')
    else:
        # checking file extension
        if os.path.splitext(pdf_path.lower())[-1] != '.pdf':
            print('File is not a PDF type')
        else:
            try:
                # extracting pdf_data
                pdf_data = read_pdf(pdf_path)

                # setting bank name
                bank_name = 'CBA-SA'
                # getting account number
                acc_num = re.findall("Account Number\n.*\d{8}", pdf_data)[0].split()[-1][-4:]
                # getting name
                name = re.findall("Name:\n.*", pdf_data)[0].split('\n')[-1]
                name = re.sub('-', ' ', name).title()
                # getting closing balance
                bal = re.findall("Closing Balance\n.*", pdf_data)[0].split('\n')[-1][:-3]
                # getting start and end period
                period = re.findall("Period\n.*", pdf_data)[0].split('\n')[-1]
                period_start, period_end = [date_time_formatter(date) for date in period.split(' - ')]

                # recreating filename
                filename_new = "-".join([bank_name, bal, acc_num, name, period_start, period_end]) + '.pdf'
                path_actual = Path(pdf_path)
                # renaming file
                try:
                    path_actual.rename(Path(path_actual.parent, f"{filename_new}"))
                    print('> Successfully renamed')
                except:
                    print('> Error while renaming')
            except:
                print('> Error while renaming')