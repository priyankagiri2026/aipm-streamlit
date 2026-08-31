import pandas as pd
import streamlit as st

from predict import FEATURE_ORDER

# set_page_config has to be the first Streamlit call in the script.
st.set_page_config(page_title="Pokemon", page_icon="🔴")

# Streamlit reruns this script on every interaction, so anything expensive or
# shared between pages goes into session_state instead of a module-level variable.
# The "not in" guard means the CSV is read once per session, not once per rerun.
if "df" not in st.session_state:
    st.session_state.df = pd.read_csv("data/pokemon.csv")

# Reusing FEATURE_ORDER keeps the column order identical to the one the model
# was trained on, so the app and predict.py cannot drift apart.
st.session_state.stats_cols = FEATURE_ORDER

# st.navigation builds the sidebar. Paths are relative to this file, so each
# page script lives next to app.py in pages/.
pg = st.navigation(
    [
        st.Page("pages/home.py", title="Welcome", icon="👋", default=True),
        st.Page("pages/eda.py", title="EDA", icon="📊"),
        st.Page("pages/prediction.py", title="Prediction", icon="🔮"),
        st.Page("pages/map.py", title="Map viz", icon="🌍"),
        st.Page("pages/pokedex.py", title="Pokédex", icon="💬"),
    ]
)

# Nothing renders until the selected page script is executed.
pg.run()
