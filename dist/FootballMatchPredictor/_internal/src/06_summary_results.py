"""
Étape 6 : Résumé final des résultats — génère un graphique de comparaison
des modèles, utile pour la présentation du projet (README, portfolio).
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

data = pd.read_csv("../data/matches_with_features.csv", parse_dates=["Date"])
feature_cols = [c for c in data.columns if "Avg" in c or "Diff" in c]

data_sorted = data.sort_values("Date")
split_idx = int(len(data_sorted) * 0.8)
train_data = data_sorted.iloc[:split_idx]
test_data = data_sorted.iloc[split_idx:]

X_train, y_train = train_data[feature_cols], train_data["FTR"]
X_test, y_test = test_data[feature_cols], test_data["FTR"]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train_scaled, y_train)
logreg_acc = accuracy_score(y_test, logreg.predict(X_test_scaled))

rf = RandomForestClassifier(n_estimators=200, max_depth=5, min_samples_leaf=20,
                              random_state=42, class_weight="balanced")
rf.fit(X_train, y_train)
rf_acc = accuracy_score(y_test, rf.predict(X_test))

baseline_acc = accuracy_score(y_test, ["H"] * len(y_test))

# Graphique de comparaison
results = {
    "Baseline\n(toujours domicile)": baseline_acc,
    "Régression\nlogistique": logreg_acc,
    "Random\nForest": rf_acc,
}

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(results.keys(), [v * 100 for v in results.values()],
               color=["#888780", "#378ADD", "#1D9E75"])
ax.set_ylabel("Précision (%)")
ax.set_title("Comparaison des modèles — prédiction résultats Premier League")
ax.set_ylim(0, 60)
for bar, val in zip(bars, results.values()):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f"{val:.1%}", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("../results/model_comparison.png", dpi=150)
print("✅ Graphique sauvegardé dans results/model_comparison.png")

# Sauvegarder un résumé texte aussi
with open("../results/summary.txt", "w") as f:
    f.write("RÉSUMÉ DES RÉSULTATS\n")
    f.write("="*40 + "\n")
    f.write(f"Dataset : {len(data)} matchs (saisons 2022/23 à 2025/26)\n")
    f.write(f"Train/Test split : {len(train_data)} / {len(test_data)} (chronologique)\n\n")
    for name, acc in results.items():
        f.write(f"{name.replace(chr(10), ' ')}: {acc:.1%}\n")

print("✅ Résumé texte sauvegardé dans results/summary.txt")
