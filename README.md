# Projeto de Engenharia de Dados — ETL de Livros 📚

Projeto desenvolvido no MBA em Data Science e Analytics (ESALQ/USP), com foco em aplicar um processo ETL (Extração, Transformação e Carregamento) sobre uma base de livros, utilizando Python e MySQL.

---

## Tecnologias Utilizadas

- Python 3.x
- Pandas
- MySQL
- SQL
- CSV

---

## Estrutura do Projeto

```
engenharia-de-dados-usp-esalq-livraria/
├── dados/
│   └── livros.csv
├── python/
│   └── limpeza_livros.py
└── sql/
    ├── criacao_tabelas.sql
    ├── autores.sql
    ├── generos.sql
    ├── livros.sql
    └── comentarios.sql
```

---

## Etapas do Projeto (ETL)

### 1. Extração  
O arquivo `livros.csv`, localizado em `dados/`, foi usado como base bruta.

### 2. Transformação  
O script `python/limpeza_livros.py` trata inconsistências, separa colunas e estrutura os dados em tabelas normalizadas.

### 3. Carga  
Os scripts SQL inserem os dados no banco de dados:

- `criacao_tabelas.sql`: cria a estrutura das tabelas
- `autores.sql`, `generos.sql`, `livros.sql`, `comentarios.sql`: inserem os dados tratados

---

## Como Executar

1. Certifique-se de ter Python e MySQL instalados.

2. Execute o script Python no terminal:

```bash
python python/limpeza_livros.py
```

3. No MySQL, execute os scripts na seguinte ordem:

   1. `criacao_tabelas.sql`
   2. `autores.sql`
   3. `generos.sql`
   4. `livros.sql`
   5. `comentarios.sql`

---

## Autor

**Davi Winder-Catelan**  
Analista de Inteligência de Mercado e Análise de Dados  
MBA em Data Science e Analytics — ESALQ/USP  
[LinkedIn](https://www.linkedin.com/in/davicatelan)
