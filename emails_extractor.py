import numpy as np 
# from matplotlib import pyplot as plt
from pdfminer3.layout import LAParams #LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
# from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
from pathlib import Path
import io
import sys
from tqdm import tqdm
# must be a loop . but for now one pic is enough 
# nzid pdf , w characters 
#for verifying if file is an email 
import re
 

#init vars 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
fileregex = r'\b[A-Za-z0-9._%+-]+\.pdf\b'
word_number = 0
old = 0
def check_file(email):

    if(re.fullmatch(fileregex, email)):
        # print("Valid Email")
        return True
    else:
        # print("Invalid Email")
        return False
def check(email):

    if(re.fullmatch(regex, email)):
        # print("Valid Email")
        return True
    else:
        # print("Invalid Email")
        return False
# os.system('dir c:\\')
resource_manager = PDFResourceManager()
fake_file_handle = io.StringIO()
converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
page_interpreter = PDFPageInterpreter(resource_manager, converter)

#getting arguemnts 
n = len(sys.argv)
print("Total arguments passed:", n)

# Arguments passed
print("\nName of Python script:", sys.argv[0])

print("\nArguments passed:", end = " ")
for i in tqdm(range(1, n)):
    # print(sys.argv[i], end = " ")
    # print(type(sys.argv[i]) == type('str'))
    if (type(sys.argv[i]) == type('str')):
        if (check_file(sys.argv[i])):
            print( 'extracting emails from the file : ' + sys.argv[i].split('.')[0]   ) # + ' '+ sys.argv[i].split('.')[1]
            with open( sys.argv[i].split('.')[0]+'_liste_emails.txt', 'w') as f:
                with open(sys.argv[i], 'rb') as fh:
                    Pages = PDFPage.get_pages(fh,caching=True,check_extractable=True)
                    # incrementing = 0
                    for pageNumber,page in tqdm(enumerate(Pages)):

                        # must exclude last
                        print("progressing .... " + str(pageNumber+1))
                        text = ""
                        page_interpreter.process_page(page)
                        text = fake_file_handle.getvalue()
                        word_content = text.split().copy()
                        new = len(word_content)
                        # print("new : "+str(new))
                        # print(" old : "+str(old))
                        # print("current: "+str(new - old))
                        # print(word_content)
                        if pageNumber > 0 :
                            del word_content[0:old]
                        old += len(word_content)
                        print(len(word_content))
                        for word in word_content:
                            if check(word):
                                if "yhoo" in word:
                                    # print("correction de l;email ")
                                    word = word.replace("yhoo", "yahoo")
                                f.write(word)
                                
                                f.write("\n")
                                
                                print(word)
                    # close open handles
              
                
                fh.close()
            f.close()
    # if check_file(sys.argv[i]):
fake_file_handle.close()    
converter.close()
exit()
# Make a regular expression
# for validating an Email

