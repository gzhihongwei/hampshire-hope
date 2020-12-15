import tabula
import pandas as pd
import numpy as np

# Eliminate unnecessary letters so we can have actual times
def preprocess_table(table):
    for i in range(len(table.columns)):
        col = table.columns[i]
        table[col] = table[col].str.replace('[\|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|-]','')

# Process info for times in the morning
def preprocess_times_morning(table):
<<<<<<< HEAD
    for i in range(int(len(table.columns)/2), len(table.columns)):
        if i != 0:
=======
    for i in range(len(table.columns)):
        # We won't actual find times at 12:00 at column 0 so we'll ignore that
        if i != 0:
            # Find the index where 12:00 occurs and then replace those after
            # 12:00 will become the empty string
>>>>>>> 84f6764 (Extract PVTA times finished)
            col = table.columns[i]
            index = table[col].str.contains('[1][2]:[0-5][0-9]').idxmax()
            table.loc[index:,col] = ''

# Process info for times in the evening
def preprocess_times_evening(table):
<<<<<<< HEAD
    for i in range(0, int(len(table.columns)/2)):
=======
    for i in range(len(table.columns)):
>>>>>>> 84f6764 (Extract PVTA times finished)
        col = table.columns[i]
        index = table[col].str.contains('[1][2]:[0-5][0-9]').idxmax()
        if index != -1:
            table.loc[0:index-1,col] = ''

if __name__ == '__main__':
    table = tabula.read_pdf("G1.pdf", pages=1)

    # Get rid of the \r
    for i in range(len(table)):
        table[i].columns = table[i].columns.str.replace(r"\r", " ")
<<<<<<< HEAD

    # Get rid of the unnamed column
    table[0] = table[0].drop(columns=["Unnamed: 0"])

    # Separate out the table into weekdays, saturdays, and sundays
=======
    table[0] = table[0].drop(columns=["Unnamed: 0"])

>>>>>>> 84f6764 (Extract PVTA times finished)
    index = table[0].index
    condition1 = table[0]['CHICOPEE BIG Y'] == "WEEKDAY"
    condition2 = table[0]['CHICOPEE BIG Y'] == 'SATURDAY'
    condition3 = table[0]['CHICOPEE BIG Y'] == 'SUNDAY'
    day_indices = index[condition1][0], index[condition2][0], index[condition3][0]

<<<<<<< HEAD
    # Do some preprocessing to get the necessarily information in each table.
    table_weekday = table[0].iloc[day_indices[0] + 1: day_indices[1] - 1]
    table_saturday = table[0].iloc[day_indices[1] + 1: day_indices[2] - 1]
    table_sunday = table[0].iloc[day_indices[2] + 1: len(table[0])]

    # Reset the indicies for each table
=======
    table_weekday = table[0].iloc[day_indices[0] + 1: day_indices[1] - 1]
    table_saturday = table[0].iloc[day_indices[1] + 1: day_indices[2] - 1]
    table_sunday = table[0].iloc[day_indices[2] + 1: len(table[0])]
>>>>>>> 84f6764 (Extract PVTA times finished)
    table_weekday.reset_index(drop=True, inplace=True)
    table_saturday.reset_index(drop=True, inplace=True)
    table_sunday.reset_index(drop=True, inplace=True)

<<<<<<< HEAD
    # Do some preprocessing on the table to get rid of any letters or --
=======
>>>>>>> 84f6764 (Extract PVTA times finished)
    preprocess_table(table_weekday)
    preprocess_table(table_saturday)
    preprocess_table(table_sunday)

    # condition on mornings for weekdays.
    condition_weekday_morning = table_weekday['CHICOPEE BIG Y'].str.contains('[1][2]:[0-5][0-9]').idxmax()
    table_weekday_morning = table_weekday.iloc[0: condition_weekday_morning]
    table_weekday_morning.reset_index(drop=True, inplace=True)

    # condition on evenings for weekdays
    condition_weekday_evening = table_weekday['CHICOPEE BIG Y.1'].str.contains('[1][2]:[0-5][0-9]').idxmax()
    table_weekday_evening = table_weekday.iloc[condition_weekday_evening - 1:]
    table_weekday_evening.reset_index(drop=True, inplace=True)

    # condition on mornings for saturdays.
    condition_saturday_morning = table_saturday['CHICOPEE BIG Y'].str.contains('[1][2]:[0-5][0-9]').idxmax()
    table_saturday_morning = table_saturday.iloc[0: condition_saturday_morning]
    table_saturday_morning.reset_index(drop=True, inplace=True)

    # condition on evenings for saturdays.
    condition_saturday_evening = table_saturday['CHICOPEE BIG Y.1'].str.contains('[1][2]:[0-5][0-9]').idxmax()
    table_saturday_evening = table_saturday.iloc[condition_saturday_evening - 1:]
    table_saturday_evening.reset_index(drop=True, inplace=True)

    # condition on mornings for sunday.
    condition_sunday_morning = table_sunday['CHICOPEE BIG Y'].str.contains('[1][2]:[0-5][0-9]').idxmax()
    table_sunday_morning = table_sunday.iloc[0: condition_sunday_morning]
    table_sunday_morning.reset_index(drop=True, inplace=True)

    # condition on evenings for sunday.
    condition_sunday_evening = table_sunday['CHICOPEE BIG Y.1'].str.contains('[1][2]:[0-5][0-9]').idxmax()
    table_sunday_evening = table_sunday.iloc[condition_sunday_evening - 1:]
    table_sunday_evening.reset_index(drop=True, inplace=True)

