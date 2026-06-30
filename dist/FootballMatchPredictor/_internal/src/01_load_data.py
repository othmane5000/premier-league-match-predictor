"""
Étape 1 : Charger et fusionner les données de 4 saisons de Premier League
"""
import pandas as pd

# Colonnes qu'on garde (on jette toutes les colonnes de cotes de paris pour l'instant)
COLS_TO_KEEP = [
    "Date", "HomeTeam", "AwayTeam",
    "FTHG", "FTAG", "FTR",      # Full Time Home/Away Goals, Full Time Result
    "HTHG", "HTAG", "HTR",      # Half Time Home/Away Goals, Half Time Result
    "HS", "AS",                 # Shots Home/Away
    "HST", "AST",               # Shots on Target Home/Away
    "HF", "AF",                 # Fouls Home/Away
    "HC", "AC",                 # Corners Home/Away
    "HY", "AY",                 # Yellow cards Home/Away
    "HR", "AR",                 # Red cards Home/Away
]

files = {
    "2022/23": "../raw_data/season2223.csv",
    "2023/24": "../raw_data/season2324.csv",
    "2024/25": "../raw_data/season2425.csv",
    "2025/26": "../raw_data/season2526.csv",
}

all_seasons = []
for season_label, path in files.items():
    df = pd.read_csv(path, encoding="utf-8-sig")
    df = df[COLS_TO_KEEP].copy()
    df["Season"] = season_label
    all_seasons.append(df)
    print(f"{season_label}: {len(df)} matchs chargés")

# Fusionner toutes les saisons
data = pd.concat(all_seasons, ignore_index=True)

# Convertir la date au bon format (jour/mois/année -> format date)
data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y", dayfirst=True)

# Trier par date (important pour calculer la "forme récente" plus tard)
data = data.sort_values("Date").reset_index(drop=True)

print(f"\nTotal matchs fusionnés : {len(data)}")
print(f"Période : {data['Date'].min().date()} -> {data['Date'].max().date()}")
print(f"\nValeurs manquantes par colonne :")
print(data.isnull().sum()[data.isnull().sum() > 0])

# Sauvegarder le dataset propre
data.to_csv("../data/matches_clean.csv", index=False)
print("\n✅ Sauvegardé dans data/matches_clean.csv")
print("\nAperçu :")
print(data.head())
