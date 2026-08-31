# Solutions

Reference implementation of the guided multipage Pokemon app. Build and test a workshop checkpoint before opening the corresponding file here, then compare the behavior and design choices with your own approach.

Run it from the repository root, so the `data/` and `assets/` paths resolve:

```bash
uv run streamlit run solutions/app.py
```

> [!IMPORTANT]
> Run `02-eda-and-modeling.ipynb` first. The prediction page needs `models/random_forest.pkl`, which the notebook creates.

| File / Folder                                 | Description                                                                                            |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [**app.py**](app.py)                          | Entry point: page configuration, the dataset loaded once into `st.session_state`, and `st.navigation`.  |
| [**Welcome**](pages/home.py)                  | Product introduction, local image, and three metrics calculated from the shared dataframe.              |
| [**EDA**](pages/eda.py)                       | Optional raw data, interactive charts, selectors, and short interpretation prompts.                     |
| [**Prediction**](pages/prediction.py)         | Validated numeric inputs and a model result with probability and an explicit limitation.                |
| [**Map viz**](pages/map.py)                   | Two tabs comparing built-in `st.map` against a configurable Plotly `scatter_geo`.                       |
| [**Pokédex**](pages/pokedex.py)               | Chat interface where the history is replayed from `st.session_state` on every rerun.                    |
| [**predict.py**](predict.py)                  | Copy of the provided helper, so imports resolve when `solutions/app.py` is the entry point.             |

For the build sequence, see [Build the Streamlit App](../03-build-the-streamlit-app.md). For the concepts behind the code, see [Streamlit Essentials](../01-streamlit-essentials.md).
