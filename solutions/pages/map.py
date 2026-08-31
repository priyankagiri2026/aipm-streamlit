import plotly.express as px
import streamlit as st

df = st.session_state.df

st.title("🌍 Pokémon Map Visualisation")
st.subheader("Where can we find these Pokémon?")
st.write("")

# Tabs put the two approaches side by side: the built-in map and the Plotly one.
tab1, tab2 = st.tabs(["Simple - Streamlit", "Advanced - Plotly"])

with tab1:
    # st.map needs nothing but latitude and longitude columns, which the
    # dataset already provides. No configuration, no legend, no styling.
    st.map(df)

with tab2:
    # scatter_geo costs more code but adds colour, size and tooltips.
    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        color="type",
        size="hit_points",
        hover_data=["name", "type", "hit_points"],
        projection="natural earth",  # Other options include mercator and orthographic.
        title="Distribution of Pokémon by generation and type",
    )

    fig.update_traces(
        hovertemplate="<b>Name:</b> %{customdata[0]}<br>"
        + "<b>Type:</b> %{customdata[1]}<br>"
        + "<b>Hit Points:</b> %{customdata[2]}<br>"
        + "<extra></extra>"
    )

    st.plotly_chart(fig)
