import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Football Match Predictor", page_icon="⚽", layout="wide")

# ==================================
# CSS
# ==================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: #050A14; }
[data-testid="stSidebar"] { background: #0A1628 !important; border-right: 1px solid #1A2744; }

.app-header { text-align: center; padding: 40px 0 28px; }
.app-header .eyebrow { font-size: 11px; letter-spacing: 4px; text-transform: uppercase;
    color: #3B82F6; font-weight: 600; margin-bottom: 10px; }
.app-header h1 { font-family: 'Bebas Neue', sans-serif; font-size: clamp(44px, 6vw, 82px);
    letter-spacing: 2px; color: #F0F4FF; line-height: 1; margin: 0 0 8px; }
.app-header .sub { color: #4A6080; font-size: 13px; letter-spacing: 1px; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; border-bottom: 1px solid #1A2744; }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px 8px 0 0;
    padding: 10px 18px; color: #4A6080; font-size: 13px; font-weight: 600; border: none; }
.stTabs [aria-selected="true"] { background: #0F1F3D !important; color: #F0F4FF !important;
    border-top: 2px solid #3B82F6; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 24px; }

.club-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 12px; margin-bottom: 28px; }
.club-card { background: #0D1B2E; border: 1px solid #1A2744; border-radius: 12px;
    padding: 16px 8px 12px; text-align: center; }
.club-card img { width: 50px; height: 50px; object-fit: contain; margin-bottom: 8px; display: block; margin-left: auto; margin-right: auto; }
.club-card .cname { font-size: 10px; font-weight: 600; color: #6A88A8; line-height: 1.3; }
.club-card .no-logo { width: 50px; height: 50px; background: #1A2744; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; margin: 0 auto 8px;
    font-size: 18px; }

.matchup-panel { background: linear-gradient(135deg, #0D1B2E 0%, #050A14 100%);
    border: 1px solid #1A2744; border-radius: 20px; padding: 32px 24px; margin: 24px 0; text-align: center; }
.matchup-row { display: flex; align-items: center; justify-content: center; gap: 20px; }
.team-slot { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 10px; }
.team-slot img { width: 80px; height: 80px; object-fit: contain; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5)); }
.team-slot .no-logo-big { width: 80px; height: 80px; background: #1A2744; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 32px; }
.team-slot .tname { font-size: 17px; font-weight: 800; color: #F0F4FF; }
.team-slot .tag { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #4A6080; font-weight: 600; }
.vs-badge { font-family: 'Bebas Neue', sans-serif; font-size: 40px; color: #1A2744; letter-spacing: 2px; flex-shrink: 0; }

.result-banner { background: linear-gradient(135deg, #0D1B2E, #091629);
    border: 1px solid #1A2744; border-radius: 16px; padding: 28px; text-align: center;
    margin-bottom: 20px; position: relative; overflow: hidden; }
.result-banner::before { content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; background: linear-gradient(90deg, #3B82F6, #00FF85, #3B82F6); }
.result-label { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #4A6080; margin-bottom: 8px; font-weight: 600; }
.result-main { font-family: 'Bebas Neue', sans-serif; font-size: 38px; letter-spacing: 3px; color: #F0F4FF; }

.prob-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 20px; }
.prob-box { background: #0D1B2E; border: 1px solid #1A2744; border-radius: 14px; padding: 20px 14px; text-align: center; }
.prob-label { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #4A6080; font-weight: 600; margin-bottom: 6px; }
.prob-val { font-family: 'Bebas Neue', sans-serif; font-size: 40px; line-height: 1; letter-spacing: 1px; }
.prob-val.home { color: #3B82F6; }
.prob-val.draw { color: #64748B; }
.prob-val.away { color: #F43F5E; }

div.stButton > button { background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: #F0F4FF !important; font-weight: 700 !important; font-size: 15px !important;
    letter-spacing: 1px !important; text-transform: uppercase !important;
    padding: 15px 32px !important; border-radius: 12px !important; border: none !important;
    width: 100% !important; box-shadow: 0 4px 20px rgba(37,99,235,0.25) !important; }
div.stButton > button:hover { box-shadow: 0 8px 28px rgba(37,99,235,0.45) !important; transform: translateY(-2px) !important; }

[data-testid="stSelectbox"] > div > div { background: #0D1B2E !important;
    border: 1px solid #1A2744 !important; border-radius: 10px !important; color: #C8D6EF !important; }
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid #1A2744; }

.section-label { font-size: 11px; letter-spacing: 3px; text-transform: uppercase;
    color: #4A6080; font-weight: 600; margin-bottom: 14px; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==================================
# LEAGUES CONFIG
# ==================================
LEAGUES = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": {
        "key": "premier_league",
        "data_file": "data/matches_with_features.csv",
        "model_file": "outputs/model_logreg.pkl",
        "scaler_file": "outputs/scaler.pkl",
        "emoji": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "teams": [
            ("Arsenal",        "theFA_003_Arsenal.svg"),
            ("Aston Villa",    "theFA_005_Aston_Villa.svg"),
            ("Bournemouth",    "theFA_006_Bournemouth.svg"),
            ("Brentford",      "theFA_007_Brentford.svg"),
            ("Brighton",       "theFA_008_Brighton.svg"),
            ("Burnley",        "theFA_022_Burnley.svg"),
            ("Chelsea",        "theFA_001_Chelsea.svg"),
            ("Crystal Palace", "theFA_009_Crystal_Palace.svg"),
            ("Everton",        "theFA_010_Everton.svg"),
            ("Fulham",         "theFA_011_Fulham.svg"),
            ("Ipswich",        "theFA_012_Ipswich.svg"),
            ("Leicester",      "theFA_013_Leicester.svg"),
            ("Liverpool",      "theFA_004_Liverpool.svg"),
            ("Man City",       "theFA_002_Man_City.svg"),
            ("Man United",     "theFA_014_Man_United.svg"),
            ("Newcastle",      "theFA_015_Newcastle.svg"),
            ("Nott'm Forest",  "theFA_016_Nottingham.svg"),
            ("Southampton",    "theFA_017_Southampton.svg"),
            ("Tottenham",      "theFA_018_Hotspur.svg"),
            ("West Ham",       "theFA_019_West_Ham.svg"),
            ("Wolves",         "theFA_020_Wolves.svg"),
        ]
    },
    "🇫🇷 Ligue 1": {
        "key": "ligue1",
        "data_file": "data/ligue1_features.csv",
        "model_file": "outputs/model_ligue1.pkl",
        "scaler_file": "outputs/scaler_ligue1.pkl",
        "emoji": "🇫🇷",
        "teams": [
            ("PSG",         "FFF_001__Paris.svg"),
            ("Marseille",   "FFF_009_Marseille.svg"),
            ("Lyon",        "FFF_008_Lyon.svg"),
            ("Monaco",      "FFF_010_Monaco.svg"),
            ("Lille",       "FFF_007_Lille.svg"),
            ("Nice",        "FFF_013_Nice.svg"),
            ("Lens",        "FFF_006_Lens.svg"),
            ("Rennes",      "FFF_015_Rennais.svg"),
            ("Reims",       "FFF_014_Reims.svg"),
            ("Strasbourg",  "FFF_016_Strasbourg.svg"),
            ("Montpellier", "FFF_011_Montpellier.svg"),
            ("Toulouse",    "FFF_018_Toulouse.svg"),
            ("Brest",       "FFF_004_Brestois.svg"),
            ("Nantes",      "FFF_012_Nantes.svg"),
            ("Le Havre",    "FFF_005_Le_Havre.svg"),
            ("Lorient",     "FFF_019_FC_Lorient.svg"),
            ("Metz",        "FFF_021_FC_Metz.svg"),
            ("Auxerre",     "FFF_003_Auxerre.svg"),
        ]
    },
    "🇪🇸 La Liga": {
        "key": "laliga",
        "data_file": "data/laliga_features.csv",
        "model_file": "outputs/model_laliga.pkl",
        "scaler_file": "outputs/scaler_laliga.pkl",
        "emoji": "🇪🇸",
        "teams": [
            ("Real Madrid",    "RFEF_001_Real_Madrid.svg"),
            ("Barcelona",      "RFEF_006_Barcelona.svg"),
            ("Atletico Madrid","RFEF_002_Atletico_Madrid.svg"),
            ("Athletic Bilbao","RFEF_004_Athletic_Bilbao.svg"),
            ("Real Sociedad",  "RFEF_017_Real_Sociedad.svg"),
            ("Villarreal",     "RFEF_021_Villarreal.svg"),
            ("Real Betis",     "RFEF_016_Real_Betis.svg"),
            ("Sevilla",        "RFEF_018_Sevilla.svg"),
            ("Girona",         "RFEF_008_Girona.svg"),
            ("Osasuna",        "RFEF_014_Osasuna.svg"),
            ("Celta",          "RFEF_007_Celta.svg"),
            ("Getafe",         "RFEF_012_Getafe.svg"),
            ("Alavés",         "RFEF_005_Alavés.svg"),
            ("Las Palmas",     "RFEF_010_Las_Palmas.svg"),
            ("Leganés",        "RFEF_011_Leganés.svg"),
            ("Vallecano",      "RFEF_015_Vallecano.svg"),
            ("Espanyol",       "RFEF_009_Espanyol.svg"),
            ("Mallorca",       "RFEF_013_Mallorca.svg"),
            ("Valencia",       "RFEF_019_Valencia.svg"),
            ("Real Valladolid","RFEF_020_Real_Valladolid.svg"),
        ]
    },
    "🇩🇪 Bundesliga": {
        "key": "bundesliga",
        "data_file": "data/bundesliga_features.csv",
        "model_file": "outputs/model_bundesliga.pkl",
        "scaler_file": "outputs/scaler_bundesliga.pkl",
        "emoji": "🇩🇪",
        "teams": [
            ("Bayern Munich",   "DFB_001_Bayern_Munich.svg"),
            ("Dortmund",        "DFB_002_Dortmund.svg"),
            ("Leipzig",         "DFB_006_Leipzig.svg"),
            ("Leverkusen",      "DFB_004_Leverkusen.svg"),
            ("Frankfurt",       "DFB_007_Frankfurt.svg"),
            ("Wolfsburg",       "DFB_012_Wolfsburg.svg"),
            ("Stuttgart",       "DFB_005_Stuttgart.svg"),
            ("Freiburg",        "DFB_011_Freiburg.svg"),
            ("Union Berlin",    "DFB_015_Union_Berlin.svg"),
            ("Mainz",           "DFB_013_Mainz.svg"),
            ("Monchengladbach", "DFB_014_Monchengladbach.svg"),
            ("Hoffenheim",      "DFB_008_Hoffenheim.svg"),
            ("Bremen",          "DFB_010_Bremen.svg"),
            ("Augsburg",        "DFB_003_Augsburg.svg"),
            ("Bochum",          "DFB_016_Bochum.svg"),
            ("Heidenheim",      "DFB_009_Heidenheim.svg"),
            ("Holstein Kiel",   "DFB_018_Holstein_Kiel.svg"),
            ("St. Pauli",       "DFB_017_St._Pauli.svg"),
        ]
    },
    "🇮🇹 Serie A": {
        "key": "seriea",
        "data_file": "data/seriea_features.csv",
        "model_file": "outputs/model_seriea.pkl",
        "scaler_file": "outputs/scaler_seriea.pkl",
        "emoji": "🇮🇹",
        "teams": [
            ("Intel Milan",  "FIGC_002_Intel_Milan.svg"),
            ("AC Milan",     "FIGC_013_AC_Milan.svg"),
            ("Juventus",     "FIGC_001_Juventus.svg"),
            ("Napoli",       "FIGC_015_Napoli.svg"),
            ("Roma",         "FIGC_017_Roma.svg"),
            ("Lazio",        "FIGC_011_Lazio.svg"),
            ("Atalanta",     "FIGC_003_Atalanta.svg"),
            ("Fiorentina",   "FIGC_008_Fiorentina.svg"),
            ("Bologna",      "FIGC_004_Bologna.svg"),
            ("Torino",       "FIGC_018_Torino.svg"),
            ("Udinese",      "FIGC_019_Udinese.svg"),
            ("Genoa",        "FIGC_009_Genoa.svg"),
            ("Verona",       "FIGC_010_Verona.svg"),
            ("Cagliari",     "FIGC_005_Cagliari.svg"),
            ("Monza",        "FIGC_014_Monza.svg"),
            ("Lecce",        "FIGC_012_Lecce.svg"),
            ("Sassuolo",     "FIGC_021_Sassuolo.svg"),
            ("Empoli",       "FIGC_007_Empoli.svg"),
            ("Venezia",      "FIGC_020_Venezia.svg"),
            ("Como",         "FIGC_006_Como.svg"),
        ]
    },
}

FEATURES = [
    'Home_AvgGoalsFor_L5','Home_AvgGoalsAgainst_L5','Home_AvgShotsFor_L5',
    'Home_AvgShotsAgainst_L5','Home_AvgShotsOnTargetFor_L5','Home_AvgShotsOnTargetAgainst_L5',
    'Home_AvgCornersFor_L5','Home_AvgCornersAgainst_L5','Home_AvgPoints_L5',
    'Away_AvgGoalsFor_L5','Away_AvgGoalsAgainst_L5','Away_AvgShotsFor_L5',
    'Away_AvgShotsAgainst_L5','Away_AvgShotsOnTargetFor_L5','Away_AvgShotsOnTargetAgainst_L5',
    'Away_AvgCornersFor_L5','Away_AvgCornersAgainst_L5','Away_AvgPoints_L5',
    'Diff_AvgPoints_L5','Diff_AvgGoalsFor_L5'
]

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

@st.cache_resource
def load_model(model_path, scaler_path):
    return joblib.load(model_path), joblib.load(scaler_path)

def logo_path(filename):
    return os.path.join("assets", "logos", filename)

def logo_img_tag(filename, size=50):
    path = logo_path(filename)
    if filename and os.path.exists(path):
        return f'<img src="app/{path}" width="{size}" height="{size}" style="object-fit:contain"/>'
    return f'<div style="width:{size}px;height:{size}px;background:#1A2744;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:{size//2}px">⚽</div>'

def get_team_stats(df, home_team, away_team):
    home_data = df[df["HomeTeam"] == home_team].tail(5)
    away_data = df[df["AwayTeam"] == away_team].tail(5)

    def safe_mean(data, col, default=1.2):
        return data[col].mean() if not data.empty and col in data.columns else default

    return {
        'home_goals':   safe_mean(home_data, 'Home_AvgGoalsFor_L5'),
        'home_points':  safe_mean(home_data, 'Home_AvgPoints_L5', 1.0),
        'home_corners': safe_mean(home_data, 'Home_AvgCornersFor_L5', 5.0),
        'home_shots':   safe_mean(home_data, 'Home_AvgShotsFor_L5', 12.0),
        'away_goals':   safe_mean(away_data, 'Away_AvgGoalsFor_L5'),
        'away_points':  safe_mean(away_data, 'Away_AvgPoints_L5', 1.0),
        'away_corners': safe_mean(away_data, 'Away_AvgCornersFor_L5', 5.0),
        'away_shots':   safe_mean(away_data, 'Away_AvgShotsFor_L5', 12.0),
    }

# ==================================
# HEADER
# ==================================
st.markdown("""
<div class="app-header">
    <div class="eyebrow">Machine Learning · 5 Major Leagues</div>
    <h1>Match Predictor</h1>
    <p class="sub">Premier League · Ligue 1 · La Liga · Bundesliga · Serie A</p>
</div>
""", unsafe_allow_html=True)

# ==================================
# TABS
# ==================================
tabs = st.tabs(list(LEAGUES.keys()))

for tab, (league_name, league) in zip(tabs, LEAGUES.items()):
    with tab:
        teams = league["teams"]
        team_names = [t[0] for t in teams]
        team_logo_map = {t[0]: t[1] for t in teams}

        # ---- Club logo grid ----
        st.markdown("<p class='section-label'>Clubs</p>", unsafe_allow_html=True)

        grid_html = '<div class="club-grid">'
        for team_name, logo_file in teams:
            lpath = logo_path(logo_file)
            if os.path.exists(lpath):
                img_tag = f'<img src="app/{lpath}" alt="{team_name}"/>'
            else:
                img_tag = f'<div class="no-logo">⚽</div>'
            grid_html += f'<div class="club-card">{img_tag}<div class="cname">{team_name}</div></div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

        st.markdown("---")

        # ---- Team selection ----
        st.markdown("<p class='section-label'>🎯 Select teams to simulate</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            home_team = st.selectbox("🏠 Home Team", team_names, key=f"home_{league['key']}")
        with c2:
            away_opts = [t for t in team_names if t != home_team]
            away_team = st.selectbox("✈️ Away Team", away_opts, key=f"away_{league['key']}")

        if home_team == away_team:
            st.error("⚠️ Sélectionne deux équipes différentes.")
            st.stop()

        # ---- Matchup panel ----
        h_logo = team_logo_map.get(home_team, "")
        a_logo = team_logo_map.get(away_team, "")
        h_img = logo_img_tag(h_logo, 80) if h_logo else '<div class="no-logo-big">⚽</div>'
        a_img = logo_img_tag(a_logo, 80) if a_logo else '<div class="no-logo-big">⚽</div>'

        st.markdown(f"""
        <div class="matchup-panel">
            <div class="matchup-row">
                <div class="team-slot">
                    <span class="tag">Domicile</span>
                    {h_img}
                    <span class="tname">{home_team}</span>
                </div>
                <div class="vs-badge">VS</div>
                <div class="team-slot">
                    <span class="tag">Extérieur</span>
                    {a_img}
                    <span class="tname">{away_team}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ---- Load data & stats ----
        df = load_data(league["data_file"])
        stats = get_team_stats(df, home_team, away_team)

        # ---- Stats table ----
        st.markdown("<p class='section-label'>Forme — 5 derniers matchs</p>", unsafe_allow_html=True)
        stats_df = pd.DataFrame({
            "Statistique":  ["Buts marqués moy.", "Points moy.", "Tirs moy.", "Corners moy."],
            home_team:      [round(stats['home_goals'],2), round(stats['home_points'],2),
                             round(stats['home_shots'],2), round(stats['home_corners'],2)],
            away_team:      [round(stats['away_goals'],2), round(stats['away_points'],2),
                             round(stats['away_shots'],2), round(stats['away_corners'],2)],
        }).set_index("Statistique")
        st.dataframe(stats_df, use_container_width=True)

        st.write("")

        # ---- Predict ----
        if st.button("⚡ Simuler le match", key=f"btn_{league['key']}"):
            model, scaler = load_model(league["model_file"], league["scaler_file"])

            features = pd.DataFrame([{
                "Home_AvgGoalsFor_L5": stats['home_goals'],
                "Home_AvgGoalsAgainst_L5": 1.2,
                "Home_AvgShotsFor_L5": stats['home_shots'],
                "Home_AvgShotsAgainst_L5": 10,
                "Home_AvgShotsOnTargetFor_L5": 5,
                "Home_AvgShotsOnTargetAgainst_L5": 4,
                "Home_AvgCornersFor_L5": stats['home_corners'],
                "Home_AvgCornersAgainst_L5": 5,
                "Home_AvgPoints_L5": stats['home_points'],
                "Away_AvgGoalsFor_L5": stats['away_goals'],
                "Away_AvgGoalsAgainst_L5": 1.2,
                "Away_AvgShotsFor_L5": stats['away_shots'],
                "Away_AvgShotsAgainst_L5": 10,
                "Away_AvgShotsOnTargetFor_L5": 4,
                "Away_AvgShotsOnTargetAgainst_L5": 4,
                "Away_AvgCornersFor_L5": stats['away_corners'],
                "Away_AvgCornersAgainst_L5": 5,
                "Away_AvgPoints_L5": stats['away_points'],
                "Diff_AvgPoints_L5": stats['home_points'] - stats['away_points'],
                "Diff_AvgGoalsFor_L5": stats['home_goals'] - stats['away_goals'],
            }])

            X = scaler.transform(features)
            prediction = model.predict(X)[0]
            probs = model.predict_proba(X)[0]
            classes = list(model.classes_)
            prob_home = probs[classes.index("H")]
            prob_draw = probs[classes.index("D")]
            prob_away = probs[classes.index("A")]

            labels = {
                "H": f"🏠 {home_team.upper()} GAGNE",
                "D": "🤝 MATCH NUL",
                "A": f"✈️ {away_team.upper()} GAGNE"
            }

            st.markdown(f"""
            <div class="result-banner">
                <div class="result-label">Résultat le plus probable</div>
                <div class="result-main">{labels[prediction]}</div>
            </div>
            <div class="prob-grid">
                <div class="prob-box">
                    <div class="prob-label">Victoire Domicile</div>
                    <div class="prob-val home">{prob_home:.0%}</div>
                </div>
                <div class="prob-box">
                    <div class="prob-label">Match Nul</div>
                    <div class="prob-val draw">{prob_draw:.0%}</div>
                </div>
                <div class="prob-box">
                    <div class="prob-label">Victoire Extérieur</div>
                    <div class="prob-val away">{prob_away:.0%}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            p1, p2, p3 = st.columns(3)
            with p1: st.progress(float(prob_home))
            with p2: st.progress(float(prob_draw))
            with p3: st.progress(float(prob_away))

            st.markdown(f"""
            <p style="text-align:center;font-size:11px;color:#2A3A54;margin-top:14px;">
                {league['emoji']} Modèle entraîné sur {len(df)} matchs · Régression Logistique
            </p>""", unsafe_allow_html=True)
