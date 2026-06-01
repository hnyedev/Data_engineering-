-- Cargar datos de inseguridad de Yucatán desde archivos CSV
-- Ejecutar este script desde la base de datos warehouse

COPY bronze.raw_insecurity FROM '/data/DATAW.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',');