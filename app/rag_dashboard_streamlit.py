import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def load_data(path="eval_results.json"):
    with open(path) as f:
        return pd.DataFrame(json.load(f))

st.set_page_config(page_title="RAG Evaluation Dashboard")
st.title("📊 RAG Evaluation Dashboard")

df = load_data()

# Detect hallucinations: high-confidence answer but low similarity
hallucination_mask = (df["similarity"] < 0.3) & (df["answer"].str.len() > 30)
df["hallucination_risk"] = hallucination_mask

score_filter = st.slider("Minimum similarity score", 0.0, 1.0, 0.5, 0.01)
filtered = df[df["similarity"] >= score_filter]

st.write(f"Showing {len(filtered)} / {len(df)} results (after filtering)")

st.dataframe(filtered[["question", "answer", "similarity", "hallucination_risk"]])

# Histogram of similarity
st.subheader("📊 Similarity Score Distribution")
fig, ax = plt.subplots()
ax.hist(df["similarity"], bins=20, color="skyblue", edgecolor="black")
ax.set_xlabel("Similarity Score")
ax.set_ylabel("Number of QA pairs")
st.pyplot(fig)

# Hallucination count
hallucination_count = df["hallucination_risk"].sum()
st.subheader(f"⚠️ Possible Hallucinations: {hallucination_count}")
st.write(df[df["hallucination_risk"]][["question", "answer", "similarity"]])

# Export
st.download_button(
    label="Download filtered results as CSV",
    data=filtered.to_csv(index=False),
    file_name="filtered_eval_results.csv",
    mime="text/csv"
)
