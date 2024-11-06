import pandas as pd
import matplotlib.pyplot as plt

# Sample data for automobile sales
data = {
    'Year': [2018, 2019, 2020, 2021, 2022, 2023],
    'Sales': [500000, 550000, 450000, 600000, 650000, 700000]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Set the 'Year' as the index
df.set_index('Year', inplace=True)

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Sales'], marker='o', linestyle='-', color='b')
plt.title('Automobile Sales Fluctuation from Year to Year')
plt.xlabel('Year')
plt.ylabel('Sales')
plt.xticks(df.index)  # Set x-ticks to be the years
plt.grid()
plt.show()
