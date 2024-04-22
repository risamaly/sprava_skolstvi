CREATE DATABASE  IF NOT EXISTS `sprava_skolstvi_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sprava_skolstvi_database`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: sprava_skolstvi_database
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `class_name` varchar(30) DEFAULT NULL,
  `user_sid` int DEFAULT NULL,
  PRIMARY KEY (`class_id`),
  KEY `user_sid` (`user_sid`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`user_sid`) REFERENCES `employees` (`user_sid`)
) ENGINE=InnoDB AUTO_INCREMENT=2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'C4c',75315);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `user_sid` int NOT NULL AUTO_INCREMENT,
  `user_password` varchar(255) DEFAULT NULL,
  `user_profile_pic` varchar(255) DEFAULT NULL,
  `first_name` varchar(40) DEFAULT NULL,
  `last_name` varchar(40) DEFAULT NULL,
  `title_before_name` varchar(20) DEFAULT NULL,
  `title_after_name` varchar(20) DEFAULT NULL,
  `bcn` varchar(255) DEFAULT NULL,
  `user_email` varchar(50) DEFAULT NULL,
  `user_phone_number` varchar(30) DEFAULT NULL,
  `user_adress` varchar(255) DEFAULT NULL,
  `user_role` enum('Ředitel/ka','Zástupce ředitele','Učitel/ka','Admin') DEFAULT NULL,
  `user_school_email` varchar(50) DEFAULT NULL,
  `user_school_phone_number` varchar(30) DEFAULT NULL,
  `school_id` int DEFAULT NULL,
  PRIMARY KEY (`user_sid`),
  KEY `school_id` (`school_id`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `school` (`school_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100002;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (11111,'scrypt:32768:8:1$JhO1844cAH4uqQGI$9642160f5c952a8f02b0060a49c16051a2e9ccdf86513cee1dc74db77419a06e0ebdf21f5cf7719aa1939c6e05aec96e1af022ddc017ecde35f9c917799e1563',NULL,'Ondra','NEky',NULL,NULL,'1111111111','aho@gmail.com',NULL,NULL,'Ředitel/ka',NULL,NULL,1),(11588,'scrypt:32768:8:1$bQ4BqRMNxJ9QW7cj$ec82205168dfb91debb045cc1a1bbe8c5848c5dd3d75e61224213b93db8a3628ccd2feeaaf59c4dd833316b0c021994af3f5f24ed896727c8afcc76bacb69290',NULL,'Petra','Mala',NULL,NULL,'8155112790','petka.ma@seznam.cz',NULL,NULL,'Zástupce ředitele',NULL,NULL,2),(12321,'scrypt:32768:8:1$qcI60LBEdE8XGaQR$d7f415de3d38843abad1630f4036590ae1a2e3c636dd5feb9c67fe5433ba830b30df268b84b9d94e0d558a8b6e4e87d1347bcb325410f8424b975955aeeb23be',NULL,'Richard','Malý',NULL,NULL,'1234567894','uh@gmail.com',NULL,NULL,'Ředitel/ka',NULL,NULL,1),(12322,'scrypt:32768:8:1$0D6peUXfZfzDZgN9$78bccfd60ee532a7303ded2db93a476d194000bf6a0fc5f3bc3b9bd10e1a90dfd2786485fe7c093ee85e2d8874bd54fb5a9e2e51fb2a72346d98023f570595be',NULL,'Hovado','Jan',NULL,NULL,'6757676876','jan@gmail.com',NULL,NULL,'Zástupce ředitele',NULL,NULL,1),(12345,'scrypt:32768:8:1$zE6SgHNDxQs3QMmt$e777b199dd86c6010a8381e380c8a5a025493b65e39b36d3aca70c364f5696cdf5eee5fa7ecbdfa505db72fc67865d4d6743bea9b09cc6fd9f2d4aa4612e342d',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Admin',NULL,NULL,1),(12567,'scrypt:32768:8:1$AtqPojFrwjIQFYeZ$9911c51cd48e05e6004273a893610e63c1887bed589335344395244973e1ec67b1f4d85c56626138cced3e596518444784c8ea155482f9efbd1abcdeda949c81',NULL,'Richard','Malý',NULL,NULL,'1234567898','ricd.maly2005@gmail.com',NULL,NULL,'Ředitel/ka',NULL,NULL,1),(13421,'scrypt:32768:8:1$xXazfpmEvi288NB4$cb8f0fbc8a191d9f171e6c9692c0568147099aa98a54dc71f31281417f7dceff55bd050c19c9b820c155377e003015227744703803b53e8b5c78022fc38c2c82',NULL,'Honza','Vylita',NULL,NULL,'1234554321','honza@gmail.com',NULL,NULL,'Zástupce ředitele',NULL,NULL,1),(15426,'scrypt:32768:8:1$3iVx7oDXqQShzReb$4e5bcf4991001878e4a695beeefef5dc196c00e2ae90ca4f2bfa72a39f91a13e0d6253000bc8ed350e1fecf7af79a0b11aea2c08dfb920e53225cd5b69b2b957',NULL,'ADAM','Bor',NULL,NULL,'4854256325','adam@gmail.com',NULL,NULL,'Zástupce ředitele',NULL,NULL,1),(17654,'scrypt:32768:8:1$6sZkO7d35M6wVwTB$de7a986f554a430e1b958c77f325b6019fb43baef881a67fd3ea946539cde8d903a5a03c1799e7906038ec714a2beb80adbc93c1f5c646b8f83d64ce700abe8c',NULL,'Richard','Malý',NULL,NULL,'1234567891','risa@gmail.com',NULL,NULL,'Učitel/ka',NULL,NULL,1),(45625,'scrypt:32768:8:1$KsoxkhEDJBIeefi8$e5a04ccd125edabb8fc0423ae97359ecb84238cb7764d025ebcdf56d423c327f7ca3741bb89b77d67010b3cc45be9cf4617b6d93b6eb728f42a218ce488430fd',NULL,'Pavel','Kubelka',NULL,NULL,'7531542689','kube@gmail.com',NULL,NULL,'Učitel/ka',NULL,NULL,1),(75315,'scrypt:32768:8:1$tN3aVndIinadLfPi$b12457914efc6b1286cc9c966c0c4503f52ffa414fcc1d627c61e4f5c460b3fb44335c2ed1267a6e0725a23234ad4b23b348d1ccc55c07661af55b787b5c7bcb',NULL,'Blanka','Novotná','','','1234567896','novotna@gmail.com','1548523456','milovice benatecka vrutice 190','Učitel/ka','skolni@gmail.com','4587451245',1),(94621,'scrypt:32768:8:1$5SM14TEW3bUT0X9c$cf68ec2b93008f7a5da535e562b7925c4ef747e15dec8ef0338fd093b79cba8a92466989b6a0063b9d078021b44b1011fbd4b8083a89d5dd4f11bb4f558df76d',NULL,'ahoj','more',NULL,NULL,'9867543786','g@gmail.com',NULL,NULL,'Zástupce ředitele',NULL,NULL,1),(98750,'scrypt:32768:8:1$iIJVDtuktsWGgHwA$e3516805c06e7267c8a0d001818be7f791a83ce428145351a3b079e5e47fead78b4d476209784ff6512107ae03acbd1ef4f51d03713f4c51c71521ba11cec1fe',NULL,'Richard','Malý','Mgr.','DiS.','1234567890','richard.maly2005@gmail.com','123456789','Ahoj','Ředitel/ka','a@gmail.com','123456789',2),(99999,'scrypt:32768:8:1$pzld6MeJE6GhB8cf$dfc9f1f6258a6630ccdc9b2d6b1e49ea752cfc62bb2277b09619a70af45707a65b6c572f5f7795d111e6a7a88ca6636174fd12a05c45ab0acc6b592b44044c6f',NULL,'karel','parek',NULL,NULL,'9999999999','karel@gmail.com',NULL,NULL,'Zástupce ředitele',NULL,NULL,1),(100001,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school`
--

DROP TABLE IF EXISTS `school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `school` (
  `school_id` int NOT NULL AUTO_INCREMENT,
  `school_name` varchar(255) DEFAULT NULL,
  `school_type` enum('Mateřská škola','Základní škola','Střední škola','Vysoká škola') DEFAULT NULL,
  `school_adress` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`school_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school`
--

LOCK TABLES `school` WRITE;
/*!40000 ALTER TABLE `school` DISABLE KEYS */;
INSERT INTO `school` VALUES (1,'SPSE Jecna','Střední škola','Praha 30, Jecna'),(2,'SPSE Jecna','Střední škola','Praha 30, Jecna');
/*!40000 ALTER TABLE `school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `user_profile_pic` varchar(255) DEFAULT NULL,
  `first_name` varchar(40) DEFAULT NULL,
  `last_name` varchar(40) DEFAULT NULL,
  `bcn` int DEFAULT NULL,
  `student_email` varchar(50) DEFAULT NULL,
  `student_phone_number` varchar(30) DEFAULT NULL,
  `student_adress` varchar(255) DEFAULT NULL,
  `parent_email` varchar(50) DEFAULT NULL,
  `parent_phone_number` varchar(30) DEFAULT NULL,
  `parent_adress` varchar(255) DEFAULT NULL,
  `class_id` int DEFAULT NULL,
  `school_id` int DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  KEY `class_id` (`class_id`),
  KEY `school_id` (`school_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`),
  CONSTRAINT `students_ibfk_2` FOREIGN KEY (`school_id`) REFERENCES `school` (`school_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'student_pic.jpg','Jan','Novák',123456789,'jan.novak@email.cz','123 456 789','Adresova 1, Mesto','rodic.email@email.cz','987 654 321','Rodiova 2, Mesto',1,1),(2,'student1_pic.jpg','Petr','Svoboda',234567890,'petr.svoboda@email.cz','234 567 890','Ulicova 2, Mesto','rodic1.email@email.cz','876 543 210','Rodiova 3, Mesto',1,1),(3,'student2_pic.jpg','Lucie','Nová',345678901,'lucie.nova@email.cz','345 678 901','Ulicova 3, Mesto','rodic2.email@email.cz','765 432 109','Rodiova 4, Mesto',1,1),(4,'student3_pic.jpg','Tomáš','Krátký',456789012,'tomas.kratky@email.cz','456 789 012','Ulicova 4, Mesto','rodic3.email@email.cz','654 321 098','Rodiova 5, Mesto',1,1),(5,'student4_pic.jpg','Anna','Dlouhá',567890123,'anna.dlouha@email.cz','567 890 123','Ulicova 5, Mesto','rodic4.email@email.cz','543 210 987','Rodiova 6, Mesto',1,1),(6,'student5_pic.jpg','David','Procházka',678901234,'david.prochazka@email.cz','678 901 234','Ulicova 6, Mesto','rodic5.email@email.cz','432 109 876','Rodiova 7, Mesto',1,1),(7,'student1_pic.jpg','Petr','Svoboda',234567890,'petr.svoboda@email.cz','234 567 890','Ulicova 2, Mesto','rodic1.email@email.cz','876 543 210','Rodiova 3, Mesto',1,1),(8,'student2_pic.jpg','Lucie','Nová',345678901,'lucie.nova@email.cz','345 678 901','Ulicova 3, Mesto','rodic2.email@email.cz','765 432 109','Rodiova 4, Mesto',1,1),(9,'student3_pic.jpg','Tomáš','Krátký',456789012,'tomas.kratky@email.cz','456 789 012','Ulicova 4, Mesto','rodic3.email@email.cz','654 321 098','Rodiova 5, Mesto',1,1),(10,'student4_pic.jpg','Anna','Dlouhá',567890123,'anna.dlouha@email.cz','567 890 123','Ulicova 5, Mesto','rodic4.email@email.cz','543 210 987','Rodiova 6, Mesto',1,1),(11,'student5_pic.jpg','David','Procházka',678901234,'david.prochazka@email.cz','678 901 234','Ulicova 6, Mesto','rodic5.email@email.cz','432 109 876','Rodiova 7, Mesto',1,1),(12,'student1_pic.jpg','Petr','Svoboda',234567890,'petr.svoboda@email.cz','234 567 890','Ulicova 2, Mesto','rodic1.email@email.cz','876 543 210','Rodiova 3, Mesto',1,1),(13,'student2_pic.jpg','Lucie','Nová',345678901,'lucie.nova@email.cz','345 678 901','Ulicova 3, Mesto','rodic2.email@email.cz','765 432 109','Rodiova 4, Mesto',1,1),(14,'student3_pic.jpg','Tomáš','Krátký',456789012,'tomas.kratky@email.cz','456 789 012','Ulicova 4, Mesto','rodic3.email@email.cz','654 321 098','Rodiova 5, Mesto',1,1),(15,'student4_pic.jpg','Anna','Dlouhá',567890123,'anna.dlouha@email.cz','567 890 123','Ulicova 5, Mesto','rodic4.email@email.cz','543 210 987','Rodiova 6, Mesto',1,1),(16,'student5_pic.jpg','David','Procházka',678901234,'david.prochazka@email.cz','678 901 234','Ulicova 6, Mesto','rodic5.email@email.cz','432 109 876','Rodiova 7, Mesto',1,1);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-21 20:10:32
