import requests
from bs4 import BeautifulSoup
import csv


def charger_donnees(en_tete, product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url):	
	with open('data_books', 'a', encoding='utf-8-sig') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(en_tete)
		writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
		

def extra_data():

	url= "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
	reponse = requests.get(url)
	page = reponse.content
	soup = BeautifulSoup(page, "html.parser")

	infos_tableur = soup.find("table", {"class" : "table table-striped"}).find_all("td") 
	info_product_description = soup.findAll('p')
	info_category = soup.find("ul", {"class": "breadcrumb"}).find_all("a")


	product_page_url = url
	universal_product_code = infos_tableur[0].text
	title = soup.find("li", {"class" : "active"}).text
	price_including_tax = infos_tableur[3].text
	price_excluding_tax = infos_tableur[2].text
	number_available = infos_tableur[5].text
	product_description = info_product_description[3].text
	category = info_category[2].text
	review_rating = soup.find("p", {"class": "star-rating"}).get("class")[1]
	image_url = soup.find("div", {"class" : "active"}).img["src"]
	en_tete = ["URL PRODUIT", "UPC", "TITRE", "PRIX TTC", "PRIX HT", "STOCK DISPONIBLE", "DESCRIPTION", "CATEGORIE", "NOTE", "URL IMAGE"] 

	charger_donnees(en_tete, product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)

extra_data()