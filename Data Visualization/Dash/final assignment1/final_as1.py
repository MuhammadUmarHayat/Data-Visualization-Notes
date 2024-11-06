import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium


file_name = "historical_automobile_sales.csv"
headers = [
    "Date","Year", "Month","Recession","Consumer_Confidence","Seasonality_Weight",
    "Price", "Advertising_Expenditure","Competition","GDP","Growth_Rate","unemployment_rate",
    "Automobile_Sales","Vehicle_Type","City"
]

# Load the CSV file, assuming it has headers
df = pd.read_csv(file_name, names=headers, header=0)

# Convert Year and Automobile_Sales to numeric
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Automobile_Sales'] = pd.to_numeric(df['Automobile_Sales'], errors='coerce')

# Group by Year and calculate the mean of Automobile_Sales
df_line = df.groupby('Year')['Automobile_Sales'].mean()

# Create the line chart
plt.figure(figsize=(10, 6))
df_line.plot(kind='line')
plt.xlabel('Year')
plt.ylabel('Automobile Sales')
plt.title('Automobile Sales Analysis')
plt.show()
#TASK 1.2: Plot different lines for categories of vehicle type and analyse the trend to answer the question Is there a noticeable difference in sales trends between different vehicle types during recession periods?


# Convert necessary columns to appropriate types
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Automobile_Sales'] = pd.to_numeric(df['Automobile_Sales'], errors='coerce')
df['Recession'] = df['Recession'].astype(bool)  # Assuming Recession is represented as 1/0 or True/False

# Remove rows with NaN in 'Year' or 'Automobile_Sales'
df = df.dropna(subset=['Year', 'Automobile_Sales', 'Vehicle_Type'])

# Group data by Year, Vehicle_Type, and Recession, and calculate the mean sales
df_grouped = df.groupby(['Year', 'Vehicle_Type', 'Recession'])['Automobile_Sales'].mean().reset_index()

# Initialize the plot
plt.figure(figsize=(12, 8))

# Plot lines for each Vehicle_Type, with separate lines for recession periods
vehicle_types = df['Vehicle_Type'].unique()
for vehicle_type in vehicle_types:
    # Plot for non-recession years
    non_recession_data = df_grouped[(df_grouped['Vehicle_Type'] == vehicle_type) & (df_grouped['Recession'] == False)]
    plt.plot(non_recession_data['Year'], non_recession_data['Automobile_Sales'], label=f'{vehicle_type} (Non-Recession)', linestyle='-', marker='o')
    
    # Plot for recession years
    recession_data = df_grouped[(df_grouped['Vehicle_Type'] == vehicle_type) & (df_grouped['Recession'] == True)]
    plt.plot(recession_data['Year'], recession_data['Automobile_Sales'], label=f'{vehicle_type} (Recession)', linestyle='--', marker='x')

# Customize plot
plt.xlabel('Year')
plt.ylabel('Average Automobile Sales')
plt.title('Automobile Sales Trends by Vehicle Type During Recession and Non-Recession Periods')
plt.legend(title="Vehicle Type and Period", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
#TASK 1.3: Use the functionality of Seaborn Library to create a visualization to compare the sales trend per vehicle type for a recession period with a non-recession period.

# Convert necessary columns to appropriate types
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Automobile_Sales'] = pd.to_numeric(df['Automobile_Sales'], errors='coerce')
df['Recession'] = df['Recession'].astype(bool)  # Assuming Recession is represented as 1/0 or True/False

# Drop rows with missing values in important columns
df = df.dropna(subset=['Year', 'Automobile_Sales', 'Vehicle_Type'])

# Group by Year, Vehicle_Type, and Recession, and calculate the mean sales
df_grouped = df.groupby(['Year', 'Vehicle_Type', 'Recession'])['Automobile_Sales'].mean().reset_index()

# Set up the plot style and context
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))

# Create a line plot with Seaborn
sns.lineplot(
    data=df_grouped,
    x='Year',
    y='Automobile_Sales',
    hue='Recession',  # Separate lines for recession and non-recession periods
    style='Vehicle_Type',  # Different styles for each vehicle type
    markers=True,
    dashes=False  # Solid lines for better comparison
)

