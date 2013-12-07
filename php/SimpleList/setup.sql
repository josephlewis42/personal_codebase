-- Creates the tables and such for the database.

-- DROP TABLE Resets;
-- DROP TABLE Photos;
-- DROP TABLE Validations;
-- DROP TABLE Articles;
-- DROP TABLE Categories;
-- DROP TRIGGER user_input;
-- DROP TRIGGER user_update;
-- DROP FUNCTION CHECK_USER;
-- DROP TABLE Users;

-- Users is a table, password hash, up to 100 chars, currently used is
-- sha1 because it is nativly supported in PHP.
CREATE TABLE `Users` (
	`usr_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	`username` VARCHAR(200) NOT NULL, 
	`usr_password` VARCHAR(100) NOT NULL,
	`is_admin` BOOL DEFAULT FALSE,
	`is_validated` BOOL DEFAULT FALSE
) ENGINE = INNODB;

-- Yes, secure things as they are added, using the username as a salt.  
-- CREATE TRIGGER user_input BEFORE INSERT ON `Users` FOR EACH ROW SET NEW.usr_password = SHA1(CONCAT(NEW.usr_password, NEW.username));
-- CREATE TRIGGER user_update BEFORE UPDATE ON `Users` FOR EACH ROW SET NEW.usr_password = SHA1(CONCAT(NEW.usr_password, NEW.username));

-- Checks if a user with the given username and password exists in the 
-- db, returns null if no and the ID if true.
-- delimiter |
-- CREATE FUNCTION CHECK_USER (usrname VARCHAR(200), password VARCHAR(1000))
-- 	RETURNS INT DETERMINISTIC
-- 	BEGIN
-- 	 DECLARE tmp INT;
-- 	 SELECT usr_id INTO tmp FROM Users WHERE username = usrname AND usr_password = SHA1(CONCAT(password,usrname));
-- 	RETURN tmp;
-- 	END|
-- delimiter ;

CREATE TABLE Categories (
	cat_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	cat_title VARCHAR(100) NOT NULL,
	cat_subtitle VARCHAR(100)
) ENGINE = INNODB;


CREATE TABLE Articles (
	article_id INT NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY(article_id),
	title VARCHAR(100) NOT NULL,
	text VARCHAR(1000) NOT NULL,
	contact_text VARCHAR(500),
	author INT NOT NULL,
	category INT NOT NULL,
	begin_time TIMESTAMP default CURRENT_TIMESTAMP,
	FOREIGN KEY (author) REFERENCES Users(usr_id)
	   ON DELETE CASCADE
	   ON UPDATE CASCADE,
	FOREIGN KEY (category) REFERENCES Categories(cat_id)
	   ON DELETE CASCADE
	   ON UPDATE CASCADE
) ENGINE = INNODB;


-- A table for all of the users who haven't validated yet through email.
CREATE TABLE `Validations` (
	`val_usr` INT NOT NULL,
	`val_time` TIMESTAMP default CURRENT_TIMESTAMP,
	`val_id` VARCHAR(20) not null PRIMARY KEY,
	FOREIGN KEY (val_usr) REFERENCES Users(usr_id)
	   ON DELETE CASCADE
) ENGINE = INNODB;

-- A table of photos, extension is a 3 char extension, data is a 1mb blob
-- this won't store huge photos.
-- CREATE TABLE `Photos` (
-- 	`ph_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
-- 	`ph_ext` char(3) NOT NULL,
-- 	`ph_data` BLOB(1048576) NOT NULL,
-- 	`ph_article` INT NOT NULL,
-- 	FOREIGN KEY (ph_article) REFERENCES Articles(article_id)
-- 	   ON DELETE CASCADE
-- ) ENGINE = INNODB;

-- A table for the users awaiting password resets.
CREATE TABLE `Resets` (
	`val_usr` INT NOT NULL,
	`val_time` TIMESTAMP default CURRENT_TIMESTAMP,
	`val_id` VARCHAR(20) not null PRIMARY KEY,
	FOREIGN KEY (val_usr) REFERENCES Users(usr_id)
	   ON DELETE CASCADE
) ENGINE = INNODB;
