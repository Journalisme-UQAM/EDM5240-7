#coding utf-8

#Étapes à BS4:
#virtualenv -p /usr/bin/python3 py3env
#source py3env/bin/activate
#sudo pip install requests
#sudo pip install BeautifulSoup4

import csv
import requests
from bs4 import BeautifulSoup

#La variable fichier contiendra le résultat final de ma moisson.
fichier = "condfem.csv"

#Je me présente:
entetes = {
	"User-Agent":"Magalie St-Amour Béland - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"magalie5412@gmail.com"
}


url = "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/2016-2017/q1-t1-fra.html"


#Je demande ensuite à la plateforme requests de se connecter à cet URL et de placer son contenu dans
# la variable "contenu".
contenu = requests.get(url, headers=entetes)


#Je demande ensuite au programme BeautifulSoup4 de "parser" ma variable contenu, d'en traduire le 
# texte HTML et de mettre le tout dans ma variable "page".
page = BeautifulSoup(contenu.text,"html.parser")

#Je teste ma "page".
#print(page)

#Je crée mon compteur.
i= 0

#Je demande ensuite à mon script de retenir tous les éléments contenant "tr".
for ligne in page.find_all("tr"):
    if i > 0:
        #print(ligne)
# Je ne veux que l'hyperlien alors je ne m'occupe que des "href". Ca me donne la fin des URL,
# la partie changeante de mes hyperliens.
        lien = ligne.a.get("href")
        #print(lien)
        
#Mon hyperlien (ce dont j'ai besoin ici) a toujours le même début, que je copie,
# puis j'ajoute ma variable lien pour que mon script aille dans chaque contrat.
        hyperlien = "http://www.swc-cfc.gc.ca/trans/account-resp/pd-dp/dc/2016-2017/" + lien
        #print(hyperlien)
        
# Je répète mes étapes du début pour que BS4 aille dans chaque contrat.        
        contenu2 = requests.get(hyperlien, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")
        
# Je crée ma liste.        
        contrat =[]

# Pour que ma liste se fasse, je vais chercher tout ce qui a été "parsé".
# La première ligne de ma liste est l'hyperlien de chaque contrat.
        contrat.append(hyperlien)
        
#J'utilise la fonction find.all pour trouver tous les tr dans mes contrats.        
        for item in page2.find_all("tr"):
            #print(item)
# Si l'une des cases de mon tableau est vide, mon script plantera. Je ne crois pas que
# ce soit le cas ici, mais dans l'optique où j'espèrais aller plus loin dans mon scriptage,
# je n'ai pas pris de chance et mis cette commande afin que None apparaisse dans mon csv
# là où il y a une bulle vide. 
            if item.td is not None:
                contrat.append(item.td.text)
            else:
                contrat.append(None)
        
        print(contrat)


# Au final, je veux créer un fichier csv avec la liste que j'ai créé.
#        fin = open(fichier,"a")
#        projet = csv.writer(fin)
#        projet.writerow(contrat)
        
    i =+ 1
