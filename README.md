# WEBSCRAPING - APP

This on-demand executable program scrapes book data from the "Books to Scrape" website by category, including their cover images.

---

## Technology

Python

---

## Author

Alice Nocquet

---

## Environment setup and program execution

```bash
$ git clone https://github.com/AlNocquet/OC-Projet2-BooksOnline.git
$ cd OC-Projet2-BooksOnline
$ source env/bin/activate        # For Linux/macOS
$ python3 -m venv env            # For Windows
$ env\Scripts\activate           # Windows activation
$ pip install -r requirements.txt
$ python app.py
```

---

## DESCRIPTION

This application is an ETL tool (Extract, Transform, Load): it extracts clean raw data from the web source “Books to Scrape” and processes it to generate usable datasets, which are then saved as CSV files (Comma-Separated Values).

---

```python
def extract_categories_urls():
```

This function retrieves all category page URLs, managing duplicates exclusion.

---

```python
def extract_books_urls(categories_urls):
```

This function extracts all book URLs listed on each category page.

---

```python
def extract_books_data(urls_books, name_cat):
```

This function creates a `CSV_books` folder containing `.CSV` files per category with the following data fields:

- "PRODUCT URL"       (`product_page_url`)
- "UPC"               (`universal_product_code`)
- "TITLE"             (`title`)
- "PRICE (incl. tax)" (`price_including_tax`)
- "PRICE (excl. tax)" (`price_excluding_tax`)
- "AVAILABILITY"      (`number_available`)
- "DESCRIPTION"       (`product_description`)
- "CATEGORY"          (`category`)
- "RATING"            (`review_rating`)
- "IMAGE URL"         (`image_url`)

It also creates the folder `Images_Books` containing the book cover images, named using the corresponding titles.
