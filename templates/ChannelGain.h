DROP TABLE IF EXISTS `ChannelGain`;

CREATE TABLE `ChannelGain` (
  `MinRun` int(11) NOT NULL,
  `MaxRun` int(11) NOT NULL,
  `SensorID` int(11) NOT NULL,
  `Centroid` float NOT NULL,
  `ErrorCentroid` float NOT NULL,
  `Sigma` float NOT NULL,
  `ErrorSigma` float NOT NULL);
