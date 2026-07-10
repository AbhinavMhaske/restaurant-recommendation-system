from src.data_loader import load_data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load cleaned dataset
df = load_data()

# Convert cuisine text into vectors
tfidf = TfidfVectorizer(stop_words="english")
df["combined_features"] = (
    df["cuisines type"] + " " +
    df["restaurant type"] + " " +
    df["area"] + " " +
    df["online_order"] + " " +
    df["table booking"]
)

tfidf_matrix = tfidf.fit_transform(df["combined_features"])
# Calculate similarity matrix
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Normalize rating (0 to 1)
df["normalized_rating"] = df["rate (out of 5)"] / 5

def recommend(
    restaurant_name,
    n=5,
    min_rating=0,
    max_cost=10000,
    area=None
):
    # Check if restaurant exists
    if restaurant_name not in df["restaurant name"].values:
        return "Restaurant not found."

    # Get index of selected restaurant
    idx = df[df["restaurant name"] == restaurant_name].index[0]
    selected = df.iloc[idx]

    # Similarity scores
    similarity_scores = list(enumerate(similarity_matrix[idx]))

    # Sort by similarity
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []
    seen = set()

    for i, score in similarity_scores:

        name = df.iloc[i]["restaurant name"]

        # Skip the searched restaurant
        if name.lower() == restaurant_name.lower():
            continue

        # Skip duplicates
        if name in seen:
            continue

        # Rating filter
        if df.iloc[i]["rate (out of 5)"] < min_rating:
            continue

        # Budget filter
        if df.iloc[i]["avg cost (two people)"] > max_cost:
            continue

        # Area filter
        if area and area != "All Areas":
            if df.iloc[i]["area"] != area:
                continue

        seen.add(name)

        candidate = df.iloc[i]

        # Rating score
        rating_score = candidate["normalized_rating"]

        # Budget similarity
        budget_difference = abs(
            candidate["avg cost (two people)"] -
            selected["avg cost (two people)"]
        )

        budget_score = max(
            0,
            1 - budget_difference / 5000
        )

        # Same restaurant type
        type_score = (
            1
            if candidate["restaurant type"] ==
               selected["restaurant type"]
            else 0
        )

        # Same area
        area_score = (
            1
            if candidate["area"] ==
               selected["area"]
            else 0
        )
        
        score_breakdown = {
            "Cuisine": round(score * 55, 2),
            "Rating": round(rating_score * 20, 2),
            "Budget": round(budget_score * 15, 2),
            "Area": round(area_score * 5, 2),
            "Type": round(type_score * 5, 2)
        }

        # Final hybrid score
        final_score = (
            score * 0.55 +
            rating_score * 0.20 +
            budget_score * 0.15 +
            area_score * 0.05 +
            type_score * 0.05
        )
        
        recommendations = sorted(
            recommendations,
            key=lambda x: x["Similarity"],
            reverse=True
        )
        
        reasons = []

        if candidate["area"] == selected["area"]:
            reasons.append("📍 Same Area")

        if candidate["restaurant type"] == selected["restaurant type"]:
            reasons.append("🏠 Same Restaurant Type")

        if abs(
            candidate["avg cost (two people)"] -
            selected["avg cost (two people)"]
        ) <= 300:
            reasons.append("💰 Similar Budget")

        if candidate["rate (out of 5)"] >= selected["rate (out of 5)"]:
            reasons.append("⭐ Highly Rated")

        reasons.append("🍜 Similar Cuisine")

        recommendations.append({
            "Restaurant": name,
            "Cuisine": df.iloc[i]["cuisines type"],
            "Rating": df.iloc[i]["rate (out of 5)"],
            "Cost": df.iloc[i]["avg cost (two people)"],
            "Area": df.iloc[i]["area"],
            "Type": df.iloc[i]["restaurant type"],
            "Similarity": round(final_score * 100, 2),
            "Reasons": reasons,
            "Breakdown": score_breakdown,
 })       

    return recommendations[:n]


if __name__ == "__main__":

    restaurant = "Empire Restaurant"

    result = recommend(restaurant)

    print(f"\nRestaurants similar to '{restaurant}'\n")

    if isinstance(result, str):
        print(result)

    else:
        for i, item in enumerate(result, start=1):

            print(f"{i}. {item['Restaurant']}")
            print(f"   Cuisine : {item['Cuisine']}")
            print(f"   Rating  : {item['Rating']}")
            print(f"   Cost    : ₹{item['Cost']}")
            print(f"   Area    : {item['Area']}")
            print(f"   Type    : {item['Type']}")
            print(f"   Similarity : {item['Similarity']}%")
            print()