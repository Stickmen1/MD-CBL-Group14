import pandas as pd

def find_lsoa_and_name_columns(df):
    """
    Tries to detect LSOA code column and area name column in a DataFrame.

    Parameters:
        df: a dataframe to search
    
    Returns:
        the LSOA code column and the LSOA name column
    """

    lsoa_col = None
    name_col = None

    for col in df.columns:
        if df[col].astype(str).str.match(r'^E01\d{6,}').any():
            lsoa_col = col
        elif df[col].dtype == 'object' and name_col is None:
            # Pick a likely candidate for area name
            sample = df[col].dropna().astype(str)
            if not sample.empty and sample.str.contains(r'[A-Za-z]').any():
                name_col = col

    return lsoa_col, name_col

# Does not work, abandoned!
def load_and_merge_sheets_with_multiindex(file_path):
    """
    Loads all sheets from an Excel file, detects LSOA + area name columns, and merges on that multi-index.

    Parameters:
        file_path: the path to the file to load
    
    Returns:
        A dataframe merging all of the datasets from the file.
    """

    custom_na_values = ['-', 'c', '..']
    xls = pd.ExcelFile(file_path)
    sheet_dfs = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, na_values=custom_na_values)

        lsoa_col, name_col = find_lsoa_and_name_columns(df)

        if not lsoa_col or not name_col:
            print(f"Skipped sheet '{sheet}': missing LSOA or name column.")
            continue

        df = df.rename(columns={lsoa_col: 'LSOA', name_col: 'AreaName'})
        df = df.set_index(['LSOA', 'AreaName'])

        # Drop duplicates in index
        if not df.index.is_unique:
            before = len(df)
            df = df[~df.index.duplicated(keep='first')]
            after = len(df)
            print(f"Sheet '{sheet}': dropped {before - after} duplicate index rows.")

        # Keep only numeric columns for regression
        numeric_df = df.select_dtypes(include='number')
        sheet_dfs.append(numeric_df)

    # Merge all on (LSOA, AreaName) multi-index
    combined_df = pd.concat(sheet_dfs, axis=1, join='inner')
    return combined_df

# Runs a regression, but not used for the summary, see stats_regression function
def run_regression(df, target_column):
    X = df.drop(columns=[target_column])
    y = df[target_column]

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)

    return model, score


# # Example usage
# file_path = 'merged_output.xlsx'
# merged_data = load_and_merge_sheets_with_multiindex(file_path)

# print("Columns in merged data:", merged_data.columns)
# print(merged_data.head())

# # Choose your target
# target_column = 'Burglary' 
# if target_column in merged_data.columns:
#     model, score = run_regression(merged_data, target_column)
#     print("R² score:", score)
# else:
#     print(f"Target column '{target_column}' not found in merged data.")

#___________________________________________________________________________
# New idea:
# Manual per sheet approach

import merged_data_analysis as mda

def merge_dataframes_from_sheets(merged_data_file_path: str = 'merged_output.xlsx') -> pd.DataFrame:
    """
    Takes the merged data excel file and goes through every sheet to create one large dataframe and saves it as an excel file.

    Parameters:
        merged_data_file_path: the path to the file containing the multi-sheet merged data (created by the dataset_merger)
    
    Returns:
        A dataframe that is a single sheet version of the input dataset, but also contains the burglary counts, all indexed by LSOA.
        This can be used for regression.
    """


    # Get crime data 2022 (2021 is the most common year, 2022 is closest to this)
    crime_df: pd.DataFrame = mda.merge_police_data_year("UK_police_data", 2022, mda.custom_na_values)

    # Get number of burglaries per LSOA
    burglary_df = mda.get_burglaries_per_lsoa(crime_data=crime_df)

