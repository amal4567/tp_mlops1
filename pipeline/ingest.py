import pandas as pd
import duckdb
from pathlib import Path

csv_path = Path("data/ventes.csv")
db_path = "ventes.duckdb"

# Chargement du fichier CSV local
df = pd.read_csv(csv_path)

# Connexion à la base DuckDB locale et chargement
con = duckdb.connect(db_path)
con.execute("CREATE OR REPLACE TABLE ventes_raw AS SELECT * FROM df")
con.close()

print("Ingestion terminée : ventes_raw créée avec succès dans DuckDB")
