import requests # permet d'envoyer des requêtes HTTP en utilisant Python. La requête HTTP renvoie un objet de réponse avec toutes les données de réponse (contenu, encodage, statut, etc.).
from bs4 import BeautifulSoup # bibliothèque Python d'analyse syntaxique de documents HTML et XML
import os #(operating system) - interargir avec le system d'exploitation
import urllib.request # functions and classes which help in opening URLs
import csv # (Comma Separated Values, valeurs séparées par des virgules) - importation et exportation bases de données


# 1 définition = 1 action


def app():                      # Englober les def
    extract_categories_urls()   # Def de départ


def extract_categories_urls():
                                #### Quoi faire ? EXTRAIRE EN LISTE CHAQUE URL DES PAGES DES CATEGORIES

                                    # Définir lien page index, 2, 3, si existent (Cibler balise html, modifier, incrémenter, condition/boléens);
                                    # Ajouter liste (Création liste) ;
                                    # Catégorie par catégorie = boucle ;

    root_url = "http://books.toscrape.com/"  # Url racine
    response = requests.get(root_url)           

    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        uls = soup.find("ul", {"class": "nav nav-list"}).find("ul").find_all("li") # Cibler Nav-list (ul) catégorie

        categories_urls = [] # Création liste urls des pages des uls (catégories)

        for ul in uls:       #### BOUCLE : Pour chaque page d'une ul (catégorie, base max 3 pages) : 
                                            # 1) Définir url Index + ajouter liste ; 
                                            # 2) Puis définir lien page 2 (modifier url Index) + (si existe) ajouter liste, sinon STOP ;
                                            # 3) Puis définir lien page 3 (Incrémenter page 2) + (si existe) ajouter liste, sinon STOP ;

            link = ul.find("a")["href"] # Cibler balise lien chaque cellule Nav-list : < Ex.: a href="../historical-fiction_4/index.html">
            name = link.replace("catalogue/category/books/", "").replace("/index.html", "") # Isoler noms catégories pour noms fichiers csv
            name_cat = name.rstrip() # Supprimer \n cachés noms catégories pour noms fichiers csv
            full_link = root_url + link # Définir (reconstruire) url : "http://books.toscrape.com/"+ <a href> = "http://books.toscrape.com/nom_catégorie_nbr/Index.html"
            categories_urls.append(full_link) # Ajouter url index à la liste
            url = full_link.replace("index.html", "page-") # Remplacer "index.html" par "page-"
            i = 2
            response_page = requests.get(url + str(i) + ".html") # Requête page 2 = "http://books.toscrape.com/nom_catégorie_nbr/page-2.html"
                                                                 # full_link(root_url + link) + 2 + ".html"
            search = False # (false/true = opérateur de comparaison) Si pas de page 2, fin de boucle pour la catégorie en cours, passer à la suivante

            if response_page: 
                search = True # Si ok
                categories_urls.append(url + str(i) + ".html") # Ajouter url catégorie en cours de boucle "page 2" à la liste

            while search: # "tant que mon expression logique est vraie, exécute le bloc d’instruction suivant:"
                          # "Sinon, sort de la boucle sans exécuter les instructions". Attention, pas de boucle infinie!!! Il faut un false.
                          # Avec if, boucle conditionnelle / On ne connait pas le nombre d'itérations
                i += 1    # Incrémenter
                response_page = requests.get(url + str(i) + ".html") # Requête page 3 = "http://books.toscrape.com/nom_catégorie_nbr/page-3.html"
                                                                     # full_link(root_url + link) + 3 + ".html"
                if not response_page:
                    search = False # Si pas de page 3, fin de boucle pour la catégorie en cours, passer à la suivante
                else:
                    categories_urls.append(url + str(i) + ".html") # Sinon, Ajouter url catégorie en cours de boucle "page 3" à la liste

            urls_books = extract_books_urls(categories_urls) # Appeler def urls livres // Redéfinir "urls_books" pour insertion extract_books_data(urls_books, name_cat)
            extract_books_data(urls_books, name_cat) # Appeler def données livres


