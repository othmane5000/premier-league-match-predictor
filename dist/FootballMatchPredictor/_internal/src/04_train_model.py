"""
Étape 4 : Entraîner notre premier modèle de Machine Learning

On utilise une régression logistique : un algorithme simple et solide
pour classer un match en 3 catégories (H = victoire domicile,
D = nul, A = victoire extérieur).
"""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

data = pd.read_csv("data/matches_with_features.csv", parse_dates=["Date"])

# Les features = tout ce qui contient "Avg" ou "Diff" dans son nom
feature_cols = [c for c in data.columns if "Avg" in c or "Diff" in c]
print(f"Nombre de features utilisées : {len(feature_cols)}")
print(feature_cols)

X = data[feature_cols]
y = data["FTR"]  # H, D, ou A

# IMPORTANT : on découpe par DATE, pas au hasard.
# On entraîne sur le passé, on teste sur les matchs les plus récents.
# C'est plus réaliste qu'un mélange aléatoire (qui mélangerait
# le futur et le passé, ce qui n'arrive jamais en vrai).
data_sorted = data.sort_values("Date")
split_idx = int(len(data_sorted) * 0.8)

train_data = data_sorted.iloc[:split_idx]
test_data = data_sorted.iloc[split_idx:]

X_train, y_train = train_data[feature_cols], train_data["FTR"]
X_test, y_test = test_data[feature_cols], test_data["FTR"]

print(f"\nMatchs d'entraînement : {len(X_train)} (du {train_data['Date'].min().date()} au {train_data['Date'].max().date()})")
print(f"Matchs de test        : {len(X_test)} (du {test_data['Date'].min().date()} au {test_data['Date'].max().date()})")

# Mise à l'échelle des features : la régression logistique fonctionne
# mieux quand toutes les colonnes sont sur une échelle comparable
# (ex: les points 0-3 et les tirs 0-25 n'ont pas la même échelle)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entraînement du modèle
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Évaluation
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*50}")
print(f"PRÉCISION DU MODÈLE : {accuracy:.1%}")
print(f"{'='*50}")

# Comparaison avec une baseline naïve : toujours prédire "victoire domicile"
baseline_pred = ["H"] * len(y_test)
baseline_accuracy = accuracy_score(y_test, baseline_pred)
print(f"Baseline (toujours 'victoire domicile') : {baseline_accuracy:.1%}")

print("\nRapport détaillé par classe :")
print(classification_report(y_test, y_pred, target_names=["Away win", "Draw", "Home win"], labels=["A", "D", "H"]))

print("Matrice de confusion (lignes = réalité, colonnes = prédiction) :")
print("            Pred_A  Pred_D  Pred_H")
cm = confusion_matrix(y_test, y_pred, labels=["A", "D", "H"])
for i, label in enumerate(["Real_A", "Real_D", "Real_H"]):
    print(f"{label}      {cm[i]}")

# Sauvegarder le modèle et le scaler pour les réutiliser plus tard
import joblib
joblib.dump(model, "outputs/model_logreg.pkl")
joblib.dump(scaler, "outputs/scaler.pkl")
print("\n✅ Modèle sauvegardé dans outputs/model_logreg.pkl")
