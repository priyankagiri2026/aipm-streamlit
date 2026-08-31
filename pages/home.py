"""Home page: introduces the app and orients a first-time visitor."""

import streamlit as st

from formatting import format_percent

df = st.session_state.df

st.title("🔴 Pokemon Data App")
st.image("assets/pokemon.png")
st.caption(
    "Pokemon character artwork © Nintendo/Creatures Inc./GAME FREAK inc. "
    "[Official legal information](https://www.pokemon.com/us/legal/)."
)

st.write(
    "Explore Pokemon battle statistics and estimate whether a new Pokemon "
    "could be legendary, using a small teaching model trained on this dataset."
)
st.info("Use the sidebar to open **Exploration** or **Prediction**.", icon="👈")

st.subheader("At a glance")
pokemon_count, type_count, legendary_share = st.columns(3)
pokemon_count.metric("Pokemon", f"{len(df):,}")
type_count.metric("Primary types", df["type"].nunique())
legendary_share.metric("Legendary share", format_percent(df["is_legendary"].mean()))

st.caption("All values are computed from the currently loaded data/pokemon.csv.")
