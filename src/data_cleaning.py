import pandas as pd


def clean_data():
    # Load dataset
    df = pd.read_csv("data/zomato.csv.csv")

    # Remove unwanted columns
    df.drop(columns=["Unnamed: 0", "Unnamed: 9"], inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove restaurants with 0 rating (Not Rated)
    df = df[df["rate (out of 5)"] > 0]

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df


if __name__ == "__main__":
    df = clean_data()

    print("Dataset cleaned successfully!\n")

    print("Number of restaurants:", len(df))

    print("\nTop 5 Restaurants")

    print(df.head())