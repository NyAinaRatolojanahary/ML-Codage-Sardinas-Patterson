from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np
from collections import Counter

app = Flask(__name__)

myModel = joblib.load('../IsCodeModel1.joblib')

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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        langages_input = request.form['langage']
        langages = [l.strip() for l in langages_input.split(',')]
        data = Traiter_langage(langages)
        
        # Convertir en DataFrame pour correspondre au format attendu par le modèle
        data_df = pd.DataFrame(data)
        
        # Prédire avec le modèle
        prediction = myModel.predict(data_df)[0]
        attribut = ['btn btn-success','btn btn-danger']
        color = attribut[0]
        if(prediction==True):
            color = attribut[0]
        else:
            color = attribut[1]
        resultat_sardinas_paterson = isCode(langages)
        false_percentage = myModel.predict_proba(data_df)[0][0] *100
        true_percentage = myModel.predict_proba(data_df)[0][1] *100
        
        return render_template('index.html', prediction=prediction,color=color, resultat_sardinas_paterson=resultat_sardinas_paterson, false_percentage = false_percentage, true_percentage= true_percentage,langages_input=langages_input)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)