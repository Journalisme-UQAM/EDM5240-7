#coding utf-8

import csv
import requests
from bs4 import BeautifulSoup

fichier = "condfem-jhr.csv"

entetes = {
	"User-Agent":"Magalie St-Amour Béland - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"magalie5412@gmail.com"
}

url = "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/2016-2017/q1-t1-fra.html"

contenu = requests.get(url, headers=entetes)
page = BeautifulSoup(contenu.text,"html.parser")

#print(page)

i = 0

for ligne in page.find_all("tr"):
    if i > 0:
        #print(ligne)
        lien = ligne.a.get("href")
        #print(lien)
        
        hyperlien = "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/2016-2017/" + lien
        #print(hyperlien)
        
        contenu2 = requests.get(hyperlien, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")
        
        contrat =[]

        contrat.append(hyperlien)

        print("#"*50)
        
        for item in page2.find_all("tr"):

            if item.td is not None:
                contrat.append(item.td.text)
            else:
                contrat.append(None)

        print(contrat)

        # Tu avais mis les trois dernières lignes en commentaire
        # ce qui fait que ton script ne créait pas de CSV.
        # En enlevant les commentaires, j'ai vu que ça ne marchait pas
        # tout simplement parce que les trois lignes n'étaient pas
        # alignées avec l'indentation...
        # il suffisait de leur ajouter un espace à chacune pour que ça marche :)
        fin = open(fichier,"a")
        projet = csv.writer(fin)
        projet.writerow(contrat)
        
# Dans un des scripts que je vous ai envoyés, j'ai fait une erreur.
# Quand on écrit « =+1 », on dit «la variable est égale à (plus) 1».
# C'est « +=1 » qu'il faut écrire pour augmenter de 1 la valeur d'une variable dans une boucle.
    # i =+ 1
    i += 1