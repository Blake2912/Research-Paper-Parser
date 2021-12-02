from pdfminer.high_level import extract_text
# import os


def extract_text1(pdf_name):
    text = extract_text(pdf_name)
    return text

# The changes made here are that i am returning the text instead of saving it into a txt file.
# If required we can save it to a txt file and then use it.
def save_in_txt_files(pdf_name):
    print(pdf_name)
    # path_splits = pdf_name.split("/")
    text = extract_text1(pdf_name)
    text = str(text)
    # filepath = str("output/"+path_splits[len(path_splits)-1]+".txt")
    # file = open(r"{}".format(filepath),"a")
    # print(text)
    # file.write(text)
    # file.close()
    return text

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