import pandas as pd
import geopandas as gpd

claimants_2023_df = pd.read_csv('datasets/1271564476123865.csv', skiprows=9)
claimants_2023_df['area_name'] = claimants_2023_df['2011 super output area - lower layer'].str.split(':').str[1].str.strip()
claimants_2023_df = claimants_2023_df.rename(columns={
    'January 2023': 'January_2023 Claimant count',
    'February 2023': 'February_2023 Claimant count',
    'March 2023': 'March_2023 Claimant count',
    'April 2023': 'April_2023 Claimant count',
    'May 2023': 'May_2023 Claimant count',
    'June 2023': 'June_2023 Claimant count',
    'July 2023': 'July_2023 Claimant count',
    'August 2023': 'August_2023 Claimant count',
    'September 2023': 'September_2023 Claimant count',
    'October 2023': 'October_2023 Claimant count',
    'November 2023': 'November_2023 Claimant count',   
    'December 2023': 'December_2023 Claimant count',
    'January 2024': 'January_2024 Claimant count',
    'February 2024': 'February_2024 Claimant count',
    'March 2024': 'March_2024 Claimant count',  
    'April 2024': 'April_2024 Claimant count', 
    'May 2024': 'May_2024 Claimant count',
    'June 2024': 'June_2024 Claimant count',
    'July 2024': 'July_2024 Claimant count',
    'August 2024': 'August_2024 Claimant count',
    'September 2024': 'September_2024 Claimant count',
    'October 2024': 'October_2024 Claimant count',
    'November 2024': 'November_2024 Claimant count',
    'December 2024': 'December_2024 Claimant count',
    'January 2025': 'January_2025 Claimant count',
    'February 2025': 'February_2025 Claimant count',
    'March 2025': 'March_2025 Claimant count',
})

economic_activity_2021_df = pd.read_excel('datasets/nomis_2025_05_09_164133.xlsx', skiprows=7)
economic_activity_2021_df['area_name'] = economic_activity_2021_df['2021 super output area - lower layer'].str.split(':').str[1].str.strip()
economic_activity_2021_df = economic_activity_2021_df.rename(columns={
   2021 : '2021_Economic_activity',
})

ctsop1_2021_df = pd.read_csv('datasets/CTSOP1_1_2021_03_31.csv')
ctsop1_2023_df = pd.read_csv('datasets/CTSOP1_1_2023_03_31.csv')

ctsop3_2021_df = pd.read_csv('datasets/CTSOP3_1_2021_03_31.csv')
ctsop3_2023_df = pd.read_csv('datasets/CTSOP3_1_2023_03_31.csv')

location_dwelligns_df = pd.read_excel('datasets/locationofsecondaddressesenglish.xlsx', skiprows=3, sheet_name='1f')

rural_urban_df = pd.read_excel('datasets/rucallsupplementarytables.xlsx', skiprows=2, sheet_name='Table 1B')

gb_ptai_2016_df = pd.read_csv('datasets/GB_LSOA_PTAI_2016.csv')

'https://www.ons.gov.uk/datasets/TS041/editions/2021/versions/3/filter-outputs/d4b56c8a-d045-4d20-977b-8e4c7b455628#get-data'
households_2021_df = pd.read_csv('datasets/TS041-2021-3-filtered-2025-05-11T21-51-58Z.csv')
households_2021_df = households_2021_df.rename(columns={
   'Observation' : 'observation_households',
})

'https://www.ons.gov.uk/datasets/TS044/editions/2021/versions/1/filter-outputs/cfe858b2-10ca-4f60-b6da-645eaa3864bb#get-data'
accomodation_2021_df = pd.read_csv('datasets/TS044-2021-1-filtered-2025-05-12T07-17-12Z.csv', delimiter=';')

'https://www.ons.gov.uk/datasets/TS045/editions/2021/versions/1/filter-outputs/6c7e0b16-89eb-4a2b-aff2-b65a577ad75a#get-data'
car_van_availability_2021_df = pd.read_csv('datasets/TS045-2021-1-filtered-2025-05-12T07-23-38Z.csv', delimiter=';')

'https://www.ons.gov.uk/datasets/TS046/editions/2021/versions/1/filter-outputs/26084dcc-9dc4-42d9-8b19-264a4dfbdfb7#get-data'
central_heating_2021_df = pd.read_csv('datasets/TS046-2021-1-filtered-2025-05-12T07-27-05Z.csv', delimiter=';')

