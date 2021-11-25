from pdfminer.high_level import extract_text
import os


def extract_text1(pdf_name):
    text = extract_text(pdf_name)
    return text

def save_in_txt_files(pdf_name):
    print(pdf_name)
    path_splits = pdf_name.split("/")
    text = extract_text1(pdf_name)
    filepath = str("output/"+path_splits[len(path_splits)-1]+".txt")
    file = open(r"{}".format(filepath),"a")
    print(text)
    file.write(text)
    file.close()

"""
************************************************************* 
    The commented lines below are the lines that are used 
    to scan a directory and get the text of multiple pdfs 
************************************************************* 
"""
# def scan_through_dir(dir_path):
#     files_list = []
#     for filename in os.scandir(dir_path):
#         if filename.is_file():
#             files_list.append(filename.path)
#     return files_list

# def do_every_thing_here(dir_path):
#     list_of_pdf = scan_through_dir(dir_path)
#     for i in list_of_pdf:
#         save_in_txt_files(i)


try:
    # Change '/' to '\' if you are using in windows for compatibilty if the code doesn't work
    os.mkdir('output/')
    save_in_txt_files("Repository/research_paper1.pdf")
    path_of_pdf = input("Enter the path of the pdf file that you want to convert to txt: ")
    # do_every_thing_here('Repository')
except:
    # do_every_thing_here('Repository')
    save_in_txt_files("Repository/research_paper1.pdf")
    path_of_pdf = input("Enter the path of the pdf file that you want to convert to txt: ")