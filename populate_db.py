
import sqlite3
from datetime import datetime
import random

conn = sqlite3.connect("wheelsets_demo.db")
cursor = conn.cursor()

cursor.executescript('''
    DROP TABLE IF EXISTS Wheelset_Master;
    DROP TABLE IF EXISTS Inspection_Log;
    DROP TABLE IF EXISTS Monitoring_Data;

    CREATE TABLE Wheelset_Master (
        Wheelset_ID TEXT PRIMARY KEY,
        Wagon_No TEXT,
        Install_Date TEXT,
        Current_Position TEXT,
        Total_Mileage INTEGER,
        Current_Condition TEXT,
        RUL_km INTEGER
    );

    CREATE TABLE Inspection_Log (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Wheelset_ID TEXT,
        Date TEXT,
        Inspector TEXT,
        Location TEXT,
        Diameter REAL,
        Flange_Height REAL,
        Flange_Thickness REAL,
        Damage_Notes TEXT
    );

    CREATE TABLE Monitoring_Data (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Wheelset_ID TEXT,
        Date TEXT,
        Source TEXT,
        Metric TEXT,
        Value REAL
    );
''')

sample_data = [
    ("52547/193", "7069552109", "2015-01-28", "A1", 183000, "Needs Maintenance", 9000),
    ("80979", "7069552810", "2015-02-03", "B2", 210000, "Good", 30000),
    ("19646/161", "7069552745", "2015-02-03", "A2", 245000, "Moderate", 12000),
    ("52547/162", "7069552000", "2015-02-18", "B1", 201000, "Good", 25000)
]

cursor.executemany("INSERT INTO Wheelset_Master VALUES (?, ?, ?, ?, ?, ?, ?)", sample_data)

for ws in sample_data:
    for _ in range(2):
        cursor.execute('''
            INSERT INTO Inspection_Log (Wheelset_ID, Date, Inspector, Location, Diameter, Flange_Height, Flange_Thickness, Damage_Notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ws[0], datetime.now().date(), "Inspector A", "Roberts Road",
            round(random.uniform(780, 820), 1),
            round(random.uniform(28, 35), 1),
            round(random.uniform(25, 33), 1),
            "Minor wear"
        ))
    for metric in ["WILD_Impact", "Temp_Sensor", "Out_Of_Round"]:
        cursor.execute('''
            INSERT INTO Monitoring_Data (Wheelset_ID, Date, Source, Metric, Value)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            ws[0], datetime.now().date(), "Trackside Sensor", metric, round(random.uniform(0.5, 1.5), 2)
        ))

conn.commit()
conn.close()
