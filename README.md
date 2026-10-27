# TP ACDC80 - Analyse GPS

Ce projet lit `input_log.txt`, filtre les lignes GPS, élimine les coordonnées invalides et exporte deux CSV.

## Lancer

```bash
python parse_gps.py
```

## Fichiers

- `input_log.txt` : fichier original, non modifié.
- `parse_gps.py` : script Python avec les 4 fonctions du TP.
- `output_cleaned.csv` : version du TP avec tolérance de +/- 1 degré.
- `output_detaille.csv` : version complémentaire avec tolérance nulle après arrondi à 2 décimales.
- `.github/workflows/main.yml` : exécution automatique sur GitHub.

## Choix de traitement

Le fichier source contient des coordonnées mais pas d'altitude. Le CSV exporte donc `timestamp`, `latitude`, `longitude`, sans inventer d'altitude. Les lignes `Trip Data` sans horodatage sont filtrées mais non exportées. Les coordonnées `nan` et hors limites sont rejetées. Les coordonnées sont arrondies à deux décimales, comme demandé dans le PDF.

Le seuil +/- 1 degré du sujet regroupe presque tout le trajet en une position. Le CSV détaillé permet de mieux examiner le parcours, mais reste arrondi à 2 décimales.

## Git

Les commits signés SSH doivent être configurés sur l'ordinateur de l'étudiant avant publication. Le dépôt ZIP ne contient aucune clé privée.
