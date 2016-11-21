#coding utf-8

import csv
import requests
from bs4 import BeautifulSoup

fichier = "condfem2-JHR.csv"

entetes = {
	"User-Agent":"Magalie St-Amour Béland - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"magalie5412@gmail.com"
}

url1= "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/rep-rap-fra.html"
contenu1 = requests.get(url1, headers=entetes)
page1 = BeautifulSoup(contenu1.text,"html.parser")

concours = 0 # Bonne idée que de vouloir compter le nombre de contrats répondant à un concours, donc à un appel d'offres

for ligne in page1.find_all("li"):
    
    if ligne.a.get("href")[:2] == "20":
        lien1 = ligne.a.get("href")
        # print(lien1)

        annees = lien1[:9]
        # print(annees)
        trimestre = lien1[13:15]
        # print(trimestre)

        hyperlien1 = "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/" + lien1
        print(hyperlien1) # Tu avais, ici, un espace entre «print» et «(hyperlien1)»
             
        contenu2 = requests.get(hyperlien1, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")

        i = 0

        for ligne in page2.find_all("tr"):
            if i != 0:
                lien2 = ligne.a.get("href")
                hyperlien2 = "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/" + annees + "/" + lien2
                print(hyperlien2)
                contrat = []
                contrat.append(hyperlien2)
                contrat.append(annees)
                contrat.append(trimestre)

                # Ici, il fallait faire une troisième boucle pour aller chercher chacun des contrats

                contenu3 = requests.get(hyperlien2, headers=entetes)
                page3 = BeautifulSoup(contenu3.text, "html.parser")

                for item in page3.find_all("tr"):
                    # print(item)
                    if item.td is not None:
                        contrat.append(item.td.text)
                    else:
                        contrat.append(None)

                # Ici, c'est moi qui t'ai induit en erreur
                # Cette vérification doit se faire à la toute fin
                # dans le dernier élément de la liste contrat
                if "concours" in contrat[-1]:
                    contrat.append("Oui")
                    concours += 1 # L'augmentation de la variable «concours» n'était pas au bon endroit :)
                else:   
                    contrat.append("Non")

                print(contrat)

                # print("La mention 'adjugé par un concours' se retrouve dans {} contrats.".format(sum("Oui"))) # Ici, tu voulais faire une somme des "Oui", mais ce n'était pas nécessaire, puisque c'était ta variable «concours» qui faisait cette somme au fur et à mesure que ton script rencontrait des contrats attibués par concours
                print("La mention 'adjugé par un concours' se retrouve dans {} contrats.".format(concours))

                fin = open(fichier,"a")
                projet = csv.writer(fin)
                projet.writerow(contrat)

                # Il resterait une chose à corriger: chaque ligne du CSV ne compte pas le même nombre de colonnes
                # Cela est dû au fait que toutes les pages des contrats individuels ne comptent pas le même nombre de lignes
                # Mais cela peut se corriger manuellement par la suite à l'aide d'un tableur

            i += 1
