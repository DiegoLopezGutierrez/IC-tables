DROP TABLE IF EXISTS `ChannelPosition`;
CREATE TABLE `ChannelPosition` (
	  `MinRun` int(11) NOT NULL,
	  `MaxRun` int(11) NOT NULL,
	  `SensorID` int(11) NOT NULL,
	  `Label` varchar(20) NOT NULL,
	  `Type` varchar(20) NOT NULL,
	  `X` float NOT NULL,
	  `Y` float NOT NULL
);
