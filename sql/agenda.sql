-- Active: 1770140831214@@127.0.0.1@3306@agenda
CREATE DATABASE agenda;

USE agenda;

CREATE TABLE contatos(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone CHAR(10) UNIQUE
);

SELECT id, nome, email, telefone FROM contatos;

DROP DATABASE agenda;

USE agenda;
SELECT * FROM contatos