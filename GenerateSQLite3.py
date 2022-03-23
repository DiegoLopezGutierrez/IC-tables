import sqlite3
from glob import glob

# Detectors: "Tst", "Next100", "Flex100", "FlexDens"

det_name = "flex.s3.0mmp3mm"

tables = [
    "ChannelGain",
    "ChannelMapping",
    "ChannelMask",
    "ChannelPosition",
    "DetectorGeo",
    "PMTFELowFrequencyNoise",
    "PMTFEMapping",
    "PmtBlr",
    "PmtNoiseRms",
    "SipmBaseline",
    "SipmNoisePDF"
]

if __name__ == "__main__":
 
    dbfile = f'localdb.{det_name}.sqlite3'
    print(f'Output file sqlite3 {dbfile}')
    print("Getting sql files")
    conn_sqlite   = sqlite3.connect(dbfile)
    cursor_sqlite = conn_sqlite.cursor()
    sql_files = glob(f'{det_name}/*sql')
 
    for sqlfile in sql_files:
        print(sqlfile)
        with open(sqlfile) as fd:
            data = fd.read()
            sentences = data.split(';')
            for sentence in sentences:
                cursor_sqlite.execute(sentence)
            print('-> done!')
            conn_sqlite.commit()
