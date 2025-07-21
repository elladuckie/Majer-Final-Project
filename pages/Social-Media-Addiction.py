import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("data/Students-Social-Media-Addiction.csv")

    # Clean money columns
    if "Debt" in df.columns:
        df["Debt"] = pd.to_numeric(df["Debt"].replace({r"[$,]": ""}, regex=True), errors="coerce")
    if "Income" in df.columns:
        df["Income"] = pd.to_numeric(df["Income"].replace({r"[$,]": ""}, regex=True), errors="coerce")

    # Convert key columns to numeric if they exist
    for col in ["Total Time Spent", "ProductivityLoss", "Addicted_Score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Order Gender
    if "Gender" in df.columns:
        df["Gender"] = pd.Categorical(df["Gender"], categories=["Male", "Female"], ordered=True)

    return df

df = load_data()

# Define group columns and numeric columns OUTSIDE tabs
group_cols = [
    "Gender", "Location", "Debt", "Owns Property", "Profession", "Demographics", "Platform", 
    "Video Category", "Frequency", "Watch Reason", "Device Type", "OS", "Watch Time", 
    "Current Activity", "Connection Type"
]
numeric_cols = [col for col in df.columns if col not in group_cols and pd.api.types.is_numeric_dtype(df[col])]

default_cats = ["Total Time Spent", "ProductivityLoss"]
default_cats = [col for col in default_cats if col in numeric_cols]

# Create three tabs
tab1, tab2, tab3 = st.tabs(["📊 Gender Pie Chart", "📈 Addiction Score Analysis", "🧩 Breakdown"])

with tab1:
    st.header("Gender Distribution Pie Charts by Selected Data")

    # Multiselect inside tab1
    categories = st.multiselect(
        "Select numeric data categories to compare by gender",
        options=numeric_cols,
        default=default_cats
    )


    st.markdown(
        """
        <p style='text-align: center;'>
        Through this data it can be concluded that men have a higher addiction rate than women,
        leading by about 0.7%. Higher addiction scores mean those people probably have a big problem with that thing, 
        and in this case that means social media addiction. It could be hurting their life, like school or friendships. 
        They might need help to stop or control it.
        </p>
        """,
        unsafe_allow_html=True
    )

    if categories:
        for cat in categories:
            st.subheader(f"Breakdown of {cat} by Gender")
            if "Gender" in df.columns and cat in df.columns:
                gender_sums = df.groupby("Gender")[cat].sum()
                fig, ax = plt.subplots()
                colors = ["#E29905FF", "#C05077"]  # Male and Female colors
                ax.pie(
                    gender_sums,
                    labels=gender_sums.index,
                    autopct="%1.1f%%",
                    colors=colors,
                    startangle=90,
                )
                ax.axis("equal")
                st.pyplot(fig)
            else:
                st.warning(f"Missing 'Gender' or '{cat}' column.")
    else:
        st.info("Please select at least one data category to compare.")

with tab2:
    st.header("Average Addiction Score by Education Level")

    if "Addicted_Score" in df.columns and "Academic_Level" in df.columns:
        # Drop missing values for safety
        edu_df = df[["Academic_Level", "Addicted_Score"]].dropna()

        # Group by Education level and calculate the average addiction score
        avg_scores = edu_df.groupby("Academic_Level")["Addicted_Score"].mean().sort_values()

        # Define custom colors
        custom_colors = ["#F1C3DD", "#D47EB0", "#D689D6"]  # Add more if you have more levels

        # Plot the bar chart
        fig2, ax2 = plt.subplots()
        bars = ax2.barh(avg_scores.index, avg_scores.values, color=custom_colors[:len(avg_scores)])

        ax2.set_xlabel("Average Addiction Score")
        ax2.set_ylabel("Education Level")
        ax2.set_title("Addiction Score by Education Level")
        ax2.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.4)

        st.pyplot(fig2)

        st.markdown(
            """
            <p style='text-align: center;'>
            This chart shows how education level might be linked to social media addiction.
            For example, higher or lower addiction scores across groups may hint at how stress, workload, or free time affect usage.
            </p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Missing 'Addicted_Score' or 'Academic_Level' column.")


with tab3:
    st.header("Breakdown of certain Data")

    # Check for scatter plot columns
    if "Avg_Daily_Usage_Hours" in df.columns and "Addicted_Score" in df.columns and "Gender" in df.columns:

        men_df = df[df["Gender"] == "Male"]

        if not men_df.empty:
            fig4, ax4 = plt.subplots()
            ax4.scatter(
                men_df["Avg_Daily_Usage_Hours"],
                men_df["Addicted_Score"],
                alpha=0.4,
                s=40,
                edgecolors='none',
                color="#8D6344C3"
            )
            ax4.set_xlabel("Average Hours Using Social Media", fontsize=12)
            ax4.set_ylabel("Addicted Score", fontsize=12)
            ax4.set_title("Men's Social Media Use vs Addiction Score", fontsize=14)
            ax4.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
            st.pyplot(fig4)
        else:
            st.warning("No data for males to plot scatter.")
    else:
        st.warning("Required columns for scatter plot not found.")
