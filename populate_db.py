import sqlite3
from datetime import datetime
import random

conn = sqlite3.connect("wheelsets_demo.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS Wheelset_Master (
    Wheelset_ID TEXT PRIMARY KEY,
    Wagon_No TEXT,
    Install_Date DATE,
    Current_Position TEXT,
    Total_Mileage INTEGER,
    Current_Condition TEXT,
    RUL_km INTEGER
);

CREATE TABLE IF NOT EXISTS Inspection_Log (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Wheelset_ID TEXT,
    Date DATE,
    Inspector TEXT,
    Location TEXT,
    Diameter REAL,
    Flange_Height REAL,
    Flange_Thickness REAL,
    Damage_Notes TEXT,
    Image_Path TEXT
);

CREATE TABLE IF NOT EXISTS Monitoring_Data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Wheelset_ID TEXT,
    Date DATE,
    Source TEXT,
    Metric TEXT,
    Value REAL
);
""")

sample_wheelsets = [
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
    }
]

for ws in sample_wheelsets:
    cursor.execute(
        "INSERT OR REPLACE INTO Wheelset_Master VALUES (?, ?, ?, ?, ?, ?, ?)",
        tuple(ws.values())
    )

for ws in sample_wheelsets:
    for _ in range(2):
        cursor.execute(
            "INSERT INTO Inspection_Log (Wheelset_ID, Date, Inspector, Location, Diameter, Flange_Height, Flange_Thickness, Damage_Notes, Image_Path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                ws["Wheelset_ID"],
                datetime.strptime(ws["Install_Date"], "%Y-%m-%d").date(),
                "Inspector A",
                "Roberts Road",
                round(random.uniform(780, 820), 1),
                round(random.uniform(28, 35), 1),
                round(random.uniform(25, 33), 1),
                "Wear - visual inspection",
                ""
            )
        )

    for metric in ["WILD_Impact", "Temp_Sensor", "Out_Of_Round"]:
        cursor.execute(
            "INSERT INTO Monitoring_Data (Wheelset_ID, Date, Source, Metric, Value) VALUES (?, ?, ?, ?, ?)",
            (
                ws["Wheelset_ID"],
                datetime.now().strftime("%Y-%m-%d"),
                "Trackside Sensor",
                metric,
                round(random.uniform(0.5, 1.5), 2)
            )
        )

conn.commit()
conn.close()
print("✅ Demo data inserted.")
