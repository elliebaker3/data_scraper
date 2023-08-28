import os
import re
import pandas as pd
import pdb
import numpy as np


def contains_number(item):
    item = str(item)
    return ((item.isalpha() and not item == "nan"))

def non_number(item):
    item = str(item)
    return ((not item.isdigit() and not item == "nan"))

def contains_nan(item):
    item = str(item)
    return item == "nan"

def contains_num(item):
    item = str(item)
    return any(char.isdigit() for char in item)

def has_num(item):
    item = str(item)
    return any(char.isdigit() for char in item)


def contains_paren(item):
    item = str(item)
    pattern = re.compile('[()]')
    matches = pattern.findall(item)
    num_chars = len(matches)
    if num_chars < 1:
        chars = False
    else:
        chars = True
    return chars

def other_val_func(item):
    item = str(item)
    pattern = re.compile(r"[^\w\s]")
    matches = pattern.findall(item)
    num_chars = len(matches)
    if num_chars < 2:
        chars = False
    else:
        chars = True
    return chars


def contains_value(item):
    value = False
    item = str(item)
    if not item == "nan":
        value = True
    return value

# get all output
pages = os.listdir('westBengal')
# filter the input pages out
    
pages = [page for page in pages if 'output' in page]
pages.sort()
#pdb.set_trace()
sorted_pages = []
# sort output pages by district and page num
for page in pages:
    #if page == "final_outputDhar.pdf179.csv":
       # pdb.set_trace()
    fullname = page
    if "RHS" in page:
        page = page.replace("RHS", "")
    else:
        page = page.replace("LHS", "")

    match = re.search(r'final_output(\w+)\.pdf(\w+)\.csv', page)
    if match:
        district = match.group(1)
        page_num = match.group(2)
        sorted_pages.append((page, fullname, district, page_num))
    else:
        print("error file doesn't match expected name type")
df = pd.DataFrame(sorted_pages, columns=['name', 'fullname', 'district', 'page_num'])
df.sort_values(by=['district', 'page_num'], inplace=True)
pd.options.display.max_rows = 500
#pdb.set_trace()
#df['page_num'].to_csv('111testing.csv')
# split the dataframe by districts
grouped = df.groupby('district')



districts = ["Midnapur","Birbhum","Bankura","Darjeeling","Malda","Murshidabad","Burdwan","Nadia","WestDinajpur"]
# ["Surguja","Sagar","Raipur","Mandla","Jabalpur","Hoshangabad","Durg","Chhindwara","Chanda","Bilaspur","Betul","Bastar","Balaghat"] # mp w/o total
# ["Akola","Amravati","Buldana","Bhandara","Raigarh","Wardha"] # mh w/o total #["Akola","Amravati","Balaghat","Bastar","Betul","Bhandara","Bilaspur","Buldana","Chanda","Chhindwara","Durg","Hoshangabad","Jabalpur","Mandla","Raigarh","Raipur","Sagar","Surguja","Wardha","Aurangabad","Bhilsa","Morena","Mandsaur","Parbhani","SataraSouth","Ujjain","Satara","Osmanabad","Sehore","Shivpuri","Jhabua","NorthSatara","Nimar","Raisen","Kolhapur","Solapur","Ratlam","Gird","Shajapur","Bhind","Nanded","Dewas","Dhar","Goona","Indore"] # mh and mp

