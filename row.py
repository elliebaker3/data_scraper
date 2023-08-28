import pandas as pd
import numpy as np
import pdb


# maybe the issue is I have to sort by left to right before applying bayes

# check if all characters of cell are digits
def contains_number(item):
    item = str(item)
    return item.isdigit()
  
def is_nan(item):
    item = str(item)
    return item == "nan"


def rowDetection(df, df_row_input, page_type):
    perc_num = 0
    max_num = 0
    max_col = 0
    # ------------------------------------------------------------------- #
    # get the row key: in this case the first column which is 90% numbers #
    # ------------------------------------------------------------------- #
    # currently always set to LHS
    if page_type == "LHS":
        sorted_cols = df_row_input['col'].unique()
        sorted_cols = sorted_cols.tolist()
        while None in sorted_cols:
            sorted_cols.remove(None)
        sorted_cols.sort()
        # for every column in the dataframe
        for col in sorted_cols:
            page_df = df_row_input[df_row_input['col'] == col]
            # if it's a long page
            if len(page_df) > 30:
                # if the column that is 90% #s hasn't been hit
                if perc_num < 50:
                    # get a T/F array of whether all chars of value are digits
                    perc_num = page_df['text'].astype(str).apply(contains_number)
                    # get a T/F array of whether value is nan or is not
                    perc_nan = page_df['text'].astype(str).apply(is_nan)
                    # get the percent of the non-nan values in a column that are numbers
                    perc_num = (perc_num.sum() / (perc_nan.count() - perc_nan.sum())) * 100
                    key_col = col
                    if perc_num > max_num:
                        max_num = perc_num
                        max_col = col

    # if there is no column that is 90% numbers...
    if max_num < 50:
        # assign the first column as a key
        key_col = 0

    # --------------------------------------- #
    # create a row dataframe from the row key #
    # --------------------------------------- #
    # create a dataframe with just information about the rows
    #rdf_int = df_row_input.copy()
    # get the key column from df_row_input
    rdf_int = df_row_input[['y0', 'y1', 'x1', 'text', 'col']]
    # crop the row dataframe to just include the key column
    rdf_int = rdf_int[rdf_int['col'] == key_col]
    # make a copy so that the rdf dataframe can be manipulated / it's not just a slice of df_row_input
    rdf = rdf_int.copy()
    #pdb.set_trace()
    rdf.reset_index(inplace=True, drop=True)
    rdf['row'] = rdf.index
    # get y midpoint for each row
    rdf['ymid'] = np.mean(rdf[['y0', 'y1']], axis=1)
    
    # make an array for each row that describes the full height of the column
    rdf["rowarray"] = rdf.apply(lambda row: np.arange(np.round(row["y0"]), np.round(row["y1"]+1)), axis=1)


    def updateRow(row, rdf, theta, rowind):
        rdf.at[rowind[0], 'ymid'] = theta * rdf.loc[rowind[0], "ymid"] + ((1-theta) * np.mean(row[['y0', 'y1']]))
        rdf.at[rowind[0], 'y0'] = theta * rdf.loc[rowind[0], "y0"] + ((1-theta) * row['y0'])
        rdf.at[rowind[0], 'y1'] = theta * rdf.loc[rowind[0], "y1"] + ((1-theta) * row['y1'])
        rdf.at[rowind[0], 'rowarray'] = np.arange(np.round(rdf.loc[rowind[0], "y0"]), np.round(rdf.loc[rowind[0], "y1"]+1))
        return rdf
    
    # ------------- #
    # 6 Assign rows #
    # ------------- #
    def match_to_row(row, rdf, theta, count):
        """
        Compare the y coords for each piece of text data
        to the coords determined for the rows. Determine the
        percentage overlap with this piece of text and every row,
        then pick the maximum overlap.
        """
        # create the array for the width of the piece of text data
        txtarray = np.arange(np.round(row["y0"]), np.round(row["y1"]))
        
        # calculate the overlap between the txtarray and each row wrt the txt array
        rdf["overlap"] = rdf["rowarray"].apply(
            lambda y: len(np.intersect1d(y, txtarray)) / len(txtarray)
        )
        # calculate the overlap between the txtarray and each row wrt each row
        rdf["overlap2"] = rdf["rowarray"].apply(
            lambda y: len(np.intersect1d(y, txtarray)) / len(y)
        )
        
        # find the index in which the overlap is maximized
        rowind = rdf.loc[rdf["overlap"] == rdf["overlap"].max()].index
        
        # check if there were multiple matches
        if len(rowind) > 1:
            rowind = rdf[rdf["overlap2"] == rdf.loc[rowind, "overlap2"].max()].index

        # isolate the row from the selected index
        r = rdf.loc[rowind[0], "row"]
        
        # if the sum is 0, then there is no overlap with any row
        # and the text data falls outside the row
        if rdf["overlap"].sum() == 0:
            r = np.nan
        else:
            rdf = updateRow(row, rdf, theta, rowind)
        return r
    
    df = df.sort_values(by=["col", "y0"]).reset_index(drop=True)
    # assign each piece of text to the proper row
    df['row'] = df.apply(lambda row: match_to_row(row, rdf, .9, 0), axis=1)
    df = df[['y0', 'x1', 'row', 'text']]
    #pdb.set_trace()
    return df

