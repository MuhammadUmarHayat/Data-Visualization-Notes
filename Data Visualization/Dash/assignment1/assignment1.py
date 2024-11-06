import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import io
import requests
import datetime as dt


# Define the file name
file_name = "Historical_Wildfires.csv"

# Define the headers (assuming you want to set custom headers)
headers = [
    "Region", "Date", 
    "Estimated_fire_area", 
    "Mean_estimated_fire_brightness", 
    "Mean_estimated_fire_radiative_power", 
    "Mean_confidence", 
    "Std_confidence", 
    "Var_confidence", 
    "Count", "Replaced"
]

# Load the CSV file
df = pd.read_csv(file_name, names=headers)

# Display the first few rows of the DataFrame
print("DataFrame Head:")
print(df.head())

# Display the column names
print("\nColumn Names:")
print(df.columns)

# Display the data types of each column
print("\nData Types:")
print(df.dtypes)

# Ensure 'Estimated_fire_area' is numeric
df['Estimated_fire_area'] = pd.to_numeric(df['Estimated_fire_area'], errors='coerce') #type conversion

# Check if the 'Date' column exists and try converting it to datetime
if 'Date' in df.columns:
    try:
        # Attempt to convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert, setting errors to NaT for invalid parsing
        
        # Extract year and month, handling any NaT values gracefully
        df['Year'] = df['Date'].dt.year  # Type conversion
        df['Month'] = df['Date'].dt.month  # Type conversion
        
        # Display to verify
        print("Year and Month columns added:")
        print(df[['Date', 'Year', 'Month']].head())
    except Exception as e:
        print(f"Error converting 'Date' column: {e}")
else:
    print("The 'Date' column is missing in the DataFrame.")

# Display the data types of each column again to verify
print("\nData Types after conversions:")
print(df.dtypes)

# TASK 1.1: Plotting the change in average estimated fire area over time

plt.figure(figsize=(12, 6))

# Group the data by 'Year' and calculate the mean of 'Estimated_fire_area'
df_new = df.groupby('Year')['Estimated_fire_area'].mean()

# Plot the data
df_new.plot()  # Index will be used for x-axis, and values for y-axis
plt.xlabel('Year')
plt.ylabel('Average Estimated Fire Area (km²)')
plt.title('Estimated Fire Area over Time')
plt.show()
#TASK 1.2: You can notice the peak in the plot between 2010 to 2013. Let's narrow down our finding, by plotting the estimated fire area for year grouped together with month.
# Grouping the data by both 'Year' and 'Month', and calculating the mean of 'Estimated_fire_area'
df_new = df.groupby(['Year','Month'])['Estimated_fire_area'].mean()
    # Plotting the data
df_new.plot(x=df_new.index, y=df_new.values)
plt.xlabel('Year, Month')
plt.ylabel('Average Estimated Fire Area (km²)')
plt.title('Estimated Fire Area over Time')
plt.show()
'''
#TASK 1.3: Let's have an insight on the distribution of mean estimated fire brightness across the regions
#use the functionality of seaborn to develop a barplot

# Creating a bar plot using seaborn to visualize the distribution of mean estimated fire brightness across regions
plt.figure(figsize=(10, 6))
# Using seaborn's barplot function to create the plot
sns.barplot(data=df, x='Region', y='Mean_estimated_fire_brightness')
plt.xlabel('Region')
plt.ylabel('Mean Estimated Fire Brightness (Kelvin)')
plt.title('Distribution of Mean Estimated Fire Brightness across Regions')
plt.show()

'''
#TASK 1.4: Let's find the portion of count of pixels for presumed vegetation fires vary across regions we will develop a pie chart for this
# Creating a pie chart to visualize the portion of count of pixels for presumed vegetation fires across regions


# Converting the 'Count' column to numeric, replacing non-numeric values with NaN, and then filling NaNs with 0
df['Count'] = pd.to_numeric(df['Count'], errors='coerce').fillna(0)

# Grouping the data by region and summing the counts
region_counts = df.groupby('Region')['Count'].sum()

