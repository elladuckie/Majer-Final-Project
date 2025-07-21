import altair as alt
import pandas as pd
import streamlit as st 
#import seaborn as sns
#import matplotlib.pyplot as plt 

st.set_page_config(page_title="FB Hours vs Mental Health by Gender", layout="wide", page_icon="👩🏾‍💻")
st.title("Internet Addiction")

@st.cache_data
def load_data():
    df = pd.read_csv("data/45.csv")
    return df

df = load_data()
df = df.drop(
    ['Education', 'Location', 'PersonalFinance', 'Devices', 'Source', 'Backpain', 'Eyestrain', 'Programstudied', 'MaritalStatuts', 'ParentingStyle', 'RExercise', 'SLDU', 'Stress', 'FBA', 'FPS', 'FRS', 'FUS', 'FSS', 'FSTS', 'BFAD', 'INAD', 'FAD', 'Age_cat', 'MLP_PredictedValue', 'MLP_PseudoProbability_1', 'MLP_PseudoProbability_2', 'BFAD_CAT'], 
    axis=1
)

# Show a slice of the data
st.dataframe(df.iloc[1:128])

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Men's Mental Health & FB Usage", layout="wide")
st.title("📊 Men's Mental Health vs Facebook Usage")

try:
    df = pd.read_csv("data/45.csv")
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces

    # DEBUG: Show column names to check actual values
    st.write("📂 Actual Columns in your file:", df.columns.tolist())

    # Rename if needed
    if "FB Hours" in df.columns:
        df.rename(columns={"FBhours": "FBhours"}, inplace=True)

    # Standardize columns
    df["Gender"] = df["Gender"].astype(str).str.strip().str.lower()
    df["MentalHealth"] = df["MentalHealth"].astype(str).str.strip()
    df["FBhours"] = df["FBhours"].astype(str).str.strip()

    # Filter for males only
    men_df = df[df["Gender"] == "male"]

    # Filter mental health labels
    valid_mh = ["Normal", "Abnormal"]
    men_df = men_df[men_df["MentalHealth"].isin(valid_mh)]

    # Group by FBHours and MentalHealth
    grouped = men_df.groupby(["FBhours", "MentalHealth"]).size().reset_index(name="Count")

    # Fill in all combinations
    fb_categories = ["All day", "Only nighttime", "Only daytime"]
    mh_categories = ["Normal", "Abnormal"]
    all_combos = pd.MultiIndex.from_product([fb_categories, mh_categories], names=["FBhours", "MentalHealth"])
    grouped = grouped.set_index(["FBhours", "MentalHealth"]).reindex(all_combos, fill_value=0).reset_index()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=grouped, x="FBhours", y="Count", hue="MentalHealth", palette={"Normal": "green", "Abnormal": "red"})
    plt.title("Men's Mental Health vs Facebook Usage")
    plt.xlabel("Facebook Usage Time")
    plt.ylabel("Number of Individuals")
    st.pyplot(fig)

    with st.expander("📋 Grouped Data"):
        st.dataframe(grouped)

except FileNotFoundError:
    st.error("❌ File not found. Make sure the file exists at 'data/45.csv'.")
except Exception as e:
    st.error(f"⚠️ Error: {e}")

