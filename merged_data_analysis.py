import os
import pandas as pd
import numpy as np

custom_na_values: list[str] = ['-', 'c', '..'] # these were helpful for filling some of the weird missing value placeholders


def merge_police_data_year(root_folder_name, year, na_values=None) -> pd.DataFrame:
    """
    Merges monthly police data CSVs from subfolders into one DataFrame for a year.

    Parameters:
        root_folder_name: Root folder containing the individual month folders
        year: Year to merge (e.g. '2022').
        na_values: Values to treat as NaN.

    Returns: Combined DataFrame of police data for the year.
    """
    year = str(year)
    df_list = []

    for folder_name in os.listdir(root_folder_name):
        if folder_name.startswith(year + '-'):
            folder_path = os.path.join(root_folder_name, folder_name)

            if not os.path.isdir(folder_path):
                continue

            # Get all CSV files in this month-folder
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv') and file_name.startswith(folder_name) and 'street' in file_name:
                    full_path = os.path.join(folder_path, file_name)
                    df = pd.read_csv(full_path, na_values=na_values)
                    df['month'] = folder_name
                    df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

# Test use:
# print(merge_police_data_year("UK_police_data", 2022, custom_na_values))


def get_burglaries_per_lsoa(crime_data) -> pd.DataFrame:
    """
    Calculates the number of burglaries per LSOA.

    Parameters:
        crime_data: DataFrame containing crime data.

    Returns:
        DataFrame containing the number of burglaries per LSOA.
    """

    burglaries = crime_data[crime_data['Crime type'] == 'Burglary']

    burglaries_per_lsoa = burglaries.groupby('LSOA code').size().reset_index(name='Burglary Count')

    return burglaries_per_lsoa


def relative_variance_from_sheet(file_path, sheet_name):
    """
    Calculates relative variance (variance divided by mean or CV) for numeric columns in an Excel sheet.
    
    Parameters:
        file_path: Path to the Excel file
        sheet_name: Sheet name to analyze

    Returns:
        Dictionary of column names and their relative variance
    """

    df = pd.read_excel(file_path, sheet_name=sheet_name, na_values=custom_na_values)

    numeric_df = df.select_dtypes(include='number')

    means = numeric_df.mean()
    variances = numeric_df.var()
    std_devs = numeric_df.std()


    relative_values = std_devs / means

    # Drop divisions by zero or NaN mean
    relative_values = relative_values.replace([np.inf, -np.inf], np.nan).dropna()

    return relative_values.to_dict()

# Test usage
# file_path = 'merged_output.xlsx'
# sheet_name = 'Rural_Urban'
# variances = relative_variance_from_sheet(file_path, sheet_name)
# print(variances)