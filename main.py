from layout import tableDetection
#from ocr import ocrText
from column import columnDetection
from row import rowDetection
from sys import argv
import fitz
from PIL import Image
import pandas as pd
import pdb
import re


def contains_chars(item):
    item = str(item)
    pattern = re.compile('[a-zA-Z]')
    matches = pattern.findall(item)
    num_chars = len(matches)
    if num_chars < 4:
        chars = False
    else:
        chars = True
    return chars


# ---------- #
# 0 Settings #
# ---------- #
# the model that Layout Parser will use to identify layout parser blocks for processing
modelType = "tableBank"
verbose = True
#argv[2]
# define the pdf
fn = "{}".format(argv[1])
doc_num = int(argv[3])
district = str(argv[4])

# --------------- #
# 1 Document Prep #
# --------------- #

# open the pdf
doc = fitz.open(fn)
# get page object for pixmap
page = doc[doc_num]
# get the ocr text layer from the pdf
# for better generalizability, add code here to ocr the text and assign to words object in case ocr text layer doesn't exist
# in the case below, words is list of items (x0, y0, x1, y1, "word", block_no, line_no, word_no)
words = page.get_text("words")

# ------------------------------------------------------------------ #
# 2 Layout Detection: (Tool: ML Object Detection - Layout Parser) #
# ------------------------------------------------------------------ #
# definitions for section 2
# prep the pdf to be compatible with layout parser

# save the page object as a png using a pixmap
page.get_pixmap(dpi=300, alpha=False).pil_save("newCensus_output/input{}{}.png".format(district, doc_num))

# open the png in correct format for layoutparser
img = Image.open("newCensus_output/input{}{}.png".format(district, doc_num)).convert('RGB')

# apply a layoutparser id algorithm to the image, and return a list of coordinate arrays for cropping
# the dataframe returned has a row for each block detected, with columns x0 y0 x1 y1 indicating coordinate in pixels

#bounding_coordinates = tableDetection(img, modelType, verbose)

# get the number of layout parser blocks
#num_blocks = len(bounding_coordinates)
# make an array to hold words from each layout parser block
#mywords = [''] * num_blocks
#i = 0

# get information about words (x0, y0, x1, y1, "word", block_no, line_no, word_no) within each layout parser block by cropping the extracted ocr text layer (words)
# crop is based on the coordinates of each layout parser block
#for i in range(num_blocks - 1):
        #mywords[i] = [w for w in words if fitz.Rect(w[:4]).intersects(fitz.Rect((bounding_coordinates["x0"].loc[i], bounding_coordinates["y0"].loc[i], bounding_coordinates["x1"].loc[i], bounding_coordinates["y1"].loc[i])))]


header = [w for w in words if fitz.Rect(w[:4]).intersects(fitz.Rect((0, 0, 2980, 150)))]

#cropped_words = [w for w in words if fitz.Rect(w[:4]).intersects(fitz.Rect((bounding_coordinates["x0"][0], bounding_coordinates["y0"][0], bounding_coordinates["x1"][0], bounding_coordinates["y1"][0])))]
# sort the list by x value
header.sort(key=lambda x: x[1])
# take the first seven items
header = header[:7]
header.sort(key=lambda x: x[0])
# assign just the text portion to new list
header = [x[4] for x in header]

header_string = " ".join(str(x) for x in header)

# ------------------------------------------------------------------------------------ #
# 3 Column Detection: (Tool: Heirarchical Agglomerative Clustering - Sci Kit Learn) #
# ------------------------------------------------------------------------------------ #
# definitions for section 3
dist_thresh = 50
linkage_type = "average"

# this will be mywords[0] once cropping is worked out
df = pd.DataFrame(words)

# set column names
df = df.rename(
    columns={
        0: 'x0',
        1: 'y0',
        2: 'x1',
        3: 'y1',
        4: 'text',
        5: 'block_no',
        6: 'line_no',
        7: 'word_no'
    }
)

# the column function takes an ocr dataframe and identifies clusters based on their relative distance from one another
# the dataframe returned is a key: item dataframe where key is column number and item is OCR'd text within the current column
# design decision: I chose to pass in full df from ocr text instead of necessary coords, then parse down within function. I think that df from ocr text is a common item. If it's not, could also just pass necessary coords
#pdb.set_trace()
df_columns = columnDetection(df, dist_thresh, linkage_type)

# ------------------------------------------------------------------------------------ #
# 3 Row Detection: (Tool: Naive Bayse - Python) #
# ------------------------------------------------------------------------------------ #

# get a column assignment that is more accurate for key purposes
df_row_input = columnDetection(df, 8, linkage_type)

df.sort_values(by=['y0'], ascending=[True], inplace=True)
#pdb.set_trace()
df_row_input = pd.merge(df, df_row_input, on=['x1', 'y0', 'y1', 'text'])

# determine if page is LHS or RHS:
# - use df_columns
# for 'text' column in items in each column
perc_character_max = 0
for col in df_columns['col'].unique():
    page_df = df_columns[df_columns['col'] == col]
    if len(page_df) > 30:
        # if there exists a column in the dataframe that is 90 percent words, this is a LHS page
        perc_character = page_df['text'].astype(str).replace('nan','').apply(contains_chars)
        #pdb.set_trace()
        perc_character = (perc_character.sum() / perc_character.count()) * 100
        if perc_character > perc_character_max:
            perc_character_max = perc_character

if perc_character_max > 50:
    page_type = "LHS"
else:
    page_type = "RHS"
print(page_type)



# need to merge this and df on x, y coordinates of text to add the "col" column to df
df = pd.merge(df, df_columns, on=['x1', 'y0', 'y1', 'text'])


df_rows = rowDetection(df, df_row_input, page_type)
print("got here")


df = pd.merge(df, df_rows, on=['x1', 'y0','text'])


df.sort_values(by=['y0'], ascending=[True], inplace=True)
# IMPORTANT: added this for the new census example... if there are issues with 1951 now this is the first thing to comment out
df.sort_values(by=['x0'], ascending=[True], inplace=True)


#pdb.set_trace()
final_text = df.groupby(['col', 'row'])['text'].apply(' '.join).reset_index()

# pivot the dataframe to align values by row and column
out_df = final_text.pivot(columns='col', index='row', values='text')
out_df['tehsil'] = header_string

filepath = 'newCensus_output/final_output{}{}{}.csv'.format(page_type, district, doc_num)
out_df.to_csv(filepath)


