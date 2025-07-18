import streamlit as st
pages = {
    "My Pages":
    [
        st.Page("pages/main.py", title = "The Effects of Social Media on Male Youth"),
        st.Page("pages/male-vs-female.py", title = "Male Vs. Female Page")
    ]
}

pg = st.navigation(pages)
pg.run()