# Customize the plot
plt.title('Automobile Sales Trend per Vehicle Type: Recession vs. Non-Recession')
plt.xlabel('Year')
plt.ylabel('Average Automobile Sales')
plt.legend(title="Recession Period")
plt.xticks(rotation=45)  # Rotate x-axis labels for readability
plt.tight_layout()
plt.show()
#TASK 1.4: Use sub plotting to compare the variations in GDP during recession and non-recession period by developing line plots for each period.

# Convert necessary columns to appropriate types
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')
df['Recession'] = df['Recession'].astype(bool)  # Assuming Recession is represented as 1/0 or True/False

# Drop rows with missing values in important columns
df = df.dropna(subset=['Year', 'GDP', 'Recession'])

# Separate the data for recession and non-recession periods
df_recession = df[df['Recession'] == True].groupby('Year')['GDP'].mean().reset_index()
df_non_recession = df[df['Recession'] == False].groupby('Year')['GDP'].mean().reset_index()

# Set up the subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Plot GDP trend during recession periods
axes[0].plot(df_recession['Year'], df_recession['GDP'], color='red', marker='o')
axes[0].set_title('GDP During Recession Periods')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('GDP')
axes[0].grid(True)

# Plot GDP trend during non-recession periods
axes[1].plot(df_non_recession['Year'], df_non_recession['GDP'], color='green', marker='o')
axes[1].set_title('GDP During Non-Recession Periods')
axes[1].set_xlabel('Year')
axes[1].grid(True)

# Adjust layout
plt.suptitle('Comparison of GDP Variations During Recession and Non-Recession Periods')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
#TASK 1.5: Develop a Bubble plot for displaying the impact of seasonality on Automobile Sales.

# Convert necessary columns to numeric types
df['Automobile_Sales'] = pd.to_numeric(df['Automobile_Sales'], errors='coerce')
df['Seasonality_Weight'] = pd.to_numeric(df['Seasonality_Weight'], errors='coerce')

# Drop rows with missing values in important columns
df = df.dropna(subset=['Automobile_Sales', 'Seasonality_Weight'])

# Create bubble plot
plt.figure(figsize=(10, 6))
bubble_sizes = df['Automobile_Sales'] / 100  # Scale down bubble sizes for better visibility

plt.scatter(df['Seasonality_Weight'], df['Automobile_Sales'], s=bubble_sizes, alpha=0.5, color='blue', edgecolor='k')

# Set plot titles and labels
plt.title('Impact of Seasonality on Automobile Sales')
plt.xlabel('Seasonality Weight')
plt.ylabel('Automobile Sales')
plt.grid(True)
plt.show()
breakpoint()
#TASK 1.6: Use the functionality of Matplotlib to develop a scatter plot to identify the correlation between average vehicle price relate to the sales volume during recessions.
#From the data, develop a scatter plot to identify if there a correlation between consumer confidence and automobile sales during recession period?

# Filter the data for recession periods
recession_data = df[df['Recession'] == 1]

# Convert necessary columns to numeric types
recession_data['Price'] = pd.to_numeric(recession_data['Price'], errors='coerce')
recession_data['Automobile_Sales'] = pd.to_numeric(recession_data['Automobile_Sales'], errors='coerce')
recession_data['Consumer_Confidence'] = pd.to_numeric(recession_data['Consumer_Confidence'], errors='coerce')

# Drop rows with missing values in important columns
recession_data = recession_data.dropna(subset=['Price', 'Automobile_Sales', 'Consumer_Confidence'])

### Scatter Plot 1: Average Vehicle Price vs. Automobile Sales (during recession)
plt.figure(figsize=(10, 6))
plt.scatter(recession_data['Price'], recession_data['Automobile_Sales'], alpha=0.6, color='blue', edgecolor='k')
plt.title('Average Vehicle Price vs. Automobile Sales (During Recession)')
plt.xlabel('Average Vehicle Price')
plt.ylabel('Automobile Sales Volume')
plt.grid(True)
plt.show()

### Scatter Plot 2: Consumer Confidence vs. Automobile Sales (during recession)
plt.figure(figsize=(10, 6))
plt.scatter(recession_data['Consumer_Confidence'], recession_data['Automobile_Sales'], alpha=0.6, color='green', edgecolor='k')
plt.title('Consumer Confidence vs. Automobile Sales (During Recession)')
plt.xlabel('Consumer Confidence')
plt.ylabel('Automobile Sales Volume')
plt.grid(True)
plt.show()
breakpoint()
#TASK 1.7: Create a pie chart to display the portion of advertising expenditure of XYZAutomotives during recession and non-recession periods.

