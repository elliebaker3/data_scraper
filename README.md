# data_scraper
### Transforming digitized text into meaningful data.
[Data Scraper Tech Talk Slides](https://docs.google.com/presentation/d/1sxa5Hi2GYrx1_uY6n696TyaZOA0UDpOAjR0OnclJq70/edit#slide=id.p)

Input: Folder containing pdfs of Census. 
Output: Folder with csvs for every page of each Census.

Note: If input pdfs do not have ocr'd text, ocring text will be a required first step of the process - this can be done in any standard pdf editor, like Adobe. To check if text is already ocr'd, see if you can highlight a section of text on a page, and copy and paste it. One common source of inaccuracy in this process is the ocr - a poor ocr means there will be many numbers that appear incorrectly as letters.

# Components
### Environment:
DDL's basic environment works! 
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

![](https://hackmd-prod-images.s3-ap-northeast-1.amazonaws.com/uploads/upload_b540a0cad07e863cfa4e79e4a80191ba.jpg?AWSAccessKeyId=AKIA3XSAAW6AWSKNINWO&Expires=1693232170&Signature=HPxfGCgF3v16WitVP4EeruDHuLE%3D)


**Output:** a dataframe that has a row for each block detected, with columns x0 y0 x1 y1 which indicate the coordinate of each detected block in pixels. This is also the information that layout parser uses to identify detected blocks. 

**Troubleshooting Tip and current problems with layout.py:** if the output csv is missing text that is clearly visible on the input pdf, check to make sure that layout.py is selecting the correct block to process. One way to do this is by reviewing the png with bounded boxes output - if these boxes don't capture the text you intended to process, then try using a different layout parser model. If the problem is still not identified, then try using words rather than cropped words in the following line of code in main.py, so the line looks like this: `df = pd.DataFrame(words)
` instead of this: `df = pd.DataFrame(cropped_words)
`. Words is the entire ocr text layer of the current pdf page assigned in this line of code in main.py: `words = page.get_text("words")`, whereas cropped_words is the ocr text layer within the bounding box identified in layout.py. 
The initial project for which this tool was created did not require the use of layout.py, so there are still some issues that need to be fixed for layout.py to work with the existing tool. Currently, when layout.py is used, some of the ocr'd text meant to be included in the final output csv does not appear in the output. Given that the bounding boxes displayed in the png are accurate, it seems there is an issue with either the integration of layout.py and its output into main.py, or with contents of the dataframe output from layout.py. Further investigation is necessary. 
For Census of India and any other documents where all, not some, of the text on a page should be processed it is recommended that code using layout.py is commented out (this is already done in the template code). Layout.py requires application of an object detection algorithm that substantially increases processing time. 

**Adjustable Parameters:** 
**modelType:** To inform your model choice, see further information about model types and layout training in this documentation: [Layout Parser Model Types](https://docs.google.com/document/d/1Oah_yv_gORY3SmzK6ZsaoZae9jURedcPjMOLDoCjYZs/edit)

### column.py
This file takes a dataframe containing ocr text data (coordinates, text, block, line numbers), an integer value indicating the distance at which text pieces should be considered part of distinct clusters, and 'linkage type' a string which determines which distance to use between sets of observation. It returns a dataframe of text pieces with coordinate and column information.
column.py assigns each text piece to a column using heirarchical agglomerative clustering, a type of clustering algorithm used in machine learning. In the case of the 1951 Census, the sets of observation are x coordinates (lower right corner) of text, the linkage type is average, and the distance metric is manhattan. 

**Input:** 
The following two variables are the most powerful determinents of how text is sorted.
1) **dist_thresh** is an integer variable or None which dictates the linkage distance threshold at or above which two text pieces X linkage distance apart will be considered part of separate columns. If this variable isn't None, n_clusters must be None. dist_thresh is assigned a value in the following line in main.py:
```
# definitions for section 3
dist_thresh = 8
```
3) **n_clusters** is an integer variable or None which indicates the number of columns to find. It must be None if dist_thresh is not none. n_clusters is assigned a value in the following line in main.py:
```
n_clusters = None
```
5) **df** is the dataframe containing ocr text data (coordinates, text, block, line numbers). This dataframe holds all text information, including row and column information determined for each text piece. This dataframe is what is ultimately converted into the final output csv for every page.
6) **linkage_type** is a string which indicates which linkage criterion to use. The linkage criterion determines which distance to use between pieces of text. The algorithm will merge the pairs of cluster (final clusters id'd are the columns) that minimize this criterion.
* ‘ward’ minimizes the variance of the clusters being merged.
* ‘average’ uses the average of the distances of each piece of text of the two sets.
* ‘complete’ or ‘maximum’ linkage uses the maximum distances between all pieces of text of the two sets.
* ‘single’ uses the minimum of the distances between all pieces of text of the two sets.

**Output:** 
**col_df:** is a dataframe containing all of the information included in the input dataframe, df, and additionally a new column, 'col' which indicates the column for each text piece.

**Troubleshooting Tip:**
If text to column/row assignment is not accurate, the first thing you should try is switching from using n_clusters to using dist_thresh, or vice versa. If there is still inaccuracy and you have decided to use dist_thresh, the second thing you should try is adjusting the dist_thresh parameter. Try extremes at first, then finetune once you've found the most accurate ballpark. dist_thresh and n_clusters are the two adjustable parameters with the biggest impact on the final output. The third most impactful adjustable parameter is xCoords.

**Adjustable Parameters:**
I recommend looking at output with both dist_thresh and n_clusters before deciding on use of one or the other.
**dist_thresh:** The smaller the value, the more distinct columns you get. Keep in mind that since this tool uses coordinates assigned to each text piece and stored in df as the input to the agglomerative clustering algorithm, the distance threshold unit is PyMuPDF defined text coordinates. I've found that for tightly spaced columns, 8 works well but it is DEFINTELY worth experimenting with this parameter. It also matters whether you would rather a misaligned text not be included in the output at all (if you've set the dist_thresh small enough a misaligned text piece will be a column all its own, and if you've set the min_cluster_size greater than 0 then this single item column will be eliminated from the final output).
**n_clusters:** Use this variable if the number of columns in tables you're analyzing is static, and you want text pieces to be "snapped" to their column of best fit. The risk with this variable (which is not present in dist_thresh) is the possibility that inaccurate column is identified as one of the N columns. 
**linkage_type:** More of a fine-tune on accuracy than the parameters above. When making this choice, think about the spread of the text pieces you want to be considered within the same column, and their relationship to text pieces in other columns. For example, if a few text pieces are misaligned, and you are using maximum linkage type, misaligned text pieces may have more impact on the final column than if you use single linkage type because as groups of text pieces are merged to form final columns, whether or not two groups of text will be merged is determined by the distance between the two farthest apart text pieces rather than the two nearest.
**min_cluster_size:** This integer variable is not an input parameter to column.py, but could be made so in an update of this tool. It indicates the minimum number (+1) of text pieces a cluster must contain to be considered a column. Remember that clusters are defined in the agglomerative clustering algorithm. Clusters that contain more text pieces than min_cluster_size are columns. 
**xCoords:** This variable's assignment is hardcoded because it is the same for all Census layout types encountered in this project thus far (a future version of this code should probably make this variable an input parameter to column.py). In the case of this code, as defined in the code following this sentence, xCoords is a list of the x1 (lower right hand corner) coordinate of each piece of text in df. More generally, xCoords is the list of observations that is used in the agglomerative clustering algorithm. In our case, it is important to use x1 (lower right hand corner) rather than x0 (upper left hand corner) because the numbers of the census (the text pieces) are right aligned (see below). ![](https://hackmd-prod-images.s3-ap-northeast-1.amazonaws.com/uploads/upload_97b0df1d0b1e25e6f6b3d0d10fbaf91b.png?AWSAccessKeyId=AKIA3XSAAW6AWSKNINWO&Expires=1693232313&Signature=eeb94TVhNyk4e%2BH9S0tqxCSEI00%3D)
### row.py
This file takes a dataframe containing an output of column.py, an indicator for whether the current Census page is LHS or RHS, and the original dataframe with ocr text data. It identifies a "key" column and finds the number and extent of every row in this column. It then moves through all the text pieces in the dataframe df, and assigns each piece to the key row of best fit. This function uses Bayes to adjust the extent of rows based on new text pieces added to a row, which addresses skew issues in pdfs. It returns a dataframe of text pieces with coordinate and row information. 

**Input:**
**df:** is exactly the same as the df input to column.py above. To reiterate, df is the dataframe containing ocr text data (coordinates, text, block, line numbers). This dataframe holds all text information, including row and column information determined for each text piece. This dataframe is what is ultimately converted into the final output csv for every page.

**df_row_input:** is another col_df output from column.py. This output is assigned the variable name df_row_input. df_row_input is necessary because row.py using a particular column as a "key" to identify the number of rows and their extent for a pdf page. This key, oftentimes the ID column of a pdf, must not contain any extraneous (and incorrect) text entries. A good way of ensuring this is by setting dist_thresh very low when calling the function in column.py. As mentioned earlier, this will ensure that values which are misaligned with columns are eliminated. 

**page_type:** 

**Output:**
**df:**

**Adjustable Parameters:**

### Post Processing:
For a pdf that has generally good initial formatting, it's very likely postprocessing will be unecessary. However, for a pdf like the 1951 Census of India, postprocessing was necessary. The two scripts below are very specific to the issues present in the 1951 Census, but could be a good starting place for post processing future projects.

### postProcessing.py

### combo.py

### dataclean.py

# Example
Use this tool to scrape the information from a new Census, with pages that are as pictured below:
![](https://hackmd-prod-images.s3-ap-northeast-1.amazonaws.com/uploads/upload_562f8a75e1b4c652ecd2a6c4a867e63d.png?AWSAccessKeyId=AKIA3XSAAW6AWSKNINWO&Expires=1693232369&Signature=20zZEL%2Bt2q%2FhYMrbSsU3ioXh8bM%3D)
* Because the columns and rows are so consistent in this census, minimal tweaking was necessary. I followed steps 1-8 in the step by step below, and found that the output contained accurate information but there were too many columns. 
* Columns 2, 3, and 4 were each being read as 2 columns. So, I adjusted dist_thresh from 8 to 20. At this point, column 2 was still be read as two columns, though columns 3 and 4 were now being read as 1 column each. 
* I adjusted dist_thresh again, this time to 50, and the output was *almost* correct. Some of the words in columns 2, 3, and 4 were out of order, though they were always in the correct row. 
* I added a line in main.py to sort text pieces by their x0 coordinate. Since the text pieces are grouped by row and column afterwards, this addition correctly sorts the words included in each csv cell. 
* The output is now extremely accurate!
# Step by Step
1) Download the source code for the data scraper from its github repo: [data_scraper](https://github.com/elliebaker3/data_scraper).
2) Identify the pdfs you would like to scrape.
3) Put all the pdfs in a folder, titled whatever you would like.
4) For each pdf, indicate the pages within the pdf that you would like scraped, then name each pdf startPage_endPage_name.pdf where name is however you would like that pdf to be identified in the final output (the output title will be final_output_pageType_name.pdf[pageNumber].csv) where pageType is RHS or LHS).
5) In Auto.py, update the input folder with the names of your folder:
Input folder updates:
```
districts = os.listdir('[YOUR INPUT FOLDER NAME]')
...
if(districtT != '[YOUR INPUT FOLDER NAME]'):
```
6) Make an output folder which will hold the csvs of the pdf page inputs.
7) In main.py, update the output folder name:
```
# save the page object as a png using a pixmap
page.get_pixmap(dpi=300, alpha=False).pil_save("[YOUR OUTPUT FOLDER NAME]/input{}{}.png".format(district, doc_num))

# open the png in correct format for layoutparser
img = Image.open("[YOUR OUTPUT FOLDER NAME]/input{}{}.png".format(district, doc_num)).convert('RGB')
...
filepath = '[YOUR OUTPUT FOLDER NAME]/final_output{}{}{}.csv'.format(page_type, district, doc_num)
```
8) Run Auto.py
9) Check a few pages of output against their input (input and output pages are next to each other in the output folder, if you sort by "last modified" - this allows for easier accuracy checking). How do they look? If columns are globbed together, consider lowering dist_thresh. If columns are separated when they shouldn't be, consider increasing dist_thresh. If neither of these fixes work, try setting dist_thresh to None and using n_clusters (only if you know the correct # of columns and it's consistent). Is the text right or left aligned? Adjust xCoord accordingly. Are text pieces being assigned to incorrect rows? Adjust theta in row.py. 
10) Run Auto.py again with adjustments.
11) If there are still innaccuracies after a few rounds of adjusting parameters, then consider postprocessing. 
# Future Improvements
