import pickle
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

FEATURE_ORDER = ["hit_points", "attack", "defense", "sp_attack", "sp_defense", "speed"]
MODEL_PATH = Path("models/random_forest.pkl")
DATA_PATH = Path("data/pokemon.csv")
RANDOM_SEED = 33


def _train_model() -> Any:
    """Train the same Random Forest as 02-eda-and-modeling.ipynb.

    Used as a deployment fallback when the notebook has not been run locally
    and no committed model file exists, so a fresh clone still works.
    """
    df = pd.read_csv(DATA_PATH)
    X_train, _, y_train, _ = train_test_split(
        df[FEATURE_ORDER],
        df["is_legendary"],
        test_size=0.2,
        random_state=RANDOM_SEED,
        stratify=df["is_legendary"],
    )
    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_SEED)
    model.fit(X_train, y_train)
    return model


@st.cache_resource
def load_model() -> Any:
    """Load the notebook-trained model, or train one on the fly if it is missing."""
    if not MODEL_PATH.exists():
        return _train_model()

    with MODEL_PATH.open("rb") as model_file:
        return pickle.load(model_file)


def predict(features: Mapping[str, float | int]) -> tuple[int, float]:
    """Predict the legendary class and probability from six battle statistics."""
    model = load_model()
    feature_frame = pd.DataFrame([features], columns=FEATURE_ORDER)
    predicted_class = model.predict(feature_frame)[0]
    legendary_probability = model.predict_proba(feature_frame)[0][1]

    return int(predicted_class), float(legendary_probability)