# Plotting the pie chart
plt.figure(figsize=(10, 6))
plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%')
plt.title('Percentage of Pixels for Presumed Vegetation Fires by Region')
plt.axis('equal')
plt.show()

#TASK 1.5: See the percentage on the pie is not looking so good as it is overlaped for Region SA, TA, VI
[(i,round(k/region_counts.sum()*100,2)) for i,k in zip(region_counts.index, region_counts)]
#TASK 1.6: Let's try to develop a histogram of the mean estimated fire brightness
#Using Matplotlib to create the histogram
# Creating a histogram to visualize the distribution of mean estimated fire brightness
plt.figure(figsize=(10, 6))
# Using plt.hist to create the histogram
# Setting the number of bins to 20 for better visualization
plt.hist(x=df['Mean_estimated_fire_brightness'], bins=20)
plt.xlabel('Mean Estimated Fire Brightness (Kelvin)')
plt.ylabel('Count')
plt.title('Histogram of Mean Estimated Fire Brightness')
plt.show()
#TASK 1.7: What if we need to understand the distribution of estimated fire brightness across regions? Let's use the functionality of seaborn and pass region as hue
#Click here for Solution
# Creating a histogram to visualize the distribution of mean estimated fire brightness across regions using Seaborn
# Using sns.histplot to create the histogram
# Specifying the DataFrame (data=df) and the column for the x-axis (x='Mean_estimated_fire_brightness')
# Adding hue='Region' to differentiate the distribution across regions
#sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region')
#plt.show()
# Creating a stacked histogram to visualize the distribution of mean estimated fire brightness across regions using Seaborn
# Using sns.histplot to create the stacked histogram
# Specifying the DataFrame (data=df) and the column for the x-axis (x='Mean_estimated_fire_brightness')
# Adding hue='Region' to differentiate the distribution across regions
# Setting multiple='stack' to stack the histograms for different regions
sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region', multiple='stack')
plt.show()

#TASK 1.8: Let's try to find if there is any correlation between mean estimated fire radiative power and mean confidence level?
# Creating a scatter plot to visualize the relationship between mean estimated fire radiative power and mean  confidence using Seaborn
plt.figure(figsize=(8, 6))
    # Using sns.scatterplot to create the scatter plot
    # Specifying the DataFrame (data=df) and the columns for the x-axis (x='Mean_confidence') and y-axis            (y='Mean_estimated_fire_radiative_power')
sns.scatterplot(data=df, x='Mean_confidence', y='Mean_estimated_fire_radiative_power')
plt.xlabel('Mean Estimated Fire Radiative Power (MW)')
plt.ylabel('Mean Confidence')
plt.title('Mean Estimated Fire Radiative Power vs. Mean Confidence')
plt.show()

#breakpoint()

#ASK 1.9: Let's mark these seven regions on the Map of Australia using Folium
import folium
import pandas as pd

# Data for the regions
region_data = {
    'region': ['NSW', 'QL', 'SA', 'TA', 'VI', 'WA', 'NT'], 
    'Lat': [-31.8759835, -22.1646782, -30.5343665, -42.035067, -36.5986096, -25.2303005, -19.491411], 
    'Lon': [147.2869493, 144.5844903, 135.6301212, 146.6366887, 144.6780052, 121.0187246, 132.550964]
}

# Creating a DataFrame
reg = pd.DataFrame(region_data)

# Instantiate a feature group 
aus_reg = folium.map.FeatureGroup()

# Create a Folium map centered on Australia
Aus_map = folium.Map(location=[-25, 135], zoom_start=4)

# Loop through the regions and add to feature group
for lat, lng, lab in zip(reg.Lat, reg.Lon, reg.region):
    aus_reg.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            popup=lab,
            radius=5,  # Define how big you want the circle markers to be
            color='red',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# Add regions to the map
Aus_map.add_child(aus_reg)

# Display the map
Aus_map  # Use this line in a Jupyter Notebook to render the map

Aus_map.save("australia_map.html")