
# WEBSCRAPING - APP :

Ce programme exécutable à la demande récupère les données des livres du site "Books to Scrape" par catégorie + leurs couvertures.


## Technologie :

- Python


## Author :

Alice Nocquet


## Installation de l'environnement et lancement du programme :

```bash
$ git clone https://github.com/AlNocquet/OC-Projet2-Webscraping.git
$ cd OC-Projet2-Webscraping
$ source env/bin/activate (Sous Invite de commande Windows > python -m venv env)
$ python3 -m venv env  (Sous Invite de commande Windows > env\Scripts\activate)
$ pip install -r requirements.txt
$ python app.py
``` 


## DESCRIPTION :


```python
def extract_categories_urls():
```
Cette fonction liste les urls des pages des catégories en gérant l'exclusion des doublons ;


```python
def extract_books_urls(categories_urls):  
```

Cette fonction liste les urls des livres présentes dans les pages des catégories ;


```python
def extract_books_data(urls_books, name_cat):  
```

Cette fonction créé un dossier CSV_books incluant les fichiers .CSV par catégorie, avec les données suivantes :

    * "URL PRODUIT"      (product_page_url)
    * "UPC"              (universal_product_code)
    * "TITRE"            (title)
    * "PRIX TTC"         (price_including_tax)
    * "PRIX HT"          (price_excluding_tax)
    * "STOCK DISPONIBLE" (number_available)
    * "DESCRIPTION"      (product_description)
    * "CATEGORIE"        (category)
    * "NOTE"             (review_rating)
    * "URL"              (image_url)

    + la création du dossier "Images_Books" incluant les images des couvertures des livres avec leurs titres associés.
