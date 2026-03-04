-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: reflexoperu-v3
-- ------------------------------------------------------
-- Server version	9.4.0

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
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `history_id` int unsigned NOT NULL,
  `patient_id` int unsigned NOT NULL,
  `therapist_id` int unsigned DEFAULT NULL,
  `appointment_date` datetime DEFAULT NULL,
  `hour` time DEFAULT NULL,
  `ailments` varchar(1000) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `diagnosis` varchar(1000) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `surgeries` varchar(1000) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `reflexology_diagnostics` varchar(1000) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `medications` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `observation` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `initial_date` date DEFAULT NULL,
  `final_date` date DEFAULT NULL,
  `appointment_type` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `room` int DEFAULT NULL,
  `social_benefit` tinyint(1) DEFAULT '1',
  `payment_type_id` int DEFAULT NULL,
  `payment_detail` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `payment_status_id` int unsigned DEFAULT NULL,
  `payment` decimal(8,2) unsigned DEFAULT NULL,
  `ticket_number` int DEFAULT NULL,
  `appointment_status` enum('COMPLETADO','PENDIENTE','ACTIVO') COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_appointments_histories` (`history_id`),
  KEY `fk_appointments_patients` (`patient_id`),
  KEY `fk_appointments_therapists` (`therapist_id`),
  KEY `fk_appointments_payment_types` (`payment_type_id`),
  KEY `fk_appointments_payment_status` (`payment_status_id`),
  CONSTRAINT `fk_appointments_histories` FOREIGN KEY (`history_id`) REFERENCES `histories` (`id`),
  CONSTRAINT `fk_appointments_patients` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  CONSTRAINT `fk_appointments_payment_status` FOREIGN KEY (`payment_status_id`) REFERENCES `payment_status` (`id`),
  CONSTRAINT `fk_appointments_payment_types` FOREIGN KEY (`payment_type_id`) REFERENCES `payment_types` (`id`),
  CONSTRAINT `fk_appointments_therapists` FOREIGN KEY (`therapist_id`) REFERENCES `therapists` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-26 14:46:04
