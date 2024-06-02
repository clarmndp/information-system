--admin
CREATE OR REPLACE USER 'foodie'@'localhost' IDENTIFIED BY 'chefP!';
GRANT ALL ON food.* TO 'foodie'@'localhost';

--casual
CREATE OR REPLACE USER 'pares'@localhost IDENTIFIED BY 'diwataP';
GRANT SELECT, INSERT, UPDATE, DELETE ON food.`food_review` TO 'pares'@'localhost';
GRANT SELECT ON food.`food_item` TO 'pares'@'localhost';
GRANT SELECT ON food.`food_establishment` TO 'pares'@'localhost';

--database creation
DROP DATABASE IF EXISTS `food`;
CREATE DATABASE IF NOT EXISTS `food`;
USE `food`;

--user table
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` INT (4) NOT NULL AUTO_INCREMENT,
    `email` VARCHAR (20) NOT NULL DEFAULT '',
    `password` VARCHAR (20) NOT NULL DEFAULT '',
    `birthday` DATE DEFAULT NULL,
    `age` INT (3),
    CONSTRAINT user_user_id_pk PRIMARY KEY (`user_id`)
); 

--initial user
INSERT INTO `user` (`email`, `password`, `birthday`, `age`) VALUES ('pares@example.com', 'diwataP', '1990-01-01', 21);

--food establishment table
DROP TABLE IF EXISTS `food_establishment`;
CREATE TABLE IF NOT EXISTS `food_establishment` (
    `establishment_id` INT(4) NOT NULL AUTO_INCREMENT,
    `location` VARCHAR(50) NOT NULL DEFAULT '',
    `rating` INT(1) DEFAULT NULL,
    `establishment_name` VARCHAR(25) NOT NULL DEFAULT '',
    CONSTRAINT food_establishment_establishment_id_pk PRIMARY KEY (`establishment_id`) 
);

--food item table
DROP TABLE IF EXISTS `food_item`;
CREATE TABLE IF NOT EXISTS `food_item` (
    `item_id` INT(4) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL DEFAULT '',
    `price` INT(4) DEFAULT NULL,
    `food_type` VARCHAR(25) NOT NULL DEFAULT '',
    `ingredient` VARCHAR(25) NOT NULL DEFAULT '',
    `establishment_id` INT(4),
    CONSTRAINT food_item_item_id_pk PRIMARY KEY (`item_id`),
    CONSTRAINT food_item_establishment_id_fk FOREIGN KEY (`establishment_id`) REFERENCES `food_establishment` (`establishment_id`) ON DELETE CASCADE
);

--food review table
DROP TABLE IF EXISTS `food_review`;
CREATE TABLE IF NOT EXISTS `food_review` (
    `review_id` INT (4) NOT NULL AUTO_INCREMENT,
    `feedback` VARCHAR (20) NOT NULL DEFAULT '',
    `date_of_review` DATE DEFAULT NULL,
    `rating` INT (1) DEFAULT NULL,
    `user_id` INT (4) DEFAULT NULL,
    `establishment_id` INT (4) DEFAULT NULL,
    `item_id` INT(4) DEFAULT NULL, 
    CONSTRAINT food_review_review_id_pk PRIMARY KEY (`review_id`),
    CONSTRAINT food_review_user_id_fk FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
    CONSTRAINT food_review_establishment_id_fk FOREIGN KEY (`establishment_id`) REFERENCES `food_establishment` (`establishment_id`) ON DELETE SET NULL,
    CONSTRAINT food_review_item_id_fk FOREIGN KEY (`item_id`) REFERENCES `food_item` (`item_id`) ON DELETE SET NULL
);

--Insert Data

INSERT INTO user (`email`, `password`, `birthday`, `age`) VALUES ( 'user@gmail.com', 'useruser', '2002-03-26', 22 );

INSERT INTO food_establishment (`location`,`rating`,`establishment_name`) VALUES 
    ( 'Los Baños', 3, 'koppi' ), 
    ( 'Los Baños', 4, 'Jollibee' ), 
    ( 'Los Baños', 4, "McDonal/'s" ), 
    ( 'Los Baños', 4, 'Dimsum'),
    ( 'Los Baños', 3, 'Minute Burger'),
    ( 'Los Baños', 4, 'WeDeliver'),
    ( 'Calamba', 5, 'Mang Inasal'),
    ( 'Calamba', 4, "Dunkin/'"), 
    ( 'Calamba', 5, "Max/'s Restaurant");


INSERT INTO food_item (`name`, `price`, `food_type`, `ingredient`, `establishment_id`) VALUES 
    ('Chicken Joy', 80, 'meat', 'chicken', 2 ),
    ('Yummy Burger', 50, 'meat', 'Cheese, beef patty, mayo', 3),
    ('Spaghetti', 55, 'pasta', 'noodles, tomato sauce', 2),
    ('Burger Steak', 70, 'meat', 'beef patty, gravy', 2),
    ('Chicken Sandwich', 45, 'sandwich', 'chicken, bread', 4),
    ('Halo-Halo', 90, 'dessert', 'ice, milk, sweets', 5),
    ('Pancit Canton', 60, 'noodles', 'noodles, vegetables', 6),
    ('Hotdog Sandwich', 40, 'sandwich', 'hotdog, bread', 7),
    ('Cheesy Fries', 35, 'snack', 'fries, cheese', 8),
    ('Chicken Nuggets', 65, 'snack', 'chicken', 9);
    
INSERT INTO food_review (`feedback`, `date_of_review`, `rating`, `user_id`, `establishment_id`, `item_id`) VALUES 
    ('amazing','2024-04-29', 5, 1, 2, 1);