"""Prediction page: collects six battle statistics, predicts, and tracks history."""

import pandas as pd
import streamlit as st

from formatting import format_percent
from predict import predict


def classify(probability: float, threshold: float) -> str:
    """Label a probability as Legendary/Not legendary at the given threshold."""
    return "Legendary" if probability >= threshold else "Not legendary"


st.title("🔮 Is this Pokemon Legendary?")
st.write("Enter six battle statistics and submit the form to get a prediction.")

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

threshold = st.slider(
    "Decision threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
    help="A probability at or above this threshold is classified as Legendary.",
)
st.caption(
    "Lower the threshold to catch more actual legendary Pokemon (fewer false "
    "negatives, more false positives). Raise it to be more conservative "
    "(fewer false positives, more false negatives). This also re-classifies "
    "the history below."
)

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        hit_points = st.number_input("Hit points", min_value=1, max_value=255, value=65)
        attack = st.number_input("Attack", min_value=5, max_value=185, value=75)
        defense = st.number_input("Defense", min_value=5, max_value=230, value=70)

    with col2:
        sp_attack = st.number_input("Special attack", min_value=10, max_value=194, value=65)
        sp_defense = st.number_input("Special defense", min_value=20, max_value=230, value=66)
        speed = st.number_input("Speed", min_value=5, max_value=180, value=65)

    submitted = st.form_submit_button("Predict")

if submitted:
    features = {
        "hit_points": hit_points,
        "attack": attack,
        "defense": defense,
        "sp_attack": sp_attack,
        "sp_defense": sp_defense,
        "speed": speed,
    }

    with st.spinner("Running the model..."):
        try:
            _, probability = predict(features)
        except FileNotFoundError as error:
            st.error(str(error))
        else:
            st.session_state.prediction_history.append({**features, "probability": probability})

if st.session_state.prediction_history:
    latest_probability = st.session_state.prediction_history[-1]["probability"]
    label = classify(latest_probability, threshold)
    message = f"Predicted **{label}** — probability {format_percent(latest_probability)}"
    if label == "Legendary":
        st.success(message)
    else:
        st.warning(message)
    st.progress(
        latest_probability,
        text=f"Legendary probability: {format_percent(latest_probability)}",
    )
else:
    st.info("Submit the form above to see a prediction here.")

st.caption(
    "This is a small teaching model trained on a limited dataset. The probability "
    "reflects the model's confidence under its training assumptions — it is not "
    "a calibrated, real-world guarantee."
)

st.subheader("Prediction history")
if not st.session_state.prediction_history:
    st.caption("No predictions yet this session.")
else:
    history_df = pd.DataFrame(st.session_state.prediction_history)
    history_df["predicted_class"] = history_df["probability"].apply(
        lambda p: classify(p, threshold)
    )
    st.dataframe(history_df, width="stretch")

    export_col, clear_col = st.columns(2)
    export_col.download_button(
        "Download history as CSV",
        history_df.to_csv(index=False).encode("utf-8"),
        file_name="prediction_history.csv",
        mime="text/csv",
    )
    if clear_col.button("Clear history"):
        st.session_state.prediction_history = []
        st.rerun()
