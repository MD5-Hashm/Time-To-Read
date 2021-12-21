import os
import sys
import re
import time
from epub_conversion.utils import open_book, convert_epub_to_lines, convert_lines_to_text
from pathlib import Path
from io import StringIO
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

if sys.platform == "win32":
    clearcommand = "cls"
else:
    clearcommand = "clear"

config = 0
tadc = 0
wordnum = 0
checkbook = 0

config_file = Path("./wpm.timetoread")
while config == 0:    
    if config_file.is_file():
        with open(config_file, "r") as f:
            wpm = f.read()
            f.close()
        config = 1
    else:
        wpm = input("Enter your avarage WPM: ")
        if wpm.isdigit():
            with open(config_file, "w") as f:
                f.write(wpm)
                f.close()
            config = 1
        else:
            print("Invalid WPM")
            time.sleep(0.5)
            config = 0
        
time_a_dayp = Path("./readingtime.timetoread")
while tadc == 0:
    if time_a_dayp.is_file():
        with open(time_a_dayp, 'r') as f:
            tad = f.read()
            f.close()
        tadc = 1
    else:
        tad = input("Enter your average reading time per day (In minutes): ")
        if tad.isdigit():
            with open(time_a_dayp, 'w') as f:
                f.write(tad)
                f.close()
            config = 1
        else:
            print('Invalid time')
            time.sleep(0.5)
            config = 0

forp = input("File or Pages?:")

if forp.lower() == "file":
    while checkbook == 0:
        bookpath = input("Enter the path to the book: ")
        bookpath = bookpath.replace('"', '')
        if Path(bookpath).is_file():
            checkbook = 1
        else:
            print(str(bookpath) + ' does not exist')
            time.sleep(0.5)
            checkbook = 0

    print('% Processing %')

    if bookpath.endswith(".epub"):
        wordnum = 0
        book = open_book(bookpath)
        lines = convert_epub_to_lines(book)
        convert_lines_to_text(lines)
        lines = str(lines)
        cleanlst = re.compile('<.*?>')
        lines = re.sub(cleanlst, '', lines)
        wordcount = lines.split()
        for wordcount in wordcount:
            wordnum += 1

    if bookpath.endswith(".pdf"):
        rsrcmgr = PDFResourceManager()
        sio = StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pdf_file = bookpath
        pdfFile = open(pdf_file, "rb")
        for page in PDFPage.get_pages(pdfFile):
            interpreter.process_page(page) 
        text = sio.getvalue()
        device.close()
        pdfFile.close()
        sio.close()
        wordcount = text.split()
        for wordcount in wordcount:
            wordnum = wordnum + 1

    if bookpath.endswith(".txt"):
        wordnum = 0
        with open(bookpath, "r") as f:
            lines = f.read()
            f.close()
        wordcount = lines.split()
        for wordcount in wordcount:
            wordnum += 1

    elif bookpath.endswith(".epub") == False and bookpath.endswith(".pdf") == False and bookpath.endswith(".txt") == False:
        print("Unsupported file type")
        time.sleep(2)
        exit()
if forp.lower() == "file":
    os.system(clearcommand)
    total_time_to_read_h = (int(wordnum) / int(wpm)) / 60
    total_time_to_read_h = round(total_time_to_read_h, 2)
    print(str(bookpath) + "'s total time to read would be " + str(total_time_to_read_h) + " hours")
    total_time_to_read_in_half_h = (int(wordnum) / int(wpm)) / 30
    total_time_to_read_in_half_h = round(total_time_to_read_in_half_h, 1)
    print('That means that it would take ' + str(total_time_to_read_in_half_h) + ' half hour sessions of reading')
    days = int(wordnum) / int(wpm) / int(tad)
    days = round(days, 1)
    print('Assuming that you would read around ' + str(tad) + ' minutes a day it would take you ' + str(days) + ' days to finish this book')

    
elif forp.lower() == "pages":
    pages = input("Enter the number of pages: ")
    if pages.isdigit():
        wordnum = int(pages) * 300
    os.system(clearcommand)
    total_time_to_read_h = (int(wordnum) / int(wpm)) / 60
    total_time_to_read_h = round(total_time_to_read_h, 2)
    print("Your books's total time to read would be " + str(total_time_to_read_h) + " hours")
    total_time_to_read_in_half_h = (int(wordnum) / int(wpm)) / 30
    total_time_to_read_in_half_h = round(total_time_to_read_in_half_h, 1)
    print('That means that it would take ' + str(total_time_to_read_in_half_h) + ' half hour sessions of reading')
    days = int(wordnum) / int(wpm) / int(tad)
    days = round(days, 1)
    print('Assuming that you would read around ' + str(tad) + ' minutes a day it would take you ' + str(days) + ' days to finish this book')

print("\n")
x = input("Press enter to exit")