"""Educational K-Means demonstration on the 50-row US Area Codes preview."""
from pathlib import Path
from datetime import datetime
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

root = Path(__file__).resolve().parent
df = pd.read_csv(root / "us_area_codes_preview_50.csv", dtype={"Area Code (NPA)": str})
df["Service Year"] = pd.to_datetime(df["Service Date"], format="%d-%b-%Y").dt.year
def complex_size(value):
    if pd.isna(value) or not str(value).strip():
        return 1  # no overlay complex listed; not proof of no overlay
    return len([part for part in str(value).split("/") if part.strip()])
df["Overlay Complex Size"] = df["Overlay Complex"].apply(complex_size)
features = df[["Service Year", "Overlay Complex Size"]]
scaled = StandardScaler().fit_transform(features)
model = KMeans(n_clusters=3, random_state=42, n_init=20)
df["Cluster"] = model.fit_predict(scaled)
print("Records:", len(df))
print("Cluster sizes:", df["Cluster"].value_counts().sort_index().to_dict())
print("Silhouette score:", round(silhouette_score(scaled, df["Cluster"]), 3))
df[["Area Code (NPA)", "State / Location", "Service Year", "Overlay Flag", "Overlay Complex", "Overlay Complex Size", "Cluster"]].to_csv(root / "us_area_codes_ml_results.csv", index=False)
