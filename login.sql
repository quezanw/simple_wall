-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema loginDB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema loginDB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `loginDB` DEFAULT CHARACTER SET latin1 ;
USE `loginDB` ;

-- -----------------------------------------------------
-- Table `loginDB`.`friendships`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loginDB`.`friendships` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `friend_1_id` INT(11) NULL DEFAULT NULL,
  `friend_2_id` INT(11) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `loginDB`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loginDB`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NULL DEFAULT NULL,
  `user2_id` INT(11) NULL DEFAULT NULL,
  `content` TEXT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 19
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `loginDB`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loginDB`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NULL DEFAULT NULL,
  `last_name` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `password_hash` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
