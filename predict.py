import pickle
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

FEATURE_ORDER = ["hit_points", "attack", "defense", "sp_attack", "sp_defense", "speed"]
MODEL_PATH = Path("models/random_forest.pkl")


@st.cache_resource
def load_model() -> Any:
    """Load the trusted model generated locally by the training notebook."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. Run 02-eda-and-modeling.ipynb before using predictions."
        )

    with MODEL_PATH.open("rb") as model_file:
        return pickle.load(model_file)


def predict(features: Mapping[str, float | int]) -> tuple[int, float]:
    """Predict the legendary class and probability from six battle statistics."""
    model = load_model()
    feature_frame = pd.DataFrame([features], columns=FEATURE_ORDER)
    predicted_class = model.predict(feature_frame)[0]
    legendary_probability = model.predict_proba(feature_frame)[0][1]

    return int(predicted_class), float(legendary_probability)
