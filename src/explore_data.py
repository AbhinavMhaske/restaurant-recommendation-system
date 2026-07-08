import pandas as pd

# Load dataset
df = pd.read_csv("data/zomato.csv.csv")

# Remove unwanted columns
df.drop(columns=["Unnamed: 0", "Unnamed: 9"], inplace=True)

print("=" * 50)
print("First 5 Rows")
print("=" * 50)
print(df.head())

print("\n" + "=" * 50)
print("Dataset Information")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("Missing Values")
print("=" * 50)
print(df.isnull().sum())

print("\n" + "=" * 50)
print("Statistics")
print("=" * 50)
print(df.describe(include="all"))