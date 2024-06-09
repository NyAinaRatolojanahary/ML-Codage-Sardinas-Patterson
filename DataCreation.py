import random
import numpy as np
from collections import Counter
import csv

def generer_mot_binaire():
    longueur = random.randint(1, 7)
    mot_binaire = ''.join(random.choice(['0', '1']) for _ in range(longueur))
    return mot_binaire

def generer_langage():
    nombre_de_mots = random.randint(1, 10)
    langage = {generer_mot_binaire() for _ in range(nombre_de_mots)}
    return langage

def generer_langage(mots_binaires):
    nombre_de_mots = random.randint(1, 10)
    langage = set(random.sample(mots_binaires, min(nombre_de_mots, len(mots_binaires))))
    return langage

# Colonnes d'entrainement

def nombre_de_mots(langage):
    return len(langage)

def longueur_moyenne(langage):
    return np.mean([len(mot) for mot in langage])

def longueur_maximale(langage):
    return max(len(mot) for mot in langage)

def longueur_minimale(langage):
    return min(len(mot) for mot in langage)

def diversite_binaire(langage):
    tous_bits = ''.join(langage)
    compte = Counter(tous_bits)
    total_bits = sum(compte.values())
    proportion_0 = compte['0'] / total_bits
    proportion_1 = compte['1'] / total_bits
    return proportion_0, proportion_1

def distribution_des_longueurs(langage):
    compte_longueurs = Counter([len(mot) for mot in langage])
    return dict(compte_longueurs)


def entropie_binaire(langage):
    tous_bits = ''.join(langage)
    compte = Counter(tous_bits)
    total_bits = sum(compte.values())
    entropie = -sum((count / total_bits) * np.log2(count / total_bits) for count in compte.values())
    return entropie

def isLongueurFixe(language):
    if not isinstance(language, list) or not language or not language[0]:  # Vérifie si c'est une liste valide et non vide
        return False
    longueur = len(language[0])
    for mot in language:
        if len(mot) != longueur:
            return False
    return True


def quotient(M, language):
    quotient_set = set()
    for u in M:
        for l in language:
            if l.startswith(u):
                temp = l[len(u):]
                if temp == "":
                    temp = "eps"
                quotient_set.add(temp)
    return quotient_set


def isCode(language):
    if not language:
        return False
    if isLongueurFixe(language):
        return True

    history = []
    if "eps" in language:
        return False

    l1 = quotient(language, language)
    if "eps" in l1:
        l1.remove("eps")

    history.append(set(language))
    history.append(l1)

    i = 2
    while True:
        l21 = quotient(language, l1)
        l22 = quotient(l1, language)
        l2 = l21 | l22

        if "eps" in l2:
            break
        if l2 in history:
            return True

        history.append(l2)
        l1 = l2
        i += 1

    return False

# Creation de donnee

def convertir_liste_en_string(liste):
    return ' '.join(liste)


def creer_donnees_entrainement(n):
    donnees = []
    for _ in range(n):
        mots = [generer_mot_binaire() for _ in range(random.randint(1, 7))]
        langage = generer_langage(mots)
        langage_string = convertir_liste_en_string(langage)
        proportion_0, proportion_1 = diversite_binaire(langage)
        distribution = distribution_des_longueurs(langage)
        donnees.append({
            'langage': langage_string,
            'nombre_de_mots': nombre_de_mots(langage),
            'longueur_moyenne': longueur_moyenne(langage),
            'longueur_maximale': longueur_maximale(langage),
            'longueur_minimale': longueur_minimale(langage),
            'diversite_binaire_0': proportion_0,
            'diversite_binaire_1': proportion_1,
            'entropie_binaire': entropie_binaire(langage),
            'distribution_des_longueurs 1': distribution.get(1,0),
            'distribution_des_longueurs 2': distribution.get(2,0),
            'distribution_des_longueurs 3': distribution.get(3,0),
            'distribution_des_longueurs 4': distribution.get(4,0),
            'distribution_des_longueurs 5': distribution.get(5,0),
            'distribution_des_longueurs 6': distribution.get(6,0),
            'distribution_des_longueurs 7': distribution.get(7,0),
            'code': isCode(langage)
        })
    return donnees

def ecrire_donnees_csv(donnees, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'langage','nombre_de_mots', 'longueur_moyenne', 'longueur_maximale', 'longueur_minimale',
            'diversite_binaire_0', 'diversite_binaire_1', 'entropie_binaire', 'distribution_des_longueurs 1','distribution_des_longueurs 2',
            'distribution_des_longueurs 3','distribution_des_longueurs 4','distribution_des_longueurs 5','distribution_des_longueurs 6','distribution_des_longueurs 7'
            ,'code'
        ])
        writer.writeheader()
        for donnee in donnees:
            writer.writerow(donnee)
            

def Traiter_langage(langage):
    # Convertir la liste de chaînes en une seule chaîne avec des espaces
    langage_string = ' '.join(langage)
    
    donnees = []
    proportion_0, proportion_1 = diversite_binaire(langage)
    distribution = distribution_des_longueurs(langage)
    donnees.append({
        'nombre_de_mots': nombre_de_mots(langage),
        'longueur_moyenne': longueur_moyenne(langage),
        'longueur_maximale': longueur_maximale(langage),
        'longueur_minimale': longueur_minimale(langage),
        'diversite_binaire_0': proportion_0,
        'diversite_binaire_1': proportion_1,
        'entropie_binaire': entropie_binaire(langage),
        'distribution_des_longueurs 1': distribution.get(1,0),
        'distribution_des_longueurs 2': distribution.get(2,0),
        'distribution_des_longueurs 3': distribution.get(3,0),
        'distribution_des_longueurs 4': distribution.get(4,0),
        'distribution_des_longueurs 5': distribution.get(5,0),
        'distribution_des_longueurs 6': distribution.get(6,0),
        'distribution_des_longueurs 7': distribution.get(7,0)
    })
    return donnees

# Exemple d'utilisation
# langage = ['0', '101', '0101', '1100']
# resultat = Traiter_langage(langage)
# print(resultat)



# mots_binaires = [generer_mot_binaire() for _ in range(100)]

# print("Liste des mots binaires générés:", mots_binaires)

# Générer et afficher 5 langages aléatoires à partir des mots binaires générés
# for _ in range(100):
#     print(generer_langage(mots_binaires))
    
# mots_binaires = [generer_mot_binaire() for _ in range(20)]
# langage = generer_langage(mots_binaires)

# print("Langage généré:", langage)
# print("Nombre de mots:", nombre_de_mots(langage))
# print("Longueur moyenne des mots:", longueur_moyenne(langage))
# print("Longueur maximale des mots:", longueur_maximale(langage))
# print("Longueur minimale des mots:", longueur_minimale(langage))
# print("Diversité binaire (proportion de '0' et '1'):", diversite_binaire(langage))
# print("Distribution des longueurs des mots:", distribution_des_longueurs(langage))
# print("Entropie binaire:", entropie_binaire(langage))

# donnees = creer_donnees_entrainement(6250)  # Vous pouvez ajuster le nombre de langages générés
# ecrire_donnees_csv(donnees, 'donnees_entrainement1.csv')


# print('1:',donnees[10])

# input_data = ['0', '101', '0101', '1100']

# val = Traiter_langage(input_data)

# print(val)
