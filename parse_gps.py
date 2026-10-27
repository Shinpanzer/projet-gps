import csv
import math
import hashlib


def lire_et_filtrer_fichier(nom_fichier):
    lignes = []
    with open(nom_fichier, 'r', encoding='latin-1') as fichier:
        for ligne in fichier:
            if 'GNSS_ACCESS_LIB' in ligne or 'Trip Data' in ligne:
                lignes.append(ligne.strip())
    return lignes


def extraire_donnees_brutes(lignes):
    donnees = []
    for ligne in lignes:
        try:
            # Les lignes Trip Data n'ont pas de date ni d'heure.
            if 'GNSS_ACCESS_LIB' not in ligne:
                continue
            champs = next(csv.reader([ligne]))
            date = champs[1].replace('/', '-')
            heure = champs[2].split('.')[0]
            coordonnees = champs[3].split(',')
            latitude = float(coordonnees[0].strip())
            longitude = float(coordonnees[1].strip())
            donnees.append((date + ' ' + heure, latitude, longitude))
        except (ValueError, IndexError, StopIteration):
            continue
    return donnees


def nettoyer_et_dedoublonner(donnees, tolerance):
    resultat = []
    for date, latitude, longitude in donnees:
        if not math.isfinite(latitude) or not math.isfinite(longitude):
            continue
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            continue
        lat = round(latitude, 2)
        lon = round(longitude, 2)
        if resultat:
            derniere_lat = resultat[-1][1]
            derniere_lon = resultat[-1][2]
            if abs(lat - derniere_lat) <= tolerance and abs(lon - derniere_lon) <= tolerance:
                continue
        resultat.append((date, lat, lon))
    return resultat


def exporter_et_hasher(donnees, nom_fichier):
    with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier)
        writer.writerow(['timestamp', 'latitude', 'longitude'])
        writer.writerows(donnees)
    with open(nom_fichier, 'rb') as fichier:
        empreinte = hashlib.sha256(fichier.read()).hexdigest()
    print(nom_fichier, ':', len(donnees), 'positions')
    print('SHA-256 :', empreinte)
    print('FLAG : FLAG_OCLCC_' + empreinte[:12])


if __name__ == '__main__':
    lignes = lire_et_filtrer_fichier('input_log.txt')
    donnees = extraire_donnees_brutes(lignes)
    print('Lignes GPS filtrées :', len(lignes))
    print('Positions lues :', len(donnees))
    # Version strictement conforme au seuil +/- 1 degré du PDF.
    strict = nettoyer_et_dedoublonner(donnees, 1.0)
    exporter_et_hasher(strict, 'output_cleaned.csv')
    # Version complémentaire : conserve les déplacements après arrondi.
    detail = nettoyer_et_dedoublonner(donnees, 0.0)
    exporter_et_hasher(detail, 'output_detaille.csv')
