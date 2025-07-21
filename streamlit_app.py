import streamlit as st
pages = {
    "My Pages":
    [
        st.Page("pages/main.py", title = "The Effects of Social Media on Male Youth"),
        st.Page("pages/male-vs-female.py", title = "Male Vs. Female Page"),
        st.Page("pages/mass-shootings.py", title = "Mass Shootings Data"),
        st.Page("pages/facebook.py", title = "Facebook Addiction"),
        st.Page("pages/Social-Media-Addiction.py", title = "Social Media Addiction")
    ]
}

pg = st.navigation(pages)
pg.run()