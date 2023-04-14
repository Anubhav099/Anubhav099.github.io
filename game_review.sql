-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 27, 2023 at 10:08 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `game_review`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `Ad_mail` varchar(40) NOT NULL,
  `pw` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`Ad_mail`, `pw`) VALUES
('ait.anubhav@gmail.com', 'pbkdf2:sha256:260000$cvAVVYU7I5nwgfvx$06a1c2732bde8c34a9aa9cde160c92ab853c27b1c69b8d9ec7967c838dcd3a03'),
('amanb.20.becs@acharya.ac.in', 'pbkdf2:sha256:260000$UFglJQfYzF2farDn$eddde9cd5d19cf131d750a29f93dd5515a48a4a82b443e3d44cb0a94ab154006');

-- --------------------------------------------------------

--
-- Table structure for table `game`
--

CREATE TABLE `game` (
  `GName` varchar(40) NOT NULL,
  `publisher` varchar(40) NOT NULL,
  `Rel_Date` date NOT NULL,
  `avail_plat` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `game`
--

INSERT INTO `game` (`GName`, `publisher`, `Rel_Date`, `avail_plat`) VALUES
('Assassins creed', 'Ubisoft', '2013-10-29', 'PS'),
('DMC: Devil May Cry', 'Ninja Theory', '2013-01-15', 'Windows'),
('Far Cry 3', 'Ubisoft', '2012-10-30', 'xbox'),
('GTA: Vice City', 'Rockstar Games', '2002-10-29', 'Windows'),
('Maneater', 'Saban Capital Group', '2022-03-02', 'xbox'),
('Minecraft', 'Mojang Studios', '2011-10-07', 'Android'),
('Naruto Shippuden', 'BNE Entertainment', '2014-09-11', 'xbox'),
('NFS: Most Wanted 2', 'EA Games', '2012-10-30', 'PS'),
('PUBG', 'Tencent Games', '2018-03-19', 'Android'),
('Spider-Man', 'Marvel', '2018-09-07', 'PS');

--
-- Triggers `game`
--
DELIMITER $$
CREATE TRIGGER `DELGames` BEFORE DELETE ON `game` FOR EACH ROW INSERT INTO triggered VALUES(OLD.GName,'DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `NAGames` AFTER INSERT ON `game` FOR EACH ROW INSERT INTO triggered VALUES(NEW.GName,'ADDED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `NDGames` AFTER UPDATE ON `game` FOR EACH ROW INSERT INTO triggered VALUES(NEW.GName,'UPDATED',NOW())
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `player`
--

CREATE TABLE `player` (
  `username` varchar(40) NOT NULL,
  `P_mail` varchar(40) NOT NULL,
  `pw` varchar(1000) NOT NULL,
  `Gender` char(1) NOT NULL,
  `Age` int(3) NOT NULL,
  `Preferred_Platform` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `player`
--

INSERT INTO `player` (`username`, `P_mail`, `pw`, `Gender`, `Age`, `Preferred_Platform`) VALUES
('Aman Rocker', 'aman27kumar0301@gmail.com', 'pbkdf2:sha256:260000$qLgLSHFvr7dcUKq2$2deeb7322044256ce082891aeb6db7a0216337f1376c1a838a8abafc8a5e1b91', 'M', 20, 'PS'),
('Cosmic', 'cosmic@gmail.com', 'pbkdf2:sha256:260000$G7DJAzMYW9DjgnXt$93d9326dda6f1f56a3fe02c6c658199d786b2df688527490097d2f110c05fb3e', 'F', 26, 'Android'),
('Homie', 'smartytekriwal@gmail.com', 'pbkdf2:sha256:260000$w5npJdY5fVtLwAvt$d6d104d85440070d3de2f0e24d23763f9577cb98763323205f9eee27cd48889a', 'M', 21, 'Windows'),
('test', 'some@gmail.com', 'pbkdf2:sha256:260000$bU87k8g4IvM15Ku3$275a5fad17e6b051fc4ee9a8f0ee8d1473013199b54df38cfc707a0162eab056', 'M', 26, 'xbox');

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `Hours_Played` int(5) NOT NULL,
  `Body` varchar(800) NOT NULL,
  `RID` int(11) NOT NULL,
  `GName` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`Hours_Played`, `Body`, `RID`, `GName`) VALUES
(12, 'Powerful action', 7, 'DMC: Devil May Cry'),
(25, 'Must play!', 7, 'Far Cry 3'),
(42, 'All time favorite', 7, 'GTA: Vice City'),
(26, 'Beautiful as well as thrilling game. Wonderful memories', 7, 'Minecraft'),
(55, 'Thrilling, Fast Paced', 7, 'NFS: Most Wanted 2'),
(86, 'GOAT.', 7, 'PUBG');

-- --------------------------------------------------------

--
-- Table structure for table `reviewer`
--

CREATE TABLE `reviewer` (
  `RID` int(11) NOT NULL,
  `R_mail` varchar(40) NOT NULL,
  `pw` varchar(1000) NOT NULL,
  `RName` varchar(40) NOT NULL,
  `Gender` char(1) NOT NULL,
  `Age` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reviewer`
--

INSERT INTO `reviewer` (`RID`, `R_mail`, `pw`, `RName`, `Gender`, `Age`) VALUES
(7, 'nmathur@gmail.com', 'pbkdf2:sha256:260000$ScnhnWpIzEt9KDqb$51c7d911b3b2fc39b424262de20c41c011a7d137f12186a6a0d210a7b3d623a2', 'Naman Mathur', 'M', 25),
(8, 'bbs@gmail.com', 'pbkdf2:sha256:260000$LOUoshKtcxKgFPVS$c1d51e6d1a48b4f7937ad1d12df1b2970503fc983a5e52c162c38a17c47a9aca', 'BeastBoyShub', 'M', 29),
(9, 'siaman@gmail.com', 'pbkdf2:sha256:260000$f0QPdFQJ39neLJGY$b82e68ce7d469e22c8031d17949448adbc68b855d582acb4199e560076d54d84', 'Saiman Says', 'M', 34),
(10, 'payal@gmail.com', 'pbkdf2:sha256:260000$KupGsyZ4mGdZi6pc$7574519620eab5c9504207804a9e478b590a08bcd71fe5c9ddf0d5889c4e9b80', 'Payal Gaming', 'F', 22),
(11, 'pdp@gmail.com', 'pbkdf2:sha256:260000$OT5wHeOODdU7MAqt$122c289a95fd85d0222304c6414b3b559a46762ef5d1e452b38c9b7aed52e4da', 'PewDiePie', 'M', 46);

-- --------------------------------------------------------

--
-- Table structure for table `triggered`
--

CREATE TABLE `triggered` (
  `GName` varchar(40) NOT NULL,
  `operation` text NOT NULL,
  `Time` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `triggered`
--

INSERT INTO `triggered` (`GName`, `operation`, `Time`) VALUES
('PUBG', 'ADDED', '2023-01-27 23:34:16'),
('PUBG', 'DELETE', '2023-01-27 23:34:24'),
('PUBG', 'ADDED', '2023-01-27 23:35:44'),
('PUBG', 'UPDATED', '2023-01-27 23:36:23'),
('PUBG', 'DELETED', '2023-01-27 23:36:34'),
('PUBG', 'ADDED', '2023-01-28 01:22:55'),
('Minecraft', 'ADDED', '2023-01-28 01:51:32'),
('Spider-Man', 'ADDED', '2023-01-28 01:55:03'),
('Maneater', 'ADDED', '2023-01-28 01:55:59'),
('Naruto Shippuden', 'ADDED', '2023-01-28 01:57:57'),
('Assassins creed', 'ADDED', '2023-01-28 01:59:14');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Ad_mail`);

--
-- Indexes for table `game`
--
ALTER TABLE `game`
  ADD PRIMARY KEY (`GName`);

--
-- Indexes for table `player`
--
ALTER TABLE `player`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `P_mail` (`P_mail`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`RID`,`GName`),
  ADD KEY `GName` (`GName`);

--
-- Indexes for table `reviewer`
--
ALTER TABLE `reviewer`
  ADD PRIMARY KEY (`RID`),
  ADD UNIQUE KEY `R_mail` (`R_mail`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `reviewer`
--
ALTER TABLE `reviewer`
  MODIFY `RID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`RID`) REFERENCES `reviewer` (`RID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`GName`) REFERENCES `game` (`GName`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
