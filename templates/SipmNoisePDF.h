DROP TABLE IF EXISTS `SipmNoisePDF`;
CREATE TABLE `SipmNoisePDF` (
  `MinRun` int(11) NOT NULL,
  `MaxRun` int(11) DEFAULT NULL,
  `SensorID` int(11) NOT NULL,
  `BinEnergyPes` float NOT NULL,
  `Probability` float NOT NULL
);
