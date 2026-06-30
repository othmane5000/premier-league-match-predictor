"""
Étape 5 : Essayer un Random Forest et comparer à la régression logistique
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

data = pd.read_csv("data/matches_with_features.csv", parse_dates=["Date"])
feature_cols = [c for c in data.columns if "Avg" in c or "Diff" in c]

data_sorted = data.sort_values("Date")
split_idx = int(len(data_sorted) * 0.8)
train_data = data_sorted.iloc[:split_idx]
test_data = data_sorted.iloc[split_idx:]

X_train, y_train = train_data[feature_cols], train_data["FTR"]
X_test, y_test = test_data[feature_cols], test_data["FTR"]

# --- Modèle 1 : régression logistique (rappel de l'étape 4) ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train_scaled, y_train)
logreg_pred = logreg.predict(X_test_scaled)
logreg_acc = accuracy_score(y_test, logreg_pred)

# --- Modèle 2 : Random Forest ---
# Random Forest n'a pas besoin de mise à l'échelle (StandardScaler),
# il travaille directement sur les valeurs brutes.
rf = RandomForestClassifier(
    n_estimators=200,      # nombre d'arbres dans la forêt
    max_depth=5,           # profondeur max de chaque arbre (évite le surapprentissage)
    min_samples_leaf=20,   # évite les arbres trop spécifiques à quelques cas
    random_state=42,       # pour reproductibilité
    class_weight="balanced"  # compense le déséquilibre des classes (peu de nuls)
)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

print("="*55)
print(f"Régression logistique : {logreg_acc:.1%}")
print(f"Random Forest         : {rf_acc:.1%}")
print("="*55)

print("\n--- Détail Random Forest ---")
print(classification_report(y_test, rf_pred, target_names=["Away win", "Draw", "Home win"], labels=["A", "D", "H"]))

print("Matrice de confusion Random Forest :")
print("            Pred_A  Pred_D  Pred_H")
cm = confusion_matrix(y_test, rf_pred, labels=["A", "D", "H"])
for i, label in enumerate(["Real_A", "Real_D", "Real_H"]):
    print(f"{label}      {cm[i]}")

# Quelles features sont les plus importantes selon le Random Forest ?
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\nTop 10 features les plus importantes (selon Random Forest) :")
print(importances.head(10))

# Sauvegarder le meilleur modèle
joblib.dump(rf, "outputs/model_rf.pkl")

print("\n✅ Random Forest sauvegardé dans outputs/model_rf.pkl")
