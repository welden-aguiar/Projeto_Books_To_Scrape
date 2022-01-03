from datetime import date
import pandas as pd
import psycopg2 as psy
from datetime import datetime
import re

#conectar ao bd
def connect():
    con = psy.connect(host='localhost', user='welden', password='12345', database='dw_books')
    return con

#inserir dados
def insert(sql):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except(Exception, psy.DatabaseError) as error:
        print("ERROR: %s" % error)
        con.rollback()
        con.close()
        return 1
    con.close()

#importar dados
colunas = ['id', 'upc', 'name', 'price', 'tax', 'availability', 'quantity', 'reviews', 'rating', 'extract_date']
df = pd.read_csv('./datas_of_books.csv', names=colunas)

#transformar os dados
df['id'] = df['id'].apply(int)
df['price'] = df['price'].apply(float)
df['tax'] = df['tax'].apply(float)
df['availability'] = df['availability'].apply(bool)
df['quantity'] = df['quantity'].apply(int)
df['rating'] = df['rating'].replace('One','1')
df['rating'] = df['rating'].replace('Two','2')
df['rating'] = df['rating'].replace('Three','3')
df['rating'] = df['rating'].replace('Four','4')
df['rating'] = df['rating'].replace('Five','5')
df['rating'] = df['rating'].apply(int)
df['extract_date'] = pd.to_datetime(df['extract_date'], format='%d/%m/%Y')
extract_date_int = []
for i in df.index:
    extract_date_int.append((df['extract_date'][i].year * 10000) + (df['extract_date'][i].month * 100) + (df['extract_date'][i].day))
df['extract_date_int'] = extract_date_int

#corrigir problema de aspas simples na string
for i in df.index:
    name_old = df['name'][i]
    name_conv = re.sub('\'+', '', name_old)
    df['name'] = df['name'].replace(name_old, name_conv)

#criar dados para dimensão tempo
colunas = ['sk_date_id', 'full_date', 'nr_day', 'nr_month', 'nr_year', 'nm_day_of_week']
interval = pd.date_range(start="2021-12-01",end="2022-12-31")
full_date = interval.date
sk_date_id = ((interval.year*10000) + (interval.month*100) + (interval.day))
nr_day = interval.day
nr_month = interval.month
nr_year = interval.year
nr_day_of_week = interval.weekday
nm_day_of_week = []
for i in nr_day_of_week:
    if(i==0) : nm_day_of_week.append('Domingo')
    if(i==1) : nm_day_of_week.append('Segunda-Feira')
    if(i==2) : nm_day_of_week.append('Terça-Feira')
    if(i==3) : nm_day_of_week.append('Quarta-Feira')
    if(i==4) : nm_day_of_week.append('Quinta-Feira')
    if(i==5) : nm_day_of_week.append('Sexta-feira')
    if(i==6) : nm_day_of_week.append('Sábado')

df_dim_date = pd.DataFrame({'sk_date_id':sk_date_id,
                        'full_Date':full_date,
                        'nr_day':nr_day,
                        'nr_month':nr_month,
                        'nr_year':nr_year,
                        'nm_day_of_week':nm_day_of_week
                        })

#Carregar dimensões

#dimensão dim_books
for i in df.index:
    sql = """
        INSERT INTO dim_books 
        (
            nk_book_id, desc_upc, nm_book
        )
        values
        (
            '%d', '%s', '%s'         
        )
    """ % (
        df['id'][i], df['upc'][i], df['name'][i]
    )
    insert(sql)

#dimensão dim_date

sql = """TRUNCATE TABLE dim_date CASCADE;"""
insert(sql)

for i in df_dim_date.index:

    sql = """
        INSERT INTO dim_date 
        (
            sk_date_id, full_date, nr_day, nr_month, nr_year, nm_day_of_week
        )
        VALUES
        (
            '%d', '%s'::DATE, '%d', '%d', '%d', '%s'
        )
    """ % (
        df_dim_date['sk_date_id'][i], 
        df_dim_date['sk_date_id'][i], 
        df_dim_date['nr_day'][i], 
        df_dim_date['nr_month'][i], 
        df_dim_date['nr_year'][i], 
        df_dim_date['nm_day_of_week'][i]
    )
    insert(sql)

# Tabela fato fact_books

for i in df.index:
    sql = """
    INSERT INTO fact_books (
        sk_book_id, sk_date_id, nr_price, nr_tax, flag_availability, nr_quantity_stock, nr_number_reviews, nr_rating, dt_extraction, dt_load
    )
    VALUES
    (
        (select sk_book_id from dim_books where nk_book_id = '%d' order by sk_book_id desc limit 1), 
        '%d', '%f', '%f', '%r', '%d', '%d', '%d', '%s'::DATE, current_date
    )
    
    """ % ( 
        i+1,
        df['extract_date_int'][i], 
        df['price'][i], 
        df['tax'][i], 
        df['availability'][i], 
        df['quantity'][i], 
        df['reviews'][i], 
        df['rating'][i], 
        df['extract_date'][i], 
    )
    insert(sql)