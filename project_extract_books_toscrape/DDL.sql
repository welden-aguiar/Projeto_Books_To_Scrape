# Arquivo dos comandos de DDL

#####################   STAGE AREA ###############################

# Criar o Banco de Dados da Stage Area

CREATE DATABASE st_area_books_db;


# Criar a tabela st_book na Stage Area

CREATE TABLE ST_BOOK (
	BOOK_ID VARCHAR(20) NOT NULL,
	UPC VARCHAR(30) NOT NULL,
	BOOK_NAME VARCHAR(255) NOT NULL,
	PRICE DECIMAL NOT NULL,
	TAX DECIMAL,
	AVAILABILITY BOOL NOT NULL,
	QUANTITY_IN_STOCK INT NOT NULL,
	NUMBER_OF_REVIEWS INT,
	RATING VARCHAR(10),
	EXTRACTION_DATE VARCHAR(20)
);

CREATE TABLE ST_DIM_BOOKS (
	NK_BOOK_ID INT NOT NULL,
	DESC_UPC VARCHAR(100) NOT NULL,
	NM_BOOK VARCHAR(255) NOT NULL
);

CREATE TABLE ST_FACT_BOOKS (
	NK_BOOK_ID INT NOT NULL,
	NR_PRICE DECIMAL NOT NULL,
	NR_TAX DECIMAL NOT NULL,
	FLAG_AVAILABILITY BOOL NOT NULL,
	NR_QUANTITY_STOCK INT NOT NULL,
	NR_NUMBER_REVIEWS INT NOT NULL,
	NR_RATING INT NOT NULL,
	DT_EXTRACTION DATE NOT NULL
);


#####################   DATA WAREHOUSE ###############################

# Criar o DW 

CREATE DATABASE dw_books;

# criar uma conexão entre diferentes bancos de dados
CREATE EXTENSION dblink;

# Criar tabelas dimensões dim_books e dim_date e tabela fato fact_books

CREATE TABLE DIM_BOOKS (
	SK_BOOK_ID SERIAL PRIMARY KEY,
	NK_BOOK_ID INT NOT NULL,
	DESC_UPC VARCHAR(100) NOT NULL,
	NM_BOOK VARCHAR(255) NOT NULL
);

CREATE TABLE DIM_DATE (
	SK_DATE_ID INT PRIMARY KEY,
	FULL_DATE DATE NOT NULL,
	NR_DAY INT NOT NULL,
	NR_MONTH INT NOT NULL,
	NR_YEAR INT NOT NULL,
	NM_DAY_OF_WEEK VARCHAR(20) NOT NULL
);

CREATE TABLE FACT_BOOKS (
	SK_BOOK_ID INT,
	SK_DATE_ID INT,
	NR_PRICE DECIMAL NOT NULL,
	NR_TAX DECIMAL NOT NULL,
	FLAG_AVAILABILITY BOOL NOT NULL,
	NR_QUANTITY_STOCK INT NOT NULL,
	NR_NUMBER_REVIEWS INT NOT NULL,
	NR_RATING INT NOT NULL,
	DT_EXTRACTION DATE NOT NULL,
	DT_CARGA DATE NOT NULL, 
	PRIMARY KEY (SK_BOOK_ID, SK_DATE_ID),
	CONSTRAINT FK_SK_BOOK_ID FOREIGN KEY (SK_BOOK_ID) REFERENCES DIM_BOOKS (SK_BOOK_ID),
	CONSTRAINT FK_SK_DATE_ID FOREIGN KEY (SK_DATE_ID) REFERENCES DIM_DATE (SK_DATE_ID)
);


