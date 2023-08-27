# data_scraper
Code and instructions for application of a flexible tool for collecting archival data. The tool transforms digitized text into meaningful data.
[Data Transformation Tool Tech Talk Slides](https://docs.google.com/presentation/d/1sxa5Hi2GYrx1_uY6n696TyaZOA0UDpOAjR0OnclJq70/edit#slide=id.p)

Input: Folder containing pdfs of Census. 
Output: Folder with csvs for every page of each Census.

Note: If input pdfs do not have ocr'd text, ocring text will be a required first step of the process - this can be done in any standard pdf editor, like Adobe. To check if text is already ocr'd, see if you can highlight a section of text on a page, and copy and paste it. One common source of inaccuracy in this process is the ocr - a poor ocr means there will be many numbers that appear incorrectly as letters.

# Components
### Set Up:
**Input:** Folder containing pdfs of Census. Each Census pdf title should indicate the first and last page number on which to parse data and a title that will identify the Census. For example, "445_638_Midnapur.pdf".

**Output:** Folder with CSVs for every page of each Census. 
### auto.py
This file takes the input folder. 
It parses the titles of each folder and includes them as arguments when calling censusAuto.py for each Census.
### censusAuto.py
Called by auto.py, this file takes a pdf of one Census, the name of the State the Census covers, and the start and end page of data to be extracted from the Census. 
It calls main.py for each page of the Census.

### Census Parsing:
### main.py
This file takes a Census pdf, option for verbose debug mode, Census District name, and Census page number. When involved in the automated workflow of this toolkit, main is called by censusAuto.py. main.py outputs a csv file containing data from one Census page.
main.py is mainly used to call the three functions below, which do the actual Census parsing. Main combines the outputs of layout, column, and row to produce a csv containing row, column, and value data (in table format) for every text piece of a given Census page.
### layout.py
Currently unused in the Census 1951 workflow, this file can be called to identify a table when the input page contains extraneous text. layout.py uses a pre-trained layout parser model to identify a table, then includes code to extract the coordinates of the table and returns them in a pandas dataframe. It is also possible to customize the layout parser model to identify different objects. Currently there are some issues with layout.py's integration into the data transformation tool, described in more detail below. However, I'm guessing these issues are more pesky debugging than fundamental problems with layout.py.

**Input:** 
1) **img** is a version of the input pdf page in the correct form for layout parser to read. It is assigned by this line of code in main.py: 
``` img = Image.open('page.png').convert('RGB')``` 
2) **modelType** is a string that indicates the layout parser model to be used to identify text for processing. For more information about layout parser see [Layout Parser Documentation](https://layout-parser.readthedocs.io/en/latest/notes/modelzoo.html#example-usage). It is assigned by this line of code in main.py: 
```modelType = "tableBank"```
The linked layout parser documentation shows available models. To add a new model, within layout.py add another if statement of the same form as the following:
    ```
    # select layout parser model and set parameters
    if modelType == "tableBank":
        model = lp.Detectron2LayoutModel(
            config_path = 'lp://TableBank/faster_rcnn_R_101_FPN_3x/config', # In model catalog
            label_map = {0: "Table"}, # In model`label_map`
            extra_config = ["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.7] # Optional
        )
    ```
    
    It is also possible to add a custom model. This process so far has yielded less accurate outcomes than provided models. [Tutorial for customizing a layout parser model](https://github.com/Layout-Parser/layout-parser/blob/main/examples/Customizing%20Layout%20Models%20with%20Label%20Studio%20Annotation/Customizing%20Layout%20Models%20with%20Label%20Studio%20Annotation.ipynb).
3) **verbose** is a boolean that determines whether or not detailed information about layout detection is presented. Specifically, setting verbose to true means a png with boxes indicating detected layouts is saved to the project directory. Below is an example of two such pngs. 

![](https://hackmd.io/_uploads/B1dOGdf6n.jpg)



**Output:** a dataframe that has a row for each block detected, with columns x0 y0 x1 y1 which indicate the coordinate of each detected block in pixels. This is also the information that layout parser uses to identify detected blocks. 

**Troubleshooting Tip and current problems with layout.py:** if the output csv is missing text that is clearly visible on the input pdf, check to make sure that layout.py is selecting the correct block to process. One way to do this is by reviewing the png with bounded boxes output - if these boxes don't capture the text you intended to process, then try using a different layout parser model. If the problem is still not identified, then try using words rather than cropped words in the following line of code in main.py, so the line looks like this: `df = pd.DataFrame(words)
` instead of this: `df = pd.DataFrame(cropped_words)
`. Words is the entire ocr text layer of the current pdf page assigned in this line of code in main.py: `words = page.get_text("words")`, whereas cropped_words is the ocr text layer within the bounding box identified in layout.py. 
The initial project for which this tool was created did not require the use of layout.py, so there are still some issues that need to be fixed for layout.py to work with the existing tool. Currently, when layout.py is used, some of the ocr'd text meant to be included in the final output csv does not appear in the output. Given that the bounding boxes displayed in the png are accurate, it seems there is an issue with either the integration of layout.py and its output into main.py, or with contents of the dataframe output from layout.py. Further investigation is necessary. 
For Census of India and any other documents where all 

**Adjustable Parameters:** 


### column.py
This file takes a dataframe containing ocr text data (coordinates, text, block, line numbers), an integer value indicating the distance at which text pieces should be considered part of distinct clusters, and 'linkage type' a string which determines which distance to use between sets of observation. It returns a dataframe of text pieces with coordinate and column information.
column.py assigns each text piece to a column using heirarchical agglomerative clustering, a type of clustering algorithm used in machine learning. In the case of the 1951 Census, the sets of observation are x coordinates (lower right corner) of text, the linkage type is average, and the distance metric is manhattan. 

**Input:**
**Output:**
**Adjustable Parameters:**

### row.py
This file takes a dataframe containing an output of column.py, an indicator for whether the current Census page is LHS or RHS, and the original dataframe with ocr text data. It returns a dataframe of text pieces with coordinate and row information. 

**Input:**
**Output:**
**Adjustable Parameters:**

### Post Processing:

### postProcessing.py

### combo.py

# Example

# Future Improvements
