import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def plot_monthly_average(data_dir: str = 'UK_police_data') -> None:
    monthly_data = []

    # Loop through each month's folder
    for month_dir in sorted(os.listdir(data_dir)):
        csv_path = os.path.join(data_dir, month_dir, f"{month_dir}-metropolitan-street.csv")
        
        if os.path.isfile(csv_path):
            df = pd.read_csv(csv_path)
            
            burglaries = df[df['Crime type'] == 'Burglary']
            
            # Extract month number
            month_num = int(month_dir[5:7])
            
            monthly_data.append({
                'Month': month_num,
                'Count': len(burglaries)
            })

    df = pd.DataFrame(monthly_data)

    # Group by month number and average
    monthly_avg = df.groupby('Month')['Count'].mean().reset_index()

    # Month labels for x-axis
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.figure(figsize=(10, 6))
    plt.plot(monthly_avg['Month'], monthly_avg['Count'], marker='o', linestyle='-')
    plt.xticks(ticks=range(1, 13), labels=month_labels)
    plt.title('Average Burglaries per Month (Across All Years)')
    plt.xlabel('Month')
    plt.ylabel('Avg. Burglaries')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_year_stacked(data_dir: str = 'UK_police_data') -> None:
    burglary_data = []

    # Loop through each month directory
    for month_dir in sorted(os.listdir(data_dir)):
        file_path = os.path.join(data_dir, month_dir, f"{month_dir}-metropolitan-street.csv")
        
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            burglaries = df[df['Crime type'] == 'Burglary']
            
            # Extract year and month
            year, month = month_dir.split('-')
            burglary_data.append({'Year': int(year), 'Month': int(month), 'Count': len(burglaries)})

    burglary_df = pd.DataFrame(burglary_data)

    # Pivot data so each year is a separate line
    pivot_df = burglary_df.pivot(index='Month', columns='Year', values='Count').sort_index()

    plt.figure(figsize=(12, 6))
    for year in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[year], marker='o', label=str(year))

    plt.title('Monthly Burglary Patterns by Year')
    plt.xlabel('Month')
    plt.ylabel('Number of Burglaries')
    plt.xticks(range(1, 13), 
            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.grid(True)
    plt.legend(title='Year')
    plt.tight_layout()
    plt.show()


def plot_monthly_average_including_all_crimes(data_dir: str = 'UK_police_data'):
    burglary_data = []
    all_crime_data = []

    for month_dir in sorted(os.listdir(data_dir)):
        csv_path = os.path.join(data_dir, month_dir, f"{month_dir}-metropolitan-street.csv")
        
        if os.path.isfile(csv_path):
            df = pd.read_csv(csv_path)
            month_num = int(month_dir[5:7])

            burglary_count = len(df[df['Crime type'] == 'Burglary'])
            all_crime_count = len(df)

            burglary_data.append({'Month': month_num, 'Count': burglary_count})
            all_crime_data.append({'Month': month_num, 'Count': all_crime_count})

    burglary_df = pd.DataFrame(burglary_data)
    all_crime_df = pd.DataFrame(all_crime_data)

    burglary_avg = burglary_df.groupby('Month')['Count'].mean().reset_index()
    all_crime_avg = all_crime_df.groupby('Month')['Count'].mean().reset_index()

    # Use MinMaxScaler to scale counts between 0 and 1
    scaler = MinMaxScaler()

    burglary_avg['Normalized'] = scaler.fit_transform(burglary_avg[['Count']])
    all_crime_avg['Normalized'] = scaler.fit_transform(all_crime_avg[['Count']])

    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.figure(figsize=(10, 6))
    plt.plot(burglary_avg['Month'], burglary_avg['Normalized'], marker='o', linestyle='-', label='Burglaries (Normalized)')
    plt.plot(all_crime_avg['Month'], all_crime_avg['Normalized'], marker='s', linestyle='--', label='All Crimes (Normalized)', alpha=0.7)

    plt.xticks(ticks=range(1, 13), labels=month_labels)
    plt.title('Normalized Average Monthly Crime Counts')
    plt.xlabel('Month')
    plt.ylabel('Normalized Count (0-1)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


plot_monthly_average()
plot_monthly_average_including_all_crimes()
plot_year_stacked()
