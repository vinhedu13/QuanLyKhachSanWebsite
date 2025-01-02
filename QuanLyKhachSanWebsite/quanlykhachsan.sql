-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: quanlykhachsan
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `hoadon`
--

DROP TABLE IF EXISTS `hoadon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoadon` (
  `tongTien` double NOT NULL,
  `trangThai` tinyint(1) NOT NULL,
  `idPhieu` int NOT NULL,
  `thoiGianTao` datetime NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idPhieu` (`idPhieu`),
  CONSTRAINT `hoadon_ibfk_1` FOREIGN KEY (`idPhieu`) REFERENCES `phieu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoadon`
--

LOCK TABLES `hoadon` WRITE;
/*!40000 ALTER TABLE `hoadon` DISABLE KEYS */;
INSERT INTO `hoadon` VALUES (500000,1,657541942,'2024-12-31 22:06:16',26),(800000,1,657674531,'2024-12-31 22:08:08',27),(1500000,1,657721743,'2024-12-31 22:08:53',28),(1500000,1,657954262,'2024-12-31 22:12:51',29),(250000,1,658387603,'2024-12-31 22:25:36',30);
/*!40000 ALTER TABLE `hoadon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khachhang`
--

DROP TABLE IF EXISTS `khachhang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khachhang` (
  `tenKhachHang` varchar(50) DEFAULT NULL,
  `hoKhachHang` varchar(50) DEFAULT NULL,
  `gioiTinh` enum('Nam','Nữ') DEFAULT NULL,
  `cccd` varchar(12) DEFAULT NULL,
  `sdt` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `diaChi` varchar(200) DEFAULT NULL,
  `idLoaiKhach` int DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `idLoaiKhach` (`idLoaiKhach`),
  CONSTRAINT `khachhang_ibfk_1` FOREIGN KEY (`idLoaiKhach`) REFERENCES `loaikhach` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=154542151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khachhang`
--

LOCK TABLES `khachhang` WRITE;
/*!40000 ALTER TABLE `khachhang` DISABLE KEYS */;
INSERT INTO `khachhang` VALUES ('Vinh',NULL,NULL,NULL,'0889100850','lequangvinh13052004@gmail.com',NULL,NULL,154542146),('Vy',NULL,NULL,NULL,'0889100850','love13052004@gmail.com',NULL,NULL,154542147),('Schole',NULL,NULL,'664222015',NULL,NULL,NULL,2,154542148),('Vinh',NULL,NULL,'66642235',NULL,NULL,NULL,1,154542149),('Vinh',NULL,NULL,'66642235',NULL,NULL,NULL,1,154542150);
/*!40000 ALTER TABLE `khachhang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loaikhach`
--

DROP TABLE IF EXISTS `loaikhach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loaikhach` (
  `tenLoaiKhach` varchar(50) NOT NULL,
  `heSo` double NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loaikhach`
--

LOCK TABLES `loaikhach` WRITE;
/*!40000 ALTER TABLE `loaikhach` DISABLE KEYS */;
INSERT INTO `loaikhach` VALUES ('Nội Địa',1,1),('Nước ngoài',1.5,2);
/*!40000 ALTER TABLE `loaikhach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loaiphieu`
--

DROP TABLE IF EXISTS `loaiphieu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loaiphieu` (
  `tenLoaiPhieu` varchar(50) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loaiphieu`
--

LOCK TABLES `loaiphieu` WRITE;
/*!40000 ALTER TABLE `loaiphieu` DISABLE KEYS */;
INSERT INTO `loaiphieu` VALUES ('Phiếu thuê phòng',1),('Phiếu đặt phòng',2);
/*!40000 ALTER TABLE `loaiphieu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loaiphong`
--

DROP TABLE IF EXISTS `loaiphong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loaiphong` (
  `tenLoaiPhong` varchar(50) NOT NULL,
  `donGia` double NOT NULL,
  `soLuong` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `dienTich` double DEFAULT NULL,
  `moTa` varchar(100) DEFAULT NULL,
  `luongKhachToiDa` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loaiphong`
--

LOCK TABLES `loaiphong` WRITE;
/*!40000 ALTER TABLE `loaiphong` DISABLE KEYS */;
INSERT INTO `loaiphong` VALUES ('Phòng thường',500000,3,1,19,NULL,3),('Phòng thương gia',800000,1,2,30,NULL,3),('Phòng VIP',1500000,1,3,45,NULL,3);
/*!40000 ALTER TABLE `loaiphong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loaitaikhoan`
--

DROP TABLE IF EXISTS `loaitaikhoan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loaitaikhoan` (
  `tenLoaiTaiKhoan` varchar(50) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loaitaikhoan`
--

LOCK TABLES `loaitaikhoan` WRITE;
/*!40000 ALTER TABLE `loaitaikhoan` DISABLE KEYS */;
INSERT INTO `loaitaikhoan` VALUES ('Admin',1),('Khách hàng',2),('Nhân viên',3);
/*!40000 ALTER TABLE `loaitaikhoan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieu`
--

DROP TABLE IF EXISTS `phieu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieu` (
  `loaiPhieu` int NOT NULL,
  `thoiGianTao` datetime NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `loaiPhieu` (`loaiPhieu`),
  CONSTRAINT `phieu_ibfk_1` FOREIGN KEY (`loaiPhieu`) REFERENCES `loaiphieu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=940632773 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieu`
--

LOCK TABLES `phieu` WRITE;
/*!40000 ALTER TABLE `phieu` DISABLE KEYS */;
INSERT INTO `phieu` VALUES (2,'2024-12-31 22:06:16',657541942),(2,'2024-12-31 22:08:08',657674531),(2,'2024-12-31 22:08:53',657721743),(1,'2024-12-31 22:12:51',657954262),(1,'2024-12-31 22:16:09',658168755),(1,'2024-12-31 22:25:36',658387603);
/*!40000 ALTER TABLE `phieu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieudatphong`
--

DROP TABLE IF EXISTS `phieudatphong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieudatphong` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idKhachHang` int NOT NULL,
  `idLoaiPhong` int NOT NULL,
  `soLuong` int NOT NULL,
  `trangThai` enum('Đã nhận phòng','Chưa nhận phòng','Đã hủy') DEFAULT NULL,
  `ngayNhanPhong` datetime DEFAULT NULL,
  `ngayTraPhong` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idKhachHang` (`idKhachHang`),
  KEY `idLoaiPhong` (`idLoaiPhong`),
  CONSTRAINT `phieudatphong_ibfk_1` FOREIGN KEY (`id`) REFERENCES `phieu` (`id`),
  CONSTRAINT `phieudatphong_ibfk_2` FOREIGN KEY (`idKhachHang`) REFERENCES `khachhang` (`id`),
  CONSTRAINT `phieudatphong_ibfk_3` FOREIGN KEY (`idLoaiPhong`) REFERENCES `loaiphong` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=940504738 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieudatphong`
--

LOCK TABLES `phieudatphong` WRITE;
/*!40000 ALTER TABLE `phieudatphong` DISABLE KEYS */;
INSERT INTO `phieudatphong` VALUES (657541942,154542146,1,1,'Đã nhận phòng','2024-12-31 14:00:00','2025-01-01 12:00:00'),(657674531,154542147,2,1,'Chưa nhận phòng','2025-01-02 14:00:00','2025-01-03 12:00:00'),(657721743,154542147,3,1,'Chưa nhận phòng','2025-01-05 14:00:00','2025-01-07 12:00:00');
/*!40000 ALTER TABLE `phieudatphong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieuthuephong`
--

DROP TABLE IF EXISTS `phieuthuephong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieuthuephong` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ngayNhanPhong` datetime NOT NULL,
  `ngayTraPhong` datetime NOT NULL,
  `idPhieuDatPhong` int DEFAULT NULL,
  `trangThai` enum('Đang sử dụng','Đã trả phòng') DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idPhieuDatPhong` (`idPhieuDatPhong`),
  CONSTRAINT `phieuthuephong_ibfk_1` FOREIGN KEY (`id`) REFERENCES `phieu` (`id`),
  CONSTRAINT `phieuthuephong_ibfk_2` FOREIGN KEY (`idPhieuDatPhong`) REFERENCES `phieudatphong` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=940632773 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieuthuephong`
--

LOCK TABLES `phieuthuephong` WRITE;
/*!40000 ALTER TABLE `phieuthuephong` DISABLE KEYS */;
INSERT INTO `phieuthuephong` VALUES (657954262,'2024-12-31 22:12:51','2025-01-01 12:00:00',NULL,NULL),(658168755,'2024-12-31 22:16:09','2025-01-01 12:00:00',657541942,NULL);
/*!40000 ALTER TABLE `phieuthuephong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieuthuephong_phong`
--

DROP TABLE IF EXISTS `phieuthuephong_phong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieuthuephong_phong` (
  `idPhong` int NOT NULL,
  `idPhieuThuePhong` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `idPhong` (`idPhong`),
  KEY `idPhieuThuePhong` (`idPhieuThuePhong`),
  CONSTRAINT `phieuthuephong_phong_ibfk_1` FOREIGN KEY (`idPhong`) REFERENCES `phong` (`id`),
  CONSTRAINT `phieuthuephong_phong_ibfk_2` FOREIGN KEY (`idPhieuThuePhong`) REFERENCES `phieuthuephong` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieuthuephong_phong`
--

LOCK TABLES `phieuthuephong_phong` WRITE;
/*!40000 ALTER TABLE `phieuthuephong_phong` DISABLE KEYS */;
INSERT INTO `phieuthuephong_phong` VALUES (101,657954262,16),(102,658168755,17);
/*!40000 ALTER TABLE `phieuthuephong_phong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieuthuephong_phong_khachhang`
--

DROP TABLE IF EXISTS `phieuthuephong_phong_khachhang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieuthuephong_phong_khachhang` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idKhachHang` int NOT NULL,
  `idPhieuThuePhong_Phong` int NOT NULL,
  `trangThai` enum('Đã nhận phòng','Đã trả phòng') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fkidKhachHang_idx` (`idKhachHang`),
  KEY `fkidPhieuThuePhong_Phong_idx` (`idPhieuThuePhong_Phong`),
  CONSTRAINT `fkidKhachHang` FOREIGN KEY (`idKhachHang`) REFERENCES `khachhang` (`id`),
  CONSTRAINT `fkidPhieuThuePhong_Phong` FOREIGN KEY (`idPhieuThuePhong_Phong`) REFERENCES `phieuthuephong_phong` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieuthuephong_phong_khachhang`
--

LOCK TABLES `phieuthuephong_phong_khachhang` WRITE;
/*!40000 ALTER TABLE `phieuthuephong_phong_khachhang` DISABLE KEYS */;
INSERT INTO `phieuthuephong_phong_khachhang` VALUES (13,154542148,16,'Đã trả phòng'),(14,154542149,17,'Đã nhận phòng');
/*!40000 ALTER TABLE `phieuthuephong_phong_khachhang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phong`
--

DROP TABLE IF EXISTS `phong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phong` (
  `tenPhong` varchar(50) NOT NULL,
  `idLoaiPhong` int NOT NULL,
  `idTinhTrangPhong` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `idLoaiPhong` (`idLoaiPhong`),
  KEY `idTinhTrangPhong` (`idTinhTrangPhong`),
  CONSTRAINT `phong_ibfk_1` FOREIGN KEY (`idLoaiPhong`) REFERENCES `loaiphong` (`id`),
  CONSTRAINT `phong_ibfk_2` FOREIGN KEY (`idTinhTrangPhong`) REFERENCES `tinhtrangphong` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=302 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phong`
--

LOCK TABLES `phong` WRITE;
/*!40000 ALTER TABLE `phong` DISABLE KEYS */;
INSERT INTO `phong` VALUES ('101',1,1,101),('102',1,1,102),('103',1,1,103),('201',2,1,201),('301',3,1,301);
/*!40000 ALTER TABLE `phong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taikhoan`
--

DROP TABLE IF EXISTS `taikhoan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `taikhoan` (
  `tenDangNhap` varchar(50) NOT NULL,
  `matKhau` varchar(50) NOT NULL,
  `soDienThoai` varchar(10) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `thoiGianTao` datetime NOT NULL,
  `idLoaiTaiKhoan` int NOT NULL,
  `idKhachHang` int DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idKhachHang` (`idKhachHang`),
  KEY `idLoaiTaiKhoan` (`idLoaiTaiKhoan`),
  CONSTRAINT `taikhoan_ibfk_1` FOREIGN KEY (`idLoaiTaiKhoan`) REFERENCES `loaitaikhoan` (`id`),
  CONSTRAINT `taikhoan_ibfk_2` FOREIGN KEY (`idKhachHang`) REFERENCES `khachhang` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taikhoan`
--

LOCK TABLES `taikhoan` WRITE;
/*!40000 ALTER TABLE `taikhoan` DISABLE KEYS */;
INSERT INTO `taikhoan` VALUES ('admin','123','0889100850','lequangvinh13052004@gmail.com','2024-12-31 21:43:27',1,NULL,9),('nhanvien','123','0889100850','lequangvinh13052004@gmail.com','2024-12-31 21:43:27',3,NULL,10),('Vinh','123','0889100850','lequangvinh13052004@gmail.com','2024-12-31 21:59:57',2,154542146,13),('Vy','123','0889100850','love13052004@gmail.com','2024-12-31 21:59:57',2,154542147,14);
/*!40000 ALTER TABLE `taikhoan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tinhtrangphong`
--

DROP TABLE IF EXISTS `tinhtrangphong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tinhtrangphong` (
  `tenTinhTrangPhong` varchar(50) DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tinhtrangphong`
--

LOCK TABLES `tinhtrangphong` WRITE;
/*!40000 ALTER TABLE `tinhtrangphong` DISABLE KEYS */;
INSERT INTO `tinhtrangphong` VALUES ('Trống',1),('Đang thuê',2),('Đang bảo trì',3);
/*!40000 ALTER TABLE `tinhtrangphong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tylephuthu`
--

DROP TABLE IF EXISTS `tylephuthu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tylephuthu` (
  `tyLe` double NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tylephuthu`
--

LOCK TABLES `tylephuthu` WRITE;
/*!40000 ALTER TABLE `tylephuthu` DISABLE KEYS */;
INSERT INTO `tylephuthu` VALUES (0.25,1);
/*!40000 ALTER TABLE `tylephuthu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-31 22:34:58
