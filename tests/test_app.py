import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

import predict

DF = pd.read_csv("data/pokemon.csv")
STATS_COLS = predict.FEATURE_ORDER


def make_page(path: str) -> AppTest:
    """Build an AppTest for one page with the session_state app.py normally sets up."""
    at = AppTest.from_file(path)
    at.session_state["df"] = DF
    at.session_state["stats_cols"] = STATS_COLS
    return at


def test_app_starts_without_an_exception():
    app = AppTest.from_file("app.py").run()
    assert not app.exception


@pytest.mark.parametrize(
    "page",
    ["pages/home.py", "pages/eda.py", "pages/prediction.py", "pages/compare.py"],
)
def test_page_starts_without_an_exception(page):
    at = make_page(page).run()
    assert not at.exception


def test_prediction_submit_adds_to_history_and_shows_a_verdict():
    at = make_page("pages/prediction.py").run()
    at.button[0].click().run()

    assert not at.exception
    assert len(at.session_state["prediction_history"]) == 1
    assert at.success or at.warning


def test_prediction_threshold_reclassifies_history():
    at = make_page("pages/prediction.py").run()
    at.button[0].click().run()
    probability = at.session_state["prediction_history"][-1]["probability"]

    # A threshold above the observed probability must classify it as not legendary.
    at.slider[0].set_value(min(probability + 0.1, 1.0)).run()
    assert not at.exception
    assert at.warning


def test_compare_page_warns_on_identical_selection():
    at = make_page("pages/compare.py").run()
    at.selectbox[1].set_value(at.selectbox[0].value).run()

    assert not at.exception
    assert at.warning


def test_missing_model_file_falls_back_to_training_on_the_fly(monkeypatch, tmp_path):
    predict.load_model.clear()
    monkeypatch.setattr(predict, "MODEL_PATH", tmp_path / "missing.pkl")

    at = make_page("pages/prediction.py").run()
    at.button[0].click().run()

    assert not at.exception
    assert not at.error
    assert len(at.session_state["prediction_history"]) == 1

    predict.load_model.clear()


def test_missing_data_file_still_shows_a_friendly_error_not_a_traceback(
    monkeypatch, tmp_path
):
    predict.load_model.clear()
    monkeypatch.setattr(predict, "MODEL_PATH", tmp_path / "missing.pkl")
    monkeypatch.setattr(predict, "DATA_PATH", tmp_path / "missing.csv")

    at = make_page("pages/prediction.py").run()
    at.button[0].click().run()

    assert not at.exception
    assert at.error
    assert at.session_state["prediction_history"] == []

    predict.load_model.clear()
