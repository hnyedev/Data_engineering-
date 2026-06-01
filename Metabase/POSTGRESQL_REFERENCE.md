# Guía Completa de PostgreSQL para DBeaver

## Tabla de Contenidos
- [Gestión de Bases de Datos](#gestión-de-bases-de-datos)
- [Gestión de Schemas](#gestión-de-schemas)
- [Gestión de Tablas](#gestión-de-tablas)
- [Inserción de Datos](#inserción-de-datos)
- [Consultas (SELECT)](#consultas-select)
- [Actualización de Datos](#actualización-de-datos)
- [Eliminación de Datos](#eliminación-de-datos)
- [Índices](#índices)
- [Vistas](#vistas)
- [Funciones y Procedimientos](#funciones-y-procedimientos)
- [Transacciones](#transacciones)
- [Usuarios y Permisos](#usuarios-y-permisos)
- [Importación/Exportación](#importaciónexportación)
- [Consultas de Información del Sistema](#consultas-de-información-del-sistema)
- [Funciones de Agregación](#funciones-de-agregación)
- [Funciones de Fecha y Hora](#funciones-de-fecha-y-hora)
- [Expresiones Regulares y Pattern Matching](#expresiones-regulares-y-pattern-matching)
- [CTEs y Subconsultas](#ctes-y-subconsultas)
- [Optimización y Performance](#optimización-y-performance)

---

## Gestión de Bases de Datos

### Crear una base de datos
```sql
CREATE DATABASE nombre_db;
CREATE DATABASE nombre_db ENCODING 'UTF8';
```

### Listar bases de datos
```sql
SELECT datname FROM pg_database;
```

### Eliminar una base de datos
```sql
DROP DATABASE nombre_db;
DROP DATABASE IF EXISTS nombre_db;  -- No falla si no existe
```

### Cambiar configuración de base de datos
```sql
ALTER DATABASE nombre_db OWNER TO nuevo_usuario;
```

---

## Gestión de Schemas

### Crear un schema
```sql
CREATE SCHEMA nombre_schema;
CREATE SCHEMA IF NOT EXISTS nombre_schema;
```

### Listar schemas
```sql
SELECT schema_name FROM information_schema.schemata;
SELECT nspname FROM pg_namespace;
```

### Establecer search_path (schema por defecto)
```sql
SET search_path TO nombre_schema, public;
SHOW search_path;
```

### Eliminar un schema
```sql
DROP SCHEMA nombre_schema;
DROP SCHEMA nombre_schema CASCADE;  -- Elimina todo su contenido
```

---

## Gestión de Tablas

### Crear tabla
```sql
CREATE TABLE nombre_tabla (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INTEGER,
    email VARCHAR(255) UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT true
);
```

### Crear tabla en un schema específico
```sql
CREATE TABLE schema.nombre_tabla (
    id SERIAL PRIMARY KEY,
    columna VARCHAR(50)
);
```

### Crear tabla desde otra tabla
```sql
CREATE TABLE nueva_tabla AS
SELECT * FROM tabla_existente;

-- Solo estructura, sin datos
CREATE TABLE nueva_tabla AS
SELECT * FROM tabla_existente WHERE 1=0;
```

### Ver estructura de tabla
```sql
\d nombre_tabla  -- En psql
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'nombre_tabla';
```

### Listar todas las tablas
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

### Modificar tabla (ALTER TABLE)

#### Agregar columna
```sql
ALTER TABLE nombre_tabla ADD COLUMN nueva_columna VARCHAR(50);
ALTER TABLE nombre_tabla ADD COLUMN nueva_columna INTEGER DEFAULT 0;
```

#### Eliminar columna
```sql
ALTER TABLE nombre_tabla DROP COLUMN nombre_columna;
ALTER TABLE nombre_tabla DROP COLUMN IF EXISTS nombre_columna;
```

#### Renombrar columna
```sql
ALTER TABLE nombre_tabla RENAME COLUMN nombre_viejo TO nombre_nuevo;
```

#### Cambiar tipo de datos
```sql
ALTER TABLE nombre_tabla ALTER COLUMN columna TYPE VARCHAR(200);
ALTER TABLE nombre_tabla ALTER COLUMN columna TYPE INTEGER USING columna::INTEGER;
```

#### Agregar constraint
```sql
ALTER TABLE nombre_tabla ADD CONSTRAINT pk_id PRIMARY KEY (id);
ALTER TABLE nombre_tabla ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE nombre_tabla ADD CONSTRAINT check_edad CHECK (edad >= 18);
ALTER TABLE nombre_tabla ADD CONSTRAINT unique_email UNIQUE (email);
```

#### Eliminar constraint
```sql
ALTER TABLE nombre_tabla DROP CONSTRAINT nombre_constraint;
```

#### Renombrar tabla
```sql
ALTER TABLE nombre_viejo RENAME TO nombre_nuevo;
```

### Eliminar tabla
```sql
DROP TABLE nombre_tabla;
DROP TABLE IF EXISTS nombre_tabla;
DROP TABLE nombre_tabla CASCADE;  -- Elimina dependencias
```

### Truncar tabla (eliminar todos los datos)
```sql
TRUNCATE TABLE nombre_tabla;
TRUNCATE TABLE nombre_tabla RESTART IDENTITY;  -- Reinicia secuencias
TRUNCATE TABLE nombre_tabla CASCADE;  -- Trunca tablas relacionadas
```

---

## Inserción de Datos

### INSERT básico
```sql
INSERT INTO tabla (columna1, columna2) VALUES ('valor1', 'valor2');
```

### INSERT múltiple
```sql
INSERT INTO tabla (columna1, columna2) VALUES
    ('valor1', 'valor2'),
    ('valor3', 'valor4'),
    ('valor5', 'valor6');
```

### INSERT desde SELECT
```sql
INSERT INTO tabla_destino (columna1, columna2)
SELECT columna1, columna2 FROM tabla_origen WHERE condicion;
```

### INSERT con RETURNING
```sql
INSERT INTO tabla (columna1) VALUES ('valor') RETURNING id;
INSERT INTO tabla (columna1) VALUES ('valor') RETURNING *;
```

### INSERT ... ON CONFLICT (UPSERT)
```sql
INSERT INTO tabla (id, nombre, valor) VALUES (1, 'Juan', 100)
ON CONFLICT (id) DO UPDATE SET
    nombre = EXCLUDED.nombre,
    valor = EXCLUDED.valor;

-- No hacer nada si hay conflicto
INSERT INTO tabla (id, nombre) VALUES (1, 'Juan')
ON CONFLICT (id) DO NOTHING;
```

---

## Consultas (SELECT)

### SELECT básico
```sql
SELECT * FROM tabla;
SELECT columna1, columna2 FROM tabla;
SELECT DISTINCT columna FROM tabla;
```

### WHERE (filtros)
```sql
SELECT * FROM tabla WHERE columna = 'valor';
SELECT * FROM tabla WHERE edad > 18;
SELECT * FROM tabla WHERE edad BETWEEN 18 AND 65;
SELECT * FROM tabla WHERE nombre IN ('Juan', 'María', 'Pedro');
SELECT * FROM tabla WHERE nombre LIKE 'J%';  -- Comienza con J
SELECT * FROM tabla WHERE nombre LIKE '%an%';  -- Contiene 'an'
SELECT * FROM tabla WHERE columna IS NULL;
SELECT * FROM tabla WHERE columna IS NOT NULL;
```

### Operadores lógicos
```sql
SELECT * FROM tabla WHERE edad > 18 AND activo = true;
SELECT * FROM tabla WHERE ciudad = 'Madrid' OR ciudad = 'Barcelona';
SELECT * FROM tabla WHERE NOT (edad < 18);
```

### ORDER BY (ordenamiento)
```sql
SELECT * FROM tabla ORDER BY columna ASC;   -- Ascendente
SELECT * FROM tabla ORDER BY columna DESC;  -- Descendente
SELECT * FROM tabla ORDER BY columna1 ASC, columna2 DESC;
```

### LIMIT y OFFSET (paginación)
```sql
SELECT * FROM tabla LIMIT 10;
SELECT * FROM tabla LIMIT 10 OFFSET 20;  -- Salta 20 registros
SELECT * FROM tabla ORDER BY id LIMIT 5;
```

### JOINs

#### INNER JOIN
```sql
SELECT a.*, b.columna
FROM tabla_a a
INNER JOIN tabla_b b ON a.id = b.tabla_a_id;
```

#### LEFT JOIN
```sql
SELECT a.*, b.columna
FROM tabla_a a
LEFT JOIN tabla_b b ON a.id = b.tabla_a_id;
```

#### RIGHT JOIN
```sql
SELECT a.*, b.columna
FROM tabla_a a
RIGHT JOIN tabla_b b ON a.id = b.tabla_a_id;
```

#### FULL OUTER JOIN
```sql
SELECT a.*, b.columna
FROM tabla_a a
FULL OUTER JOIN tabla_b b ON a.id = b.tabla_a_id;
```

#### CROSS JOIN
```sql
SELECT * FROM tabla_a CROSS JOIN tabla_b;
```

#### SELF JOIN
```sql
SELECT a.nombre, b.nombre as manager
FROM empleados a
LEFT JOIN empleados b ON a.manager_id = b.id;
```

### GROUP BY
```sql
SELECT columna, COUNT(*) FROM tabla GROUP BY columna;
SELECT ciudad, AVG(edad) FROM usuarios GROUP BY ciudad;
SELECT ciudad, COUNT(*) as total
FROM usuarios
GROUP BY ciudad
HAVING COUNT(*) > 5;
```

### HAVING
```sql
SELECT ciudad, COUNT(*) as total
FROM usuarios
GROUP BY ciudad
HAVING COUNT(*) > 10;
```

---

## Actualización de Datos

### UPDATE básico
```sql
UPDATE tabla SET columna = 'nuevo_valor' WHERE condicion;
```

### UPDATE múltiples columnas
```sql
UPDATE tabla
SET columna1 = 'valor1',
    columna2 = 'valor2'
WHERE id = 1;
```

### UPDATE desde otra tabla
```sql
UPDATE tabla_a
SET columna = tabla_b.valor
FROM tabla_b
WHERE tabla_a.id = tabla_b.tabla_a_id;
```

### UPDATE con RETURNING
```sql
UPDATE tabla
SET columna = 'nuevo_valor'
WHERE id = 1
RETURNING *;
```

---

## Eliminación de Datos

### DELETE básico
```sql
DELETE FROM tabla WHERE condicion;
```

### DELETE con JOIN
```sql
DELETE FROM tabla_a
USING tabla_b
WHERE tabla_a.id = tabla_b.tabla_a_id
AND tabla_b.condicion = 'valor';
```

### DELETE con RETURNING
```sql
DELETE FROM tabla WHERE id = 1 RETURNING *;
```

### DELETE todos los registros
```sql
DELETE FROM tabla;  -- Lento, puede usar TRUNCATE en su lugar
```

---

## Índices

### Crear índice
```sql
CREATE INDEX idx_columna ON tabla(columna);
CREATE INDEX idx_nombre ON usuarios(nombre);
```

### Índice único
```sql
CREATE UNIQUE INDEX idx_email ON usuarios(email);
```

### Índice compuesto
```sql
CREATE INDEX idx_compuesto ON tabla(columna1, columna2);
```

### Índice parcial
```sql
CREATE INDEX idx_activos ON usuarios(nombre) WHERE activo = true;
```

### Índice con expresión
```sql
CREATE INDEX idx_lower_email ON usuarios(LOWER(email));
```

### Listar índices
```sql
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public';
```

### Eliminar índice
```sql
DROP INDEX idx_nombre;
DROP INDEX IF EXISTS idx_nombre;
```

---

## Vistas

### Crear vista
```sql
CREATE VIEW vista_usuarios AS
SELECT id, nombre, email FROM usuarios WHERE activo = true;
```

### Crear o reemplazar vista
```sql
CREATE OR REPLACE VIEW vista_usuarios AS
SELECT id, nombre, email, ciudad FROM usuarios WHERE activo = true;
```

### Vista materializada
```sql
CREATE MATERIALIZED VIEW mv_stats AS
SELECT ciudad, COUNT(*) as total
FROM usuarios
GROUP BY ciudad;

-- Refrescar vista materializada
REFRESH MATERIALIZED VIEW mv_stats;
```

### Listar vistas
```sql
SELECT table_name
FROM information_schema.views
WHERE table_schema = 'public';
```

### Eliminar vista
```sql
DROP VIEW vista_usuarios;
DROP VIEW IF EXISTS vista_usuarios;
```

---

## Funciones y Procedimientos

### Crear función
```sql
CREATE OR REPLACE FUNCTION calcular_edad(fecha_nacimiento DATE)
RETURNS INTEGER AS $$
BEGIN
    RETURN EXTRACT(YEAR FROM AGE(fecha_nacimiento));
END;
$$ LANGUAGE plpgsql;

-- Usar función
SELECT calcular_edad('1990-01-01');
```

### Función con múltiples parámetros
```sql
CREATE OR REPLACE FUNCTION sumar(a INTEGER, b INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN a + b;
END;
$$ LANGUAGE plpgsql;
```

### Función que retorna tabla
```sql
CREATE OR REPLACE FUNCTION usuarios_por_ciudad(ciudad_param VARCHAR)
RETURNS TABLE(id INTEGER, nombre VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.nombre, u.email
    FROM usuarios u
    WHERE u.ciudad = ciudad_param;
END;
$$ LANGUAGE plpgsql;

-- Usar
SELECT * FROM usuarios_por_ciudad('Madrid');
```

### Crear procedimiento
```sql
CREATE OR REPLACE PROCEDURE actualizar_precios(porcentaje DECIMAL)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE productos SET precio = precio * (1 + porcentaje/100);
    COMMIT;
END;
$$;

-- Ejecutar procedimiento
CALL actualizar_precios(10);
```

### Listar funciones
```sql
SELECT routine_name
FROM information_schema.routines
WHERE routine_type = 'FUNCTION' AND routine_schema = 'public';
```

### Eliminar función
```sql
DROP FUNCTION calcular_edad(DATE);
DROP FUNCTION IF EXISTS calcular_edad(DATE);
```

---

## Transacciones

### BEGIN, COMMIT, ROLLBACK
```sql
BEGIN;
UPDATE cuentas SET saldo = saldo - 100 WHERE id = 1;
UPDATE cuentas SET saldo = saldo + 100 WHERE id = 2;
COMMIT;

-- Con rollback en caso de error
BEGIN;
UPDATE cuentas SET saldo = saldo - 100 WHERE id = 1;
-- Si hay error:
ROLLBACK;
```

### Savepoints
```sql
BEGIN;
UPDATE tabla SET columna = 'valor1' WHERE id = 1;
SAVEPOINT sp1;
UPDATE tabla SET columna = 'valor2' WHERE id = 2;
ROLLBACK TO SAVEPOINT sp1;
COMMIT;
```

---

## Usuarios y Permisos

### Crear usuario
```sql
CREATE USER nombre_usuario WITH PASSWORD 'contraseña';
CREATE USER nombre_usuario WITH PASSWORD 'contraseña' CREATEDB;
```

### Modificar usuario
```sql
ALTER USER nombre_usuario WITH PASSWORD 'nueva_contraseña';
ALTER USER nombre_usuario WITH SUPERUSER;
```

### Eliminar usuario
```sql
DROP USER nombre_usuario;
DROP USER IF EXISTS nombre_usuario;
```

### Otorgar permisos

#### Permisos en base de datos
```sql
GRANT ALL PRIVILEGES ON DATABASE nombre_db TO usuario;
GRANT CONNECT ON DATABASE nombre_db TO usuario;
```

#### Permisos en schema
```sql
GRANT ALL PRIVILEGES ON SCHEMA nombre_schema TO usuario;
GRANT USAGE ON SCHEMA nombre_schema TO usuario;
```

#### Permisos en tabla
```sql
GRANT ALL PRIVILEGES ON TABLE tabla TO usuario;
GRANT SELECT ON TABLE tabla TO usuario;
GRANT SELECT, INSERT, UPDATE ON TABLE tabla TO usuario;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO usuario;
```

#### Permisos en secuencias
```sql
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO usuario;
```

#### Permisos por defecto
```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO usuario;

ALTER DEFAULT PRIVILEGES FOR ROLE usuario IN SCHEMA public
GRANT ALL ON TABLES TO usuario;
```

### Revocar permisos
```sql
REVOKE ALL PRIVILEGES ON TABLE tabla FROM usuario;
REVOKE SELECT ON TABLE tabla FROM usuario;
```

### Ver permisos
```sql
-- Permisos en tablas
SELECT grantee, privilege_type
FROM information_schema.table_privileges
WHERE table_name = 'nombre_tabla';

-- Permisos de usuario
\du nombre_usuario  -- En psql
```

---

## Importación/Exportación

### COPY - Importar CSV
```sql
COPY tabla(columna1, columna2)
FROM '/ruta/archivo.csv'
DELIMITER ','
CSV HEADER;

-- Sin header
COPY tabla(columna1, columna2)
FROM '/ruta/archivo.csv'
DELIMITER ',';
```

### COPY - Exportar a CSV
```sql
COPY tabla TO '/ruta/archivo.csv' DELIMITER ',' CSV HEADER;
COPY (SELECT * FROM tabla WHERE condicion)
TO '/ruta/archivo.csv' DELIMITER ',' CSV HEADER;
```

### Importar con \copy (en psql, lee desde cliente)
```sql
\copy tabla FROM '/ruta/archivo.csv' DELIMITER ',' CSV HEADER
```

---

## Consultas de Información del Sistema

### Información de tablas
```sql
-- Listar todas las tablas
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Tamaño de tabla
SELECT pg_size_pretty(pg_total_relation_size('nombre_tabla'));

-- Información de columnas
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'nombre_tabla';
```

### Información de base de datos
```sql
-- Tamaño de base de datos
SELECT pg_size_pretty(pg_database_size('nombre_db'));

-- Bases de datos y sus tamaños
SELECT datname, pg_size_pretty(pg_database_size(datname))
FROM pg_database;
```

### Estadísticas de tablas
```sql
SELECT schemaname, tablename, n_live_tup as filas
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

### Ver consultas en ejecución
```sql
SELECT pid, usename, state, query
FROM pg_stat_activity
WHERE state = 'active';
```

### Cancelar/Terminar consultas
```sql
-- Cancelar consulta
SELECT pg_cancel_backend(pid);

-- Terminar conexión
SELECT pg_terminate_backend(pid);
```

### Ver versión de PostgreSQL
```sql
SELECT version();
SHOW server_version;
```

---

## Funciones de Agregación

### Funciones básicas
```sql
SELECT COUNT(*) FROM tabla;
SELECT COUNT(columna) FROM tabla;  -- No cuenta NULLs
SELECT COUNT(DISTINCT columna) FROM tabla;
SELECT SUM(columna) FROM tabla;
SELECT AVG(columna) FROM tabla;
SELECT MIN(columna) FROM tabla;
SELECT MAX(columna) FROM tabla;
```

### Funciones avanzadas
```sql
-- Concatenar strings
SELECT STRING_AGG(nombre, ', ') FROM usuarios;
SELECT STRING_AGG(nombre, ', ' ORDER BY nombre) FROM usuarios;

-- Array de valores
SELECT ARRAY_AGG(nombre) FROM usuarios;

-- Desviación estándar
SELECT STDDEV(columna) FROM tabla;
SELECT VARIANCE(columna) FROM tabla;
```

---

## Funciones de Fecha y Hora

### Fecha y hora actual
```sql
SELECT CURRENT_DATE;
SELECT CURRENT_TIME;
SELECT CURRENT_TIMESTAMP;
SELECT NOW();
```

### Extraer partes de fecha
```sql
SELECT EXTRACT(YEAR FROM fecha_columna) FROM tabla;
SELECT EXTRACT(MONTH FROM fecha_columna) FROM tabla;
SELECT EXTRACT(DAY FROM fecha_columna) FROM tabla;
SELECT DATE_PART('year', fecha_columna) FROM tabla;
```

### Operaciones con fechas
```sql
-- Sumar días
SELECT fecha + INTERVAL '7 days';
SELECT fecha + INTERVAL '1 month';
SELECT fecha + INTERVAL '1 year';

-- Restar fechas
SELECT AGE(fecha_fin, fecha_inicio);
SELECT fecha_fin - fecha_inicio;  -- Retorna intervalo

-- Formatear fechas
SELECT TO_CHAR(fecha, 'DD/MM/YYYY') FROM tabla;
SELECT TO_CHAR(fecha, 'YYYY-MM-DD HH24:MI:SS') FROM tabla;

-- Convertir string a fecha
SELECT TO_DATE('2024-01-15', 'YYYY-MM-DD');
SELECT TO_TIMESTAMP('2024-01-15 10:30:00', 'YYYY-MM-DD HH24:MI:SS');
```

### Funciones útiles
```sql
-- Truncar fecha
SELECT DATE_TRUNC('day', timestamp_columna);
SELECT DATE_TRUNC('month', timestamp_columna);
SELECT DATE_TRUNC('year', timestamp_columna);

-- Edad desde fecha
SELECT AGE(fecha_nacimiento);
SELECT EXTRACT(YEAR FROM AGE(fecha_nacimiento)) as edad;
```

---

## Expresiones Regulares y Pattern Matching

### LIKE y ILIKE
```sql
SELECT * FROM tabla WHERE columna LIKE 'patrón%';   -- Case sensitive
SELECT * FROM tabla WHERE columna ILIKE 'patrón%';  -- Case insensitive

-- Wildcards
-- % = cualquier cantidad de caracteres
-- _ = un solo carácter
SELECT * FROM tabla WHERE nombre LIKE 'J%';      -- Comienza con J
SELECT * FROM tabla WHERE nombre LIKE '%ez';     -- Termina con ez
SELECT * FROM tabla WHERE nombre LIKE '%an%';    -- Contiene 'an'
SELECT * FROM tabla WHERE nombre LIKE 'J__n';    -- J + 2 chars + n
```

### Expresiones regulares
```sql
-- ~ (case sensitive), ~* (case insensitive)
SELECT * FROM tabla WHERE columna ~ '^[A-Z]';        -- Comienza con mayúscula
SELECT * FROM tabla WHERE columna ~* '^[a-z]+$';     -- Solo letras minúsculas
SELECT * FROM tabla WHERE email ~ '^[^@]+@[^@]+\.[^@]+$';  -- Validar email

-- Negación: !~ y !~*
SELECT * FROM tabla WHERE columna !~ '[0-9]';        -- No contiene números
```

### Funciones de string
```sql
SELECT UPPER(columna) FROM tabla;
SELECT LOWER(columna) FROM tabla;
SELECT CONCAT(columna1, ' ', columna2) FROM tabla;
SELECT columna1 || ' ' || columna2 FROM tabla;  -- Concatenación
SELECT LENGTH(columna) FROM tabla;
SELECT SUBSTRING(columna FROM 1 FOR 5) FROM tabla;
SELECT TRIM(columna) FROM tabla;
SELECT REPLACE(columna, 'viejo', 'nuevo') FROM tabla;
SELECT SPLIT_PART('a,b,c', ',', 2);  -- Retorna 'b'
```

---

## CTEs y Subconsultas

### Common Table Expressions (WITH)
```sql
WITH usuarios_activos AS (
    SELECT * FROM usuarios WHERE activo = true
)
SELECT * FROM usuarios_activos WHERE ciudad = 'Madrid';

-- Múltiples CTEs
WITH
    activos AS (SELECT * FROM usuarios WHERE activo = true),
    madrid AS (SELECT * FROM activos WHERE ciudad = 'Madrid')
SELECT * FROM madrid;
```

### CTE Recursivo
```sql
WITH RECURSIVE contador AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM contador WHERE n < 10
)
SELECT * FROM contador;

-- Jerarquías
WITH RECURSIVE jerarquia AS (
    SELECT id, nombre, manager_id, 1 as nivel
    FROM empleados
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.nombre, e.manager_id, j.nivel + 1
    FROM empleados e
    INNER JOIN jerarquia j ON e.manager_id = j.id
)
SELECT * FROM jerarquia;
```

### Subconsultas
```sql
-- En WHERE
SELECT * FROM usuarios
WHERE ciudad IN (SELECT ciudad FROM ciudades WHERE pais = 'España');

-- En SELECT
SELECT nombre, (SELECT COUNT(*) FROM pedidos WHERE user_id = usuarios.id) as total_pedidos
FROM usuarios;

-- En FROM
SELECT promedio.ciudad, promedio.edad_promedio
FROM (
    SELECT ciudad, AVG(edad) as edad_promedio
    FROM usuarios
    GROUP BY ciudad
) as promedio
WHERE promedio.edad_promedio > 30;

-- EXISTS
SELECT * FROM usuarios u
WHERE EXISTS (SELECT 1 FROM pedidos p WHERE p.user_id = u.id);
```

---

## Optimización y Performance

### EXPLAIN y ANALYZE
```sql
EXPLAIN SELECT * FROM tabla WHERE columna = 'valor';
EXPLAIN ANALYZE SELECT * FROM tabla WHERE columna = 'valor';
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM tabla;
```

### Vacuum y Analyze
```sql
VACUUM tabla;
VACUUM FULL tabla;
VACUUM ANALYZE tabla;
ANALYZE tabla;
```

### Reindexar
```sql
REINDEX TABLE tabla;
REINDEX INDEX idx_nombre;
REINDEX DATABASE nombre_db;
```

### Configuración de memoria
```sql
-- Ver configuración
SHOW shared_buffers;
SHOW work_mem;
SHOW maintenance_work_mem;

-- Establecer para sesión actual
SET work_mem = '256MB';
```

### Locks y bloqueos
```sql
-- Ver locks activos
SELECT * FROM pg_locks;

-- Ver bloqueos con queries
SELECT l.*, a.query
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid;
```

---

## Comandos Especiales para DBeaver

### Ejecutar script completo
- Ctrl + Alt + X (Windows/Linux)
- Cmd + Alt + X (Mac)

### Ejecutar statement actual
- Ctrl + Enter (Windows/Linux)
- Cmd + Enter (Mac)

### Formatear SQL
- Ctrl + Shift + F (Windows/Linux)
- Cmd + Shift + F (Mac)

### Autocompletar
- Ctrl + Space

### Ver Plan de Ejecución
- Ctrl + Shift + E (Windows/Linux)
- Cmd + Shift + E (Mac)

---

## Tips y Buenas Prácticas

1. **Siempre usa transacciones para cambios importantes**
   ```sql
   BEGIN;
   -- tus cambios
   COMMIT;  -- o ROLLBACK si hay error
   ```

2. **Usa índices en columnas de búsqueda frecuente**
   ```sql
   CREATE INDEX idx_email ON usuarios(email);
   ```

3. **Evita SELECT * en producción**
   ```sql
   -- Mal
   SELECT * FROM tabla;

   -- Bien
   SELECT id, nombre, email FROM tabla;
   ```

4. **Usa LIMIT para probar queries**
   ```sql
   SELECT * FROM tabla_grande LIMIT 10;
   ```

5. **Comenta tu código SQL**
   ```sql
   -- Este query obtiene usuarios activos de Madrid
   SELECT * FROM usuarios WHERE activo = true AND ciudad = 'Madrid';

   /* Query complejo para reportes
      que hace múltiples cálculos */
   ```

6. **Nombra constraints explícitamente**
   ```sql
   ALTER TABLE usuarios
   ADD CONSTRAINT pk_usuarios_id PRIMARY KEY (id);
   ```

7. **Usa schemas para organizar**
   ```sql
   CREATE SCHEMA analytics;
   CREATE TABLE analytics.reportes (...);
   ```

8. **Backup antes de cambios grandes**
   ```sql
   -- En terminal
   pg_dump -U usuario -d nombre_db > backup.sql
   ```
