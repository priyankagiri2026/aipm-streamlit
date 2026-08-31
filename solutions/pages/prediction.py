import streamlit as st

from predict import predict

st.title("⚡️ Is my Pokémon legendary??")
st.write("")

st.subheader("Enter Pokémon Stats")

# A form batches all six widget values into one rerun when submitted.
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        attack = st.number_input("Attack", min_value=1, max_value=255, value=80, step=5)
        sp_attack = st.number_input(
            "Special Attack", min_value=1, max_value=255, value=75, step=5
        )

    with col2:
        defense = st.slider("Defense", min_value=1, max_value=255, value=80)
        sp_defense = st.slider("Special Defense", min_value=20, max_value=255, value=75)

    with col3:
        hit_points = st.number_input("Hit points", min_value=1, max_value=255, value=70)
        speed = st.number_input("Speed", min_value=5, max_value=255, value=10)

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

    # predict() returns the class and the probability of the positive class.
    y_pred, y_prob = predict(features)

    if y_pred == 1:
        st.success(f"✅ This Pokémon is **Legendary**! (prob = {y_prob:.2%})")
        st.balloons()
    else:
        st.error(f"❌ This Pokémon is **Not Legendary** (prob = {y_prob:.2%})")
        st.snow()

st.caption(
    "This probability comes from a small teaching model. It describes the "
    "model's output, not certainty about a real Pokemon."
)
