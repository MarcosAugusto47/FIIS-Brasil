# FIIS-Brasil
Web scraping do site https://fiis.com.br/lista-de-fundos-imobiliarios/, com o objetivo de criar um dataset com informações relevantes de todos os fundos imobiliários do Brasil negociados na B3. Além disso, também são extraídos os dados de composição do IFIX.

* fiis_scraping: pacote AWS Lambda, utilizado em produção.
* notebook-scraping: notebook de trabalho (não entra em produção).

Além disso, há uma aplicação simples com FastAPI que serve como uma interface para puxar 
os dados.

* /: puxa todos os FII's, do dia mais recente.
* /ticker/{}: puxa os dados do ticker do FII inserido, do dia mais recente.
* /ifix/: puxa a composição do IFIX.
