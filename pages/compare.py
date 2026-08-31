"""Compare page: overlays two Pokemon on one radar chart and saves favourites."""

import plotly.graph_objects as go
import streamlit as st

df = st.session_state.df
stats_cols = st.session_state.stats_cols

st.title("⚔️ Compare Two Pokemon")
st.write("Pick two Pokemon to compare their battle statistics on the same scale.")

# A fixed radial maximum (dataset-wide, not per-Pokemon) keeps every radar
# comparable, mirroring the approach used in the training notebook.
radar_max = df[stats_cols].max().max()
names = df["name"].tolist()

if "favourite_comparisons" not in st.session_state:
    st.session_state.favourite_comparisons = []

col1, col2 = st.columns(2)
with col1:
    name_a = st.selectbox("Pokemon A", names, index=names.index("Pikachu"))
with col2:
    name_b = st.selectbox("Pokemon B", names, index=names.index("Charizard"))


def render_radar(name_a: str, name_b: str) -> None:
    row_a = df.loc[df["name"] == name_a].iloc[0]
    row_b = df.loc[df["name"] == name_b].iloc[0]

    fig = go.Figure()
    for row, color in [(row_a, "#FFA3E4"), (row_b, "#5DA9E9")]:
        fig.add_trace(
            go.Scatterpolar(
                r=row[stats_cols].tolist(),
                theta=stats_cols,
                fill="toself",
                name=row["name"],
                line_color=color,
                hovertemplate="<b>%{theta}</b>: %{r}<extra>" + row["name"] + "</extra>",
            )
        )
    fig.update_layout(polar={"radialaxis": {"range": [0, radar_max]}}, showlegend=True)
    st.plotly_chart(fig, width="stretch")


if name_a == name_b:
    st.warning("Pick two different Pokemon to compare.")
else:
    render_radar(name_a, name_b)

    if st.button("Save this comparison"):
        pair = (name_a, name_b)
        if pair in st.session_state.favourite_comparisons:
            st.toast("Already saved.")
        else:
            st.session_state.favourite_comparisons.append(pair)
            st.toast(f"Saved {name_a} vs {name_b}.")

st.subheader("Saved comparisons")
if not st.session_state.favourite_comparisons:
    st.caption("No comparisons saved yet. Save one above to see it here.")
else:
    for saved_a, saved_b in st.session_state.favourite_comparisons:
        st.write(f"- {saved_a} vs {saved_b}")

    if st.button("Clear all saved comparisons"):
        st.session_state.favourite_comparisons = []
        st.rerun()
