CREATE DATABASE dbHort;
use dbHort;

CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  
  nome varchar(50) not null,
  email varchar(100) not null,
  endereco varchar(100),
  cpf int(11),
  telefone varchar(12),
  
  pass varchar(25) not null,
  access int(1) NOT NULL
)

CREATE TABLE voluntario (
  vol_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  
  dataDisp date(10) NOT null,
  tipo varchar(50) NOT null,
  
  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user(user_id)
)

CREATE TABLE calendarioVol (
  calendVol_id INTEGER PRIMARY KEY NOT NULL,
  
  data date(10) NOT null,
  tipo varchar(50) NOT null,
  quantidade int(100) NOT null
)

CREATE TABLE horta (
  horta_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  endereço varchar(255) NOT null
)

CREATE TABLE cesta (
  cesta_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  
  alimentos varchar(200) Not null,
  status varchar(10) Not null,

  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user(user_id)
)

CREATE TABLE calendarioDist (
  dist_id INTEGER PRIMARY KEY NOT NULL,
  
  local varchar(100) NOT null,
  data date(10) NOT null,
  alimento varchar(200) NOT null
)

INSERT INTO user (nome, email, cpf, pass, access)
VALUES ('Root', 'admin@adm.com', '12345678901', 'mypass', 3);