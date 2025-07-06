# ======================================================
# Projeto: Engenharia de Dados - MBA USP/ESALQ
# Script: Limpeza e exportação de dados de livros
# Autor: Davi Winder-Catelan
# Descrição: Este script realiza a limpeza de uma base 
#   de dados de livros, gera IDs únicos para autores e 
#   gêneros, traduz os gêneros para português e exporta 
#   os dados tratados em arquivos SQL para uso no MySQL.
# Data: [coloque a data aqui]
# ======================================================

# ==========================
# BLOCO 1: Importação da base
# ==========================
import pandas as pd

df = pd.read_csv('C:/Users/davic/OneDrive/Área de Trabalho/MBA_USP/5.Engenharia de Dados II/livros.csv')
df.head()

df.shape
df.info()
df.columns

# ==========================
# BLOCO 2: Renomear colunas para o português
# ==========================
traducao = {
    'Book':'livro',
    'Author(s)':'autor',
    'Original language':'idioma_original',
    'First published':'ano_publicacao',
    'Approximate sales in millions':'vendas',
    'Genre':'genero'
}

df.rename(columns=traducao, inplace=True)
df.head()

# ==========================
# BLOCO 3: Análise inicial e filtro
# ==========================
df.isnull().sum()
df['autor'].value_counts().head(10)
df[df['autor'] == 'J. K. Rowling']

# ==========================
# BLOCO 4: Criar IDs únicos para autores
# ==========================
autores_unicos = pd.DataFrame(df['autor'].unique(), columns=['autor'])
autores_unicos['autor_id'] = autores_unicos.index + 1
df = df.merge(autores_unicos, on='autor', how='left')
df.head()
df[df['autor'] == 'J. K. Rowling']

# ==========================
# BLOCO 5: Criar IDs únicos para gêneros
# ==========================
generos_unicos = pd.DataFrame(df['genero'].unique(), columns=['genero'])
generos_unicos['genero_id'] = generos_unicos.index + 1
df = df.merge(generos_unicos, on='genero', how='left')
df.head()
df[df['autor'] == 'J. K. Rowling']

# ==========================
# BLOCO 6: Separar DataFrames de autores e gêneros
# ==========================
autores = pd.DataFrame(df['autor'].unique(), columns=['nome'])
generos = pd.DataFrame(df['genero'].unique(), columns=['genero'])

# ==========================
# BLOCO 7: Gerar arquivo autores.sql
# ==========================
# Neste bloco, geramos o arquivo 'autores.sql' contendo os comandos INSERT
# para preencher a tabela 'autores' no banco de dados.
# Cada linha insere um autor único da base.
# As aspas simples no nome são escapadas (duplicadas) para evitar erro de sintaxe no SQL.
with open('autores.sql', 'w', encoding='utf-8') as f:
  for _, row in autores.iterrows():
        nome = row['nome'].replace("'", "''")  # aspas simples para SQL
        f.write(f"INSERT INTO autores (nome) VALUES ('{nome}');\n")

# ==========================
# BLOCO 8: Preencher nulos em 'genero' e revisar
# ==========================
df['genero'] = df['genero'].fillna('Unknown')
df.head(20)
df['genero'].isnull().sum()

generos = pd.DataFrame(df['genero'].unique(), columns=['genero'])
generos

# ==========================
# BLOCO 9: Instalar e importar tradutor
# ==========================
!pip install -q deep-translator
from deep_translator import GoogleTranslator

# ==========================
# BLOCO 10: Traduzir os gêneros para português
# ==========================
generos['genero_pt'] = generos['genero'].apply(
    lambda x: GoogleTranslator(source='auto', target='pt').translate(x)
)

generos.head()
generos['genero_pt'] = generos['genero_pt'].replace('Novella', 'Novela')
generos.head()
generos['genero_pt'] = generos['genero_pt'].str.lower()
generos.head()
generos.shape

# ==========================
# BLOCO 11: Gerar arquivo generos.sql
# ==========================
with open('generos.sql', 'w', encoding='utf-8') as f:
    for nome in generos['genero_pt']:
        nome_escapado = nome.replace("'", "''")
        f.write(f"INSERT INTO generos (nome) VALUES ('{nome_escapado}');\n")

# ==========================
# BLOCO 12: Gerar arquivo livros.sql
# ==========================
with open('livros.sql', 'w', encoding='utf-8') as f:
    for _, row in df.iterrows():
        nome_livro = row['livro'].replace("'", "''")
        idioma = row['idioma_original'].replace("'", "''")
        ano = int(row['ano_publicacao'])
        vendas = float(row['vendas'])
        autor_id = int(row['autor_id'])
        genero_id = int(row['genero_id'])

        sql = (
            f"INSERT INTO livros (nome, idioma, ano_publicacao, vendas, autor_id, genero_id) "
            f"VALUES ('{nome_livro}', '{idioma}', {ano}, {vendas:.2f}, {autor_id}, {genero_id});\n"
        )
        f.write(sql)

# ==========================
# BLOCO 13: Carregar comentários da API (JSON)
# ==========================
api = 'https://raw.githubusercontent.com/guilhermeonrails/datas-csv/refs/heads/main/comentarios.json'
df_comentarios = pd.read_json(api)
df_comentarios.head()
df_comentarios.shape
df.head(2)

# ==========================
# BLOCO 14: Associar comentários aos livros por nome
# ==========================
df_comentarios = df_comentarios.merge(
    df[['livro']].reset_index().rename(columns={'index': 'id_livro'}),
    on='livro',
    how='left'
)
df_comentarios.head()
df_comentarios.isnull().sum()

print(f"{df_comentarios['id_livro'].max()} {df_comentarios['id_livro'].min()}")
df_comentarios[df_comentarios['id_livro'] == 0]

# ==========================
# BLOCO 15: Ajustar IDs de livros
# ==========================
df_comentarios['id_livro'] += 1
print(f"{df_comentarios['id_livro'].max()} {df_comentarios['id_livro'].min()}")

# ==========================
# BLOCO 16: Função auxiliar para tratar valores
# ==========================
def format_value(value):
    if pd.isna(value):
        return 'NULL'
    elif isinstance(value, str):
        value = value.replace("'", "''")
        return f"'{value}'"
    else:
        return str(value)

# ==========================
# BLOCO 17: Gerar arquivo comentarios.sql
# ==========================
output_file = "comentarios.sql"

with open(output_file, 'w', encoding='utf-8') as f:
    for _, row in df_comentarios.iterrows():
        values = (
            format_value(row['id_livro']),
            format_value(row['nome']),
            format_value(row['sobrenome']),
            format_value(row['comentario'])
        )
        sql = f"INSERT INTO comentarios (livro_id, nome, sobrenome, comentario) VALUES ({', '.join(values)});\n"
        f.write(sql)

print(f"Arquivo '{output_file}' gerado com sucesso.")
