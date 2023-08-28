import layoutparser as lp
import pandas as pd
import sys

def tableDetection(img, modelType, verbose):
    directory_fp = '/Users/elliebaker/ddl/ocr/modelTest/modular/'
    # select layout parser model and set parameters
    if modelType == "tableBank":
        model = lp.Detectron2LayoutModel(
            config_path = 'lp://TableBank/faster_rcnn_R_101_FPN_3x/config', # In model catalog
            label_map = {0: "Table"}, # In model`label_map`
            extra_config = ["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.7] # Optional
        )
        # apply layout parser model to image to get layout parser block
        layout = model.detect(img)
        # get blocks from layout parser block
        text_blocks = lp.Layout([b for b in layout])
        # if no objects are detected, stop and display warning
        if len(text_blocks) == 0:
            print(f"Error: layout parser model {modelType} did not detect any layout objects")
            sys.exit()
        if len(text_blocks) > 1:
            print(f"Error: layout parser model {modelType} did not detect any layout objects")
            sys.exit()
        # verbose option prints and displays the objects detected
        if verbose:
            print("number of objects detected: {}".format(len(text_blocks)))
            # use layoutparser wrapper to display detected layout parser block
            imgDisplay = lp.draw_box(img, text_blocks,
            box_width=3)
            # save as layout to project directory
            layout_fp = directory_fp + 'layout.png'
            imgDisplay.save(layout_fp)
        # create a dataframe to hold block information
        df_blocks = pd.DataFrame()
        # read block information into dataframe
        i = 0
        # create columns for the dataframe
        df_blocks["x0"] = None
        df_blocks["y0"] = None
        df_blocks["x1"] = None
        df_blocks["y1"] = None

        for block in text_blocks:
            # get upper left and lower right coordinates of each layout parser block
            coords = block.coordinates
            df_blocks.loc[i, "x0"] = int(coords[0])
            df_blocks.loc[i, "y0"] = int(coords[1])
            df_blocks.loc[i, "x1"] = int(coords[2])
            df_blocks.loc[i, "y1"] = int(coords[3])
            i = i + 1

        # get the width of the page so upper left x is 0
        df_blocks.loc[i, "x0"] = 0
        # get the height of the page so upper left y is total height
        df_blocks.loc[i, "y0"] = img.height
        # get the width of the page so lower right x is width
        df_blocks.loc[i, "x1"] = img.width
        # the lower right y coordinate for the header block is the upper right y coordinate for the table block
        df_blocks.loc[i, "y1"] = df_blocks["y1"].loc[0]
    # return the data frame with layout parser block coordinates
    return df_blocks
