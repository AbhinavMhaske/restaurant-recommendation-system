import streamlit as st

from src.content_recommender import recommend
from src.data_loader import load_data
from src.image_helper import get_restaurant_image

from src.charts import (
    show_top_cuisines,
    show_rating_distribution,
    show_cost_distribution,
    show_restaurant_types,
)

# Load dataset
df = load_data()
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Restaurant Recommendation System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.title("🍽️ Restaurant Recommendation System")

dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=True
)

if dark_mode:

    st.markdown("""
    <style>

    .stApp{
        background:#0E1117;
        color:white;
    }

    [data-testid="metric-container"]{
        background:#1E1E1E;
        border-radius:15px;
        border:1px solid #30363D;
        padding:18px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]{
        background:#161B22;
        border-radius:18px;
        border:1px solid #30363D;
        box-shadow:0px 5px 15px rgba(0,0,0,.35);
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>

    .stApp{
        background:#F8FAFC;
        color:#111827;
    }

    /* All text */
    .stApp,
    .stMarkdown,
    p,
    span,
    div,
    label,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6{
        color:#111827 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"]{
        background:white;
    }

    [data-testid="stSidebar"] *{
        color:#111827 !important;
    }

    /* Metric cards */
    [data-testid="metric-container"]{
        background:white;
        color:#111827 !important;
        border-radius:15px;
        border:1px solid #E5E7EB;
        padding:18px;
    }

    /* Recommendation cards */
    div[data-testid="stVerticalBlockBorderWrapper"]{
        background:white;
        border-radius:18px;
        border:1px solid #E5E7EB;
        box-shadow:0px 4px 10px rgba(0,0,0,.08);
    }

    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.subheader("❤️ Favorites")

if len(st.session_state.favorites) == 0:
    st.sidebar.write("No favorites yet.")

else:
    for restaurant in st.session_state.favorites:
        st.sidebar.write("❤️", restaurant)

st.sidebar.write("### Dataset Statistics")

st.sidebar.metric("Restaurants", len(df))
st.sidebar.metric("Average Rating", round(df["rate (out of 5)"].mean(), 2))
st.sidebar.metric("Unique Cuisines", df["cuisines type"].nunique())

st.sidebar.markdown("---")

st.sidebar.info("""
### 👨‍💻 Developer

**Abhinav Mhaske**

Computer Science Student

Interested in:
- 🔐 Cybersecurity
- 🤖 Machine Learning
- 🌐 Full Stack Development
""")

st.sidebar.markdown("---")

st.sidebar.success("🚀 Version 1.0")

st.sidebar.caption("Made with ❤️ using Python & Streamlit")

# ----------------------------
# Main Page
# ----------------------------
st.markdown("""
<h1 style='text-align:center;font-size:52px;'>
🍽️ Restaurant Recommendation Engine
</h1>

<p style='text-align:center;font-size:22px;color:gray;'>
Discover restaurants you'll love using Machine Learning
</p>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs([
    "🍽 Recommendation",
    "⚖️ Compare Restaurants"
])

with tab1:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
        "🍴 Restaurants",
        len(df)
        )

    with col2:
        st.metric(
        "⭐ Avg Rating",
        round(df["rate (out of 5)"].mean(), 2)
        )

    with col3:
        st.metric(
        "🍜 Cuisine Types",
        df["cuisines type"].nunique()
        )

    with col4:
        st.metric(
        "💰 Avg Cost",
        f"₹{int(df['avg cost (two people)'].mean())}"
        )
    
        st.subheader("📈 Quick Insights")
        
        high_rating = len(
            df[df["rate (out of 5)"] >= 4]
        )

        percentage = round(
            high_rating / len(df) * 100,
            1
        )

        st.success(
            f"⭐ {percentage}% of restaurants have a rating above 4."
        )
        popular_area = (
            df["area"]
            .value_counts()
            .idxmax()
        )

        st.info(
            f"📍 Most popular area: {popular_area}"
        )

        popular_cuisine = (
            df["cuisines type"]
            .str.split(",")
            .explode()
            .str.strip()
            .value_counts()
            .idxmax()
        )

        st.info(
            f"🍜 Most popular cuisine: {popular_cuisine}"
        )

with col1:
    st.metric("🍴 Restaurants", len(df))

with col2:
    st.metric(
        "⭐ Avg Rating",
        round(df["rate (out of 5)"].mean(), 2)
    )

with col3:
    st.metric(
        "🍜 Cuisine Types",
        df["cuisines type"].nunique()
    )
st.write("Find restaurants similar to your favourite restaurant.")

