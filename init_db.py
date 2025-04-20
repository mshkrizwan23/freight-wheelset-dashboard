import sqlite3
from datetime import datetime
import random

# Connect to database
conn = sqlite3.connect("wheelsets_demo.db")
cursor = conn.cursor()

# Create tables
cursor.executescript("""
DROP TABLE IF EXISTS Wheelset_Master;
DROP TABLE IF EXISTS Inspection_Log;
DROP TABLE IF EXISTS Monitoring_Data;
DROP TABLE IF EXISTS Maintenance_Log;
DROP TABLE IF EXISTS Wagon_Operational_Log;

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
    Damage_Notes TEXT,
    Image_Path TEXT
);

CREATE TABLE Monitoring_Data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Wheelset_ID TEXT,
    Date TEXT,
    Source TEXT,
    Metric TEXT,
    Value REAL,
    Flag TEXT
);

CREATE TABLE Wagon_Operational_Log (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Wheelset_ID TEXT,
    Wagon_No TEXT,
    Date TEXT,
    Mileage_This_Month INTEGER
);

CREATE TABLE Maintenance_Log (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Wheelset_ID TEXT,
    Date TEXT,
    Action TEXT,
    Reason TEXT,
    Location TEXT
);
""")

# Populate demo wheelsets
wheelsets = [
    {
        "Wheelset_ID": "52547/193",
        "Wagon_No": "7069552109",
        "Install_Date": "2015-01-28",
        "Current_Position": "A1",
        "Total_Mileage": 183000,
        "Current_Condition": "Needs Maintenance",
        "RUL_km": 9000
    },
    {
        "Wheelset_ID": "80979",
        "Wagon_No": "7069552810",
        "Install_Date": "2015-02-03",
        "Current_Position": "B2",
        "Total_Mileage": 210000,
        "Current_Condition": "Good",
        "RUL_km": 30000
    },
    {
        "Wheelset_ID": "19646/161",
        "Wagon_No": "7069552745",
        "Install_Date": "2015-02-03",
        "Current_Position": "A2",
        "Total_Mileage": 245000,
        "Current_Condition": "Moderate",
        "RUL_km": 12000
    }
]

for ws in wheelsets:
    cursor.execute("""
        INSERT INTO Wheelset_Master (Wheelset_ID, Wagon_No, Install_Date, Current_Position, Total_Mileage, Current_Condition, RUL_km)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        ws["Wheelset_ID"], ws["Wagon_No"], ws["Install_Date"], ws["Current_Position"],
        ws["Total_Mileage"], ws["Current_Condition"], ws["RUL_km"]
    ))

    # Add inspection logs
    for _ in range(2):
        cursor.execute("""
            INSERT INTO Inspection_Log (Wheelset_ID, Date, Inspector, Location, Diameter, Flange_Height, Flange_Thickness, Damage_Notes, Image_Path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ws["Wheelset_ID"],
            ws["Install_Date"],
            "Inspector A",
            "Roberts Road",
            round(random.uniform(780, 820), 1),
            round(random.uniform(28, 35), 1),
            round(random.uniform(25, 33), 1),
            "Wear - visual inspection",
            ""
        ))

    # Add monitoring data with occasional flags
    for metric in ["WILD_Impact", "Temp_Sensor", "Out_Of_Round"]:
        val = round(random.uniform(0.5, 1.7), 2)
        flag = "ALERT" if val > 1.4 else ""
        cursor.execute("""
            INSERT INTO Monitoring_Data (Wheelset_ID, Date, Source, Metric, Value, Flag)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ws["Wheelset_ID"],
            datetime.now().strftime("%Y-%m-%d"),
            "Trackside Sensor",
            metric,
            val,
            flag
        ))

    # Add wagon operational logs
    for m in range(1, 4):
        cursor.execute("""
            INSERT INTO Wagon_Operational_Log (Wheelset_ID, Wagon_No, Date, Mileage_This_Month)
            VALUES (?, ?, ?, ?)
        """, (
            ws["Wheelset_ID"],
            ws["Wagon_No"],
            f"2024-{m:02d}-01",
            random.randint(4000, 8000)
        ))

    # Add maintenance record
    cursor.execute("""
        INSERT INTO Maintenance_Log (Wheelset_ID, Date, Action, Reason, Location)
        VALUES (?, ?, ?, ?, ?)
    """, (
        ws["Wheelset_ID"],
        "2024-12-10",
        "Re-profile",
        "Excessive flange wear",
        "Crewe Depot"
    ))

conn.commit()
conn.close()

print("✅ All tables created and populated successfully.")
