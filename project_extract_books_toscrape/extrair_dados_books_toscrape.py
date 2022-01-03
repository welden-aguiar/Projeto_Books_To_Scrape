#!/usr/bin/env python
# coding: utf-8

#importando biblioteca
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import date
import re
import os


#obter URLs das páginas para navegar com selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get('http://books.toscrape.com/catalogue/page-1.html')
sleep(1)

link_livros = []

while True:
    html_pagina = bs(driver.page_source)
    lista_livros = html_pagina.findAll('li', attrs='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for item in lista_livros:
        link_livros.append(item.find('a')['href'])
    try:
        driver.find_element_by_class_name('next').find_element_by_tag_name('a').click()
        sleep(0.5)
    except NoSuchElementException:
        driver.close()
        break

#obter dados de cada livro

incremento = 0
driver = webdriver.Firefox(options=options)
lista_valores = []

for url in link_livros:
    incremento += 1
    url_completa = ('http://books.toscrape.com/catalogue/'+url)
    driver.get(url_completa)
    sleep(0.5)
    html_livro = bs(driver.page_source)
    
    #buscar valores na tabela
    valores = (html_livro.find('table', attrs={'class':'table table-striped'}).findAll('td'))
    
    #preenchervariáveis
    id = incremento
    upc = valores[0].text
    product_name = (html_livro.find('div',attrs={'class':'col-sm-6 product_main'}).find('h1')).text
    #valores[2].text
    price = float( re.findall(r'\d+.\d+', valores[2].text)[0] )
    #valores[4].text
    tax = float( re.findall(r'\d+.\d+', valores[4].text)[0])
    if (re.findall(r'\d+',valores[5].text) != 0):
        availability = 1
        quantity = int(re.findall(r'\d+',valores[5].text)[0])
    else:
        availability = 0
        quantity = 0
    num_reviews = valores[6].text   
    rating = html_livro.find('div',attrs={'class':'col-sm-6 product_main'}).find('p', attrs={'class':'star-rating'})['class'][1]
    date_today = date.today()
    
    #carregar a lista
    lista_valores.append([id, upc, product_name, price, tax, availability, quantity, num_reviews, rating, date_today.strftime('%d/%m/%Y')])

driver.close()   

#carregar o Data Frame

#criando a tabela que irá receber os valores
colunas = [
        'ID',
        'UPC',
        'Product Name',
        'Price',
        'Tax',
        'Availability',
        'Quantity in Stock',
        'Number of Reviews',
        'Rating',
        'Extraction Date'
]
dados_livros = pd.DataFrame(lista_valores, columns=colunas)   

#salvar dados em arquivo CSV
dir_path = os.getcwd()
nome_arquivo = dir_path + '/datas_of_books.csv'
dados_livros.to_csv(nome_arquivo, index=False, header=False)

