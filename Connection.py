from hana_ml import ConnectionContext
import pandas as pd

# Dane połączenia
host = "9663b0fe-0111-4666-9825-03ece29f4327.hna0.prod-eu10.hanacloud.ondemand.com"
port = 443
user = "ZEO#SADOWNIKD"
password = "~k1a?cKt?kx#.~TZ8yyKW[0VJVqI%C,,"

# Nawiązanie połączenia
conn = ConnectionContext(
    address=host,
    port=port,
    user=user,
    password=password,
    encrypt=True  # wymagane dla SAP HANA Cloud
)

# Sprawdzenie połączenia
print(f"Połączono: {conn.connection.isconnected()}")
print(f"Wersja HANA: {conn.hana_version()}")

# Przykład zapytania
#cursor = conn.connection.cursor()
#cursor.execute("SELECT CURRENT_USER FROM DUMMY")
#print(f"Zalogowany jako: {cursor.fetchone()[0]}")


# Podłączenie do tabeli
# Schema to zazwyczaj nazwa Twojej przestrzeni (space) w Datasphere
df = conn.table("Test_view", schema="ZEO").collect()
print("Połączenie z ZEO nawiązane")



#Kod do transformacji w Data Flow
def transform(data):
    split_names = data['Name'].str.split(',', n=1, expand=True)
    data['first_name'] = split_names[0].str.strip().astype(str)
    data['last_name'] = split_names[1].str.strip().astype(str)
    data.drop(['Name'], axis=1, inplace=True)
    return data

#test
print(transform(df))

# Zamknięcie połączenia
conn.close()