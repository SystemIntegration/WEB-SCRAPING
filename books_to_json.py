#!/usr/bin/env python
# -*-coding:utf-8 -*-
#
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
# File          : books_to_json.py 
# Author        : BMV System Integration Pvt Ltd.
# Version       : 1.0.0
# Date          : 02nd January 2023
# Contact       : info@systemintegration.in
# Purpose       : This is the python script to scrape the data from website and write it into a json file.
# import        : bs4       - to extract the data from requested website.
#                 json      - to convert the data into json data.
#                 requests  - to request the website.
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------


from bs4 import BeautifulSoup
import requests
import json

# get the urls of each book from page 1
def get_book_urls():
    """
    Fetches the books' url from the page 1 of main site url.

    Return : list of books' url
    """
    book_titles = []
    page_no = 1
    try:
        while page_no < 2: # put number of upto pages 
            bookurl = f"https://books.toscrape.com/catalogue/page-{page_no}.html"
            page_no += 1
            r = requests.get(bookurl)
            if r.status_code == 404:
                return None
            htmlContent = r.content
            soup = BeautifulSoup(htmlContent, 'html.parser')
            all_a = soup.find_all('a')
            for j in all_a:
                if not str(j['href']).find('category') != -1 and not str(j['href']).find('..') != -1:
                    if j.has_attr('title'):
                        bname = str(j['href']).split('/')[0]
                        book_titles.append(f"https://books.toscrape.com/catalogue/{bname}/index.html")

        return book_titles
    except Exception as e:
        print("Exception :", e)

# get the books' detail in dictionary
def get_book_details():
    """
    Fetch the detail for each book from respected url

    Returns : dict of Book's details
    """
    books = {}
    book_url = get_book_urls()
    if book_url is None:
        return None

    for burl in book_url:
        res = requests.get(burl)
        htmlcontent = res.content
        soup = BeautifulSoup(htmlcontent, 'html.parser')
        price = soup.find('p', {"class": "price_color"}).get_text().strip()
        availability = soup.find('p', {"class" : "instock availability"}).get_text().strip()
        title = soup.find('h1').get_text().strip()

        books[title] = {"Price" : price, "Availability": availability, "url" : burl}
    return books

# get the books' detail in JSON file
def to_json(books):
    """
    Write the Book's dictionary into JSON file.
    """
    try:
        with open("C:\\Users\\bmvsi-117\\Documents\\books.json", 'w') as bookjson:
            bookjson.write(json.dumps(books))
    except Exception as e:
        print("Exception : ",e)
    

if __name__ == "__main__":

    books = get_book_details()
    if books == None:
        print("Url not Found !!")
    else:
        # print(books)
        to_json(books)
    