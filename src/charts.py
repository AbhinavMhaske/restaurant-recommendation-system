print("Loading charts.py...")

import streamlit as st
import plotly.express as px


def show_top_cuisines(df):

    st.subheader("🍜 Top 10 Cuisines")

    cuisines = (
        df["cuisines type"]
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )

    cuisines.columns = ["Cuisine", "Count"]

    fig = px.bar(
        cuisines,
        x="Cuisine",
        y="Count",
        color="Count",
        text="Count"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)


def show_rating_distribution(df):

    st.subheader("⭐ Rating Distribution")

    fig = px.histogram(
        df,
        x="rate (out of 5)",
        nbins=20
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)


def show_cost_distribution(df):

    st.subheader("💰 Cost Distribution")

    fig = px.histogram(
        df,
        x="avg cost (two people)",
        nbins=20
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)


def show_restaurant_types(df):

    st.subheader("🏠 Restaurant Types")

    data = (
        df["restaurant type"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    data.columns = ["Type", "Count"]

    fig = px.bar(
        data,
        x="Type",
        y="Count",
        color="Count",
        text="Count"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)