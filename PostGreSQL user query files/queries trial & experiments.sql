SELECT * FROM tweets;
SELECT username, tweet_content FROM tweets;
SELECT tweet_content AS tweet FROM tweets;
SELECT * FROM tweets WHERE id = 9;
SELECT * FROM tweets WHERE username = 'Scholar';
SELECT * FROM tweets WHERE id <=5;
SELECT * FROM tweets WHERE id <=5 AND username = 'Scholar';
SELECT * FROM tweets WHERE id <=5 AND username = 'Scholar';
SELECT * FROM tweets WHERE username IN ('Scholar','AvDude');
SELECT * FROM tweets WHERE tweet_content LIKE '%are%';
SELECT * FROM tweets WHERE tweet_content LIKE 'Hello%';
SELECT * FROM tweets WHERE tweet_content NOT LIKE 'Hell%';
SELECT * FROM tweets ORDER BY timestamp;
SELECT * FROM tweets ORDER BY timestamp DESC;
SELECT * FROM tweets ORDER BY username, id DESC;
SELECT * FROM tweets WHERE id <=5 ORDER BY username ;
SELECT * FROM tweets ORDER BY id DESC LIMIT 3;
SELECT * FROM tweets ORDER BY id DESC LIMIT 3 OFFSET 2;

INSERT INTO tweets (username, tweet_content, device) VALUES ('AvDude', 'Apna time ayega', 'BAJA machine');
INSERT INTO tweets (username, tweet_content, device) VALUES ('AvDude', 'Apna time jayega', 'BAJA machine') RETURNING *;
INSERT INTO tweets (username, tweet_content, device) VALUES ('AvDude', 'Apna time ata jayega', 'BAJA machine') RETURNING id;
INSERT INTO tweets (username, tweet_content, device) VALUES ('Philomath', 'Test1', 'Aurora'), ('Philomath', 'Test2', 'Aurora') RETURNING id, tweet_content;

DELETE FROM tweets WHERE tweet_content LIKE 'Apna%' AND id != 11;
DELETE FROM tweets WHERE tweet_content LIKE 'Test%' RETURNING *;
SELECT * FROM tweets;

UPDATE tweets SET device = 'Soumitra''s Windows Laptop' WHERE device != 'Soumitra''s Windows Laptop' RETURNING *;