def extract_books_urls(categories_urls): # Appeler liste urls pages

                                            #### Quoi faire ? EXTRAIRE EN LISTE CHAQUE URL DES LIVRES

                                                # Définir url livre (Cibler balise url, modifier);
                                                # Ajouter liste (Création liste) ;
                                                # Appliquer Url livre par Url livre = Boucle ;

    urls_books = [] # Création liste urls livres

    for link in categories_urls:
        response = requests.get(link)

        if response.ok:
            soup = BeautifulSoup(response.content, "lxml")
            lis = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"}) # Cibler balises li + class des liens urls des livres

            for li in lis:          #### BOUCLE CHANGEMENT LIEN SUR CHAQUE URL puis LISTE (urls finissent tous par index.html)
                                    # Définir url livre (modifier) + ajouter liste, puis passer à la suivante ;
                a = li.find("a")
                link = a["href"]
                clean = link.replace("../../../", "")                             # Exemple : <a href="../../../titre_livre/index.html">
                urls_books.append("http://books.toscrape.com/catalogue/" + clean) # http://books.toscrape.com/catalogue/ + fin lien livre, ajouter.

    return urls_books # Conserver > compiler avec def extract_categories_urls()


def extract_books_data(urls_books, name_cat): # Appeler liste urls livres, noms fichiers csv

                                    #### Quoi faire ?
                                    #### 1) CREER FICHIERS CSV PAR CATEGORIE : os/makedir, inclure def CSV phase 1 dans def books_data, appeler name_cat pour noms csv ;
                                    #### 2) DEDANS, EXTRAIRE EN LISTE LES 10 DONNEES DES LIVRES : ciblage balise, url = urls_books, création liste ;
                                    #### 3) EXTRAIRES LES IMAGES DE COUVERTURE ET LES RENOMMER AVEC TITRES CORRESPONDANTS : 
                                    # Appliquer Livre par livre = Boucle ;
            
    if not os.path.exists("./CSV_books"): # Répertoire racine où se trouve l'app : "si dossier CSV_books n'existe pas, le créer "
            os.makedirs("./CSV_books")

    with open("./CSV_books/" + name_cat + ".csv", "w", encoding="utf-8-sig", newline="") as outf: # A cet endroit, ouvrir un csv avec nom catégorie correspondante
            writer = csv.writer(outf, delimiter="|")
            outf.write("URL PRODUIT" + "," + "UPC" + "," + "TITRE" + "," + "PRIX TTC" + "," + "PRIX HT" + "," + "STOCK DISPONIBLE" + "," + "DESCRIPTION" + "," 
                   + "CATEGORIE" + "," + "NOTE" + "," + "URL IMAGE" + "\n") # En têtes
        
            for link in urls_books:
                books_data = []               # Création liste 10 datas livres
                response = requests.get(link) # Requête lien url livre en cours
                if response.ok:
                    soup = BeautifulSoup(response.content, "html.parser")
                        
                    infos_tableur = soup.find("table", {"class" : "table table-striped"}).find_all("td") # Cibler cellules tableaux DIV pour se déplacer via [valeur]
                    info_product_description = soup.findAll('p')
                    info_category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")

                    product_page_url = link  # Lien url livre en cours
                    books_data.append(product_page_url) # Ajouter à la liste datas livres
                            
                    universal_product_code = infos_tableur[0].text # Cibler valeur [0] + format texte
                    books_data.append(universal_product_code)

                    title = soup.find("li", {"class" : "active"}).text
                    books_data.append(title)

                    price_including_tax = infos_tableur[3].text
                    books_data.append(price_including_tax)

                    price_excluding_tax = infos_tableur[2].text
                    books_data.append(price_excluding_tax)

                    number_available = infos_tableur[5].text
                    books_data.append(number_available)

                    product_description = info_product_description[3].text
                    books_data.append(product_description)

                    category = info_category[2].text
                    books_data.append(category)

                    review_rating = soup.find("p", {"class": "star-rating"}).get("class")[1]
                    books_data.append(review_rating)

                    img = soup.find("div", {"class": "item active"}).find("img") 
                    img_url = img["src"]
                    cleaner = img_url.replace("../../", "")     # Enlever début cible html ; Ex : <img src="../../media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg">
                    image_url = ("http://books.toscrape.com/" + cleaner) # Définir (reconstruire) url : http://books.toscrape.com/catalogue/nomImage.jpg
                    books_data.append(image_url)
                    
                    writer.writerow(books_data) # colonnes = datas livres

app()
