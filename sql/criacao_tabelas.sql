-- ========================================
-- CRIAÇÃO DO BANCO DE DADOS E TABELAS
-- Projeto: Engenharia de Dados - MBA USP/ESALQ
-- Objetivo: Estruturar o modelo relacional para importar dados tratados via Python
-- ========================================


-- ==========================
-- BANCO DE DADOS: Livraria
-- ==========================
-- Cria o banco de dados chamado 'livraria'
-- (Execute apenas se ainda não existir. Se já existir, pule esta linha)
CREATE DATABASE livraria;

-- Seleciona o banco de dados 'livraria' como o contexto atual
USE livraria;


-- ==========================
-- TABELA: autores
-- Cada autor será armazenado uma única vez, com ID único
-- ==========================
CREATE TABLE autores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(200)
);

SELECT * FROM autores


-- ==========================
-- TABELA: generos
-- Cada gênero literário traduzido e padronizado com ID
-- ==========================
CREATE TABLE generos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(200)
);

SELECT * FROM generos


-- ==========================
-- TABELA: livros
-- Cada linha representa um livro, relacionado a um autor e a um gênero
-- Inclui dados como idioma, ano e volume de vendas
-- ==========================
CREATE TABLE livros (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(200),
    idioma VARCHAR(100),
    ano_publicacao INT,
    vendas DECIMAL(10,2),

    -- Chave estrangeira para a tabela de autores
    autor_id INT,
    FOREIGN KEY (autor_id) REFERENCES autores(id),

    -- Chave estrangeira para a tabela de gêneros
    genero_id INT,
    FOREIGN KEY (genero_id) REFERENCES generos(id)
);

SELECT * FROM livros

-- ==========================
-- TABELA: comentarios
-- Armazena comentários associados a cada livro (nome, sobrenome e texto)
-- ==========================
CREATE TABLE comentarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Referência ao ID do livro comentado
    livro_id INT,
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    
    nome VARCHAR(100),
    sobrenome VARCHAR(100),
    comentario TEXT
);

SELECT * FROM comentarios

-- ========================================
-- CONSULTAS DE VERIFICAÇÃO DOS DADOS
-- Continuação do projeto Engenharia de Dados - MBA USP/ESALQ
-- ========================================

-- Seleciona todos os autores cadastrados
SELECT * FROM autores;

-- Seleciona todos os gêneros cadastrados
SELECT * FROM generos;

-- Seleciona todos os livros, ordenados por ID
SELECT * FROM livros ORDER BY id;

-- Seleciona todos os comentários cadastrados
SELECT * FROM comentarios;

-- Seleciona os primeiros 5.000 comentários (caso existam muitos registros)
SELECT * FROM comentarios LIMIT 5000;

