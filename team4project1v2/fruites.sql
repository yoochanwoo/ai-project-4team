--테이블 생성
CREATE TABLE fruits(
	name varchar(20) NOT NULL,
	cnt INT 
);

drop TABLE fruits;

--등록, 조회 id,name

INSERT INTO fruits (name, cnt) VALUES ('귤', 0);
INSERT INTO fruits (name, cnt) VALUES ('수박', 0);
INSERT INTO fruits (name, cnt) VALUES ('애플망고', 0);
INSERT INTO fruits (name, cnt) VALUES ('무화과', 0);
INSERT INTO fruits (name, cnt) VALUES ('용과', 0);


SELECT * FROM fruits;

UPDATE fruits SET cnt = cnt +1  WHERE name = '사과';

-- 사과,포도,딸기,복숭아, 바나나,귤, 수박,애플망고,무화과,용과 리스트
-- SELECT name, COUNT() FROM fruits f ;

SELECT name,cnt,(cnt / (SELECT SUM(cnt) FROM fruits)) * 100 AS ratio
FROM fruits;
