-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 19 Bulan Mei 2024 pada 17.41
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `local_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `gps`
--

CREATE TABLE `gps` (
  `id_gps` int(11) NOT NULL,
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `lahan`
--

CREATE TABLE `lahan` (
  `id_lahan` varchar(15) NOT NULL,
  `nama_lahan` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `npk`
--

CREATE TABLE `npk` (
  `id_npk` int(11) NOT NULL,
  `natrium` float DEFAULT NULL,
  `fosfor` float DEFAULT NULL,
  `kalium` float DEFAULT NULL,
  `ph` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `record`
--

CREATE TABLE `record` (
  `id_record` int(11) NOT NULL,
  `id_varietas` int(11) DEFAULT NULL,
  `id_lahan` int(18) DEFAULT NULL,
  `id_gps` int(11) DEFAULT NULL,
  `id_npk` int(11) DEFAULT NULL,
  `time_records` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `varietas`
--

CREATE TABLE `varietas` (
  `id_varietas` varchar(15) NOT NULL,
  `id_lahan` varchar(15) DEFAULT NULL,
  `nama_varietas` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `wilayah`
--

CREATE TABLE `wilayah` (
  `nid` BIGINT,
  `parent_nid` BIGINT,
  `name` VARCHAR(1024),
  `serial` BIGINT,
  `type` BIGINT,
  `latitude` DOUBLE,
  `longitude` DOUBLE,
  `status` BIGINT
);
--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `gps`
--
ALTER TABLE `gps`
  ADD PRIMARY KEY (`id_gps`);

--
-- Indeks untuk tabel `lahan`
--
ALTER TABLE `lahan`
  ADD PRIMARY KEY (`id_lahan`);

--
-- Indeks untuk tabel `npk`
--
ALTER TABLE `npk`
  ADD PRIMARY KEY (`id_npk`);

--
-- Indeks untuk tabel `record`
--
ALTER TABLE `record`
  ADD PRIMARY KEY (`id_record`),
  ADD KEY `id_varietas` (`id_varietas`),
  ADD KEY `id_lahan` (`id_lahan`),
  ADD KEY `id_gps` (`id_gps`),
  ADD KEY `id_npk` (`id_npk`);

--
-- Indeks untuk tabel `varietas`
--
ALTER TABLE `varietas`
  ADD PRIMARY KEY (`id_varietas`),
  ADD KEY `id_lahan` (`id_lahan`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `record`
--
ALTER TABLE `record`
  ADD CONSTRAINT `record_ibfk_1` FOREIGN KEY (`id_varietas`) REFERENCES `varietas` (`id_varietas`),
  ADD CONSTRAINT `record_ibfk_2` FOREIGN KEY (`id_lahan`) REFERENCES `lahan` (`id_lahan`),
  ADD CONSTRAINT `record_ibfk_3` FOREIGN KEY (`id_gps`) REFERENCES `gps` (`id_gps`),
  ADD CONSTRAINT `record_ibfk_4` FOREIGN KEY (`id_npk`) REFERENCES `npk` (`id_npk`);

--
-- Ketidakleluasaan untuk tabel `varietas`
--
ALTER TABLE `varietas`
  ADD CONSTRAINT `varietas_ibfk_1` FOREIGN KEY (`id_lahan`) REFERENCES `lahan` (`id_lahan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