<<<<<<< HEAD
    # Create copies of the table so we don't have any interfering deletions
    # from each table. Then more preprocessing.
=======
>>>>>>> 84f6764 (Extract PVTA times finished)
    table_weekday_evening = table_weekday_evening.copy()
    preprocess_times_evening(table_weekday_evening)
    table_saturday_evening = table_saturday_evening.copy()
    preprocess_times_evening(table_saturday_evening)
    table_sunday_evening = table_sunday_evening.copy()
    preprocess_times_evening(table_sunday_evening)
    table_weekday_morning = table_weekday_morning.copy()
    preprocess_times_morning(table_weekday_morning)
    table_saturday_morning = table_saturday_morning.copy()
    preprocess_times_morning(table_saturday_morning)
    table_sunday_morning = table_sunday_morning.copy()
    preprocess_times_morning(table_sunday_morning)

<<<<<<< HEAD
    # Send the 6 tables to their respective csv file.
    table_weekday_morning.to_csv(r'./PVTA_Route_Data/weekday_morning.csv', index=False, header=True)
    table_weekday_evening.to_csv(r'./PVTA_Route_Data/weekday_evening.csv', index=False, header=True)
    table_saturday_morning.to_csv(r'./PVTA_Route_Data/saturday_morning.csv', index=False, header=True)
    table_saturday_evening.to_csv(r'./PVTA_Route_Data/saturday_evening.csv', index=False, header=True)
    table_sunday_morning.to_csv(r'./PVTA_Route_Data/sunday_morning.csv', index=False, header=True)
    table_sunday_evening.to_csv(r'./PVTA_Route_Data/sunday_evening.csv', index=False, header=True)
=======
    table_weekday_morning = table_weekday_morning.replace(r'^\s*$', np.nan, regex=True)
    table_weekday_evening = table_weekday_evening.replace(r'^\s*$', np.nan, regex=True)
    table_saturday_morning = table_saturday_morning.replace(r'^\s*$', np.nan, regex=True)
    table_saturday_evening = table_saturday_evening.replace(r'^\s*$', np.nan, regex=True)
    table_sunday_morning = table_sunday_morning.replace(r'^\s*$', np.nan, regex=True)
    table_sunday_evening = table_sunday_evening.replace(r'^\s*$', np.nan, regex=True)

    # Drop apply
    table_weekday_morning = table_weekday_morning.apply(lambda x: pd.Series(x.dropna().values)).fillna('')
    table_weekday_evening = table_weekday_evening.apply(lambda x: pd.Series(x.dropna().values)).fillna('')
    table_saturday_morning = table_saturday_morning.apply(lambda x: pd.Series(x.dropna().values)).fillna('')
    table_saturday_evening = table_saturday_evening.apply(lambda x: pd.Series(x.dropna().values)).fillna('')
    table_sunday_morning = table_sunday_morning.apply(lambda x: pd.Series(x.dropna().values)).fillna('')
    table_sunday_evening = table_sunday_evening.apply(lambda x: pd.Series(x.dropna().values)).fillna('')

    table_weekday_morning.to_csv(r'weekday_morning.csv', index=False, header=True)
    table_weekday_evening.to_csv(r'weekday_evening.csv', index=False, header=True)
    table_saturday_morning.to_csv(r'saturday_morning.csv', index=False, header=True)
    table_saturday_evening.to_csv(r'saturday_evening.csv', index=False, header=True)
    table_sunday_morning.to_csv(r'sunday_morning.csv', index=False, header=True)
    table_sunday_evening.to_csv(r'sunday_evening.csv', index=False, header=True)
>>>>>>> 84f6764 (Extract PVTA times finished)

