import os

"""
The following code is to perform cleanup in the files and remove all unwanted empty files.
**** RUN WITH CAUTION THIS CODE WILL PERMANENTLY DELETE THE FILE WRITE THE FILENAME WITH OUT SPELLING MISTAKE **** 
"""
def browse_the_folder(folder_name):
    file_list = []
    temp_file_list = []
    try:
        for(files) in os.walk(str(folder_name),topdown=True):
            temp_file_list = files[len(files) - 1]
            for i in temp_file_list:
                file_list.append(files[0]+'/'+i)
        return file_list
    except:
        print("folder not found!")
        raise FileNotFoundError

def perform_cleanup(file_name):
    if os.path.getsize(file_name) == 0:
        print("Deleting the file: {0}".format(file_name))
        os.remove(file_name)


cleanup_folder = input("Enter the path of the folder to cleanup: ")
file_list = browse_the_folder(cleanup_folder)
# print(file_list)
if file_list == []:
    print("Folder Not Found!")
else:
    for i in file_list:
        perform_cleanup(i)

