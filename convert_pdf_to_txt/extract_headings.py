# Extracting  the headings from text files
import pdf_to_txt
import re

def execute_pdf_to_text(path_to_pdf):
    """
    This function runs the pdf_to_txt script
    It will convert pdf to txt.
    returns: string
    """
    text = pdf_to_txt.save_in_txt_files(path_to_pdf)
    return text


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
    # print("HEADINGS:")
    # print(heading_list)
    return heading_list

def convert_to_single_string(headings):
    return ' '.join(headings)

def extract_heading_in_single_line(path_to_pdf):
    content = execute_pdf_to_text(path_to_pdf)
    headings = extract_headings(content)
    single_lined_heading = convert_to_single_string(headings)
    return single_lined_heading


def extract_heading_in_list(path_to_pdf):
    content = execute_pdf_to_text(path_to_pdf)
    headings = extract_headings(content)
    return headings


# Give the path instead of the given path in the variable path_to_pdf, and run the code
path_to_pdf = "Repository/research_paper4.pdf"
print(extract_heading_in_list(path_to_pdf))
