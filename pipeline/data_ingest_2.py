import pandas as pd
from sqlalchemy import create_engine, text

# ----------------------------
# 1. DATABASE CONFIG
# ----------------------------
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"      # use "pgdatabase" if running inside Docker
DB_PORT = "5432"
DB_NAME = "ny_taxi"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=True   # shows SQL logs (good for debugging)
)

# ----------------------------
# 2. READ CSV
# ----------------------------
CSV_PATH = "taxi_zone_lookup.csv"

df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.lower()

print("CSV loaded successfully")
print("Rows:", len(df))
print(df.head())

# ----------------------------
# 3. CREATE TABLE (DDL)
# ----------------------------
create_table_sql = """
CREATE TABLE IF NOT EXISTS taxi_zone_lookup (
    locationid INTEGER PRIMARY KEY,
    borough TEXT,
    zone TEXT,
    service_zone TEXT
);
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    print("Table ensured")

# ----------------------------
# 4. REFRESH DATA (TRUNCATE + LOAD)
# ----------------------------
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE taxi_zone_lookup"))
    print("Table truncated")

df.to_sql(
    name="taxi_zone_lookup",
    con=engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("Data inserted successfully")

# ----------------------------
# 5. VERIFY LOAD
# ----------------------------
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM taxi_zone_lookup"))
    print("Total rows in table:", result.fetchone()[0])
