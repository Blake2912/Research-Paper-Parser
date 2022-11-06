from os import mkdir, walk
from pdfminer.high_level import extract_text

import re
"""
***************************
  CONVERT PDF TO TXT CODE
***************************
"""
def remove_pdf_extension(string):
    string = str(string)
    string = string.split('.')
    return string[0]

def extract_text1(pdf_name):
    text = extract_text(pdf_name)
    return text

def save_in_txt_files(pdf_path):
    """
    Points to be noted while passing the pdf_name...
        1. The pdf_name is the pdf path like => Repository/pdf_name.pdf
    """
    print(pdf_path)
    path_splits = pdf_path.split("/")
    filepath = str("output/"+remove_pdf_extension(path_splits[len(path_splits)-1])+".txt")
    try:
        file = open(r"{}".format(filepath),"w")
        text = extract_text1(pdf_path)
        text = str(text)
        file.write(text)
        file.close()
        return text
    except:
        mkdir('output')

def get_file_list_from_folder(folder_name):
    file_list = []
    try:
        for(files) in walk(str(folder_name),topdown=True):
            file_list = files[len(files) - 1]
            # Code for cleaning up the file list remove all files starting with ._
            for i in file_list:
                if i.startswith("._"):
                    file_list.remove(i)
        return file_list
    except:
        raise FileNotFoundError

"""
*************************
    EXTRACT HEADINGS
*************************
"""
def extract_headings(text):
    """
        This function will find any headings in the text file. The regular expression finds the
    string with a number at the start following a period, following a space, following a alphanumberic characters

    Args: String - text
    Return: List(String)
    """
    line_list = []
    heading_list = []
    line_list = str(text).split("\n")
    for i in line_list:
        matchOject = re.compile(r'^[0-9]\.+\s+\w+[\s\w]+')
        temp_heading = matchOject.findall(i)
        if temp_heading != []:
            for i in temp_heading:
                heading_list.append(i)
    return heading_list

def extract_heading_in_list(path_to_txt_file):
    with open(path_to_txt_file,"r") as f:
        content = f.read()
        headings = extract_headings(content)
        f.close()
        return headings

def get_headings_from_list(txt_file_list,txt_folder_name):
    heading_frequency_dict = {}
    replaceObject = re.compile(r'^[0-9]\.+\s+')
    for i in txt_file_list:
        heading_list = extract_heading_in_list("{0}/{1}".format(txt_folder_name,i))
        for j in heading_list:
            processed_txt = replaceObject.split(j)
            processed_heading = processed_txt[len(processed_txt) - 1].upper().strip()
            # print(processed_heading)
            if processed_heading in heading_frequency_dict:
                heading_frequency_dict[processed_heading] += 1
            else:
                heading_frequency_dict[processed_heading] = 1
    print(heading_frequency_dict,end='\n')


if __name__ == '__main__':
    option = int(input(
        """
        What operation do you want to perform select the appropriate option
            1. To setup the repository, convert the pdf data files to text
            2. To extract headings and display its frequency
            3. To extract references

        Enter the number for performing the given operation:
        """
    ))
    if option == 1:
        folder_name = str(input("Enter the folder name which has the pdf files: "))
        file_list = get_file_list_from_folder(folder_name)
        for pdf_path in file_list:
            save_in_txt_files("{0}/{1}".format(folder_name,pdf_path))
    elif option == 2:
        # NOTE 1: GET YOUR PDF AND TXT FILES SETUP BEFORE RUNNING THIS OPTION
        # NOTE 2: THIS IS A GENERATED FOLDER IT WILL BE GENERATED SO NEED OF CHANGING THE FOLDER NAME
        folder_name = 'output'
        file_list = get_file_list_from_folder(folder_name)
        get_headings_from_list(file_list,folder_name)

        
