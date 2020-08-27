SHOW TABLES;
SELECT * FROM users;
SELECT * FROM dosages;
SELECT * FROM medicinesUsed;
SELECT * FROM asthmaFactors;
SELECT * FROM controlTests;
SELECT * FROM allergies;
SELECT * FROM weather;

TRUNCATE TABLE users;
TRUNCATE TABLE medicinesUsed;
TRUNCATE TABLE allergies;

-- wypisuje istotne dane z bazy 
SELECT DISTINCT u.name AS name, ct.date AS date, ct.value AS W, ct.value_medicines AS WPrim, d.dosage AS dosage, w.temperature, w.wind, w.rain, t.trend AS trend FROM users u JOIN controlTests ct ON (u.id_user=ct.id_user) JOIN medicineEvents me ON (me.date=ct.date) JOIN dosages d ON (d.id_dosage=me.id_dosage) JOIN weather w ON (me.date=w.date) JOIN trends t ON (t.date=w.date) WHERE me.id_dosage=d.id_dosage AND u.id_user=t.id_user ORDER BY name, date DESC;

-- rozpisanie powyższego
SELECT DISTINCT u.name AS name, ct.date AS date, ct.value AS W, ct.value_medicines AS WPrim, d.dosage AS dosage, w.temperature, w.wind, w.rain, t.trend AS trend FROM users u JOIN controlTests ct ON (u.id_user=ct.id_user) JOIN medicineEvents me ON (me.date=ct.date) JOIN dosages d ON (d.id_dosage=me.id_dosage) JOIN weather w ON (me.date=w.date) JOIN trends t ON (t.date=w.date) WHERE me.id_dosage=d.id_dosage AND u.id_user=t.id_user ORDER BY name, date DESC;

-- dostarcza id_user dla urzytkowników bez historii
SELECT u.id_user AS id_user, ct.id_control_test FROM users u LEFT JOIN controlTests ct ON (u.id_user=ct.id_user) WHERE ct.id_control_test IS NULL;



-- SELECT wind, count(wind) FROM weather GROUP BY wind;

-- SELECT rain FROM weather WHERE rain != 0;
-- SELECT max(rain), count(rain) FROM weather WHERE rain != 0 GROUP BY rain;

-- DROP TABLE users;
-- DROP TABLE allergies;
-- DROP TABLE controlTests;

-- INSERT INTO allergies (id_user, name) VALUES (1,"a");
-- 
-- INSERT INTO medicineEvents (id_user, implemented, date) VALUES (1,TRUE,"2020-01-01");
-- INSERT INTO medicineEvents (id_user, implemented, date) VALUES (1,TRUE,"2020-01-02");
-- INSERT INTO medicineEvents (id_user, implemented, date) VALUES (1,TRUE,"2020-01-03");
-- INSERT INTO medicineEvents (id_user, implemented, date) VALUES (1,TRUE,"2020-01-04");
-- INSERT INTO medicineEvents (id_user, implemented, date) VALUES (1,TRUE,"2020-01-05");
-- INSERT INTO medicineEvents (id_user, implemented, date) VALUES (1,TRUE,"2020-01-06");

-- SELECT d.dosage AS dosage FROM medicineEvents me JOIN medicinesUsed mu ON (mu.id_user = me.id_user) JOIN dosages d ON (d.id_dosage = mu.id_dosage) WHERE mu.id_user = 1 ORDER BY me.date DESC LIMIT 5;

-- INSERT INTO controlTests (id_user, date, value, value_medicines) VALUES (1,"2020-01-06",25,25);
-- INSERT INTO controlTests (id_user, date, value, value_medicines) VALUES (1,"2020-01-07",25,25);
-- INSERT INTO controlTests (id_user, date, value, value_medicines) VALUES (1,"2020-01-08",25,25);

-- SELECT value_medicines FROM controlTests WHERE id_user=1 ORDER BY date DESC LIMIT 14;

-- DROP TABLE IF EXISTS users, dosages, medicinesUsed, controlTests, medicines, medicineEvents, trends, allergies;
-- DROP TABLE IF EXISTS medicinesUsed, medicineEvents;
-- TRUNCATE users;