# Ensure 'Advertising_Expenditure' and 'Recession' columns are numeric
df['Advertising_Expenditure'] = pd.to_numeric(df['Advertising_Expenditure'], errors='coerce')
df['Recession'] = pd.to_numeric(df['Recession'], errors='coerce')

# Drop any rows with missing values in important columns
df = df.dropna(subset=['Advertising_Expenditure', 'Recession'])

# Separate advertising expenditures for recession and non-recession periods
recession_ad_exp = df[df['Recession'] == 1]['Advertising_Expenditure'].sum()
non_recession_ad_exp = df[df['Recession'] == 0]['Advertising_Expenditure'].sum()

# Pie chart labels and data
labels = ['Recession Period', 'Non-Recession Period']
ad_expenditures = [recession_ad_exp, non_recession_ad_exp]
colors = ['skyblue', 'lightgreen']

# Create the pie chart
plt.figure(figsize=(8, 6))
plt.pie(ad_expenditures, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title('Advertising Expenditure of XYZAutomotives During Recession vs. Non-Recession Periods')
plt.axis('equal')  # Ensures pie chart is a circle
plt.show()
breakpoint()

#TASK 1.8: Develop a pie chart to display the total Advertisement expenditure for each vehicle type during recession period.

# Convert necessary columns to numeric, and drop rows with missing data
df['Advertising_Expenditure'] = pd.to_numeric(df['Advertising_Expenditure'], errors='coerce')
df['Recession'] = pd.to_numeric(df['Recession'], errors='coerce')
df = df.dropna(subset=['Advertising_Expenditure', 'Recession', 'Vehicle_Type'])

# Filter data for recession periods only
recession_df = df[df['Recession'] == 1]

# Group by vehicle type and sum the advertising expenditure for each type
ad_expenditure_by_vehicle = recession_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()

# Plotting the pie chart
plt.figure(figsize=(8, 6))
plt.pie(ad_expenditure_by_vehicle, labels=ad_expenditure_by_vehicle.index, autopct='%1.1f%%', startangle=90)
plt.title('Total Advertisement Expenditure by Vehicle Type During Recession Period')
plt.axis('equal')  # Ensures the pie chart is circular
plt.show()
#TASK 1.9: Develop a lineplot to analyse the effect of the unemployment rate on vehicle type and sales during the Recession Period.
#From the above plot, what insights have you gained on the sales of superminicar, smallfamilycar, mediumminicar?


# Convert necessary columns to numeric
df['Automobile_Sales'] = pd.to_numeric(df['Automobile_Sales'], errors='coerce')
df['unemployment_rate'] = pd.to_numeric(df['unemployment_rate'], errors='coerce')
df['Recession'] = pd.to_numeric(df['Recession'], errors='coerce')

# Drop rows with missing data
df = df.dropna(subset=['Automobile_Sales', 'unemployment_rate', 'Recession', 'Vehicle_Type'])

# Filter for recession periods only
recession_df = df[df['Recession'] == 1]

# Filter for specific vehicle types to focus on the analysis
vehicle_types_of_interest = ['superminicar', 'smallfamilycar', 'mediumminicar']
recession_df = recession_df[recession_df['Vehicle_Type'].isin(vehicle_types_of_interest)]

# Group by unemployment rate and vehicle type, then calculate the mean sales for each combination
sales_by_unemployment_vehicle = (
    recession_df.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales']
    .mean()
    .reset_index()
)

# Plotting with Seaborn lineplot to show the trend
plt.figure(figsize=(12, 8))
sns.lineplot(
    data=sales_by_unemployment_vehicle,
    x='unemployment_rate',
    y='Automobile_Sales',
    hue='Vehicle_Type',
    marker='o'
)

plt.xlabel('Unemployment Rate (%)')
plt.ylabel('Mean Automobile Sales')
plt.title('Effect of Unemployment Rate on Automobile Sales by Vehicle Type During Recession')
plt.legend(title='Vehicle Type')
plt.grid(True)
plt.show()

