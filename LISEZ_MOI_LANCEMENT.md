# 🖥️ Football Match Predictor — Lancement Bureau (méthode rapide)

## Installation (une seule fois, zéro étape manuelle)

1. **Placer le dossier** `foot_project` où tu veux sur ton PC (ex: `Documents\foot_project`).

2. **Créer un raccourci sur le bureau** :
   - Clique droit sur `Lancer_App.bat` → **Créer un raccourci**
   - Coupe-colle ce raccourci sur ton Bureau
   - (Optionnel) Renomme-le en "Match Predictor"
   - (Optionnel) Clique droit sur le raccourci → Propriétés → Changer d'icône

C'est tout. Pas besoin d'installer Python toi-même : le script s'en charge automatiquement au premier lancement (via winget, déjà présent sur Windows 10/11).

## Utilisation

Double-clique sur le raccourci du Bureau.

- **Premier lancement** : si Python n'est pas détecté, il s'installe automatiquement (1-2 min) — une fenêtre te demandera de relancer l'app une fois l'installation terminée. Ensuite les dépendances Python s'installent aussi automatiquement (1-2 min).
- **Lancements suivants** : tout est déjà en place, l'app démarre en quelques secondes et ton navigateur s'ouvre automatiquement.

Pour fermer l'app : ferme simplement la fenêtre noire du terminal.

## Notes

- L'adresse s'ouvre toujours sur `localhost:8501` dans le navigateur — c'est normal, c'est juste l'adresse locale de ton PC, personne d'autre n'y a accès.
- Si l'installation automatique de Python échoue (PC ancien ou sans winget), le script t'indiquera de l'installer manuellement depuis [python.org](https://www.python.org/downloads/) en cochant bien "Add Python to PATH".
