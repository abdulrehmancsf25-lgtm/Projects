"""
Pandas & NumPy Playground
--------------------------
An interactive Streamlit app for learning data analysis with pandas and numpy.

HOW TO RUN:
    pip install streamlit pandas numpy seaborn matplotlib
    streamlit run app.py

WHAT IT DOES:
    - Lets you load a sample dataset OR upload your own CSV
    - Every operation shows the CODE next to the OUTPUT (so you learn as you click)
    - Sidebar lets you explore: overview, cleaning, filtering, groupby, numpy ops, and simple charts
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pandas & NumPy Playground",
    page_icon="🐼",
    layout="wide",
)

# ----------------------------------------------------------------------------
# HELPER: show code + let the reader actually see what ran
# ----------------------------------------------------------------------------
def code_and_output(code_str, output_fn):
    """Show a code snippet, then run output_fn() and display its return value."""
    st.code(code_str, language="python")
    result = output_fn()
    if result is not None:
        st.write(result)


# ----------------------------------------------------------------------------
# SIDEBAR — data source + navigation
# ----------------------------------------------------------------------------
st.sidebar.title("🐼 Pandas & NumPy Playground")
st.sidebar.markdown("Learn by *seeing the code* run on real data.")

st.sidebar.header("1️⃣ Choose a dataset")
data_source = st.sidebar.radio(
    "Data source",
    ["Sample: Titanic", "Sample: Tips", "Sample: Iris", "Upload your own CSV"],
)

if data_source == "Upload your own CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.sidebar.info("Upload a file to continue, or pick a sample dataset.")
        st.stop()
elif data_source == "Sample: Titanic":
    df = sns.load_dataset("titanic")
elif data_source == "Sample: Tips":
    df = sns.load_dataset("tips")
else:
    df = sns.load_dataset("iris")

# Keep an original copy so "reset" always works
if "original_df" not in st.session_state or st.session_state.get("last_source") != data_source:
    st.session_state["original_df"] = df.copy()
    st.session_state["last_source"] = data_source

st.sidebar.header("2️⃣ Choose a section")
section = st.sidebar.radio(
    "Explore",
    [
        "📋 Overview",
        "🧹 Data Cleaning",
        "🔍 Filtering & Selection",
        "📊 GroupBy & Aggregation",
        "🔢 NumPy Playground",
        "📈 Quick Visualization",
    ],
)

st.sidebar.header("3️⃣ Utilities")
if st.sidebar.button("🔄 Reset dataset"):
    df = st.session_state["original_df"].copy()
    st.sidebar.success("Dataset reset to original.")

show_dtypes = st.sidebar.checkbox("Show dtypes in every table", value=False)
st.sidebar.download_button(
    "⬇️ Download current CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="data.csv",
    mime="text/csv",
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Tip: pandas 2.x → 3.x changed some default behaviors "
    "(e.g. Copy-on-Write is now always on). If a tutorial's code "
    "behaves differently here, that's usually why."
)

# ----------------------------------------------------------------------------
# MAIN AREA
# ----------------------------------------------------------------------------
st.title("Pandas & NumPy Playground")
st.caption(f"Current dataset: **{data_source}** — shape: {df.shape[0]} rows × {df.shape[1]} columns")

# =============================================================================
# SECTION: OVERVIEW
# =============================================================================
if section == "📋 Overview":
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Head")
        code_and_output("df.head()", lambda: df.head())

        st.subheader("Shape")
        code_and_output("df.shape", lambda: df.shape)

    with col2:
        st.subheader("Info (columns & non-null counts)")
        info_df = pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str).values,
            "non_null": df.notna().sum().values,
            "nulls": df.isna().sum().values,
        })
        st.code("df.info()  # summarized below as a table", language="python")
        st.dataframe(info_df, use_container_width=True)

        st.subheader("Describe (numeric summary)")
        code_and_output("df.describe()", lambda: df.describe())

    if show_dtypes:
        st.subheader("dtypes")
        st.write(df.dtypes)

# =============================================================================
# SECTION: DATA CLEANING
# =============================================================================
elif section == "🧹 Data Cleaning":
    st.subheader("Missing values")
    code_and_output("df.isna().sum()", lambda: df.isna().sum())

    st.markdown("---")
    st.subheader("Handle missing values")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    strategy = st.selectbox(
        "Strategy for missing values",
        ["-- choose --", "Drop rows with any NaN", "Fill numeric NaNs with mean",
         "Fill numeric NaNs with median", "Fill all NaNs with 0"],
    )

    if strategy == "Drop rows with any NaN":
        code_and_output("df.dropna()", lambda: df.dropna().head())
    elif strategy == "Fill numeric NaNs with mean":
        code_and_output(
            "df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())",
            lambda: df.fillna(df[numeric_cols].mean(numeric_only=True)).head(),
        )
    elif strategy == "Fill numeric NaNs with median":
        code_and_output(
            "df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())",
            lambda: df.fillna(df[numeric_cols].median(numeric_only=True)).head(),
        )
    elif strategy == "Fill all NaNs with 0":
        code_and_output("df.fillna(0)", lambda: df.fillna(0).head())

    st.markdown("---")
    st.subheader("Duplicates")
    code_and_output("df.duplicated().sum()", lambda: int(df.duplicated().sum()))

    st.markdown("---")
    st.subheader("Type conversion — pd.to_numeric")
    col_to_convert = st.selectbox("Pick a column to try pd.to_numeric on", df.columns)
    code_and_output(
        f"pd.to_numeric(df['{col_to_convert}'], errors='coerce')",
        lambda: pd.to_numeric(df[col_to_convert], errors="coerce").head(10),
    )

# =============================================================================
# SECTION: FILTERING & SELECTION
# =============================================================================
elif section == "🔍 Filtering & Selection":
    st.subheader("Column selection")
    cols = st.multiselect("Pick columns", df.columns.tolist(), default=df.columns.tolist()[:3])
    if cols:
        code_and_output(f"df[{cols}]", lambda: df[cols].head())

    st.markdown("---")
    st.subheader("Boolean masking (row filter)")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        filt_col = st.selectbox("Numeric column to filter on", numeric_cols)
        min_v, max_v = float(df[filt_col].min()), float(df[filt_col].max())
        threshold = st.slider(f"Show rows where {filt_col} >", min_v, max_v, min_v)
        code_and_output(
            f"df[df['{filt_col}'] > {threshold:.2f}]",
            lambda: df[df[filt_col] > threshold].head(10),
        )

    st.markdown("---")
    st.subheader("Sort values")
    sort_col = st.selectbox("Sort by column", df.columns.tolist())
    ascending = st.checkbox("Ascending", value=True)
    code_and_output(
        f"df.sort_values('{sort_col}', ascending={ascending})",
        lambda: df.sort_values(sort_col, ascending=ascending).head(10),
    )

# =============================================================================
# SECTION: GROUPBY & AGGREGATION
# =============================================================================
elif section == "📊 GroupBy & Aggregation":
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if not cat_cols or not numeric_cols:
        st.warning("This dataset needs at least one categorical and one numeric column for groupby demos.")
    else:
        group_col = st.selectbox("Group by (categorical column)", cat_cols)
        agg_col = st.selectbox("Aggregate (numeric column)", numeric_cols)
        agg_fn = st.selectbox("Aggregation function", ["mean", "sum", "count", "min", "max", "median"])

        code_and_output(
            f"df.groupby('{group_col}')['{agg_col}'].{agg_fn}()",
            lambda: getattr(df.groupby(group_col)[agg_col], agg_fn)(),
        )

        st.markdown("---")
        st.subheader("Multiple aggregations at once")
        code_and_output(
            f"df.groupby('{group_col}')['{agg_col}'].agg(['mean', 'count', 'min', 'max'])",
            lambda: df.groupby(group_col)[agg_col].agg(["mean", "count", "min", "max"]),
        )

        st.markdown("---")
        st.subheader("Value counts")
        code_and_output(
            f"df['{group_col}'].value_counts()",
            lambda: df[group_col].value_counts(),
        )

# =============================================================================
# SECTION: NUMPY PLAYGROUND
# =============================================================================
elif section == "🔢 NumPy Playground":
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns in this dataset for NumPy demos.")
    else:
        col_choice = st.selectbox("Pick a numeric column to convert to a NumPy array", numeric_cols)
        st.code(f"arr = df['{col_choice}'].dropna().to_numpy()", language="python")
        arr = df[col_choice].dropna().to_numpy()
        st.write(f"Array shape: `{arr.shape}`, dtype: `{arr.dtype}`")

        st.markdown("---")
        st.subheader("Basic stats")
        code_and_output(
            "arr.mean(), arr.std(), arr.min(), arr.max()",
            lambda: {"mean": arr.mean(), "std": arr.std(), "min": arr.min(), "max": arr.max()},
        )

        st.markdown("---")
        st.subheader("Sorting & argsort")
        code_and_output("np.sort(arr)[:10]", lambda: np.sort(arr)[:10])
        code_and_output(
            "np.argsort(arr)[:10]  # indices that WOULD sort the array",
            lambda: np.argsort(arr)[:10],
        )

        st.markdown("---")
        st.subheader("Boolean masking")
        threshold = st.slider("Threshold", float(arr.min()), float(arr.max()), float(arr.mean()))
        code_and_output(
            f"arr[arr > {threshold:.2f}]",
            lambda: arr[arr > threshold][:20],
        )

        st.markdown("---")
        st.subheader("np.random demo")
        code_and_output(
            "np.random.seed(42); np.random.randint(1, 100, size=10)",
            lambda: (np.random.seed(42), np.random.randint(1, 100, size=10))[1],
        )

# =============================================================================
# SECTION: QUICK VISUALIZATION
# =============================================================================
elif section == "📈 Quick Visualization":
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    chart_type = st.selectbox("Chart type", ["Histogram", "Scatter", "Bar (category counts)", "Boxplot"])

    fig, ax = plt.subplots(figsize=(8, 4))

    if chart_type == "Histogram" and numeric_cols:
        col = st.selectbox("Column", numeric_cols)
        st.code(f"df['{col}'].hist(bins=30)", language="python")
        df[col].hist(bins=30, ax=ax)
        ax.set_xlabel(col)
        st.pyplot(fig)

    elif chart_type == "Scatter" and len(numeric_cols) >= 2:
        x_col = st.selectbox("X axis", numeric_cols, index=0)
        y_col = st.selectbox("Y axis", numeric_cols, index=1)
        st.code(f"df.plot.scatter(x='{x_col}', y='{y_col}')", language="python")
        ax.scatter(df[x_col], df[y_col], alpha=0.6)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        st.pyplot(fig)

    elif chart_type == "Bar (category counts)" and cat_cols:
        col = st.selectbox("Column", cat_cols)
        st.code(f"df['{col}'].value_counts().plot.bar()", language="python")
        df[col].value_counts().plot.bar(ax=ax)
        st.pyplot(fig)

    elif chart_type == "Boxplot" and numeric_cols:
        col = st.selectbox("Column", numeric_cols)
        st.code(f"df.boxplot(column='{col}')", language="python")
        df.boxplot(column=col, ax=ax)
        st.pyplot(fig)

    else:
        st.info("This dataset doesn't have the right column types for that chart. Try another option.")

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "Built as a learning sandbox — change the sidebar options and watch the "
    "code + output update together. Try breaking things; that's how you learn pandas."
)