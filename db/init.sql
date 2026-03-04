-- Script de inicialización de la base de datos
-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS reflexo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE reflexo;

-- Crear usuario para Django si no existe
CREATE USER IF NOT EXISTS 'django'@'%' IDENTIFIED BY 'django123';
GRANT ALL PRIVILEGES ON reflexo.* TO 'django'@'%';

-- Crear usuario para la aplicación web si no existe
CREATE USER IF NOT EXISTS 'web'@'%' IDENTIFIED BY 'web123';
GRANT SELECT, INSERT, UPDATE, DELETE ON reflexo.* TO 'web'@'%';

-- Aplicar privilegios
FLUSH PRIVILEGES;

-- Configurar el modo SQL para compatibilidad con Django
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';

-- Configurar timezone
SET GLOBAL time_zone = '+00:00';
SET SESSION time_zone = '+00:00';
