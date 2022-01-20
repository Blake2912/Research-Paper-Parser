import re
import os


def get_file_list_from_folder(folder_name):
    file_list = []
    try:
        for(files) in os.walk(str(folder_name),topdown=True):
            file_list = files[len(files) - 1]
        return file_list
    except:
        raise FileNotFoundError

def extract_reference_from_txt_file(path_of_txt_file,source_folder_name):
    txt_path = str(source_folder_name+"/"+path_of_txt_file)
    txt_file = open(txt_path,'r')
    ref_int = 0
    references = str("references/"+path_of_txt_file)
    try:
        ref_file = open(r"{}".format(references),"w")
        for i in txt_file:
            if ref_int == 1:
                ref_file.write(i)
            i = i.rstrip()

            if re.search(".*References|.*REFERENCES",i):
                ref_int=1
    except:
        try:
            os.mkdir('references')
        except:
            print("directory found!")
    txt_file.close()


folder_name = 'output'
file_list = get_file_list_from_folder(folder_name)
for i in file_list:
    extract_reference_from_txt_file(i,folder_name)