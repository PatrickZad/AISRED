drop database if exists GWT2RUCM;
create database GWT2RUCM;
use GWT2RUCM;
CREATE TABLE IF NOT EXISTS GWT_tb(
   id INT UNSIGNED AUTO_INCREMENT,
   scenario text NOT NULL,
   useCaseName tinytext null,
   flowType tinytext null,
   PRIMARY KEY (id)
)engine=innodb DEFAULT CHARSET=UTF8MB4;

create table if not exists Sentence(
	id int unsigned auto_increment,
    Stype tinytext null,
    secondType tinytext null,
    content text not null,
    sequence tinyint unsigned,
    primary key (id)
)engine=innodb default charset = utf8mb4;

create table if not exists SentenceSentence(
	s1 int unsigned not null,
    s2 int unsigned not null,
    connectType tinytext not null
)engine=innodb default charset = utf8mb4;

create table if not exists gwtSentence(
	gwt_id int unsigned not null,
    sentence_id int unsigned not null,
    position_in_gwt tinytext not null
)engine=innodb default charset = utf8mb4;

--外键还没有进行配置，或许也可以不用进行配置，但是在操作数据库的时候需要小心