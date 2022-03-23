import sys,os,os.path

sys.path.append(os.path.expanduser('~/code/eol_hsrl_python'))
os.environ['ICTDIR']='/n/holystore01/LABS/guenette_lab/Users/dlopezgutierrez/IC/'
sys.path.insert(1, '/n/holystore01/LABS/guenette_lab/Users/dlopezgutierrez/IC')

import json
import random

import invisible_cities.database.load_db as db

import sqlite3
from glob import glob

# Detectors: "Tst", "Next100", "Flex100", "FlexDens"

det_name = "flex.s1.3mmp1.3mm"

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

def load_detector_config(det_name):
    config_fname = f"config/{det_name}.config"

    with open(config_fname) as config_file:
        det_config = json.load(config_file)
    
    # Getting sensors info
    sensor_labels = det_config["SensorLabels"]
    for label in sensor_labels:
        det_config[label] = []
    
    sensors_fname = det_config["SensorFile"]
    with open(f"config/{sensors_fname}", 'r') as sensors_file:
        for entry in sensors_file.read().splitlines():
            words = entry.split()
            if (len(words) and (words[0] in sensor_labels)):
                sensor_id = int(words[1])
                pos = words[2][1:-1].split(',')
                sensor_x = float(pos[0])
                sensor_y = float(pos[1])
                det_config[words[0]].append((sensor_id, sensor_x, sensor_y))

    return det_config

def get_ChannelGain_entries(det_config):
    
    template = open("templates/ChannelGain.entry").read()
    
    
    MinRun = det_config["MinRun"]
    MaxRun = det_config["MaxRun"]
    
    entries = ""
    for label in det_config["SensorLabels"]:
        entries += "\n"
        for sensor in det_config[label]:
            SensorID      = sensor[0]
            Centroid      = det_config[label + "_Centroid"]
            ErrorCentroid = det_config[label + "_ErrorCentroid"]
            Sigma         = det_config[label + "_Sigma"]
            ErrorSigma    = det_config[label + "_ErrorSigma"]
            params        = locals()
            entries      += template.format(**params) + "\n"

    return entries

def get_ChannelMapping_entries(det_config):
    
    template = open("templates/ChannelMapping.entry").read()
    
    MinRun = det_config["MinRun"]
    MaxRun = det_config["MaxRun"]

    entries = ""
    for label in det_config["SensorLabels"]:
        entries += "\n"
        for sensor in det_config[label]:
            SensorID = sensor[0]
            ElecID   = SensorID
            params   = locals()
            entries += template.format(**params) + "\n"

    return entries

def get_ChannelPosition_entries(det_config):
    
    template = open("templates/ChannelPosition.entry").read()
    
    MinRun = det_config["MinRun"]
    MaxRun = det_config["MaxRun"]

    entries = ""
    for label in det_config["SensorLabels"]:
        entries += "\n"
        for sensor in det_config[label]:
            SensorID      = sensor[0]
            Label         = label
            Type          = det_config[label + "_Type"]
            X             = sensor[1]
            Y             = sensor[2]
            params        = locals()
            entries      += template.format(**params) + "\n"

    return entries

def get_DetectorGeo_entries(det_config):
    
    template = open("templates/DetectorGeo.entry").read()
    
    XMIN = det_config["XMIN"]
    XMAX = det_config["XMAX"]
    YMIN = det_config["YMIN"]
    YMAX = det_config["YMAX"]
    ZMIN = det_config["ZMIN"]
    ZMAX = det_config["ZMAX"]
    RMAX = det_config["RMAX"]

    params  = locals()
    entries = template.format(**params) + "\n"

    return entries

def get_SipmBaseline_entries(det_config):
    
    template = open("templates/SipmBaseline.entry").read()
    
    MinRun = det_config["MinRun"]
    MaxRun = "NULL"

    entries = ""
    for label in det_config["SensorLabels"]:
        if "SiPM" in label:
            entries += "\n"
            for sensor in det_config[label]:
                SensorID = sensor[0]
                Energy   = det_config[label + "_BaseLine"]
                params   = locals()
                entries += template.format(**params) + "\n"

    return entries

def generate_SipmNoisePDF_DB(tPath, table_fname):
    
    table = "SipmNoisePDF"
    print(f"Generating table {table} ...")

    #det_config = load_detector_config(det_name)
    
    # Getting header
    header_fname = f"{tPath}/{table}.h"
    with open(header_fname, 'r') as header_file:
        header = header_file.read() + "\n"
    with open(table_fname, 'w') as table_file:
        table_file.write(header)

    # Generating entries
    template = open("templates/SipmNoisePDF.entry").read()
    MinRun = det_config["MinRun"]
    MaxRun = "NULL"
    num_sipms = 0
    entries   = ""
    for label in det_config["SensorLabels"]:
        if "SiPM" in label:            
            noiseDB = det_config[label + "_NoiseDB"]
            noise, noise_bins, baselines = db.SiPMNoise(noiseDB[0], noiseDB[1])
            
            sipm_data    = db.DataSiPM(noiseDB[0], noiseDB[1])
            masked_sipms = sipm_data[sipm_data.Active == 0].index.to_numpy()
            
            for sensor in det_config[label]:
                num_sipms += 1
                SensorID   = sensor[0]
                # Randomly select a NEW SiPM pdf
                NEW_sensor_id = random.randint(0, 1791)
                while NEW_sensor_id in masked_sipms:
                    NEW_sensor_id = random.randint(0, 1791)
                noise_pdf = noise[NEW_sensor_id]
                
                for BinEnergyPes, Probability in zip(noise_bins, noise_pdf):
                    params   = locals()
                    entries += template.format(**params) + "\n"
                
                if(num_sipms % 10 == 0):
                    print(f"  SiPMs managed: {num_sipms}", end="\r")
                    with open(table_fname, 'a') as table_file:
                        table_file.write(entries)
                    entries=''

    ### Writing table
    with open(table_fname, 'a') as table_file:
        table_file.write(entries)

    print(f"Total SiPMs managed: {num_sipms}")

if __name__ == "__main__":
 
    ### Reading Detector Configuration
    det_config = load_detector_config(det_name)


    ### PATHs
    tPath = "./templates"
    oPath = f"{det_name}"
    if not os.path.isdir(oPath):
        os.makedirs(oPath)


    ### Generating tables
    for table in tables:
    
        print(f"Generating table {table} ...")
        table_fname  = f"{oPath}/{table}.sql"

        if table == "SipmNoisePDF":
            generate_SipmNoisePDF_DB(tPath, table_fname)
        else:
            # Getting header
            header_fname = f"{tPath}/{table}.h"
            with open(header_fname, 'r') as header_file:
                content = header_file.read() + "\n"

            # Add table registers
            if table   == "ChannelGain"    : content += get_ChannelGain_entries(det_config)
            elif table == "ChannelMapping" : content += get_ChannelMapping_entries(det_config)
            elif table == "ChannelPosition": content += get_ChannelPosition_entries(det_config)
            elif table == "DetectorGeo"    : content += get_DetectorGeo_entries(det_config)
            elif table == "SipmBaseline"   : content += get_SipmBaseline_entries(det_config)

            # Writing table
            with open(table_fname, 'w') as table_file:
                table_file.write(content)

    print("Done !!")

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
