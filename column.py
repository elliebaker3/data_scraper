from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import numpy as np
from tabulate import tabulate
import pdb

# given a dataframe from ocr'd text and AC parameters, assign each piece of text a column using HAC
# return a dataframe with x0, y0, and column information
def columnDetection(df, dist_thresh, linkage_type):
    #pdb.set_trace()
    # create the column dataframe which will be returned after column assignment
    col_df = df[['x1', 'y0', 'y1', 'text']]
    col_df['col'] = None
    # select the x coordinates from the df and convert them to correct format for HAC
    xCoords = col_df.apply(lambda x: (x['x1'], 0), axis=1)
    xCoords = xCoords.values.tolist()
    # apply hierarchical agglomerative clustering to the coordinates
    clustering = AgglomerativeClustering(
        n_clusters=None,
        affinity="manhattan", # manhattan
        linkage=linkage_type,
        distance_threshold=dist_thresh)
    clustering.fit(xCoords)
    
    
    # initialize our list of sorted clusters
    sortedClusters = []
    min_cluster_size = 2
    # loop over all clusters
    for l in np.unique(clustering.labels_):
        # extract the indexes for the coordinates belonging to the
        # current cluster
        idxs = np.where(clustering.labels_ == l)[0]
        # verify that the cluster is sufficiently large
        if len(idxs) > min_cluster_size:
            # compute the average x-coordinate value of the cluster and
            # update our clusters list with the current label and the
            # average x-coordinate
            avg = np.average([df.loc[idxs,'x0']])
            sortedClusters.append((l, avg))
    # sort the clusters by their average x-coordinate and initialize our
    # data frame
    sortedClusters.sort(key=lambda x: x[1])

    col_num = 0
    # loop over the clusters again, this time in sorted order
    for (l, _) in sortedClusters:
        # extract the indexes for the coordinates belonging to the
        # current cluster
        idxs = np.where(clustering.labels_ == l)[0]
        col_df.loc[idxs, 'col'] = col_num
        col_num = col_num + 1
        
    # replace NaN values with an empty string and then show a nicely
    # formatted version of our multi-column OCR'd text
    df.fillna("", inplace=True)
    #pdb.set_trace()
    return col_df
