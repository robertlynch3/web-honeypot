CREATE DATABASE IF NOT EXISTS `honeypot`;

USE honeypot;
CREATE TABLE IF NOT EXISTS `addresses`(
    `ipAddress` varchar(15) NOT NULL,
    PRIMARY KEY (`ipAddress`),
    UNIQUE KEY `ipAddress` (`ipAddress`)
);
CREATE TABLE IF NOT EXISTS `login_attempts`(
    `attemptID` int AUTO_INCREMENT,
    `ipAddress` varchar(15) NOT NULL,
    `username` tinytext,
    `password` tinytext,
    `host` tinytext,
    `useragent` mediumtext,
    `date` int NOT NULL,
    PRIMARY KEY (`attemptID`),
    CONSTRAINT `la_ip_ibfk` FOREIGN KEY (`ipAddress`) REFERENCES `addresses` (`ipAddress`) 
);
CREATE TABLE IF NOT EXISTS `loads`(
    `loadID` int AUTO_INCREMENT,
    `ipAddress` varchar(15) NOT NULL,
    `host` tinytext,
    `useragent` mediumtext,
    `location` tinytext,
    `date` int NOT NULL,
    PRIMARY KEY (`loadID`),
    CONSTRAINT `l_ip_ibfk` FOREIGN KEY (`ipAddress`) REFERENCES `addresses` (`ipAddress`) 
);