st.divider()
st.subheader("⚙️ Recommendation Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:

    cuisines = ["All"] + sorted(
        df["cuisines type"]
        .str.split(",")
        .explode()
        .str.strip()
        .unique()
    )

    selected_cuisine = st.selectbox(
        "🍜 Preferred Cuisine",
        cuisines
    )

    if selected_cuisine != "All":

        filtered = df[
            df["cuisines type"].str.contains(
                selected_cuisine,
                case=False,
                na=False
            )
        ]

    else:
        filtered = df

    restaurant = st.selectbox(
        "🍴 Search Restaurant",
        sorted(filtered["restaurant name"].unique()),
        placeholder="Type restaurant name..."
    )
with col2:
    num = st.slider(
        "📋 Number of Recommendations",
        1,
        10,
        5
    )
with col3:
    min_rating = st.slider(
        "⭐ Minimum Rating",
        0.0,
        5.0,
        3.5,
        0.1
    )
with col4:
    max_cost = st.number_input(
        "💰 Maximum Budget",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )
areas = ["All Areas"] + sorted(df["area"].unique().tolist())

selected_area = st.selectbox(
    "📍 Area",
    areas
)

if restaurant:

    selected = df[df["restaurant name"] == restaurant].iloc[0]

    st.subheader("🎯 Selected Restaurant")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("⭐ Rating", selected["rate (out of 5)"])

    with c2:
        st.metric("💰 Cost", f"₹{selected['avg cost (two people)']}")

    with c3:
        st.metric("📍 Area", selected["area"])

    with c4:
        st.metric("🏠 Type", selected["restaurant type"])

    st.write(f"**🍜 Cuisine:** {selected['cuisines type']}")
# ----------------------------
# Button
# ----------------------------
if st.button("🔍 Recommend"):

    with st.spinner("🔎 Finding the best restaurants for you..."):

        recommendations = recommend(
            restaurant_name=restaurant,
            n=num,
            min_rating=min_rating,
            max_cost=max_cost,
            area=selected_area
        )
    
    import pandas as pd

    rec_df = pd.DataFrame(recommendations)
    
    if isinstance(recommendations, str):
        st.error(recommendations)

    else:

        st.success(
            f"Showing {len(recommendations)} recommendations for **{restaurant}**"
        )
        avg_rating = round(rec_df["Rating"].mean(), 2)

        avg_cost = int(rec_df["Cost"].mean())

        popular_area = rec_df["Area"].mode()[0]

        popular_type = rec_df["Type"].mode()[0]

        popular_cuisine = (
            rec_df["Cuisine"]
            .str.split(",")
            .explode()
            .str.strip()
            .mode()[0]
        )

        st.info(f"""
        ### 🤖 Recommendation Summary

        Based on **{restaurant}**, we found restaurants that are:

       🍜 Mostly **{popular_cuisine}**

       ⭐ Average Rating **{avg_rating}/5**

       💰 Average Budget **₹{avg_cost}**

       📍 Mostly located in **{popular_area}**

       🏠 Mostly **{popular_type}**
  """)

        rec_df = pd.DataFrame(recommendations)

        st.download_button(
        label="📥 Download Recommendations (CSV)",
        data=rec_df.to_csv(index=False),
        file_name="restaurant_recommendations.csv",
        mime="text/csv"
        )

        st.divider()
        st.subheader("📊 Recommendation Summary")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "⭐ Avg Rating",
                round(rec_df["Rating"].mean(), 2)
            )

        with c2:
            st.metric(
                "💰 Avg Cost",
                f"₹{int(rec_df['Cost'].mean())}"
            )

        with c3:
            st.metric(
                "🍜 Top Cuisine",
                rec_df["Cuisine"].mode()[0]
            )

        with c4:
            st.metric(
                "📍 Popular Area",
                rec_df["Area"].mode()[0]
            )

        st.subheader("🍴 Recommended Restaurants")

        for item in recommendations:

            with st.container(border=True):

                st.markdown(f"## 🍽️ {item['Restaurant']}")

                image_url = get_restaurant_image(item["Restaurant"])

                if image_url:
                    st.image(
                        image_url,
                        use_container_width=True
                    )

                st.image(
                    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
                    use_container_width=True
                )
            
                image_url = get_restaurant_image(item["Cuisine"])

                st.image(
                    image_url,
                    use_container_width=True
                )

                st.markdown(f"## 🍽️ {item['Restaurant']}")
                if st.button(
                    f"❤️ Save {item['Restaurant']}",
                    key=f"fav_{item['Restaurant']}"
                ):

                    if item["Restaurant"] not in st.session_state.favorites:
                        st.session_state.favorites.append(item["Restaurant"])

                left, right = st.columns([2, 1])

                with left:

                    st.markdown(f"""
                **🍜 Cuisine**

                {item['Cuisine']}
                """)

                    rating = float(item["Rating"])

                    if rating >= 4.5:
                        badge = "🟢 Excellent"
                    elif rating >= 4.0:
                        badge = "🟡 Very Good"
                    elif rating >= 3.0:
                        badge = "🟠 Good"
                    else:
                        badge = "🔴 Average"

                    st.markdown(f"### ⭐ {rating}/5")
                    st.caption(badge)

                    cost = item["Cost"]

                    if cost <= 500:
                        budget = "🟢 Budget"
                    elif cost <= 1000:
                        budget = "🟡 Moderate"
                    else:
                        budget = "🔴 Premium"

                    st.markdown(f"""
                **💰 Cost for Two**

                ₹{cost}

                {budget}
                """)

                    st.write(f"📍 **Area:** {item['Area']}")
                    st.write(f"🏠 **Type:** {item['Type']}")

                    st.markdown("#### 🎯 Why this recommendation?")

                    for reason in item["Reasons"]:
                        st.write(reason)

                with right:

                    match = item["Similarity"]

                    st.metric(
                        label="🎯 Match Score",
                        value=f"{match}%"
                    )

                    if match >= 90:
                        st.success("🔥 Excellent Match")

                    elif match >= 80:
                          st.info("⭐ Highly Recommended")

                    elif match >= 70:
                          st.warning("👍 Good Match")

                    else:
                        st.error("⚠️ Low Match")

                    badges = []

                    if item["Rating"] >= 4.5:
                        badges.append("🏆 Top Rated")

                    if item["Cost"] <= 500:
                        badges.append("💰 Budget")

                    if item["Similarity"] >= 90:
                        badges.append("🔥 Popular")

                    if "Family" in item["Type"]:
                        badges.append("👨‍👩‍👧 Family")

                    if "Cafe" in item["Type"]:
                        badges.append("☕ Cafe")

                    if match > 90:
                        st.success("Excellent Match")
                    elif match > 80:
                        st.info("Very Similar")
                    else:
                        st.warning("Worth Trying")

                st.markdown(" ".join(badges))

                st.caption("Recommendation Confidence")
                
                st.caption("🤖 AI Recommendation Confidence")
                
                st.progress(match / 100)

                st.caption(
                    f"{100 - match:.1f}% different from your selected restaurant"
                )

                st.divider()

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")

