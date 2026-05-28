import duckdb

db_path = "ventes.duckdb"
required_columns = {"date", "produit", "categorie",
                    "quantite", "prix_unitaire", "ville"}

# Connexion à DuckDB
con = duckdb.connect(db_path)
columns = con.execute("DESCRIBE ventes_raw").fetchall()
existing_columns = {col[0] for col in columns}

# 1. Vérification du schéma
missing = required_columns - existing_columns
if missing:
    raise ValueError(f"Colonnes obligatoires manquantes : {missing}")

# 2. Vérification des valeurs nulles sur les champs critiques
null_count = con.execute("""
    SELECT COUNT(*) FROM ventes_raw
    WHERE produit IS NULL OR quantite IS NULL OR prix_unitaire IS NULL
""").fetchone()[0]
con.close()

if null_count > 0:
    raise ValueError(
        f"Données invalides : {null_count} ligne(s) incomplète(s)")
else:
    print("Validation réussie : schéma et qualité minimale OK")
