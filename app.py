"""Entry point for the Pokemon Data App."""

import pandas as pd
import streamlit as st

from predict import FEATURE_ORDER

# set_page_config must be the first Streamlit call in the script.
st.set_page_config(page_title="Pokemon Data App", page_icon="🔴")

# Streamlit reruns this script on every interaction, so shared, expensive data
# goes into session_state. The "not in" guard means the CSV is read once per
# session, not once per rerun.
if "df" not in st.session_state:
    st.session_state.df = pd.read_csv("data/pokemon.csv")

# Reusing FEATURE_ORDER keeps the column order identical to the one the model
# was trained on, so app.py and predict.py cannot drift apart.
st.session_state.stats_cols = FEATURE_ORDER

# st.navigation builds the sidebar; page paths are relative to this file.
pg = st.navigation(
    [
        st.Page("pages/home.py", title="Home", icon="👋", default=True),
        st.Page("pages/eda.py", title="Exploration", icon="📊"),
        st.Page("pages/prediction.py", title="Prediction", icon="🔮"),
        st.Page("pages/compare.py", title="Compare", icon="⚔️"),
    ]
)

pg.run()
