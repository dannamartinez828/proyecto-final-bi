import pandas as pd

ARCHIVO = "ParcialFinal_BI.xlsx"
SALIDA = "sql/01_insert_sensors_data_temp.sql"
LOTE = 1000  # máximo de filas por INSERT en SQL Server

df = pd.read_excel(ARCHIVO, sheet_name="Datos", header=None, dtype=str)
mapa = pd.read_excel(ARCHIVO, sheet_name="VALOR_SENSORES", dtype=str)
ids = dict(zip(mapa["DATO"].str.strip(), mapa["ID_SENSOR"].astype(int)))
id_resto = ids.pop("RESTO")

bloques = df.iloc[0, 2:95].str.strip()   # fila 1 del Excel: block_name
tipos = df.iloc[2, 2:95].str.strip()     # fila 3 del Excel: data_type
datos = df.iloc[3:].reset_index(drop=True)
fechas = datos[0].str.strip() + " " + datos[1].str.strip() + ":00"
fechas = pd.to_datetime(fechas).dt.strftime("%Y%m%d %H:%M:%S")

filas = []
for i, col in enumerate(range(2, 95)):
    b, t = bloques.iloc[i], tipos.iloc[i]
    id_s = ids.get(b, id_resto)
    serie = pd.to_numeric(datos[col], errors="coerce")
    for fecha, v in zip(fechas, serie):
        if pd.notna(v):  # data_value es NOT NULL: se omiten celdas vacías
            filas.append(f"({id_s},'{t}',{v:g},'{fecha}','{b}')")

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("USE deptmaintenance\nGO\nTRUNCATE TABLE dbo.tbl_sensors_data_temp\nGO\n")
    for i in range(0, len(filas), LOTE):
        f.write("INSERT INTO dbo.tbl_sensors_data_temp (id_sensor,data_type,data_value,data_date,block_name) VALUES\n")
        f.write(",\n".join(filas[i:i + LOTE]) + "\nGO\n")
    f.write("SELECT COUNT(*) AS total FROM dbo.tbl_sensors_data_temp\nGO\n")

print("filas generadas:", len(filas))
