CREATE TABLE `asthmaFactors` (
  `name` VARCHAR(15) NOT NULL,
  `january1` TINYINT NOT NULL,
  `january2` TINYINT NOT NULL,
  `january3` TINYINT NOT NULL,
  `february1` TINYINT NOT NULL,
  `february2` TINYINT NOT NULL,
  `february3` TINYINT NOT NULL,
  `march1` TINYINT NOT NULL,
  `march2` TINYINT NOT NULL,
  `march3` TINYINT NOT NULL,
  `april1` TINYINT NOT NULL,
  `april2` TINYINT NOT NULL,
  `april3` TINYINT NOT NULL,
  `may1` TINYINT NOT NULL,
  `may2` TINYINT NOT NULL,
  `may3` TINYINT NOT NULL,
  `june1` TINYINT NOT NULL,
  `june2` TINYINT NOT NULL,
  `june3` TINYINT NOT NULL,
  `july1` TINYINT NOT NULL,
  `july2` TINYINT NOT NULL,
  `july3` TINYINT NOT NULL,
  `august1` TINYINT NOT NULL,
  `august2` TINYINT NOT NULL,
  `august3` TINYINT NOT NULL,
  `september1` TINYINT NOT NULL,
  `september2` TINYINT NOT NULL,
  `september3` TINYINT NOT NULL,
  `october1` TINYINT NOT NULL,
  `october2` TINYINT NOT NULL,
  `october3` TINYINT NOT NULL,
  `november1` TINYINT NOT NULL,
  `november2` TINYINT NOT NULL,
  `november3` TINYINT NOT NULL,
  `december1` TINYINT NOT NULL,
  `december2` TINYINT NOT NULL,
  `december3` TINYINT NOT NULL,
  PRIMARY KEY (`name`)
);

CREATE TABLE `users` (
  `id_user` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50),
  `surname` VARCHAR(50),
  `sex` CHAR(1),
  `email` VARCHAR(50) NOT NULL,
  `birth` DATE,
  `height` SMALLINT,
  `weight` SMALLINT,
  `disease_start` DATE,
  `password` VARCHAR(125) NOT NULL,
  `type` SMALLINT,
  PRIMARY KEY (`id_user`)
);

CREATE TABLE `dosages` (
  `id_dosage` INT NOT NULL AUTO_INCREMENT,
  `dosage` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_dosage`)
);

CREATE TABLE `medicinesUsed` (
  `id_medicine_used` INT NOT NULL AUTO_INCREMENT,
  `id_medicine` INT NOT NULL,
  `id_user` INT NOT NULL,
  `start_date` DATE,
  `stop_date` DATE,
  PRIMARY KEY (`id_medicine_used`)
);

CREATE TABLE `controlTests` (
  `id_control_test` INT NOT NULL AUTO_INCREMENT,
  `id_user` INT NOT NULL,
  `date` DATE NOT NULL,
  `value` TINYINT NOT NULL,
  `value_medicines` TINYINT,
  PRIMARY KEY (`id_control_test`)
);

CREATE TABLE `medicines` (
  `id_medicine` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_medicine`)
);

CREATE TABLE `medicineEvents` (
  `id_medicine_event` INT NOT NULL AUTO_INCREMENT,
  `id_user` INT NOT NULL,
  `implemented` BOOLEAN NOT NULL,
  `date` DATE NOT NULL,
  `id_dosage` INT NOT NULL,
  PRIMARY KEY (`id_medicine_event`)
);

CREATE TABLE `weather` (
  `date` DATE NOT NULL,
  `temperature` FLOAT NOT NULL,
  `humidity` FLOAT NOT NULL,
  `wind` FLOAT NOT NULL,
  `rain` FLOAT NOT NULL,
  PRIMARY KEY (`date`)
);

CREATE TABLE `trends` (
  `id_trend` INT NOT NULL AUTO_INCREMENT,
  `id_user` INT NOT NULL,
  `date` DATE NOT NULL,
  `trend` VARCHAR(2) NOT NULL,
  PRIMARY KEY (`id_trend`)
);

CREATE TABLE `allergies` (
  `id_allergie` INT NOT NULL AUTO_INCREMENT,
  `id_user` INT NOT NULL,
  `name` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`id_allergie`)
);

SHOW TABLES;