"""Exploration page: two views into how battle statistics relate to type and speed."""

import plotly.express as px
import streamlit as st

df = st.session_state.df

st.title("📊 Explore the Data")

if st.checkbox("Show raw data"):
    st.dataframe(df)

st.subheader("How do attack and defense relate to speed, by type?")

type_options = sorted(df["type"].unique())
selected_types = st.multiselect("Filter by type", type_options, default=type_options)

filtered_df = df[df["type"].isin(selected_types)]

fig = px.scatter(
    filtered_df,
    x="attack",
    y="defense",
    color="type",
    size="speed",
    hover_data=["name", "speed"],
    labels={"attack": "Attack", "defense": "Defense", "type": "Primary type"},
)
fig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>"
    "Attack: %{x}<br>"
    "Defense: %{y}<br>"
    "Speed: %{customdata[1]}<extra></extra>"
)
st.plotly_chart(fig, width="stretch")

if filtered_df.empty:
    st.warning("No Pokemon match the selected types.")
else:
    st.caption(
        f"Showing {len(filtered_df):,} of {len(df):,} Pokemon. Marker size represents "
        "speed — larger, higher-right markers combine high attack, defense, and speed."
    )
