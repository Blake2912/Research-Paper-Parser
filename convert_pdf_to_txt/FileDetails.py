class FileDetails:
    """
    This is a data class that is storing the title and the file path of the corresponding file in db
    """
    def __init__(self,title,path,encoding_data):
        self.title = title
        self.path = path
        self.encoding_data = encoding_data
    