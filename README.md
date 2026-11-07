# Proyecto Final BI

Carga de datos de sensores desde Excel a SQL Server y una interfaz web con filtros.

## Contenido
- `ParcialFinal_BI.xlsx`: datos originales.
- `generar_inserts.py`: lee el Excel y genera `sql/01_insert_sensors_data_temp.sql`.
- `sql/`: scripts de la base de datos (ejecutar en este orden: `00a`, `00_create_table_tmp`, `01_insert`).
- `web/`: interfaz con filtros (fecha_inicio, fecha_fin, block_name, data_type).

## Cómo funciona
1. Fecha + Hora del Excel se concatenan en `data_date`.
2. `block_name` y `data_type` se toman de las filas 1 y 3 de cada columna del Excel.
3. `id_sensor` se asigna con la hoja `VALOR_SENSORES` (AG16=62, 35=63, J8=64, SM5=65, resto=0).
4. Las celdas vacías no se insertan porque `data_value` es NOT NULL: quedan 227.771 filas.

## Ejecutar
```
pip install pandas openpyxl
python generar_inserts.py
```
Luego ejecutar los 3 scripts de `sql/` en SSMS y:
```
cd web
npm install
node server.js
```
Abrir http://localhost:3000 (editar usuario y contraseña en `web/server.js`).
