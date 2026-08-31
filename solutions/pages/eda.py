import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Read what app.py put in session_state. This page is never run on its own,
# so the keys are guaranteed to exist.
df = st.session_state.df
stats_cols = st.session_state.stats_cols

st.title("📊 EDA Visualisation")
st.write("")

# Hiding the raw table behind a checkbox keeps the page short by default.
if st.checkbox("Show raw data"):
    st.dataframe(df)


# Scatter plot

st.subheader("Height vs Weight Scatter Plot")

# plotly.express covers the common cases in a single call: colour by category,
# size by a numeric column, and extra columns available to the tooltip.
fig = px.scatter(
    df,
    x="height_m",
    y="weight_kg",
    color="type",
    size="speed",
    hover_data=["name", "type", "speed"],
)

# hover_data lands in customdata in the order it was passed, which is what the
# indices below refer to. <extra></extra> removes Plotly's default trace box.
fig.update_traces(
    hovertemplate="<b>Name:</b> %{customdata[0]}<br>"
    + "<b>Height (m):</b> %{x}<br>"
    + "<b>Weight (kg):</b> %{y}<br>"
    + "<b>Type:</b> %{customdata[1]}<br>"
    + "<b>Speed:</b> %{customdata[2]}<br>"
    + "<extra></extra>"
)

st.plotly_chart(fig)
st.caption(
    "Marker size represents speed. Use the legend and hover details to compare "
    "physical characteristics across types."
)


# Radar chart

st.subheader("Pokémon Stats Radar Chart")

pokemon_name = st.selectbox("Select Pokemon", df["name"].tolist())

row = df[df["name"] == pokemon_name].iloc[0]

# Scaling every radar to the dataset maximum keeps the charts comparable
# between Pokémon instead of rescaling to each one.
max_stat = df[stats_cols].values.max()
color = st.color_picker("Pick a color", "#FFA3E4")

# A radar chart has no express shortcut, so it is built with graph_objects.
fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=row[stats_cols].values,
        theta=stats_cols,
        fill="toself",
        name=pokemon_name,
        line_color=color,
    )
)

fig.update_layout(polar={"radialaxis": {"range": [0, max_stat]}})

st.plotly_chart(fig)
st.caption(
    "Every Pokemon uses the same radial scale, so the shape can be compared "
    "honestly after changing the selection."
)
