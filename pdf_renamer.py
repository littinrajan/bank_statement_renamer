#import required libraries
import re
import os
from PyPDF2 import PdfFileReader
from datetime import datetime
from pathlib import Path
from tkinter import *
from tkinter import filedialog as fd

#function to get file
def get_file():
    file = fd.askopenfile()
    if file:
        file_name = file.name
        file.close()
        print(f"Filename: {file_name}")
        format_filename(file.name)
 
#function to get directory 
def get_directory():
    directory = fd.askdirectory()
    if directory:
        print(f"Directory: {directory}")
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            # checking if it is a file
            if os.path.isfile(file_path):
                print(f"Filename: {file_name}")
                format_filename(file_path)

def date_time_formatter(ip_date):
    # convert extracted date to datetime format
    datetime_date = datetime.strptime(ip_date, '%d %b %Y')
    # format the date to ddmmyyyy
    formated_date = datetime_date.strftime('%d%m%Y')
    return formated_date

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

#creating root window               
root = Tk()

#adding button for file picker
file_btn = Button(root, text="Rename a File", fg='blue', command=get_file)
file_btn.place(x=110, y=100)

#adding button for directory picker
dir_btn = Button(root, text="Choose Directory", fg='green', command=get_directory)
dir_btn.place(x=100, y=150)

#setting title and dimension of application window
root.title('File Renamer')
root.geometry("300x300")
root.mainloop()
