-- Crear tabla raw_insecurity en el schema bronze
CREATE TABLE bronze.raw_insecurity (
    nom_ent VARCHAR(100),
    nom_mun VARCHAR(100),
    cd VARCHAR(100),
    total_registered INTEGER,
    total_secure INTEGER,
    total_insecure INTEGER,
    no_answer INTEGER,
    percentage_secure DECIMAL(5,2),
    percentage_insecure DECIMAL(5,2),
    percentage_no_answer DECIMAL(5,2),
    qq_yy VARCHAR(10)
);

-- Otorgar permisos al usuario data_engineer
GRANT ALL PRIVILEGES ON TABLE bronze.raw_insecurity TO data_engineer;
