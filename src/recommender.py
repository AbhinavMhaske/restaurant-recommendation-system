from src.data_loader import load_data


def recommend_restaurants(cuisine, min_rating, max_cost):
    """
    Recommend restaurants based on cuisine, rating and budget.
    """

    # Load cleaned dataset
    df = load_data()

    # Apply filters
    recommendations = df[
        (df["cuisines type"].str.contains(cuisine, case=False, na=False))
        & (df["rate (out of 5)"] >= min_rating)
        & (df["avg cost (two people)"] <= max_cost)
    ]

    # Sort by rating first, then number of ratings
    recommendations = recommendations.sort_values(
        by=["rate (out of 5)", "num of ratings"],
        ascending=False
    )

    return recommendations
if __name__ == "__main__":

    result = recommend_restaurants(
        cuisine="North Indian",
        min_rating=4.0,
        max_cost=800
    )

    print("\nRecommended Restaurants\n")

    print(
        result[
            [
                "restaurant name",
                "cuisines type",
                "rate (out of 5)",
                "avg cost (two people)",
                "area"
            ]
        ].head(10)
    )