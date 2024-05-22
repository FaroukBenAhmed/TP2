'''
TP2 données géographiques
@auteur(e)s     Riad Bennabi et Farouk Ben Ahmed
@matricules     e2357457 et e2078564
@date              21-05-2024
            '''
import csv
import json
import math
import os


class DonneesGeo:
    def __init__(self, ville, pays, latitude, longitude):
        self.ville = str(ville)
        self.pays = str(pays)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __str__(self):
        return f"{self.ville}, {self.pays}, {self.latitude}, {self.longitude}"

    @staticmethod
    def lireDonneesCsv(nomFichier):
        if not os.path.exists(nomFichier):
            print(f"Erreur : le fichier {nomFichier} n'existe pas.")
            return []

        donnees = []
        with open(nomFichier, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'ville' not in row or 'pays' not in row or 'latitude' not in row or 'longitude' not in row:
                    print(f"Erreur : le fichier CSV doit contenir les colonnes 'ville', 'pays', 'latitude' et 'longitude'.")
                    return []
                donnees.append(DonneesGeo(row['ville'], row['pays'], row['latitude'], row['longitude']))
        return donnees

    @staticmethod
    def ecrireDonneesJson(fichier_json, liste_obj_donnees_geo):
        liste_dicts = [obj.__dict__ for obj in liste_obj_donnees_geo]
        with open(fichier_json, 'w', encoding='utf-8') as jsonfile:
            json.dump(liste_dicts, jsonfile, ensure_ascii=False, indent=4)

    @staticmethod
    def calculer_distance(lat1, lon1, lat2, lon2):
        r = 6371  # Rayon de la Terre en kilomètres
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2) ** 2 +
             math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c

    @staticmethod
    def trouverDistanceMin(fichier_json):
        if not os.path.exists(fichier_json):
            print(f"Erreur : le fichier {fichier_json} n'existe pas.")
            return

        with open(fichier_json, 'r', encoding='utf-8') as jsonfile:
            villes = json.load(jsonfile)

        min_distance = float('inf')
        ville1 = ville2 = None

        for i in range(len(villes)):
            for j in range(i + 1, len(villes)):
                d = DonneesGeo.calculer_distance(villes[i]['latitude'], villes[i]['longitude'],
                                                 villes[j]['latitude'], villes[j]['longitude'])
                if d < min_distance:
                    min_distance = d
                    ville1, ville2 = villes[i], villes[j]

        print(
            f"Distance minimale en kilomètres entre 2 villes : Ville 1 : {ville1['ville']} {ville1['pays']} {ville1['latitude']} {ville1['longitude']} et Ville 2 : {ville2['ville']} {ville2['pays']} {ville2['latitude']} {ville2['longitude']} Distance en kilomètres : {min_distance}")

        with open('distances.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ville1', 'ville2', 'distance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'ville1': ville1['ville'], 'ville2': ville2['ville'], 'distance': min_distance})


def affichermenu():
    print("1- Lire les données du fichier csv, créer les objets et afficher les données.")
    print("2- Sauvegarder les données dans un fichier .json.")
    print("3- Lire les données du fichier .json, déterminer et afficher les données associées à la distance minimale entre deux villes et sauvegarder les calculs dans distances.csv.")
    print("Entrez un numéro pour choisir une option ou appuyez sur 'q' pour quitter 😊")


def main():
    while True:
        affichermenu()
        choix = input()
        if choix == '1':
            donnees = DonneesGeo.lireDonneesCsv('Donnees.csv')
            if donnees:
                print("Ville, Pays, Latitude, Longitude")
                for donnee in donnees:
                    print(donnee)
            input("Appuyez sur une touche pour continuer...")
        elif choix == '2':
            if os.path.exists('Donnees.csv'):
                DonneesGeo.ecrireDonneesJson('Donnees.json', donnees)
                print("Données sauvegardées dans Donnees.json")
            else:
                print("Veuillez d'abord lire les données CSV.")
        elif choix == '3':
            if os.path.exists('Donnees.json'):
                DonneesGeo.trouverDistanceMin('Donnees.json')
            else:
                print("Veuillez d'abord sauvegarder les données en JSON.")
        elif choix == 'q':
            break


if __name__ == "__main__":
    main()
