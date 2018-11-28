create database GWT2RUCM;
show variables like '%char%';
use GWT2RUCM;
CREATE TABLE IF NOT EXISTS GWT_tb(
   id INT UNSIGNED AUTO_INCREMENT,
   scenario text NOT NULL,
   useCaseName tinytext null,
   flowType tinytext null,
   PRIMARY KEY (id)
)DEFAULT CHARSET=UTF8MB4;

create table if not exists Sentence(
	id int unsigned auto_increment,
    Stype tinytext null,
    secondType tinytext null,
    content text not null,
    sequence tinyint unsigned,
    primary key (id)
)default charset = utf8mb4;

create table if not exists SentenceSentence(
	s1 int unsigned not null,
    s2 int unsigned not null,
    connectType tinytext not null
)default charset = utf8mb4;

create table if not exists gwtSentence(
	gwt_id int unsigned not null,
    sentence_id int unsigned not null,
    position_in_gwt tinytext not null
)default charset = utf8mb4;