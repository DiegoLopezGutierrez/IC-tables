DROP TABLE IF EXISTS `PMTFELowFrequencyNoise`;
CREATE TABLE `PMTFELowFrequencyNoise` (
	  `MinRun` int(11) NOT NULL,
	  `MaxRun` int(11) NOT NULL,
	  `Frequency` float NOT NULL,
	  `FE0Magnitude` float NOT NULL,
	  `FE1Magnitude` float NOT NULL,
	  `FE2Magnitude` float NOT NULL
);