st.header("📊 Dataset Analytics")

show_top_cuisines(df)
show_rating_distribution(df)
show_cost_distribution(df)
show_restaurant_types(df)

st.caption(
    "Restaurant Recommendation System | Built using Python, Pandas, Scikit-Learn and Streamlit"
)

with tab2:

    st.header("⚖️ Compare Restaurants")

    # Select Restaurants
    colA, colB = st.columns(2)

    with colA:
        restaurant1 = st.selectbox(
            "🍽️ Restaurant 1",
            sorted(df["restaurant name"].unique()),
            key="compare1"
        )

    with colB:
        restaurant2 = st.selectbox(
            "🍽️ Restaurant 2",
            sorted(df["restaurant name"].unique()),
            index=1,
            key="compare2"
        )

    # Get restaurant details
    r1 = df[df["restaurant name"] == restaurant1].iloc[0]
    r2 = df[df["restaurant name"] == restaurant2].iloc[0]

    st.divider()

    # Comparison Cards
    left, right = st.columns(2)

    with left:

        st.subheader(f"🍽️ {restaurant1}")

        st.metric(
            "⭐ Rating",
            r1["rate (out of 5)"]
        )

        st.metric(
            "💰 Cost for Two",
            f"₹{r1['avg cost (two people)']}"
        )

        st.write("🍜 **Cuisine:**", r1["cuisines type"])
        st.write("📍 **Area:**", r1["area"])
        st.write("🏠 **Type:**", r1["restaurant type"])
        st.write("📱 **Online Order:**", r1["online_order"])
        st.write("🍽️ **Table Booking:**", r1["table booking"])

    with right:

        st.subheader(f"🍽️ {restaurant2}")

        st.metric(
            "⭐ Rating",
            r2["rate (out of 5)"]
        )

        st.metric(
            "💰 Cost for Two",
            f"₹{r2['avg cost (two people)']}"
        )

        st.write("🍜 **Cuisine:**", r2["cuisines type"])
        st.write("📍 **Area:**", r2["area"])
        st.write("🏠 **Type:**", r2["restaurant type"])
        st.write("📱 **Online Order:**", r2["online_order"])
        st.write("🍽️ **Table Booking:**", r2["table booking"])

    st.divider()

    st.subheader("🏆 Comparison Result")

    # Rating Winner
    if r1["rate (out of 5)"] > r2["rate (out of 5)"]:
        st.success(f"⭐ **{restaurant1}** has the higher rating.")

    elif r2["rate (out of 5)"] > r1["rate (out of 5)"]:
        st.success(f"⭐ **{restaurant2}** has the higher rating.")

    else:
        st.info("⭐ Both restaurants have the same rating.")

    # Budget Winner
    if r1["avg cost (two people)"] < r2["avg cost (two people)"]:
        st.info(f"💰 **{restaurant1}** is more budget-friendly.")

    elif r2["avg cost (two people)"] < r1["avg cost (two people)"]:
        st.info(f"💰 **{restaurant2}** is more budget-friendly.")

    else:
        st.info("💰 Both restaurants have the same price.")

    # Same Area
    if r1["area"] == r2["area"]:
        st.success("📍 Both restaurants are in the same area.")

    # Same Cuisine
    if r1["cuisines type"] == r2["cuisines type"]:
        st.success("🍜 Both restaurants serve similar cuisine.")

    # Same Restaurant Type
    if r1["restaurant type"] == r2["restaurant type"]:
        st.success("🏠 Both are the same restaurant type.")   

