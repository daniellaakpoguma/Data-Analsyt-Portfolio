import pandas as pd

# Absolute path to the CSV file
csv_file_path = 'C:/Users/rukev/OneDrive/Desktop/Data Analsyt Portfolio/Data-Analsyt-Portfolio/Data Sets/Supermarket Sales/supermarket_sales.csv'

# Load data from CSV file
df = pd.read_csv(csv_file_path)

# Drop rows with missing values
df.dropna(inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Convert Date and Time to datetime format
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Rename columns
df = df.rename(columns={'cogs': 'Cost of Goods Sold', 'gross margin percentage': 'Gross Margin Percentage', 'gross income': 'Gross Income'})

df.info()

