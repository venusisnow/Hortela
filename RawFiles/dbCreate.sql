CREATE DATABASE dbHort;
use dbHort;

CREATE TABLE hortas (
  horta_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  endereço varchar(50)
);

CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  
  nome varchar(50) not null,
  email varchar(50) not null,
  pass varchar(25) not null,
  
  telefone varchar(12),
  endereco varchar(50),
  
  access int(1) NOT NULL, /*1-Cliente, 2-FuncTerra, 3-ADM*/
  
  horta_id INTEGER,
  FOREIGN KEY (horta_id) REFERENCES hortas(horta_id)
);

CREATE TABLE agendas (
  agenda_id INTEGER PRIMARY KEY NOT NULL,
  data date(10) NOT null,
  conteudo varchar(200) NOT null,
  
  user_id int(5),
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE recibos (
  pag_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  type int(1) NOT null, /*1-Semente, 2-Fruto, 3-Cerejeira*/
  valor varchar(6) Not null, /*999,99*/
  expire date(10) NOT null,
  
  paym_Type varchar(3) Not null,
  paym_Status int(2) Not null, /* 1-Paid, 2-NotPaid */

  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

/* Admin login standar */
INSERT INTO user (user_id, nome, email, pass, access)
VALUES (1, 'root', 'admin@adm.com', 'mikemike', 3);

DELETE FROM user WHERE nome = 'root';
SELECT * FROM user WHERE nome = 'root' AND pass = 'mikemike';