# ["Bangalore","Belgaum","Bidar","Bijapur","Chikmagalur","Gulbarga","Hassan","Kolar","Mysore","Raichur","Shimoga","Tumkur"] # karnataka
# ["Akola","Amravati","Aurangabad","Bhandara","Buldana","Kolhapur","Nanded","Osmanabad","Parbhani","Raigarh","Satara","SataraSouth","Solapur","Wardha"] # mh
# ["Ujjain","Shivpuri","Shajapur","Sehore","Ratlam","Raisen","NorthSatara","Nimar","Morena","Mandsaur","Jhabua","Indore","Goona","Gird","Dhar","Dewas","Bhind","Bhilsa","Surguja","Sagar","Raipur","Mandla","Jabalpur","Hoshangabad","Durg","Chhindwara","Chanda","Bilaspur","Betul","Bastar","Balaghat"] # mp
# ["Amreli","Banaskantha","Dangs","PanchMahals","Sabarkantha","Surat"] # gujarat
# ["Midnapur","Birbhum","Bankura","Darjeeling","Malda","Murshidabad","Burdwan","Nadia","WestDinajpur"] # west_bengal
# ["Agra","Allahabad","Almora","Azamgarh","Bahraich","Banda","Bareilly","Basti","Bijnor","Budaun","Dehra","Etah","Etawah","Faizabad","Farrukhabad","Fatehpur","Garhwal","Ghazipur","Gonda","Hamirpur","Hardoi","Jalaun","Jaunpur","Jhansi","Kanpur","Kheri","Lucknow","Manipuri","Mathura","Meerut","Mirzapur","Moradabad","Muzaffarnagar","Naini","Pilibhit","Pratapgarh","Rae","Rampur","Saharanpur","Shahjahanpur","Sitapur","Sultanpur","TehriGarhwal","Unnao"] # up
# ["Banswara","Barmer","Bhilwara","Bundi","Chittaurgarh","Jaipur","Jaisalmer","Jalor","Jhalawar","Jhunjhunu","Jodhpur","Nagaur","Pali","Sikar","Sirohi","Udaipur"] # rajasthan





#{"Jaisalmer": 12, "Pali": 12, "Nagaur": 12, "Sirohi":12, "Jodhpur": 12, "Banswara":12, "Jhalawar": 12, "Chittaurgarh": 12, "Udaipur":12, "Jalor": 12, "Barmer": 12, "Bundi": 12, "Sikar": 12, "Jhunjhunu":12, "Bhilwara": 12, "Jaipur": 12}
 #{"Akola":12,"Amravati":12,"Balaghat":12,"Bastar":12,"Betul":12,"Bhandara":12,"Bilaspur":12,"Buldana":12,"Chanda":12,"Chhindwara":12,"Durg":12,"Hoshangabad":12,"Jabalpur":12,"Mandla":12,"Raigarh":12,"Raipur":12,"Sagar":12,"Surguja":12,"Wardha":12,"Aurangabad":9,"Bhilsa":17,"Morena":17,"Mandsaur":17,"Parbhani":9,"SataraSouth":10,"Ujjain":17,"Satara":10,"Osmanabad":9,"Sehore":13,"Shivpuri":17,"Jhabua":17,"NorthSatara":10,"Nimar":17,"Raisen":13,"Kolhapur":10,"Solapur":10,"Ratlam":17,"Gird":17,"Shajapur":17,"Bhind":17,"Nanded":9,"Dewas":17,"Dhar":17,"Goona":17,"Indore":17}

