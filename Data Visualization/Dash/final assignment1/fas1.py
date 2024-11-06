import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file with predefined headers
file_name = "historical_automobile_sales.csv"
headers = [
    "Date", "Year", "Month", "Recession", "Consumer_Confidence", "Seasonality_Weight",
    "Price", "Advertising_Expenditure", "Competition", "GDP", "Growth_Rate", "unemployment_rate",
    "Automobile_Sales", "Vehicle_Type", "City"
]

df = pd.read_csv(file_name, names=headers, header=0)

# Convert necessary columns to numeric, with error handling and drop NaNs
numeric_columns = ['Year', 'Automobile_Sales', 'Price', 'Advertising_Expenditure', 'GDP', 'Growth_Rate', 'unemployment_rate', 'Consumer_Confidence', 'Seasonality_Weight']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert Recession to boolean
df['Recession'] = df['Recession'].astype(bool)

# Drop rows with NaN in essential columns
df.dropna(subset=['Year', 'Automobile_Sales', 'Vehicle_Type'], inplace=True)

# Task 1.1: Line chart of Automobile Sales over the Years
df_line = df.groupby('Year')['Automobile_Sales'].mean()
plt.figure(figsize=(10, 6))
df_line.plot(kind='line')
plt.xlabel('Year')
plt.ylabel('Automobile Sales')
plt.title('Automobile Sales Analysis')
plt.grid(True)
plt.show()

# Task 1.2: Analyze sales trends by Vehicle Type during Recession
df_grouped = df.groupby(['Year', 'Vehicle_Type', 'Recession'])['Automobile_Sales'].mean().reset_index()

plt.figure(figsize=(12, 8))
for vehicle_type in df['Vehicle_Type'].unique():
    # Plot for recession and non-recession years
    for recession in [False, True]:
        subset = df_grouped[(df_grouped['Vehicle_Type'] == vehicle_type) & (df_grouped['Recession'] == recession)]
        linestyle = '-' if not recession else '--'
        marker = 'o' if not recession else 'x'
        plt.plot(subset['Year'], subset['Automobile_Sales'], label=f'{vehicle_type} ({"Non-Recession" if not recession else "Recession"})', linestyle=linestyle, marker=marker)

# Customize plot
plt.xlabel('Year')
plt.ylabel('Average Automobile Sales')
plt.title('Automobile Sales Trends by Vehicle Type During Recession and Non-Recession Periods')
plt.legend(title="Vehicle Type and Period", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

# Task 1.3: Seaborn lineplot for sales trend by Vehicle Type
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
sns.lineplot(
    data=df_grouped,
    x='Year',
    y='Automobile_Sales',
    hue='Recession',
    style='Vehicle_Type',
    markers=True,
    dashes=False
)

plt.title('Automobile Sales Trend per Vehicle Type: Recession vs. Non-Recession')
plt.xlabel('Year')
plt.ylabel('Average Automobile Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Task 1.4: Subplots to compare GDP during recession and non-recession periods
df.dropna(subset=['GDP'], inplace=True)

# Separate the data for recession and non-recession periods
df_recession = df[df['Recession']].groupby('Year')['GDP'].mean().reset_index()
df_non_recession = df[~df['Recession']].groupby('Year')['GDP'].mean().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
axes[0].plot(df_recession['Year'], df_recession['GDP'], color='red', marker='o')
axes[0].set_title('GDP During Recession Periods')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('GDP')
axes[0].grid(True)

axes[1].plot(df_non_recession['Year'], df_non_recession['GDP'], color='green', marker='o')
axes[1].set_title('GDP During Non-Recession Periods')
axes[1].set_xlabel('Year')
axes[1].grid(True)

plt.suptitle('Comparison of GDP Variations During Recession and Non-Recession Periods')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Task 1.5: Bubble plot for the impact of seasonality on Automobile Sales
df.dropna(subset=['Seasonality_Weight'], inplace=True)
plt.figure(figsize=(10, 6))
bubble_sizes = df['Automobile_Sales'] / 100  # Scale bubble sizes
plt.scatter(df['Seasonality_Weight'], df['Automobile_Sales'], s=bubble_sizes, alpha=0.5, color='blue', edgecolor='k')
plt.title('Impact of Seasonality on Automobile Sales')
plt.xlabel('Seasonality Weight')
plt.ylabel('Automobile Sales')
plt.grid(True)
plt.show()

# Task 1.6: Scatter plots for correlations during recession
recession_data = df[df['Recession']]

# Scatter Plot 1: Average Vehicle Price vs. Automobile Sales
plt.figure(figsize=(10, 6))
plt.scatter(recession_data['Price'], recession_data['Automobile_Sales'], alpha=0.6, color='blue', edgecolor='k')
plt.title('Average Vehicle Price vs. Automobile Sales (During Recession)')
plt.xlabel('Average Vehicle Price')
plt.ylabel('Automobile Sales Volume')
plt.grid(True)
plt.show()

# Scatter Plot 2: Consumer Confidence vs. Automobile Sales
plt.figure(figsize=(10, 6))
plt.scatter(recession_data['Consumer_Confidence'], recession_data['Automobile_Sales'], alpha=0.6, color='green', edgecolor='k')
plt.title('Consumer Confidence vs. Automobile Sales (During Recession)')
plt.xlabel('Consumer Confidence')
plt.ylabel('Automobile Sales Volume')
plt.grid(True)
plt.show()

# Task 1.7: Pie chart for advertising expenditure during recession and non-recession
df.dropna(subset=['Advertising_Expenditure'], inplace=True)
recession_ad_exp = df[df['Recession']]['Advertising_Expenditure'].sum()
non_recession_ad_exp = df[~df['Recession']]['Advertising_Expenditure'].sum()

labels = ['Recession Period', 'Non-Recession Period']
ad_expenditures = [recession_ad_exp, non_recession_ad_exp]
colors = ['skyblue', 'lightgreen']

plt.figure(figsize=(8, 6))
plt.pie(ad_expenditures, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title('Advertising Expenditure During Recession vs. Non-Recession Periods')
plt.axis('equal')
plt.show()

# Task 1.8: Pie chart for total advertisement expenditure by Vehicle Type during recession
recession_df = df[df['Recession']]
ad_expenditure_by_vehicle = recession_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()

plt.figure(figsize=(8, 6))
plt.pie(ad_expenditure_by_vehicle, labels=ad_expenditure_by_vehicle.index, autopct='%1.1f%%', startangle=90)
plt.title('Total Advertisement Expenditure by Vehicle Type During Recession Period')
plt.axis('equal')
plt.show()

# Task 1.9: Lineplot to analyze the effect of the unemployment rate on vehicle sales during recession
df.dropna(subset=['unemployment_rate'], inplace=True)

plt.figure(figsize=(12, 6))
sns.lineplot(data=recession_data, x='unemployment_rate', y='Automobile_Sales', hue='Vehicle_Type', markers=True)
plt.title('Effect of Unemployment Rate on Vehicle Sales During Recession')
plt.xlabel('Unemployment Rate')
plt.ylabel('Automobile Sales')
plt.legend(title="Vehicle Type")
plt.grid(True)
plt.tight_layout()
plt.show()

