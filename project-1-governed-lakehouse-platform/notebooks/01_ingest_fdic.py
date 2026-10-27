# Databricks notebook source
# COMMAND ----------
# Public FDIC ingest. Creates nothing until a metastore exists.
# Device is irrelevant here; this is a SQL/API job, not a GPU job.

import json
from datetime import datetime, timezone

import requests

HOST = "https://api.fdic.gov/banks"
dbutils.widgets.text("catalog", "prod")  # noqa: F821
catalog = dbutils.widgets.get("catalog")  # noqa: F821


def fetch(dataset: str, fields: list[str], limit: int = 200, filters: str | None = None) -> list[dict]:
    params = {"fields": ",".join(fields), "limit": limit, "offset": 0}
    if filters:
        params["filters"] = filters
    response = requests.get(f"{HOST}/{dataset}", params=params, timeout=60)
    response.raise_for_status()
    body = response.json()
    return [row["data"] for row in body.get("data", [])]


failures = fetch("failures", ["NAME", "CERT", "FAILDATE", "CITY", "STATE", "QBFASSET"], limit=100)
institutions = fetch(
    "institutions",
    ["NAME", "CERT", "STALP", "CITY", "ASSET", "ACTIVE"],
    limit=100,
    filters="ACTIVE:1",
)
print(json.dumps({"failures": len(failures), "institutions": len(institutions), "at": datetime.now(timezone.utc).isoformat()}))

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")  # noqa: F821
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.bronze")  # noqa: F821
fail_df = spark.createDataFrame(failures)  # noqa: F821
fail_df.write.mode("overwrite").format("delta").saveAsTable(f"{catalog}.bronze.bank_failures")
inst_df = spark.createDataFrame(institutions)  # noqa: F821
inst_df.write.mode("overwrite").format("delta").saveAsTable(f"{catalog}.bronze.institutions")
print("wrote bronze tables")
