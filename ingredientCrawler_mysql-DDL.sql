-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema recipe
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema recipe
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `recipe` DEFAULT CHARACTER SET utf8 ;
USE `recipe` ;

-- -----------------------------------------------------
-- Table `recipe`.`ingredient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recipe`.`ingredient` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `imageURL` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  INDEX `nameIndex` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recipe`.`food`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recipe`.`food` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `mainItem` INT NOT NULL,
  `subItem` INT NOT NULL,
  `kind` VARCHAR(45) NOT NULL,
  `recipeURL` VARCHAR(200) NOT NULL,
  INDEX `fk_food_ingredient1_idx` (`subItem` ASC),
  PRIMARY KEY (`id`),
  CONSTRAINT `mainID`
    FOREIGN KEY (`mainItem`)
    REFERENCES `recipe`.`ingredient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `subID`
    FOREIGN KEY (`subItem`)
    REFERENCES `recipe`.`ingredient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
