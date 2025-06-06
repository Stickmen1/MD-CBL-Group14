import pandas as pd
import numpy as np
import statsmodels.api as sm
from dateutil.relativedelta import relativedelta

# 1. Load burglary data and aggregate per LSOA per month
df = pd.read_csv("all_burglary_data.csv")
df["Month"] = pd.to_datetime(df["Month"], format="%Y-%m").dt.to_period("M").astype(str)

df_burglary = df[df["Crime type"] == "Burglary"]
burglary_counts = (
    df_burglary
    .groupby(["LSOA name", "Month"])
    .size()
    .reset_index(name="Burglary Count")
    .sort_values(by=["Month", "Burglary Count"], ascending=[True, False])
)

burglary_counts.to_csv("burglary_risk_by_ward.csv", index=False)
print("Burglary risk per LSOA ward per month saved to 'burglary_risk_by_ward.csv'.")

# 2. Load IMD data and merge with burglary data
risk_df = pd.read_csv("burglary_risk_by_ward.csv")
imd_df = pd.read_csv("merged_lsoa_crime_data.csv")
risk_df.rename(columns={"LSOA name": "LSOA"}, inplace=True)
imd_df.rename(columns={"LSOA name (2011)": "LSOA"}, inplace=True)

data = risk_df.merge(imd_df, on="LSOA", how="left", validate="many_to_one").dropna(subset=["Burglary Count"])

# 3. time/seasonality features
data["Month"] = pd.to_datetime(data["Month"])
data["Month_Period"] = data["Month"].dt.to_period("M")
min_period = data["Month_Period"].min()
data["month_num"] = (data["Month_Period"] - min_period).apply(lambda x: x.n)
data["sin12"] = np.sin(2 * np.pi * data["month_num"] / 12)
data["cos12"] = np.cos(2 * np.pi * data["month_num"] / 12)

# 4. regression model 
X_cols = {
    "Income Score (rate)": "x1",
    "Employment Score (rate)": "x2",
    "Education, Skills and Training Score": "x3",
    "Health Deprivation and Disability Score": "x4",
    "Barriers to Housing and Services Score": "x5",
    "Living Environment Score": "x6",
    "Children and Young People Sub-domain Score": "x7",
    "Adult Skills Sub-domain Score": "x8",
    "Wider Barriers Sub-domain Score": "x9",
    "Indoors Sub-domain Score": "x10",
    "Outdoors Sub-domain Score": "x11",
}
X_use = {csv: alias for csv, alias in X_cols.items() if csv in data.columns}

X = data[list(X_use.keys()) + ["month_num", "sin12", "cos12"]]
X = sm.add_constant(X)
y = data["Burglary Count"]
combined = pd.concat([X, y], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
X = combined.drop("Burglary Count", axis=1)
y = combined["Burglary Count"]

model = sm.OLS(y, X).fit()
print(model.summary())

# 5. forecast for each calendar month across years 
imd_df = pd.read_csv("merged_lsoa_crime_data.csv")
imd_df.rename(columns={"LSOA name (2011)": "LSOA"}, inplace=True)
X_use_list = list(X_use.keys())

ref_month = pd.to_datetime("2022-03")  
forecast_months = [f"Month-{i+1:02d}" for i in range(12)]  # Month-01 to Month-12
forecast_results = []

for i in range(12):
    target_month = pd.to_datetime(f"2025-{i+1:02d}")
    month_num = ((target_month.to_period("M") - ref_month.to_period("M")).n)
    sin12 = np.sin(2 * np.pi * month_num / 12)
    cos12 = np.cos(2 * np.pi * month_num / 12)

    pred_df = imd_df[["LSOA"] + X_use_list].copy()
    pred_df["month_num"] = month_num
    pred_df["sin12"] = sin12
    pred_df["cos12"] = cos12
    pred_df["Month"] = forecast_months[i]

    X_pred = sm.add_constant(pred_df[X_use_list + ["month_num", "sin12", "cos12"]], has_constant="add")
    pred_df["Predicted Burglary Count"] = model.predict(X_pred)
    forecast_results.append(pred_df)

full_forecast = pd.concat(forecast_results, ignore_index=True)

# mormalize within each calendar month
full_forecast["Risk %"] = (
    full_forecast.groupby("Month")["Predicted Burglary Count"]
    .transform(lambda x: 100 * (x - x.min()) / (x.max() - x.min()))
)

full_forecast.to_csv("burglary_risk_forecast_all_months.csv", index=False)
print("Forecast for every calendar month saved to 'burglary_risk_forecast_all_months.csv'.")

# example for January
print("\n Top 5 most at-risk LSOAs in January:")
print(full_forecast[full_forecast["Month"] == "Month-01"]
      .sort_values("Risk %", ascending=False)[["LSOA", "Predicted Burglary Count", "Risk %"]].head(5))
