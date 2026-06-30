# 🖥️ Créer l'application .exe — Guide complet

Tu as déjà Python installé, donc voici les étapes pour transformer ton app en vraie
application desktop Windows (`.exe`), avec sa propre fenêtre, sans navigateur ni terminal visible.

---

## Étape 1 — Construire l'exécutable (à faire une seule fois)

1. Dézippe le projet où tu veux sur ton PC (ex: `Documents\foot_project`).
2. Ouvre le dossier `foot_project\desktop_build`.
3. **Double-clique sur `Construire_Exe.bat`**.
4. Une fenêtre noire s'ouvre et installe automatiquement :
   - Les dépendances du projet (pandas, scikit-learn, streamlit...)
   - `pyinstaller` (l'outil qui crée le .exe)
   - `pywebview` (pour avoir une vraie fenêtre desktop, sans barre d'adresse navigateur)
5. La construction prend **2 à 5 minutes**. Tu verras défiler beaucoup de texte — c'est normal.
6. À la fin, tu verras : `Construction terminee !`

⚠️ Si une erreur apparaît à propos d'un module manquant, dis-le moi et je corrige le script de build.

---

## Étape 2 — Mettre l'app sur le Bureau

1. Ouvre le dossier `foot_project\desktop_build\dist\FootballMatchPredictor`
2. Tu y trouveras `FootballMatchPredictor.exe`
3. **Clique droit dessus** → **Envoyer vers** → **Bureau (créer un raccourci)**
4. (Optionnel) Renomme le raccourci sur le Bureau en "Match Predictor"
5. (Optionnel) Clique droit sur le raccourci → Propriétés → Changer d'icône, pour personnaliser

⚠️ Important : **ne déplace pas** le fichier `.exe` tout seul hors de son dossier
`FootballMatchPredictor` — il a besoin des fichiers autour de lui pour fonctionner.
Le raccourci, lui, peut être placé n'importe où (Bureau, barre des tâches, etc.).

---

## Étape 3 — Lancer l'application

Double-clique sur le raccourci du Bureau.

- Une fenêtre dédiée à l'application s'ouvre directement (pas de navigateur, pas de terminal).
- Le premier lancement peut prendre 5-10 secondes (démarrage du serveur interne).
- Les lancements suivants sont plus rapides.

Pour fermer : ferme simplement la fenêtre de l'application, comme n'importe quel logiciel.

---

## Dépannage rapide

**"Windows a protégé votre ordinateur" (SmartScreen) au premier lancement**
→ Normal pour un .exe non signé numériquement. Clique sur **"Informations complémentaires"**
puis **"Exécuter quand même"**.

**La fenêtre reste blanche quelques secondes**
→ Normal, le serveur interne démarre. Attends 5-10 secondes.

**Antivirus qui bloque le .exe**
→ Certains antivirus sont méfiants envers les .exe créés par PyInstaller (faux positif
fréquent et connu). Ajoute une exception pour le dossier `FootballMatchPredictor` si besoin.

**Erreur pendant la construction (Étape 1)**
→ Copie-colle moi le message d'erreur exact affiché dans la fenêtre noire, je corrigerai
le script immédiatement.
