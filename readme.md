# Sobre

	Projeto de integração de dados do site books.toscrap

	Este projeto tem como objetivo extrair os dados do site books.toscrap de forma automática e programada, e inserir em um Data Warehouse para futuras análises com ferramentas BI ou IA.

# Tabela de Conteúdos

	# Sobre
	# Tabela de Conteúdos
	# Instalação
	# Como Usar
		# Pré-requisitos
		# Passo a Passo
	# Status do Projeto
	# Autor
	# Agradecimentos
	# Conclusão

# Instalação

	Para a reprodução deste projeto, não é necessária a instalação, porém, é preciso que todos os requisitos tenham sido verificados e instalados no computador. Este projeto foi realizado utilizando o Pop! OS, uma distribuição linux baseada em Debian. Caso esteja utilizando outro sistema operacional, será necessário realizar algumas modificações no arquivo extrair_dados_books_toscrape.py e criar um novo arquivo de script.

# Como Usar

	# Pré-requisitos
	
	Para reprodução deste projeto será necessário ter instalado os seguintes requisitos:
	
	* Sistema Operacional Linux Pop! OS, ou outro baseado em Debian;
	* Python 3.9.7;
	* Seguintes bibliotecas do Python:
		* BeautifulSoup 4
		* Pandas
		* Selenium
		* Psycopg2
	* Ferramenta de edição de texto ou IDE de desenvolvimento que suporte linguagem Python (pycharm, jupyter notebook, etc);
	* Bibliotecas Python: BeautifulSoap4, Pandas e Selenium;
	* Banco de Dados PostegreSQL;
	* PhpPgAdmin ou outra ferramenta de administração de banco de dados para PostgreSQL;
	
	
	# Passo a Passo
	
	Para verificar a execução deste projeto é necessário fazer o download da pasta do projeto e executá-lo.
	Este projeto pode ser executado de duas formas, manualmente executando cada arquivo na sequência que será descrita, ou de forma automática utilizando o Apache Airflow:
	Execução manual:

		* No Terminal ir até a pasta que estão os arquivos;
		* Executar o comando: python3 script_extrair_dados_books_toscrape ;
		* Ao final da execução do comando acima deverá ter um arquivo na sua pasta atual chamado 'datas_of_books.csv';
		* Será necessário criar o banco de dados;
		* Criar um banco de dados no PostgreSql com o nome 'st_area_books_db', os comandos para definição do banco de dados no arquivo DDL.sql;
		* Conectar ao banco 'st_area_books_db' e criar as tabelas: 'st_book', 'st_dim_book' e 'st_dim_facts';
		* Executar o código \COPY, no arquivo DMS.sql para carregar os dados na tabela 'st_book' da stage area;
		* Fazer a conversão dos dados na stage área carregando as tabelas 'st_dim_book' e 'st_dim_facts';
		* Criar um banco de dados com o nome 'dw_books', códigos no arquivo DDL.sql;
		* Criar a extensão dblink, para permitir o acesso a outras tabelas;
		* Conectar ao banco 'dw_books' e crias as tabelas: 'dim_books', 'dim_date' e 'fact_books';
		* Carregar as tabelas: 'dim_books' e 'dim_date', então carregar a tabela 'fact_books';
	
	Após seguir estes passos terá um DW carregado para consultas.
	Lógico que realizar manualmente estes passos está fora de questão, para a idéia de automatizar o preenchimento do DW, seguiremos o fluxo com Airflow:
		
		* Primeiro é necessário já ter criado o banco de dados 'dw_books', com as tabelas 'dim_books', 'dim_date' 'fact_books';
		* Faça alterações nos endereços de diretórios no arquivo 'fluxo_programado_books_toscrape.py', para o endereço onde estão localizados os arquivos no seu computador;
		* Após a criação coloque o arquivo 'fluxo_programado_books_toscrape.py' na sua pasta de dags do Airflow;
		* Agora basta agendar a execução que o processo será realizado de forma automática;
		
	Conforme manual, após esta execução dos passos o DW estará carregado para consultas.
	
# Status do Projeto
	
	Este projeto foi finalizado na sua primeira versão, poderá ainda ser melhorado em suas próximas versões.
	
# Autor

	Este projeto foi realizado pelo proprietário desta conta do GitHub, Welden Aguiar.
	Está permitida a utilização para fins de consulta e aprendizado.
	O projeto foi realizado entre as datas 05/12/2021 até 03/01/2022, com as pausas de recesso de fim de ano.
	
# Agradecimentos

	Agradeço a minha esposa pela compreensão e paciencia durante o planejamento e desenvolvimento deste projeto. Agradeço aos diversos sites de documentação e tutoriais que permitiram obter conhecimento durante a execuação do projeto.
	

# Conclusão
	
	Ao longo da implementação deste projeto tive diversos desafíos e dúvidas que foram vencidas com muita pesquisa e dedicação. Ter diversos materiais tanto em inglês quanto em português me ajudaram muito a finalizar o projeto e executar o planejado. Neste projeto coloquei em prática meus conhecimentos com python e banco de dados. Aprendi a utilizar o PostgreSQL e algumas bibliotecas python como o Apache Airflow. Finalizar este projeto agregou bastante na minha experiência profissional e abriu meus olhos para muitas possibilidades. Este projeto será o primeiro projeto do meu portifólio para a carreira de Engenheiro de Dados.	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
