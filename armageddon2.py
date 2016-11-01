#EDM5240
#coding utf-8

import csv
import requests
from bs4 import BeautifulSoup

fichier = "condfem2.csv"

entetes = {
	"User-Agent":"Magalie St-Amour Béland - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"magalie5412@gmail.com"
}

#Ici, j'ai tenté de créer deux boucles au lieu d'une seule. Je suis donc parti une page avant mon premier script,
# c'est à dire à la liste des trimestres.

#Je demande d'aller cherche ce qui se trouve sur cette page et le mettre dans ma variable contenu1.
url1= "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/rep-rap-fra.html"
contenu1 = requests.get(url1, headers=entetes)

#Je demande ensuite à BS4 de "parser" ce qui se trouve dans mon contenu1 et de le mettre dans ma variale page1.
page1 = BeautifulSoup(contenu1.text,"html.parser")
#print(page1)
#CE PRINT MARCHE

# Je débute alors ma première liste.
i = 0
# concours = 0

#Je demande à trouver dans chaque ligne contenue dans ma variable page1, celles qui contiennent de "li".
for ligne in page1.find_all("li"):
    
# Ca me sort alors tous les liens de la page sur lesquels il est possible de cliquer, pas seulement les trimestres.
# Je dois donc ajouter une restriction. Je demande de ne garder les lignes "li" qui ont "20" dedans (pour
# les trimestres qui ont des années. de 2003 à 2017)
    if ligne.a.get("href")[:2] == "20":
#       print(ligne.a.get("href"))
#       print(ligne)
        if ligne.find("a",class_="ui-link"):
#            print(ligne.find("a",class_="ui-link"))
# Je demande à mon script d'aller chercher chaque lien, donc chaque trimestre et de mettre le tout dans ma variable lien1.
            lien1 = ligne.a.get("href")
# J'ai besoin de mes hyperliens de chaque trimestres, donc je crée la variable contenant la partie d'URL constante
# et ma viable lien1.
            hyperlien1 = "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/" + lien1
            print (hyperlien1)
             
#Je commence ensuite ma deuxième boucle. Je veux que pour chaque trimestre, mon script aille dans chaque contrat et les analyse.
# Je lui demande donc de parser le contenu2 qu'il trouve dans mes hyperlien, et de mettre le tout dans page2.
            contenu2 = requests.get(hyperlien1, headers=entetes)
            page2 = BeautifulSoup(contenu2.text, "html.parser")
#Je commence ensuite ma seconde liste, celle de tous les contrats. C'est le même principe que dans mon premier script (armageddon.py)
            i = 0
            for ligne in page2.find_all("tr"):
                #print(ligne)
                if i != 0:
                    lien2 = ligne.a.get("href")
                    hyperlien2 = "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/" + lien2
                    #print(hyperlien2)
# Je crée ma liste finale avec tous les contrats de chaque trimestre.                     
                    contrat = []
                    contrat.append(hyperlien2)
                    for item in page2.find_all("tr"):
# Je ne prend pas de chance, si l'une des cases est vide, je demande à ce que ca ajoute None.                         
                        print(item)
                        if item.td is not None:

#J'ajoute ici une contrainte. Je tente de savoir combien de contrats ont été adjugés par concours. Je demande donc
# qu'à chaque fois que le mot "concours" apparait dans ma liste, mon script ajoute une ligne, et écrive "Oui".
                            contrat.append(item.td.text)
                            if "concours" in item.td.text:
                                contrat.append("Oui")
#S'il n'y a pas le mot "concours", il ajoute "Non".
                            else:   
                                contrat.append("Non")
                                #concours += 1
                        else:
                            contrat.append(None)
                            #print(contrat)
#Je me prépare une petite formule pour qu'une phrase apparaisse quand je fais rouler mon script. Je veux que dans mes {} se
# trouve la somme totale de fois que le mot "Oui" se retrouve dans ma liste.
                            print("La mention 'adjugé par un concours' se retrouve dans {} contrats.".format(sum("Oui")))

#Je crée finalement un dossier csv avec le tout.
            #         #fin = open(fichier,"a")
            #         #projet = csv.writer(fin)
            #         #projet.writerow(contrat)


                    i += 1
