import altair as alt
import pandas as pd
import streamlit as st
import numpy as np

#This sets the title of the page
st.set_page_config(page_title=":rainbow[Male Vs. Female]")
st.title(":rainbow[Male Vs. Female]")
#little description
st.write("The page shows the comparison between men and women, and what the effects of social media are for them. This can show how much time they've wasted, how much productivity they've lost, etc.")

#start of code, getting url so we have the data
@st.cache_data
def male_vs_female():
    df = pd.read_csv("data/Time-Wasters-on-Social-Media.csv")

#orders the chart in male first, then female
    df["Gender"] = pd.Categorical(
        df["Gender"],
        categories = ["Male", "Female"],
        ordered = True
    )
#this replaces any dollar sign with a blank space so that it becomes easier to read.
#Ex. $500.00 -> 500.00
#Errors part makes sure that if it can't change the money sign to a space(maybe the sign is in euro), then it just says NaN
    if "Debt" in df.columns:
        df["Debt"] = pd.to_numeric(df["Debt"].replace({f"[$,]": ""}, regex = True), errors = "coerce")
#same for income
    if "Income" in df.columns:
        df["Income"] = pd.to_numeric(df["Income"].replace({f"[$,]": ""}, regex = True), errors = "coerce")


    return df
    
df = male_vs_female()

#this helps to remove all the categories that are strings so the code doesn't break
potential_grouping_columns = ["Gender", "Location", "Debt", "Owns Property", "Profession", "Demographics", "Platform", "Video Category", "Frequency", "Watch Reason", "Device Type", "OS", "Watch Time", "Current Activity", "Connection Type"]
columns_for_multiselect = [col for col in df.columns.tolist() if col not in potential_grouping_columns]

#This makes the default columns that should start there, they can add more but they always have to have at least one
default_categories = ["Total Time Spent", "ProductivityLoss"]
default_categories = [col for col in default_categories if col in columns_for_multiselect]

#This makes the buttons
categories = st.multiselect(
    "Data",
    options = columns_for_multiselect,
    default = default_categories
)

#This makes sure that if there is nothing selected, then it won't crash the whole program
#It should display a yellow warning message
if not categories:
    st.warning("Please select at least one data category to display.")
    st.stop()

#This basically makes the graph actually only show the categories selected
#And then .select_dtypes(include=np.number) makes sure that it only has values that are numbers that are possible to choose
numbered_columns_for_aggregation = df[categories].select_dtypes(include=np.number).columns.tolist()

#if they choose a value that is not a number and cannot be compiled into a mean, it will show a warning
if not numbered_columns_for_aggregation:
    st.warning(f"None of the categories can be compiled into the mean. Please select a category that uses numbers")
    st.stop()

#making a copy of the original data so it doesn't get changed
df_filtered = df

#summary of the data I am choosing
df_reshaped = df_filtered.pivot_table(
    #Want rows grouped by gender
    index = "Gender", 
    #Any values that can be numbered
    values = numbered_columns_for_aggregation,
    #The mean of all the numbers
    aggfunc = "mean"
#reset = turn it into a column to sort easier
#sort = do males then females(since I ordered them earlier)
#index = turn it back into the index to make it look nice
).reset_index().sort_values("Gender").set_index("Gender")

#Just turns the index back into a column again
df_table = df_reshaped.reset_index()



st.dataframe(df_table)

#start of the two extra visualizations
st.header("Data Visualization")

#This just title's my graphs
st.subheader("Male Vs. Female Screen Time per Platform")
#This groups the gender and platforms together so that it can be split and seen. Then, the total time spent is calculated to find the sum
df_grouped = df.groupby(["Gender", "Platform"])["Total Time Spent"].sum().reset_index()

#This makes the actual bar graph show up
chart = alt.Chart(df_grouped).mark_bar().encode(
    x="Platform",
    y="Total Time Spent",
    color="Gender"
)
#The st.altair_chart(chart) part makes the graph appear
#The use_container_width = True makes it fit within the screen
st.altair_chart(chart, use_container_width = True)

#This makes it only calculate the male values, so it disregards anyone else's data
df_male_only = df_table[df_table["Gender"] == "Male"]
#This groups why they watched and what they watched and then finds the sum of how much time they spent
df_grouped2 = df.groupby(["Watch Reason", "Video Category"])["Total Time Spent"].sum().reset_index()

#This makes the actual chart
st.subheader("Male: What, Why, and How Long They Are Watching")
chart2 = alt.Chart(df_grouped2).mark_bar().encode(
    x = "Watch Reason:N",
    y = "Total Time Spent:Q",
    color = "Video Category:N"
)
st.altair_chart(chart2, use_container_width = True)

