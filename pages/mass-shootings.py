#ally's data:
import altair as alt
import pandas as pd
import streamlit as st
#import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Mass Shootings")
st.title(":red[Mass Shootings]")


def load_data():
    df = pd.read_csv("data/mass-shootings.csv")
    return df

df = load_data()
st.dataframe(df)

# df = df.drop(
#     ['']
# )
columns = df[['Date','Gender','Mental Health Issues']]

#visuals: line chart, graphviz
#connections to make: increase of shootings to increase of internet usage
#mental health issues in shooters and internet users
shootings = df.groupby("Date").size().reset_index(name="Count")
shootings

st.lineplot(data=shootings, x="Date", y="Count", marker="o")
st.title("Mass Shootings per year")
st.xlabel("Year")
st.ylabel("Number of Shootings")
st.show()
