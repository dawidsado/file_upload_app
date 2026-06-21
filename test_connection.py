import requests

HOST  = "https://dbc-b46bbf5e-b6bf.cloud.databricks.com"
TOKEN = "dapi6667262808ec4f27e5848f62e7711e51"

response = requests.get(
    f"{HOST}/api/2.0/clusters/list",
    headers={"Authorization": f"Bearer {TOKEN}"}
)

print(response.status_code)
print(response.json())