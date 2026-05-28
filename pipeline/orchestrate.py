from dagster import job, op
import os


@op
def ingest() -> str:
    exit_code = os.system("python pipeline/ingest.py")
    if exit_code != 0:
        raise Exception("L'ingestion a échoué.")
    return "OK"


@op
def validate(ingest_status: str) -> str:
    exit_code = os.system("python pipeline/validate.py")
    if exit_code != 0:
        raise Exception("La validation a échoué.")
    return "OK"


@op
def transform(validation_status: str) -> str:
    exit_code = os.system("cd dbt_pipeline && dbt run --profiles-dir .")
    if exit_code != 0:
        raise Exception("La transformation dbt a échoué.")
    return "OK"


@op
def test_data(transform_status: str) -> str:
    exit_code = os.system("cd dbt_pipeline && dbt test --profiles-dir .")
    if exit_code != 0:
        raise Exception("Les tests de données dbt ont échoué.")
    return "OK"


@job
def ventes_pipeline():
    # Chaînage strict des statuts d'exécution pour Dagster
    ingest_res = ingest()
    validate_res = validate(ingest_res)
    transform_res = transform(validate_res)
    test_data(transform_res)
