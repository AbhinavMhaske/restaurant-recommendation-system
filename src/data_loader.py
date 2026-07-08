import pandas as pd

def load_data():
    # Load the dataset
    df = pd.read_csv("data/zomato.csv.csv")

    # Remove unwanted columns
    df.drop(columns=["Unnamed: 0", "Unnamed: 9"], inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove rows with missing values
    df.dropna(inplace=True)

    return df


if __name__ == "__main__":
    df = load_data()

    print("Dataset loaded successfully!\n")
    print(df.head())

    print("\nNumber of rows:", df.shape[0])
    print("Number of columns:", df.shape[1])