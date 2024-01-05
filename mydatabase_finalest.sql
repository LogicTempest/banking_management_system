-- MySQL dump 10.13  Distrib 8.1.0, for macos13.3 (arm64)
--
-- Host: localhost    Database: banking_management_system
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `AccountID` int NOT NULL,
  `CustomerID` int DEFAULT NULL,
  `BranchID` int DEFAULT NULL,
  `Balance` decimal(15,2) DEFAULT NULL,
  `AccountType` varchar(50) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`AccountID`),
  KEY `BranchID` (`BranchID`),
  KEY `fk_customer` (`CustomerID`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`),
  CONSTRAINT `account_ibfk_2` FOREIGN KEY (`BranchID`) REFERENCES `Branch` (`BranchID`),
  CONSTRAINT `fk_customer` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (30049682,2496,22,95915795.00,'fixed deposit','active'),(32636177,5933,45,50000.00,'savings','active'),(39741440,2041,35,5186707.00,'fixed deposit','active'),(68078572,2496,45,27000.00,'fixed deposit','active');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Branch`
--

DROP TABLE IF EXISTS `Branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Branch` (
  `BranchID` int NOT NULL,
  `Location` varchar(80) DEFAULT NULL,
  `ManagerID` int DEFAULT NULL,
  PRIMARY KEY (`BranchID`),
  KEY `ManagerID` (`ManagerID`),
  CONSTRAINT `branch_ibfk_1` FOREIGN KEY (`ManagerID`) REFERENCES `Employee` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Branch`
--

LOCK TABLES `Branch` WRITE;
/*!40000 ALTER TABLE `Branch` DISABLE KEYS */;
INSERT INTO `Branch` VALUES (10,'Bangalore',1020),(18,'Hyderabad',1005),(22,'Mumbai',1010),(35,'Delhi',1015),(45,'Chennai',1025);
/*!40000 ALTER TABLE `Branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customer` (
  `CustomerID` int NOT NULL,
  `FName` varchar(25) DEFAULT NULL,
  `LName` varchar(25) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `PhoneNo` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  CONSTRAINT `NumericTenDigitPhoneNumber` CHECK (regexp_like(`phoneno`,_utf8mb4'^[0-9]{10}$'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1983,'asdfa','asdfasdf','asdfasd','2345679873'),(2041,'fadsfsd','asdfsd','asdfasdf','2342334643'),(2441,'asdf','aaa','bangalore','1345756476'),(2496,'asdf','asdf','adsf','9800345670'),(3239,'asdf','dfdd','sdfsdf','1234567890'),(3439,'haha','haha','bangalore','1231231231'),(4026,'asdfa','asdfasdf','asdfasd','2345679873'),(4656,'asdfa','asdfasdf','mathikere','2345679873'),(5933,'vamsi','sat','bangalore','1234567890');
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CustomerLogin`
--

DROP TABLE IF EXISTS `CustomerLogin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CustomerLogin` (
  `CustomerID` int DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `PasswordHash` varchar(255) DEFAULT NULL,
  UNIQUE KEY `Username` (`Username`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `customerlogin_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CustomerLogin`
--

LOCK TABLES `CustomerLogin` WRITE;
/*!40000 ALTER TABLE `CustomerLogin` DISABLE KEYS */;
INSERT INTO `CustomerLogin` VALUES (2496,'asdf','$2b$12$MvtrQ3.NvIkRmen.oI1BZuv069HKyvS.y5wK1Fvsxsto1wOtKuqKK'),(3439,'haha','$2b$12$Y1a9D1HT/d9StWnR0T4JGOl9oIodvJyaDHPOvKbfT6QBOiD9be0ty'),(1983,'asdf2','$2b$12$mw/AXcdKBIYr9UHNxjonXO1XXiVAf7TxdW1QZ9d2yz2NYHPRB36TK'),(2041,'moo','$2b$12$hbGnvc6OiJkvx0xPhfWDy./gBA9X75QJiHxo8TisKtLWgkSs1Q6bG'),(3239,'adfs','$2b$12$x/c53C6ujHrly0U7rG4oX.twbHPXZvHLhxkbrqeykk5rbRIesbSEC'),(5933,'sid','$2b$12$i9ZV.kyTJk27L6Hq0L6kl.dqbUAjF8LWh/0ZYRcpJTEAuJYMqvQii'),(2441,'aaa','$2b$12$q/Q7kXbbrqO2kg22lRzSHu1D1zb/vLcRlLvVK45jQVqzZl7alTpIm');
/*!40000 ALTER TABLE `CustomerLogin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `EmployeeID` int NOT NULL,
  `FName` varchar(25) DEFAULT NULL,
  `LName` varchar(25) DEFAULT NULL,
  `Salary` decimal(10,2) DEFAULT NULL,
  `RoleID` int DEFAULT NULL,
  `BranchID` int DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`EmployeeID`),
  KEY `RoleID` (`RoleID`),
  KEY `BranchID` (`BranchID`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`RoleID`) REFERENCES `EmployeeRoles` (`EmployeeRoleID`),
  CONSTRAINT `employee_ibfk_2` FOREIGN KEY (`BranchID`) REFERENCES `Branch` (`BranchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Vamsi','P',200000.00,4,10,'employeed'),(2,'Siddharth','s',200000.00,4,10,'employeed'),(1001,'Amit','Kumar',55000.00,1,10,'employeed'),(1002,'Priya','Sharma',60000.00,1,22,'employeed'),(1003,'Rajesh','Singh',70000.00,2,35,'employeed'),(1004,'Anita','Patel',80000.00,2,45,'employeed'),(1005,'Sachin','Gupta',95000.00,3,18,'employeed'),(1006,'Smita','Das',55000.00,1,10,'employeed'),(1007,'Vikram','Mishra',60000.00,1,22,'employeed'),(1008,'Anjali','Verma',70000.00,2,35,'employeed'),(1009,'Alok','Chatterjee',80000.00,2,45,'employeed'),(1010,'Neha','Rao',95000.00,3,22,'employeed'),(1011,'Rahul','Gupta',60000.00,1,10,'employeed'),(1012,'Meera','Patil',65000.00,1,22,'employeed'),(1013,'Sanjay','Yadav',72000.00,2,35,'employeed'),(1014,'Jyoti','Shukla',78000.00,2,45,'dismissed'),(1015,'Aditya','Malhotra',92000.00,3,35,'employeed'),(1016,'Aishwarya','Roy',55000.00,1,10,'employeed'),(1017,'Rajat','Banerjee',60000.00,1,22,'employeed'),(1018,'Nisha','Rathore',70000.00,2,35,'employeed'),(1019,'Amitabh','Mukherjee',85000.00,2,45,'employeed'),(1020,'Pooja','Shah',95000.00,3,10,'employeed'),(1021,'Rahul','Chopra',58000.00,1,10,'employeed'),(1022,'Kavita','Nair',62000.00,1,22,'employeed'),(1023,'Vivek','Iyer',73000.00,2,35,'dismissed'),(1024,'Ananya','Kapoor',78000.00,2,45,'employeed'),(1025,'Rohit','Raj',90000.00,3,45,'employeed'),(1026,'Arun','Khanna',59000.00,1,10,'employeed'),(1027,'Priyanka','Gupta',63000.00,1,22,'dismissed'),(1028,'Vijay','Sharma',72000.00,2,35,'employeed'),(1029,'Neha','Chopra',76000.00,2,45,'employeed'),(1030,'Ajay','Mishra',91000.00,1,18,'employeed'),(1031,'Asha','Verma',56000.00,1,10,'employeed'),(1032,'Rahul','Singh',64000.00,1,22,'employeed'),(1033,'Kavita','Sharma',71000.00,2,35,'employeed'),(1034,'Amit','Chaudhary',79000.00,2,45,'employeed'),(1035,'Deepak','Agarwal',94000.00,2,18,'employeed'),(1036,'Swati','Sharma',57000.00,1,10,'employeed'),(1037,'Rahul','Goyal',66000.00,1,22,'employeed'),(1038,'Anu','Shukla',75000.00,2,35,'employeed'),(1039,'Prateek','Yadav',80000.00,2,45,'employeed'),(1040,'Neha','Sharma',93000.00,1,18,'employeed'),(1041,'Ravi','Singh',59000.00,1,10,'employeed'),(1042,'Sneha','Verma',67000.00,1,22,'employeed'),(1043,'Rahul','Chauhan',74000.00,2,35,'dismissed'),(1044,'Aarti','Saxena',78000.00,2,45,'employeed'),(1045,'Sachin','Mishra',92000.00,2,18,'employeed'),(1046,'Neha','Reddy',60000.00,1,10,'employeed'),(1047,'Suresh','Kumar',70000.00,1,22,'employeed'),(1048,'Aishwarya','Iyer',78000.00,2,35,'employeed'),(1049,'Rahul','Reddy',83000.00,2,45,'employeed'),(1050,'Meera','Joshi',96000.00,1,18,'dismissed');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EmployeeLogin`
--

DROP TABLE IF EXISTS `EmployeeLogin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EmployeeLogin` (
  `EmployeeID` int DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `PasswordHash` varchar(255) DEFAULT NULL,
  UNIQUE KEY `Username` (`Username`),
  KEY `EmployeeID` (`EmployeeID`),
  CONSTRAINT `employeelogin_ibfk_1` FOREIGN KEY (`EmployeeID`) REFERENCES `Employee` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmployeeLogin`
--

LOCK TABLES `EmployeeLogin` WRITE;
/*!40000 ALTER TABLE `EmployeeLogin` DISABLE KEYS */;
INSERT INTO `EmployeeLogin` VALUES (1001,'Chiaroscuro','$2b$12$nMk3SQvUKNdLk9msgFS71.hrXCHolWHlLXajivVYa5TfWsrtDeIVO'),(1002,'Geez God','$2b$12$QPkGp6oyjCQ9XUBilXnR6.FKtRpr2lP5RcATjDg84dWh6eF6/vZhW'),(1003,'Locomate','$2b$12$fRKKfZJL4YOb.xQQubVREOpEcm1Msk.42WeLNuiwsavNmk.V4R6Lm'),(1004,'Speckled Dudess','$2b$12$QvaJA9QsuturS2raJ8II/e1TrpVnPNxg5vEzcZy.lk.lwquqRhiFS'),(1005,'Genialkeebz','$2b$12$t5YVBSFtzq.Eh3mhqRGLyuxyPdK2yzo.AmyFKGoe0RLDwP0hnyeZy'),(1006,'Lovestump','$2b$12$C2aUp8wkkespy48QkyJ68.NY7k6NJKeiNrR7vs8tgdyopE7tT0bhi'),(1007,'Hyper Zoom','$2b$12$jiy9YSQwbY5vVoPe6wxQY.y5AlwU6UpP0F/FTa3AiqGdorN/L7Wxq'),(1008,'Doggondivis','$2b$12$O7tHDWzRC4NTw//86y8BP.qwQsj89M4Yg/wTQA4hJaK1A/zasQcoG'),(1009,'Funambulist','$2b$12$PXris1f4QQn21KCR2w4ftOFzKP6gRtRo460X2mLlQDKnLUSxlLit6'),(1010,'Dream Girl','$2b$12$MIcsgUh8xfETK.nuAJrMWer6tRtjlYymoUnDL3yspEJCFmnh.jkM6'),(1011,'Evil Weevil','$2b$12$429XYDzwsQVjIzmMiLMafe6sf4nJVwANezO14sFTKrsHq.hJUTQb6'),(1012,'Bold_Style','$2b$12$nlrL7LkEqo4WEEywXEA6t.RITP5SGFeqvaMIpEzfJOUx6RdQgtWrC'),(1013,'Bold_Touch','$2b$12$mmy5kNybZMkCIyxRdFNege2ktLnKr8FmQY7i5yMhp0I0M7CmTjL4W'),(1014,'Thought Motel','$2b$12$96MF4oOVIwUjoliFFAtyH..1WFEcac4kp/0g0QXx.TnxlL7EmDRsK'),(1015,'Piggy_Honeybear','$2b$12$4oiQ5sX/PxG3x5kiaocd2eYytSoZcGpO4ShsWjRd9rfy/jP3U2rLC'),(1016,'Cyber Floss Lord','$2b$12$nEXqUt78mysM.tCfWlSwGu6l01mdYIlq0Bu4BdI8he/SAkF.bw4lu'),(1017,'Awesome_Girls','$2b$12$wJJ8ccj/q7dqDDq9jj5vsOUU8T6jTT3boAFmYg6yrsUpcKo/kuOXS'),(1018,'Glam Angel','$2b$12$IGcx9/E9X1YEzyHoSKd07O3Z9TbELwyWSqobu.UxKxz9yxq.8v0vC'),(1019,'Zombie Guide','$2b$12$.5Tja8jFRWfR0eOx6aGq4OJ/9c6BNxfj3p7z8vI.BwvFrLb79BhnO'),(1020,'Muffinhead','$2b$12$yOS/l7O7qetIGNsaXsllPOnGvCbCXM/jChTzvXoqbq5SXIt8r.NPi'),(1021,'Pixel Anatomy','$2b$12$6ykTUry43/XN8WXxFW5tQuWdNdAIjwnmtwcRstrOPd5tZPgn47TvC'),(1022,'Honey_Bell','$2b$12$IcmTPMm2fWiEdFKaLITSkOpHVoeH0zE1AJwc4rKfE0y9JvKah1zN.'),(1023,'Purrienne','$2b$12$6St6sW1gHkYJWfB6HWfRYOBp48dM3S8PSqXfuDsLg8kwzcrAKacpe'),(1024,'Sweet_Quail','$2b$12$ehgZyHPh16E5ldkqHy37QuhTZ3USlaLIuN51vVgWKGu39gBazh3be'),(1025,'Summer Rain','$2b$12$vcyC3s4AluSGn1O2shlpc.gE7xvFWSvzOmCM6HpSf539lO7rWaD06'),(1026,'TheWanderlustKing/Queen','$2b$12$8sBEE0Bw.ISIEHJEX3wk6e1AZHVtGGiJUHWE9RBjR8F85xlVpEdCW'),(1027,'TheSocialButterfly','$2b$12$gbTKRzFdaLMYP8VoYYHDwOnnZN3gi2X6UGgmHnZmQ5LYx2YCaSJuK'),(1028,'TheDesignDiva','$2b$12$.9Rvx8/AnmKwThhrnh2rqOHdyd6vxtQ2.NMUcVXJEvAn45nbL/h1i'),(1029,'TheEntrepreneurMind','$2b$12$2BEIBlamCTV9qVncuds/we0Ng1fGeZluXOXWlm33aiQD8HcagRiTe'),(1030,'TheStyleMaven','$2b$12$RPv4ZqJbG3pdz.DMo7Q3V.BBSmKroCxoEk3eVEaZ3LKPpoikprNkC'),(1031,'Luffgirl','$2b$12$NwXCSVFeFRpSaTh7qws0c.FxQukbbxeDxaVFh.Zdk2x0BYUJmdSuG'),(1032,'Cute_Sugarr','$2b$12$cTbC/L0FMAVnhVFH2Dyi/.dGKRY5dmixj4Pxx3Dbs2VOWjrPrjDZy'),(1033,'Sweet_Sparrow','$2b$12$SEFmu8yqDvAoQRnjxcv7eOMwNblZKhU4wyQVC45OWqkvMuqYwLd92'),(1034,'The Inner Thing','$2b$12$ispXnPnSRM6SSYEZYYO9FeLXWRR5zg0o.FniDY3zui7siTGodt.Cm'),(1035,'Etiolate','$2b$12$B5tWgCsHfFdlHeVTfONN/uque/9w4UUbcABRHiBxYEBCJU4UkTFXW'),(1036,'RoseGarden','$2b$12$Ci9q61y4vmQ4trY/RnYuWOu7k/5/y/rm2l1/ZwS53e51mJJCKk3cm'),(1037,'MoonlitMystic','$2b$12$6LQE4H9DIbEDIJauhe2tNOXl73r7h4bJbuJ2.2k3CqBe6afRRKHPW'),(1038,'OceanBreeze','$2b$12$GdHmTFAAxDXQdvW7pSqSv.MIRxxPgeK/IXWkr4m2Yk3g9JJKL6cpu'),(1039,'LavenderLullaby','$2b$12$zMD6Q5YP/akRQsn0bGtFpeDduxNXvhysAu5IGYKlkvSrhEne38sqC'),(1040,'SerendipitySiren','$2b$12$KccdFpfo8GPJym0R3jDJiuUx1.ZjlNby4LiYu1qUopkwqZWXNZvBy'),(1041,'MidnightMelody','$2b$12$NHmDtbMUJyhd6KelGVt8ve2FGkiWMcYCNtQ8/0sUbo9nPVHeosP7S'),(1042,'GoldenGoddess','$2b$12$VEOYwntv83ASJe3oieaNgOeIxGVcMVAUaQJ7s5f7jji8FyDPa7I52'),(1043,'BlossomBreeze','$2b$12$V3BW0dJv7B6OZaEv51b.xOAehI31/fpRk3AUn6mj8F/5ogZtUgBaa'),(1044,'EnchantedEcho','$2b$12$RbZsWW7n6MWzaW97SefcHeU9ufcn/0WFx88WZUAicw1SMDktyms42'),(1045,'MoonBabe','$2b$12$jl5gaYCAua7nkp/4Jzo6MOls2YGt.YDC0Fwque/mSiqr7zD9tM0hG'),(1046,'GlitteryHearts','$2b$12$lWWVHykrEm0YQyQyLnI1bu56MNI3mA8RGwM9Yeu5W6M031F6OvUWu'),(1047,'SoftandMushy','$2b$12$DiS00rflO5mx8gyir04SheqlEO17epmOhpMJjS01pbikJX18LSNC.'),(1048,'LegendsofNarnia','$2b$12$hLYd3d7dTBjng/6Du.1ctOW2iLDutp7ZY7eoYAvGUfYXOSClUdEUa'),(1049,'BigBellySanta','$2b$12$Gd61jdSDlncbRyYxIHbhZ.8x.MJN/xMHNgl6jQwlx0/Zj/9f29mr.'),(1050,'LifeinBlackandWhite','$2b$12$Cn.vPFHH3.4BSe6DVE0Ii.l5J72yK2/EtMaNDI/rRNGtKYlbPIptq'),(1,'BlazeFury','$2b$12$ZfAsVwxs3E8BXHbXL..BB.k/GuP9.3V.XNpHd/xglUQ231rJcJIp.'),(2,'Sid','$2b$12$1pkcVQUaeR1PRFy4ngrjOuxshK/EoweYTAB4sy8PDNvChzhiVKRjW');
/*!40000 ALTER TABLE `EmployeeLogin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EmployeeRoles`
--

DROP TABLE IF EXISTS `EmployeeRoles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EmployeeRoles` (
  `EmployeeRoleID` int NOT NULL,
  `RoleName` varchar(50) DEFAULT NULL,
  `RoleDescription` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`EmployeeRoleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmployeeRoles`
--

LOCK TABLES `EmployeeRoles` WRITE;
/*!40000 ALTER TABLE `EmployeeRoles` DISABLE KEYS */;
INSERT INTO `EmployeeRoles` VALUES (1,'Customer Service Representative/Teller','Relevant for handling customer transactions and inquiries within the application. Can create accounts, close accounts, and update account details.'),(2,'Loan Officer','Responsible for loan management and processing. Can approve and reject loans.'),(3,'Branch Manager','Relevant for branch-level operations and management. Can dismiss other employees.'),(4,'IT Specialist/Systems Administrator','Responsible for managing and maintaining the information technology aspects of the application.');
/*!40000 ALTER TABLE `EmployeeRoles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Loan`
--

DROP TABLE IF EXISTS `Loan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Loan` (
  `LoanID` int NOT NULL,
  `CustomerID` int DEFAULT NULL,
  `EmployeeID` int DEFAULT NULL,
  `Amount` decimal(15,2) DEFAULT NULL,
  `InterestRate` decimal(5,2) DEFAULT NULL,
  `ApprovalStatus` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`LoanID`),
  KEY `CustomerID` (`CustomerID`),
  KEY `EmployeeID` (`EmployeeID`),
  CONSTRAINT `loan_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`),
  CONSTRAINT `loan_ibfk_2` FOREIGN KEY (`EmployeeID`) REFERENCES `Employee` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Loan`
--

LOCK TABLES `Loan` WRITE;
/*!40000 ALTER TABLE `Loan` DISABLE KEYS */;
INSERT INTO `Loan` VALUES (1705,2496,1,50000.00,8.45,'approved'),(2352,2041,1,100000.00,8.45,'rejected'),(4840,2496,1,30000.00,8.45,'approved'),(5396,5933,2,50000.00,8.45,'approved'),(6144,2496,NULL,40000.00,8.45,'pending');
/*!40000 ALTER TABLE `Loan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `to_be_reviewed`
--

DROP TABLE IF EXISTS `to_be_reviewed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `to_be_reviewed` (
  `id` int NOT NULL AUTO_INCREMENT,
  `transaction_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `to_be_reviewed_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`TransactionID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `to_be_reviewed`
--

LOCK TABLES `to_be_reviewed` WRITE;
/*!40000 ALTER TABLE `to_be_reviewed` DISABLE KEYS */;
INSERT INTO `to_be_reviewed` VALUES (1,1384,'2023-12-28 05:29:06'),(2,5195,'2023-12-28 08:12:04'),(3,3322,'2023-12-28 08:14:13'),(4,5309,'2023-12-28 08:38:49');
/*!40000 ALTER TABLE `to_be_reviewed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `TransactionID` int NOT NULL,
  `SourceAccountID` int DEFAULT NULL,
  `DestinationAccountID` int DEFAULT NULL,
  `Amount` decimal(15,2) DEFAULT NULL,
  `AssistedBy` int DEFAULT NULL,
  `Timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`TransactionID`),
  KEY `SourceAccountID` (`SourceAccountID`),
  KEY `DestinationAccountID` (`DestinationAccountID`),
  KEY `AssistedBy` (`AssistedBy`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`SourceAccountID`) REFERENCES `Account` (`AccountID`),
  CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`DestinationAccountID`) REFERENCES `Account` (`AccountID`),
  CONSTRAINT `transaction_ibfk_3` FOREIGN KEY (`AssistedBy`) REFERENCES `Employee` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` VALUES (1384,30049682,39741440,1000001.00,NULL,'2023-12-28 05:29:07'),(3058,30049682,68078572,500.00,NULL,'2023-12-25 11:30:02'),(3196,30049682,39741440,300.00,1,'2023-12-27 19:56:43'),(3322,30049682,39741440,2000000.00,NULL,'2023-12-28 08:14:14'),(3782,30049682,39741440,30000.00,NULL,'2023-12-28 07:45:54'),(4765,30049682,68078572,3000.00,NULL,'2023-12-25 11:31:17'),(4948,32636177,39741440,50000.00,2,'2023-12-28 08:03:09'),(4956,30049682,68078572,200.00,NULL,'2023-12-27 19:40:42'),(5195,30049682,39741440,1000003.00,NULL,'2023-12-28 08:12:05'),(5309,30049682,39741440,1000002.00,1016,'2023-12-28 08:38:50'),(6603,30049682,39741440,100001.00,NULL,'2023-12-28 05:15:32');
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `review_high_value_transaction` AFTER INSERT ON `transaction` FOR EACH ROW BEGIN
    IF NEW.amount > 1000000 THEN
        INSERT INTO to_be_reviewed (transaction_id, created_at) VALUES (NEW.transactionid, NOW());
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-05 13:20:47
