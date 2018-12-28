-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        10.3.11-MariaDB - mariadb.org binary distribution
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 ap 的数据库结构
CREATE DATABASE IF NOT EXISTS `ap` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `ap`;

-- 导出  表 ap.colleges 结构
CREATE TABLE IF NOT EXISTS `colleges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `times` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- 正在导出表  ap.colleges 的数据：~21 rows (大约)
DELETE FROM `colleges`;
/*!40000 ALTER TABLE `colleges` DISABLE KEYS */;
INSERT INTO `colleges` (`id`, `name`, `times`) VALUES
	(1, '法学院', 0),
	(2, '文传学院', 0),
	(3, '美术学院', 0),
	(4, '民社学院', 0),
	(5, '外语学院', 0),
	(6, '经济学院', 0),
	(7, '管理学院', 0),
	(8, '公管学院', 0),
	(9, '教育学院', 0),
	(10, '马克思学院', 0),
	(11, '计科学院', 0),
	(12, '数统学院', 0),
	(13, '电信学院', 0),
	(14, '生医学院', 0),
	(15, '化材学院', 0),
	(16, '资环学院', 0),
	(17, '生科学院', 0),
	(18, '药学院', 0),
	(19, '预科学院', 0),
	(20, '体育学院', 0),
	(21, '音舞学院', 0);
/*!40000 ALTER TABLE `colleges` ENABLE KEYS */;

-- 导出  表 ap.users 结构
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong_college` int(11) DEFAULT NULL,
  `Sno` varchar(12) DEFAULT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  KEY `belong_college` (`belong_college`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`belong_college`) REFERENCES `colleges` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- 正在导出表  ap.users 的数据：~0 rows (大约)
DELETE FROM `users`;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
