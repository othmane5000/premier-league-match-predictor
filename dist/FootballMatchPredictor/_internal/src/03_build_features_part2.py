"""
Étape 3 (suite) : recombiner les features de forme dans le format
"1 ligne = 1 match" avec les stats HOME et AWAY côte à côte.
C'est ce dataset final qui servira à entraîner le modèle.
"""
import pandas as pd

data = pd.read_csv("../data/matches_clean.csv", parse_dates=["Date"])
team_matches = pd.read_csv("../data/team_match_history.csv", parse_dates=["Date"])

feature_cols = [c for c in team_matches.columns if c.startswith("Avg")] + ["MatchesPlayed"]

# On a besoin d'une clé unique par (Date, Team) pour merger correctement
# car une équipe ne joue qu'une fois par date
home_features = team_matches[["Date", "Team"] + feature_cols].copy()
home_features.columns = ["Date", "HomeTeam"] + [f"Home_{c}" for c in feature_cols]

away_features = team_matches[["Date", "Team"] + feature_cols].copy()
away_features.columns = ["Date", "AwayTeam"] + [f"Away_{c}" for c in feature_cols]

# Fusionner avec le dataset de matchs original
final = data.merge(home_features, on=["Date", "HomeTeam"], how="left")
final = final.merge(away_features, on=["Date", "AwayTeam"], how="left")

# Feature supplémentaire utile : différence de forme entre les 2 équipes
final["Diff_AvgPoints_L5"] = final["Home_AvgPoints_L5"] - final["Away_AvgPoints_L5"]
final["Diff_AvgGoalsFor_L5"] = final["Home_AvgGoalsFor_L5"] - final["Away_AvgGoalsFor_L5"]

# On enlève les tout premiers matchs de chaque saison où il n'y a pas encore
# assez d'historique pour calculer une forme fiable (NaN)
before = len(final)
final_clean = final.dropna(subset=[f"Home_{c}" for c in feature_cols] + [f"Away_{c}" for c in feature_cols])
after = len(final_clean)

print(f"Matchs avant nettoyage : {before}")
print(f"Matchs après nettoyage (avec historique suffisant) : {after}")
print(f"Matchs supprimés (début de saison, pas d'historique) : {before - after}")

final_clean.to_csv("../data/matches_with_features.csv", index=False)
print("\n✅ Sauvegardé dans data/matches_with_features.csv")

print("\nColonnes disponibles pour le modèle :")
print([c for c in final_clean.columns if "Avg" in c or "Diff" in c])

print("\nAperçu d'un match avec ses features :")
sample = final_clean[["Date", "HomeTeam", "AwayTeam", "FTR",
                        "Home_AvgPoints_L5", "Away_AvgPoints_L5",
                        "Home_AvgGoalsFor_L5", "Away_AvgGoalsFor_L5"]].tail(5)
print(sample.to_string(index=False))