# Get all sheets as dfs:
    # Claimants_2023
    Claimants_df = pd.read_excel(merged_data_file_path, sheet_name='Claimants_2023')
    Claimants_df[['LSOA code', 'LSOA name']] = Claimants_df['2011 super output area - lower layer'].str.split(' : ', expand=True)
    claimant_cols = [col for col in Claimants_df.columns if 'Claimant count' in col]
    Claimants_df['2023 Claimant Total'] = Claimants_df[claimant_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1)
    Claimants_df = Claimants_df[['LSOA code', 'LSOA name', '2023 Claimant Total']]

    final_df = pd.merge(burglary_df, Claimants_df, on='LSOA code', how='inner')

    # Econ_Activity_2021
    Econ_Activity_df = pd.read_excel(merged_data_file_path, sheet_name='Econ_Activity_2021')
    Econ_Activity_df[['LSOA code', 'LSOA name']] = Econ_Activity_df['2021 super output area - lower layer'].str.split(' : ', expand=True)
    Econ_Activity_df = Econ_Activity_df[['LSOA code', 'LSOA name', '2021_Economic_activity']]

    final_df = pd.merge(final_df, Econ_Activity_df, on='LSOA code', how='inner')

    # These categories have duplicate LSOA indexes, making them hard to merge
    # # CTSOP1_2021
    # CTSOP1_2021_df = pd.read_excel(merged_data_file_path, sheet_name='CTSOP1_2021', na_values=['-'])

    # # CTSOP3_2021
    # CTSOP3_2021_df = pd.read_excel(merged_data_file_path, sheet_name='CTSOP3_2021', na_values=['-'])

    # Second_Addresses
    Second_Addresses_df = pd.read_excel(merged_data_file_path, sheet_name='Second_Addresses', na_values=['c'])
    Second_Addresses_df = Second_Addresses_df.drop('Area Name', axis=1)
    Second_Addresses_df = Second_Addresses_df.rename(columns={'Area Code': 'LSOA code'})

    final_df = pd.merge(final_df, Second_Addresses_df, on='LSOA code', how='inner')
 
    # Rural_Urban
    Rural_Urban_df = pd.read_excel(merged_data_file_path, sheet_name='Rural_Urban')
    Rural_Urban_df = Rural_Urban_df[['LSOA21CD', 'Rural Urban flag', 'RUC21 settlement class', 'Proportion of population in settlement class (%)', 'RUC21 relative access', 'Proportion of population in relative access category (%)']]
    Rural_Urban_df = Rural_Urban_df.rename(columns={'LSOA21CD': 'LSOA code'})

    final_df = pd.merge(final_df, Rural_Urban_df, on='LSOA code', how='inner')

    # PTAI_2016
    PTAI_2016_df = pd.read_excel(merged_data_file_path, sheet_name='PTAI_2016')
    PTAI_2016_df = PTAI_2016_df.rename(columns={'LSOA11CD': 'LSOA code'})

    final_df = pd.merge(final_df, PTAI_2016_df, on='LSOA code', how='inner')

    # Households_2021
    Households_2021_df = pd.read_excel(merged_data_file_path, sheet_name='Households_2021')
    Households_2021_df = Households_2021_df.rename(columns={'Lower layer Super Output Areas Code': 'LSOA code'})
    Households_2021_df = Households_2021_df.drop('Lower layer Super Output Areas', axis=1)

    final_df = pd.merge(final_df, Households_2021_df, on='LSOA code', how='inner')
    
    # These categories have duplicate LSOA indexes, making them hard to merge
    # # Accommodation_2021
    # Accommodation_2021_df = pd.read_excel(merged_data_file_path, sheet_name='Accommodation_2021')

    # # Car_Van_2021
    # Car_Van_2021_df = pd.read_excel(merged_data_file_path, sheet_name='Car_Van_2021')

    # # Heating_2021
    # Heating_2021_df = pd.read_excel(merged_data_file_path, sheet_name='Heating_2021')

    # # Bedrooms_2021
    # Bedrooms_2021_df = pd.read_excel(merged_data_file_path, sheet_name='Bedrooms_2021')

    # # Rooms_2021
    # Rooms_2021_df = pd.read_excel(merged_data_file_path, sheet_name='Rooms_2021')

    # # Rating_Bedrooms
    # Rating_Bedrooms_df = pd.read_excel(merged_data_file_path, sheet_name='Rating_Bedrooms')

    # # Rating_Rooms
    # Rating_Rooms_df = pd.read_excel(merged_data_file_path, sheet_name='Rating_Rooms')

    # # Tenure_2021
    # Tenure_2021_df = pd.read_excel(merged_data_file_path, sheet_name='Tenure_2021')

    # IMD_2019
    IMD_2019_df = pd.read_excel(merged_data_file_path, sheet_name='IMD_2019')
    IMD_2019_df = IMD_2019_df.rename(columns={'LSOA code (2011)' : 'LSOA code'})
    IMD_2019_df = IMD_2019_df.drop(['LSOA name (2011)', 'Local Authority District code (2019)', 'Local Authority District name (2019)'], axis=1)

    final_df = pd.merge(final_df, IMD_2019_df, on='LSOA code', how='inner')

    # Subdomains_2019
    Subdomains_2019_df = pd.read_excel(merged_data_file_path, sheet_name='Subdomains_2019')
    Subdomains_2019_df = Subdomains_2019_df.rename(columns={'LSOA code (2011)' : 'LSOA code'})
    Subdomains_2019_df = Subdomains_2019_df.drop(['LSOA name (2011)', 'Local Authority District code (2019)', 'Local Authority District name (2019)'], axis=1)

    final_df = pd.merge(final_df, Subdomains_2019_df, on='LSOA code', how='inner')

    # IDACI_2019
    IDACI_2019_df = pd.read_excel(merged_data_file_path, sheet_name='IDACI_2019')
    IDACI_2019_df = IDACI_2019_df.rename(columns={'LSOA code (2011)' : 'LSOA code'})
    IDACI_2019_df = IDACI_2019_df.drop(['LSOA name (2011)', 'Local Authority District code (2019)', 'Local Authority District name (2019)'], axis=1)

    final_df = pd.merge(final_df, IDACI_2019_df, on='LSOA code', how='inner')

    # Population_2019
    Population_2019_df = pd.read_excel(merged_data_file_path, sheet_name='Population_2019')
    Population_2019_df = Population_2019_df.rename(columns={'LSOA code (2011)' : 'LSOA code'})
    Population_2019_df = Population_2019_df.drop(['LSOA name (2011)', 'Local Authority District code (2019)', 'Local Authority District name (2019)', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'], axis=1)

    final_df = pd.merge(final_df, Population_2019_df, on='LSOA code', how='inner')

    # Indicators_2019
    Indicators_2019_df = pd.read_excel(merged_data_file_path, sheet_name='Indicators_2019')
    Indicators_2019_df = Indicators_2019_df.rename(columns={'LSOA code (2011)' : 'LSOA code'})
    Indicators_2019_df = Indicators_2019_df.drop(['LSOA name (2011)', 'Local Authority District code (2019)', 'Local Authority District name (2019)'], axis=1)

    final_df = pd.merge(final_df, Indicators_2019_df, on='LSOA code', how='inner')

    # Finalize the dataframe and save it
    final_df = final_df.drop(['LSOA name_x', 'LSOA name_y'], axis=1)

    final_df.to_excel('single_sheet_merged.xlsx', index=False)

    return final_df


# New regression function using statsmodels library
import statsmodels.api as sm

def stats_regression(df: pd.DataFrame, target_column_name: str):
    # Separate target and features
    X = df.drop(columns=[target_column_name])
    y = df[target_column_name]

    # Add constant term for intercept
    X = sm.add_constant(X)

    # Fit the OLS model
    model = sm.OLS(y, X).fit()

    return model


# Get dataframe
df = merge_dataframes_from_sheets()

# Prepare df for regression
# As each house in london is classified as urban, we can drop the rural/urban classification
df = df.drop(['Rural Urban flag', 'RUC21 settlement class', 'Proportion of population in settlement class (%)', 'RUC21 relative access', 'Proportion of population in relative access category (%)'], axis=1)

df = df.drop("Student’s term-time address",axis=1) # Get rid of this column as it is completely empty

df = df.drop(['LSOA code'], axis=1) # Get rid of the LSOA code as it is no longer needed

df = df.fillna(df.mean(numeric_only=False)) # Fill in the missing values with the means

# Print full summary with t-tests, p-values, R², etc.
print(stats_regression(df, 'Burglary Count').summary())