'https://www.ons.gov.uk/datasets/TS050/editions/2021/versions/1/filter-outputs/dc89e274-a9db-451b-a10f-d867b44c3b02#get-data'
bedrooms_2021_df = pd.read_csv('datasets/TS050-2021-1-filtered-2025-05-12T07-33-44Z.csv', delimiter=';')

'https://www.ons.gov.uk/datasets/TS051/editions/2021/versions/1/filter-outputs/6ea59421-437f-41eb-abe1-6bf8041be446#get-data'
rooms_2021_df = pd.read_csv('datasets/TS051-2021-1-filtered-2025-05-12T07-35-26Z.csv')

'https://www.ons.gov.uk/datasets/TS051/editions/2021/versions/1/filter-outputs/6ea59421-437f-41eb-abe1-6bf8041be446#get-data'
rating_bedrooms_2021_df = pd.read_csv('datasets/TS052-2021-1-filtered-2025-05-12T07-42-36Z.csv')

'https://www.ons.gov.uk/datasets/TS053/editions/2021/versions/1/filter-outputs/bac5876e-e626-4eb0-b699-cd144aece229#get-data'
rating_rooms_2021_df = pd.read_csv('datasets/TS053-2021-1-filtered-2025-05-12T07-50-04Z.csv')

'https://www.ons.gov.uk/datasets/TS054/editions/2021/versions/1/filter-outputs/0224c0ce-1d29-4b5d-ad6e-747eac167482#get-data'
tenure_2021_df = pd.read_csv('datasets/TS054-2021-1-filtered-2025-05-12T07-55-50Z.csv')

imd_2019_df = pd.read_excel('datasets/ID 2019 for London.xlsx', sheet_name='IMD 2019')

subdomains_2019_df = pd.read_excel('datasets/ID 2019 for London.xlsx', sheet_name='Sub domains')

idaci_2019_df = pd.read_excel('datasets/ID 2019 for London.xlsx', sheet_name='IDACI and IDAOPI')

population_figures_2019_df = pd.read_excel('datasets/ID 2019 for London.xlsx', sheet_name='Population figures')

underlying_indicators_2019_df = pd.read_excel('datasets/ID 2019 for London.xlsx', sheet_name='Underlying indicators')

print("Loading...")
with pd.ExcelWriter('merged_output.xlsx', engine='xlsxwriter') as writer:
    claimants_2023_df.to_excel(writer, sheet_name='Claimants_2023', index=False)
    economic_activity_2021_df.to_excel(writer, sheet_name='Econ_Activity_2021', index=False)
    ctsop1_2021_df.to_excel(writer, sheet_name='CTSOP1_2021', index=False)
    ctsop1_2023_df.to_excel(writer, sheet_name='CTSOP1_2023', index=False)
    ctsop3_2021_df.to_excel(writer, sheet_name='CTSOP3_2021', index=False)
    ctsop3_2023_df.to_excel(writer, sheet_name='CTSOP3_2023', index=False)
    location_dwelligns_df.to_excel(writer, sheet_name='Second_Addresses', index=False)
    rural_urban_df.to_excel(writer, sheet_name='Rural_Urban', index=False)
    gb_ptai_2016_df.to_excel(writer, sheet_name='PTAI_2016', index=False)
    households_2021_df.to_excel(writer, sheet_name='Households_2021', index=False)
    accomodation_2021_df.to_excel(writer, sheet_name='Accommodation_2021', index=False)
    car_van_availability_2021_df.to_excel(writer, sheet_name='Car_Van_2021', index=False)
    central_heating_2021_df.to_excel(writer, sheet_name='Heating_2021', index=False)
    bedrooms_2021_df.to_excel(writer, sheet_name='Bedrooms_2021', index=False)
    rooms_2021_df.to_excel(writer, sheet_name='Rooms_2021', index=False)
    rating_bedrooms_2021_df.to_excel(writer, sheet_name='Rating_Bedrooms', index=False)
    rating_rooms_2021_df.to_excel(writer, sheet_name='Rating_Rooms', index=False)
    tenure_2021_df.to_excel(writer, sheet_name='Tenure_2021', index=False)
    imd_2019_df.to_excel(writer, sheet_name='IMD_2019', index=False)
    subdomains_2019_df.to_excel(writer, sheet_name='Subdomains_2019', index=False)
    idaci_2019_df.to_excel(writer, sheet_name='IDACI_2019', index=False)
    population_figures_2019_df.to_excel(writer, sheet_name='Population_2019', index=False)
    underlying_indicators_2019_df.to_excel(writer, sheet_name='Indicators_2019', index=False)
print('Ready!')
