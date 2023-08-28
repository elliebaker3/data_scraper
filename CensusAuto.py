from sys import argv
import pdb
import os
#import cv2 
import pandas as pd
from PIL import Image
import pytesseract as pt
import fitz  # pip install PyMuPDF
from skimage import morphology
import numpy as np
#from ImagePrepPC51 import ImagePrepPC51
import pandas as pd
from IPython.display import display
import layoutparser as lp
from numpy import asarray
# set filepath for tesseract dictionary
# # this will need to be set custom to your system (if you are using tesseract)
os.environ['TESSDATA_PREFIX']= "/usr/local/share/tessdata"

for i in range(int(argv[3]) - int(argv[2])):
    doc_num = int(argv[2]) + i
    district = str(argv[4])
    exitCode = os.system("python main.py one.pdf True {} {}".format(doc_num, district))
    print(exitCode)
