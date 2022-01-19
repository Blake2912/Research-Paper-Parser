from os import mkdir
from pdfminer.high_level import extract_text


def extract_text1(pdf_name):
    text = extract_text(pdf_name)
    return text

# The changes made here are that i am returning the text instead of saving it into a txt file.
# If required we can save it to a txt file and then use it.
def save_in_txt_files(pdf_name):
    print(pdf_name)
    path_splits = pdf_name.split("/")
    filepath = str("output/"+remove_pdf_extension(path_splits[len(path_splits)-1])+".txt")
    try:
        file = open(r"{}".format(filepath),"w")
        text = extract_text1(pdf_name)
        text = str(text)
        file.write(text)
        file.close()
        return text
    except:
        mkdir('output')


def remove_pdf_extension(string):
    string = str(string)
    string = string.split('.')
    return string[0]