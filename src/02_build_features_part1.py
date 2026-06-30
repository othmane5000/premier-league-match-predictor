"""
Étape 3 : Créer les features (la partie la plus importante du ML)

Principe : pour chaque match, on calcule les stats des 2 équipes
basées UNIQUEMENT sur leurs matchs précédents (jamais sur le match
qu'on essaie de prédire, sinon on "tricherait").
"""
import pandas as pd

data = pd.read_csv("../data/matches_clean.csv", parse_dates=["Date"])
data = data.sort_values("Date").reset_index(drop=True)

N_MATCHES = 5  # nombre de matchs récents à regarder pour la "forme"

def build_team_match_history(data):
    """
    Transforme le dataframe (1 ligne = 1 match avec home/away)
    en un format où 1 ligne = 1 équipe + 1 match.
    Ça facilite énormément le calcul de la forme récente.
    """
    home = data[["Date", "HomeTeam", "FTHG", "FTAG", "FTR", "HS", "AS", "HST", "AST", "HC", "AC"]].copy()
    home.columns = ["Date", "Team", "GoalsFor", "GoalsAgainst", "FTR", "ShotsFor", "ShotsAgainst", "ShotsOnTargetFor", "ShotsOnTargetAgainst", "CornersFor", "CornersAgainst"]
    home["Points"] = home["FTR"].map({"H": 3, "D": 1, "A": 0})
    home["IsHome"] = 1

    away = data[["Date", "AwayTeam", "FTAG", "FTHG", "FTR", "AS", "HS", "AST", "HST", "AC", "HC"]].copy()
    away.columns = ["Date", "Team", "GoalsFor", "GoalsAgainst", "FTR", "ShotsFor", "ShotsAgainst", "ShotsOnTargetFor", "ShotsOnTargetAgainst", "CornersFor", "CornersAgainst"]
    away["Points"] = away["FTR"].map({"A": 3, "D": 1, "H": 0})
    away["IsHome"] = 0

    team_matches = pd.concat([home, away], ignore_index=True)
    team_matches = team_matches.sort_values(["Team", "Date"]).reset_index(drop=True)
    return team_matches

team_matches = build_team_match_history(data)

# Pour chaque équipe, calculer la moyenne glissante des N derniers matchs
# .shift(1) est CRUCIAL : ça décale d'un match pour ne jamais inclure le match actuel
rolling_cols = ["GoalsFor", "GoalsAgainst", "ShotsFor", "ShotsAgainst",
                 "ShotsOnTargetFor", "ShotsOnTargetAgainst", "CornersFor", "CornersAgainst", "Points"]

for col in rolling_cols:
    team_matches[f"Avg{col}_L5"] = (
        team_matches.groupby("Team")[col]
        .transform(lambda s: s.shift(1).rolling(N_MATCHES, min_periods=1).mean())
    )

# Nombre de matchs déjà joués par l'équipe avant ce match (pour savoir si on a assez d'historique)
team_matches["MatchesPlayed"] = team_matches.groupby("Team").cumcount()

print("Aperçu de l'historique par équipe :")
print(team_matches[team_matches["Team"] == "Arsenal"][
    ["Date", "Team", "GoalsFor", "GoalsAgainst", "Points", "AvgPoints_L5", "MatchesPlayed"]
].head(10))

team_matches.to_csv("../data/team_match_history.csv", index=False)
print(f"\n✅ Sauvegardé : {len(team_matches)} lignes (équipe x match) dans data/team_match_history.csv")
