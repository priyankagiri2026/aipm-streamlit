import streamlit as st

df = st.session_state.df

# st.title accepts a subset of Markdown, including the :rainbow[...] colour directive.
st.title("🔴⚪️ Welcome to my :rainbow[Pokémon] - Streamlit Demo!")

# The same heading written as raw HTML. It needs unsafe_allow_html=True and is
# kept here only to show the alternative: prefer the Markdown version.
# st.markdown(
#     "<h1 style='font-size: 33px;'><p style='color:red;'>Welcome to my Pokémon - Streamlit Demo!</h1></p>",
#     unsafe_allow_html=True,
# )

# Paths are resolved against the folder you run streamlit from, which is the
# repository root, so the image path does not need a solutions/ prefix.
st.image("assets/pokemon.png")
st.caption(
    "Pokemon character artwork © Nintendo/Creatures Inc./GAME FREAK inc. "
    "[Official legal information](https://www.pokemon.com/us/legal/)."
)

st.subheader("Explore the data and test the model")
st.write(
    "Inspect Pokemon characteristics, compare battle statistics, and estimate "
    "whether a new Pokemon could be legendary."
)

pokemon_count, type_count, legendary_share = st.columns(3)
pokemon_count.metric("Pokemon", f"{len(df):,}")
type_count.metric("Primary types", df["type"].nunique())
legendary_share.metric("Legendary", f"{df['is_legendary'].mean():.1%}")

st.caption("All values are calculated from data/pokemon.csv.")
