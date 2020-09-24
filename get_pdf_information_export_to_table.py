import os
import PyPDF2
import tabula
import csv
'''
    For the given path, get the List of all files in the directory tree 
'''


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def main():
    dirName = './mass_dot_gov_pdfs'

    '''
    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)

    # Print the files
    for elem in listOfFiles:
        print(elem)
    print("****************")
    '''
    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    pdf_files = list()
    # Print the files
    for elem in listOfFiles:
        # Check if we get the pdf
        if elem[-4:] == '.pdf':
            pdf_files.append(elem)

    for elem in pdf_files:
        '''
        pdfFileObj = open(elem, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # number of pages in pdf
        print(pdfReader.numPages)
        # a page object
        pageObj = pdfReader.getPage(0)
        # extracting text from page.
        # this will print the text you can also save that into String
        print(pageObj.extractText())
        '''
        # readinf the PDF file that contain Table Data
        # you can find find the pdf file with complete code in below
        # read_pdf will save the pdf table into Pandas Dataframe
        df = tabula.read_pdf(elem)
        print(elem[:-4])
        df.to_csv('./mass_dot_gov_csv/' + elem[:-4] + ".csv", index=False)



if __name__ == '__main__':
    main()