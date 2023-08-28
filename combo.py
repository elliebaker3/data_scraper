import os
import pandas as pd
import re
import pdb
import numpy as np

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


def checkperiod(string):
    count = 0
    for char in string:
        if char == '.':
            count += 1
        if count > 1:
            return False
    return True

districts = ["Midnapur","Birbhum","Bankura","Darjeeling","Malda","Murshidabad","Burdwan","Nadia","WestDinajpur"]
 #["Akola","Amravati","Buldana","Bhandara","Raigarh","Wardha"] # mp w/o total pop
#["Bangalore","Chikmagalur","Hassan","Kolar","Mysore","Shimoga","Tumkur"]
# ["Bangalore","Chikmagalur","Hassan","Kolar","Mysore","Shimoga","Tumkur"]
#["Lucknow", "Bahraich","TehriGarhwal","Garhwal","Fatehpur","Sultanpur","Almora","Pilibhit","Sitapur","Ghazipur","Jalaun","Manipuri","Unnao","Hardoi","Pratapgarh","Banda","Kheri","Etah","Mirzapur","Hamirpur","Rampur","Farrukhabad","Rae","Basti","Gonda","Budaun","Etawah","Bareilly","Shahjahanpur","Bijnor","Faizabad","Mathura","Naini","Azamgarh","Gorakhpur","Jaunpur","Muzaffarnagar","Kanpur","Saharanpur","Jhansi","Meerut","Dehra","Moradabad","Allahabad","Agra"]
# ["Jaisalmer", "Pali", "Nagaur", "Sirohi", "Jodhpur", "Banswara", "Jhalawar", "Chittaurgarh", "Udaipur", "Jalor", "Barmer", "Bundi", "Sikar", "Jhunjhunu", "Bhilwara", "Jaipur"] #["Aurangabad","Bhilsa","Morena","Mandsaur","Parbhani","SataraSouth","Ujjain","Satara","Osmanabad","Sehore","Shivpuri","Jhabua","NorthSatara","Nimar","Raisen","Kolhapur","Solapur","Ratlam","Gird","Shajapur","Bhind","Nanded","Dewas","Dhar","Goona","Indore"] #["Akola","Amravati","Balaghat","Bastar","Betul","Bhandara","Bilaspur","Buldana","Chanda","Chhindwara","Durg","Hoshangabad","Jabalpur","Mandla","Raigarh","Raipur","Sagar","Surguja","Wardha"] #["Aurangabad","Bhilsa","Morena","Mandsaur","Parbhani","SataraSouth","Ujjain","Satara","Osmanabad","Sehore","Shivpuri","Jhabua","NorthSatara","Nimar","Raisen","Kolhapur","Solapur","Ratlam","Gird","Shajapur","Bhind","Nanded","Dewas","Dhar","Goona","Indore"]
for district_select in districts:
    # set the directory path for the folder containing the CSV files
    folder_path = "west_bengal_pp4"

    # create an empty list to hold the dataframes for each CSV file
    df_list = []
    df_manual_tehsil = pd.read_csv("manual_tehsil.csv")
    # loop through all CSV files in the folder and append their dataframes to the list
    count = 0
    for filename in os.listdir(folder_path):
        # just for bad namingi issue
        if '-' in filename:
            filename = filename.replace("-", "")
        match = re.search(r'final_output(\w+)\.pdf(\w+)\.csv.csv', filename)
        search_district = ""
        search_page_num = ""
        if match:
            search_district = match.group(1)
            search_district = search_district[3:]
            search_page_num = match.group(2)
        # just for the messed up name section
        else:
            #pdb.set_trace()
            match = re.search(r'final_output(\w+)\.csv.csv', filename)
            if match:
                search_district = match.group(1)[3:-3]
                search_page_num = match.group(1)[-3:]
            #else:
             #   pdb.set_trace()
        filtered_df = df_manual_tehsil[(df_manual_tehsil['Page #'] == float(search_page_num)) & (df_manual_tehsil['District'] == search_district)]
        if len(filtered_df) == 0:
            manual_tehsil = "not found"
        else:
            #pdb.set_trace()
            manual_tehsil = filtered_df['Tehsil'].iloc[0]
        if district_select in filename:
            #print(filename)
            #if district_select == 'Budaun':
             #   print(filename)
            #pdb.set_trace()
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            #df['filename'] = filename
            # only append dataframes with >10 rows
            if df.shape[0] > 10:

                if 'ID' not in df.columns:
                    pdb.set_trace()
                df_edit = df
                df_edit.drop(columns = 'tehsil')
                df_edit['tehsil'] = manual_tehsil
                # rename the numbered columns to 1, 2, 3
                #pdb.set_trace()
                if df_edit.columns[0] != 'district':
                    df_edit = df_edit.drop(columns = df_edit.columns[0])
                num_cols = [col for col in df_edit.columns if not col.isalpha()]
                num_cols_sorted = sorted(num_cols, key=lambda x: int(''.join(filter(str.isdigit, x))))
                rename_dict = {num_cols_sorted[i]: str(i+1) for i in range(len(num_cols_sorted))}
                df_edit = df_edit.rename(columns=rename_dict)
                #pdb.set_trace()
                df_edit = df_edit.rename(columns = {'1':'pc51_pca_land_tot','2':'pc51_pca_no_h','3':'pc51_pca_tot_p','4':'pc51_pca_p_lit'})
                # pc51_pca_village_name,pc51_pca_tehsil_name,pc51_pca_village_id,pc51_pca_t,pc51_pca_t_m,pc51_pca_t_f
                df_edit = df_edit.reset_index(drop=True)
                df_list.append(df_edit)
        #pdb.set_trace()



    #pdb.set_trace()
    # concatenate the dataframes in the list into a single dataframe
    if len(df_list) > 0:
        #duplicated_index = df_list.index.duplicated()
        concatenated_df = pd.DataFrame()
        count = 0
        for df in df_list:
            if not df.columns.duplicated().any():
                concatenated_df = pd.concat([df.astype(str), concatenated_df])
           # else:
            #    pdb.set_trace()
                print(df)
       # if district_select == 'Budaun':
        #    pdb.set_trace()
        concatenated_df = concatenated_df.reset_index(drop=True)
        concatenated_df.drop(columns=[concatenated_df.columns[0]], inplace=True)
        #concatenated_df.sort_values(by=['district'], inplace=True)
        # write the resulting dataframe to a new CSV file
        output_file_path = "west_bengal_post5/{}.csv".format(district_select)
        concatenated_df.to_csv(output_file_path, index=False)
    else:
        print("Error: no readable data for district {}".format(district_select))
