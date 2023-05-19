import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import csv 

# Une fonction = une action


def extract_categories_urls():
                                #### Quoi faire ? EXTRAIRE EN LISTE CHAQUE URL DES PAGES DES CATEGORIES

                                    # Définir lien page index, 2, 3, si existent (Cibler balise html, modifier, incrémenter, condition/boléens);
                                    # Ajouter liste (Création liste) ;
                                    # Catégorie par catégorie = boucle ;
                                    # Gérer les doublons (listes de comparaison, boucle) ;

    liste_titres = [] # Création liste référence pour gestion des doublons

    root_url = "http://books.toscrape.com/" 
    response = requests.get(root_url)           

    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        uls = soup.find("ul", {"class": "nav nav-list"}).find("ul").find_all("li") 

        categories_urls = [] # Création liste urls des pages des uls (catégories)

        for ul in uls:       #### BOUCLE : Pour chaque page d'une ul (catégorie, base max 3 pages) : 
                                            # 1) Définir url Index + ajouter liste ; 
                                            # 2) Puis définir lien page 2 (modifier url Index) + (si existe) ajouter liste, sinon STOP ;
                                            # 3) Puis définir lien page 3 (Incrémenter page 2) + (si existe) ajouter liste, sinon STOP ;

            link = ul.find("a")["href"] 
            name = link.replace("catalogue/category/books/", "").replace("/index.html", "")
            name_cat = name.rstrip() 
            full_link = root_url + link 
            categories_urls.append(full_link) 
            url = full_link.replace("index.html", "page-") 
            i = 2
            response_page = requests.get(url + str(i) + ".html") # Requête page 2 = "http://books.toscrape.com/nom_catégorie_nbr/page-2.html"

            search = False
            if response_page: 
                search = True 
                categories_urls.append(url + str(i) + ".html") 

            while search: 
                i += 1 
                response_page = requests.get(url + str(i) + ".html") # Requête page 3 = "http://books.toscrape.com/nom_catégorie_nbr/page-3.html"

                if not response_page:
                    search = False
                else:
                    categories_urls.append(url + str(i) + ".html")

            urls_books = extract_books_urls(categories_urls)

            new_book = [] # Création liste sans doublons pour comparaison à liste_titres
            for book in urls_books : #### BOUCLE : Lister les livres dans une première liste pour affiner dans la seconde
                if book not in liste_titres : # Condition : "si le livre n'existe pas dans liste_titres, ajouter dans new_book"
                    liste_titres.append(book) # Première liste de référence
                    new_book.append(book) # Liste affinée utilisée pour extraction data ;

            extract_books_data(new_book, name_cat) # Appeler def données livres


def extract_books_urls(categories_urls): # Appeler liste urls pages

                                            #### Quoi faire ? EXTRAIRE EN LISTE CHAQUE URL DES LIVRES

                                                # Définir url livre (Cibler balise url, modifier);
                                                # Ajouter liste (Création liste) ;
                                                # Appliquer Url livre par Url livre = Boucle ;

    urls_books = [] # Création liste urls livres (Gestion doublons)

    for link in categories_urls:
        response = requests.get(link)

        if response.ok:
            soup = BeautifulSoup(response.content, "lxml")
            lis = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

            for li in lis:          
                a = li.find("a")
                link = a["href"]
                clean = link.replace("../../../", "")                             # Exemple : <a href="../../../titre_livre/index.html">
                urls_books.append("http://books.toscrape.com/catalogue/" + clean) # http://books.toscrape.com/catalogue/ + fin lien livre, ajouter.

    return urls_books


def extract_books_data(urls_books, name_cat): # Appeler liste urls livres, noms fichiers csv

                                    #### Quoi faire ?
                                    #### 1) CREER FICHIERS CSV PAR CATEGORIE : os/makedir, inclure def CSV phase 1 dans def books_data, appeler name_cat pour noms csv ;
                                    #### 2) DEDANS, EXTRAIRE EN LISTE LES 10 DONNEES DES LIVRES : ciblage balise, url = urls_books, création liste ;
                                    #### 3) EXTRAIRES LES IMAGES DE COUVERTURE ET LES RENOMMER AVEC TITRES CORRESPONDANTS : 
                                    # Appliquer Livre par livre = Boucle ;
            
    if not os.path.exists("./CSV_books"):
            os.makedirs("./CSV_books")

    with open("./CSV_books/" + name_cat + ".csv", "w", encoding="utf-8-sig", newline="") as outf:
            writer = csv.writer(outf, delimiter="|")
            outf.write("URL PRODUIT" + "|" + "UPC" + "|" + "TITRE" + "|" + "PRIX TTC" + "|" + "PRIX HT" + "|" + "STOCK DISPONIBLE" + "|" + "DESCRIPTION" + "|" 
                   + "CATEGORIE" + "|" + "NOTE" + "|" + "URL IMAGE" + "\n") # En têtes
        
            for link in urls_books:
                books_data = []               
                response = requests.get(link)
                if response.ok:
                    soup = BeautifulSoup(response.content, "html.parser")
                        
                    infos_tableur = soup.find("table", {"class" : "table table-striped"}).find_all("td")
                    info_product_description = soup.findAll('p')
                    info_category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")

                    product_page_url = link
                    books_data.append(product_page_url)
                            
                    universal_product_code = infos_tableur[0].text
                    books_data.append(universal_product_code)

                    title = soup.find("li", {"class" : "active"}).text
                    books_data.append(title)

                    titres = soup.find("li", {"class" : "active"}).text # Définir noms livres format texte pour images
                    titre = titres.rstrip()                             # Enlever espaces \n cachés

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

                    if not os.path.exists("./Images_books"): # Répertoire racine où se trouve l'app : "si dossier Images_books n'existe pas, le créer "
                        os.makedirs("./Images_books")
                    with open("./Images_books/" + titre.replace(":", "").replace("/", "").replace("-", "").replace("\"", "").replace("*", "").replace("?", "").replace("_", "").replace(",", "").replace("#", "") + ".jpg", 'wb') as image:
                        image.write(urllib.request.urlopen(image_url).read()) # A cet endroit, rappatrier image via urllib.request
                                                                              # Définir (reconstruire) nom image via Titre + enlever caractères spéciaux
                    
                    writer.writerow(books_data) # colonnes = datas livres

extract_categories_urls()
