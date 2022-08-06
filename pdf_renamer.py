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