for district_select in districts:
    # for every district in the data
    for name, group in grouped:
        # select a specific district
        if name == district_select:
            # for every page that is this district
            for i in range(0, len(group)):
                # read the page in as a csv
                df_LHS = pd.read_csv('westBengal/' + group[i:i+1]['fullname'].values[0])
                # format the page for intake
                df_LHS.drop(columns=['row'], inplace=True)
                # set up arrays for village name col id
                village_cols = []
                village_del = []
                village_cols_to_drop = []
                start_num = 200
                end_villages = False
                # for every column of the current page
                for col_num in range(len(df_LHS.columns)):
                    # convert to a string
                    df_LHS[df_LHS.columns[col_num]].astype(str)
                    # id the cells that contain only letters
                    perc_character = df_LHS[df_LHS.columns[col_num]].apply(contains_number)
                    # id the cells that have empty values
                    perc_nan = df_LHS[df_LHS.columns[col_num]].apply(contains_nan)
                    # of the values that are non-null, percent that are characters
                    perc_val_char = (perc_character.sum() / (perc_character.count() - perc_nan.sum())) * 100
                    # get the percent of a given column that contains cells that are only letters
                    perc_character = (perc_character.sum() / perc_character.count()) * 100
                    # get the percent of a given column that contains cells that are empty values
                    perc_nan = (perc_nan.sum() / perc_nan.count()) * 100
                      
                    # id the cells that have a numeric value
                    perc_num = df_LHS[df_LHS.columns[col_num]].apply(contains_num)
                    # get the percent of a given column that contains cells that have numeric value
                    perc_num = (perc_num.sum() / perc_num.count()) * 100
                    perc_other = df_LHS[df_LHS.columns[col_num]].apply(other_val_func)
                    perc_other = (perc_other.sum() / perc_other.count()) * 100
                    # get the first column that is more than 40% characters
                    if perc_character > 40 and start_num > col_num:
                        start_num = col_num
                    
                    # if we reach a numeric column after going through the village column
                    if perc_num > 40 and start_num != 200:
                        end_villages = True

                    # while we're still in village col space
                    if end_villages == False:
                        # In the if/elif statement below we try to catch all instances of a village column
                        if perc_character > 25 and perc_other < 5:
                            village_cols.append(col_num)
                        elif perc_num < 2 and perc_character > 3 and perc_other < 5:
                            village_cols.append(col_num)
                        # if of the values that are non-null, 90% are characters
                        elif perc_val_char > 90 and perc_other < 5:
                            village_cols.append(col_num)
                        elif perc_character > 10 and perc_nan > 20 and perc_other < 5:
                            village_cols.append(col_num)
                        elif perc_character > 1 and perc_nan > 80 and perc_num < 10 and perc_other < 5:
                            village_cols.append(col_num)
                    
                        # while we're still in village col space
                        elif start_num != 200:
                            village_cols.append(col_num)
                    
                    
                # if there is no column that has more than 25 percent characters it is not a LHS page (it's a RHS page)
                if start_num == 200:
                    LHS = False
                # if there is a column with more than 25 percent characters it is a LHS page
                else:
                    LHS = True
                
                flag = False
                inc = 0
                # create a villages dataframe
                villages = pd.DataFrame()
                # if village columns are detected
                if len(village_cols) > 0:
                    # concatenate the columns to create one village column
                    villages['village'] = df_LHS[df_LHS.columns[village_cols[0]]].astype(str).replace('nan','')
                    for col in range(len(village_cols)-1):
                        villages['village'] = villages['village'] + ' ' + df_LHS[df_LHS.columns[village_cols[col+1]]].astype(str).replace('nan','')
                
                # if no village cols were detected throw an error but continue
                else:
                    print("error: no village columns detected")
                    villages['village'] = None
                    villages['village_test'] = None
                
                # drop the columns that are adjacent and are id'd as village columns
                for col in village_cols:
                    if flag == True:
                        if col == start_num + inc:
                            df_LHS.drop(columns = df_LHS.columns[col-inc], inplace=True)
                            inc = inc + 1
                    # beginning with the first village column
                    if start_num == col:
                        flag = True
                        df_LHS.drop(columns = df_LHS.columns[col], inplace=True)
                        inc = inc + 1

                # identify the column header row
                # find the values that contain parentheses
                paren = df_LHS.apply(lambda row: row.apply(contains_paren), axis=1)
                # id any rows with more than siz parens
                has_sum_ge_two = (paren.sum(axis=1) >= 6).any()
                if has_sum_ge_two:
                    header = paren.index[(paren.sum(axis=1) >= 6).idxmax()]
                    print(df_LHS.iloc[header])
                else:
                    header = None
                
                # if this page is not the last in the district, get the tehsil from the next page
                if len(group) > i+1:
                    df_RHS = pd.read_csv('westBengal/' + group[i+1:i+2]['fullname'].values[0])
                    df_RHS.drop(columns=['row'], inplace=True)
                    # return the last column with the maximum count
                    nan_percent = df_RHS[df_RHS.columns[len(df_RHS.columns)-2]].isnull().mean() * 100
         
                    tehsils_int = df_RHS[df_RHS.columns[len(df_RHS.columns)-1]]

                    tehsil = str(tehsils_int.iloc[0]).split()
                    if len(tehsil) > 0:
                        if 'and' in tehsil:
                            index = tehsil.index('and')
                            tehsil = tehsil[index-1] + ' ' + tehsil[index] + ' ' + tehsil[index+1]
                        elif 'Tehsil' in tehsil:
                            index = tehsil.index('Tehsil')
                            tehsil = tehsil[index + 1]
                        elif 'Tahsil' in tehsil:
                            index = tehsil.index('Tahsil')
                            tehsil = tehsil[index + 1]
                        else:
                            tehsil = tehsil[len(tehsil)-1]
                    else:
                        tehsil = "test"
                    villages['tehsil'] = tehsil
                    
                    # get the filepath for the new dataset
                    filepath = 'west_bengal_pp4/{}.csv'.format(group[i:i+1]['fullname'].values[0])
                    # assign district to the village dataframe
                    villages['district'] = name

                    # eliminate all non-letter characters from the village column
                    letter_mask = villages['village'].str.contains('[a-zA-Z]')
                    villages = villages[letter_mask]
                    pattern = r'[^a-zA-Z- ()]'
                    # eliminate all numbers from the dataframe
                    villages = villages.replace(to_replace=pattern, value='', regex=True)
                    
                    # reorder the dataset and add the village, tehsil, district columns
                    if 'tehsil' in df_LHS.columns:
                        #pdb.set_trace()
                        df_LHS.drop(columns = 'tehsil')
                    #else:
                     #   pdb.set_trace()
                    df_LHS['village'] = villages['village']
                    df_LHS['district'] = villages['district']
                    df_LHS['tehsil'] = villages['tehsil']
                    
                    # crop the dataframe below the header
                    if header != None:
                        df_LHS = df_LHS.drop(index=df_LHS.index[:header+1])
                    # don't include the village, tehsil district columns in this section
                    df_LHS_m = df_LHS.iloc[:, :-2]
                    
                    
                    # identify additional columns that are extraneous
                    to_drop = []
                    for col_num in range(len(df_LHS_m.columns)-1):
                        df_LHS_m[df_LHS_m.columns[col_num]].astype(str)
                        perc_number = df_LHS_m[df_LHS_m.columns[col_num]].astype(str).apply(contains_num)
                        num_number = perc_number.sum()
                        num_nan = df_LHS_m[df_LHS_m.columns[col_num]].astype(str).apply(contains_nan)
                        perc_nan = (num_nan.sum() / num_nan.count()) * 100
                        perc_letter = df_LHS_m[df_LHS_m.columns[col_num]].astype(str).apply(contains_number)
                        num_letter = perc_letter.sum()
                        perc_letter = (perc_letter.sum() / (perc_letter.count() - num_nan.sum())) * 100
                        perc_other_val = df_LHS_m[df_LHS_m.columns[col_num]].astype(str).apply(other_val_func)
                        perc_other_val = (perc_other_val.sum() / (num_nan.count() - num_nan.sum())) * 100
                        contains_val = df_LHS_m[df_LHS_m.columns[col_num]].astype(str).apply(contains_value)
                        contains_val = (contains_val.sum() / contains_val.count()) * 100
                       
                        perc_not_num = df_LHS_m[df_LHS_m.columns[col_num]].astype(str).apply(has_num)
                        perc_not_num = (perc_not_num.sum() / (perc_not_num.count())) * 100

                   #     if num_number == 0:
                    #        to_drop.append(col_num)
                        # if of the values in a column, 80% are all letter values
                        #if perc_other_val > 20:
                         #   to_drop.append(col_num)
                       # if perc_letter > 80:
                        #    to_drop.append(col_num)
                        #if num_letter > 4:
                         #   to_drop.append(col_num)
                        #elif perc_letter > 20 and num_number < 5:
                            #to_drop.append(col_num)
                        #pdb.set_trace()
                        # if a column is entirely empty or contains no all letter values or values containing numbers
                        #elif perc_nan == 100 or (perc_letter == 0 and num_number == 0):
                         #   print(df_LHS_m[df_LHS_m.columns[col_num]].astype(str))
                          #  to_drop.append(col_num)
                       # if "final_outputLHSBanaskantha.pdf266.csv" == group[i:i+1]['fullname'].values[0]:
                        #    pdb.set_trace()
                        
                        # if more than 40% of a columns values (excluding nulls) are all letters (excluding null), drop it
                        if perc_letter > 40:
                            to_drop.append(col_num)
                        # if more than 50% of a columns values do not contain numbers, drop it
                       # if perc_not_num < 50:
                        #    to_drop.append(col_num)
                        # if a column is more than 70% nan values, drop it
                        if contains_val < 30:
                            to_drop.append(col_num)
                    
                #    if "final_outputLHSBanaskantha.pdf266.csv" == group[i:i+1]['fullname'].values[0]:
                 #       pdb.set_trace()
                    #drop the extraneous column values
                    df_LHS.drop(df_LHS.columns[to_drop], axis=1, inplace=True)
                    # if the village cell is empty drop the row
                    df_LHS.dropna(subset=['village'], inplace=True)
                    
                    column_to_move1 = df_LHS.pop('tehsil')
                    #df_LHS.insert(0, 'tehsil', column_to_move)
                    column_to_move2 = df_LHS.pop('village')
                    #df_LHS.insert(0, 'village', column_to_move)
                    column_to_move3 = df_LHS.pop('district')
                   # df_LHS.insert(0, 'district', column_to_move)
                    
                    
                    # eliminate columns until
                    min_value = 1000
                    min_col = -100
                    col_num = 0

                    # create array for columns to drop
                    extra_cols = []
                    exclude_nums = []
                    length = len(df_LHS.columns)
                    

                    num_cols = [col for col in df_LHS.columns if not col.isalpha()]
                    num_cols_sorted = sorted(num_cols, key=lambda x: int(''.join(filter(str.isdigit, x))))
                    rename_dict = {num_cols_sorted[i]: str(i+1) for i in range(len(num_cols_sorted))}
                    df_LHS = df_LHS.rename(columns=rename_dict)

                    #while length > districts[district_select]-1:
                            #pdb.set_trace()
                        # sort columns in dataframe by the number of characters they have - since other option didn't work
                            # for each column of the dataframe
                     #       for col_num in range(len(df_LHS.columns)-1):
                                # assuming the col num has not already been id'd as a min
                      #          if col_num not in exclude_nums:
                                    # get the number of values in the column
                       #             num_value = df_LHS[df_LHS.columns[col_num]].astype(str).apply(contains_value)
                        #            num_value = num_value.sum()
                         #           if min_value > num_value:
                          #              min_value = num_value
                           #             min_col = col_num
                                    # this should be the case but implemented flag bc of an error
                            #extra_cols.append(min_col)
                            #exclude_nums.append(min_col)
                        #    length = length - 1
                         #   min_value = 1000
                          #  min_col = -100
           
           
                        
                   # pdb.set_trace()
               #     df_LHS.drop(df_LHS.columns[extra_cols], axis=1, inplace=True)
                    if len(df_LHS.columns) > 1:
                        df_LHS.rename(columns={df_LHS.columns[0]: 'ID'}, inplace=True)
           
                    df_LHS.insert(0, 'tehsil', column_to_move1)
                    df_LHS.insert(0, 'village', column_to_move2)
                    df_LHS.insert(0, 'district', column_to_move3)
                    
                    
                  
                    num_cols = [col for col in df_LHS.columns if not col.isalpha()]
                    num_cols_sorted = sorted(num_cols, key=lambda x: int(''.join(filter(str.isdigit, x))))
                    rename_dict = {num_cols_sorted[i]: str(i+1) for i in range(len(num_cols_sorted))}
                    df_LHS = df_LHS.rename(columns=rename_dict)
                    
                    if len(df_LHS.columns) > 3:
                        df_LHS.rename(columns={df_LHS.columns[3]: 'ID'}, inplace=True)
                    
                    df_LHS.to_csv(filepath)
