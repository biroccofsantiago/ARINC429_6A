# CRUD de instrumentos ARINC429_6A

Aplicación de consola en Python para crear, listar, modificar y eliminar
instrumentos en MySQL.

## Preparar MySQL

Desde el repositorio, crear la base de datos y la tabla solicitadas:

```bash
sudo mysql < schema.sql
```

Para no conectar la aplicación como `root`, crear un usuario de aplicación
desde la consola de MySQL (`sudo mysql`), reemplazando la contraseña de ejemplo:

```sql
CREATE USER 'arinc429_app'@'localhost' IDENTIFIED BY 'elegi_una_clave';
GRANT SELECT, INSERT, UPDATE, DELETE ON ARINC429_6A.* TO 'arinc429_app'@'localhost';
```

## Instalar y ejecutar

```bash
python3 -m pip install -r requirements.txt
export MYSQL_USER=arinc429_app
export MYSQL_PASSWORD='elegi_una_clave'
python3 app.py
```

La aplicación usa por defecto `localhost:3306` y la base `ARINC429_6A`.
Se pueden configurar `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`,
`MYSQL_PASSWORD` y `MYSQL_DATABASE` mediante variables de entorno. La contraseña
no se guarda en el código.

## Verificar los datos

Después de agregar, modificar o eliminar un instrumento, consultar los cambios
desde MySQL:

```bash
sudo mysql ARINC429_6A -e "SELECT ins_id, ins_descripcion FROM instrumentos;"
```
