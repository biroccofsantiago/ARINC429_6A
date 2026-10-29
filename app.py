import os
from contextlib import contextmanager

import mysql.connector


def conectar():
    """Establece la conexión con la base de datos MySQL."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "ARINC429_6A"),
    )


@contextmanager
def conexion_cursor():
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        try:
            yield conexion, cursor
        finally:
            cursor.close()
    finally:
        conexion.close()


def validar_descripcion(descripcion):
    descripcion = descripcion.strip()
    if not descripcion:
        raise ValueError("La descripción no puede estar vacía.")
    if len(descripcion) > 50:
        raise ValueError("La descripción no puede superar los 50 caracteres.")
    return descripcion


def crear_instrumento(descripcion):
    descripcion = validar_descripcion(descripcion)
    with conexion_cursor() as (conexion, cursor):
        cursor.execute(
            "INSERT INTO instrumentos (ins_descripcion) VALUES (%s)",
            (descripcion,),
        )
        conexion.commit()
        print(f"Instrumento '{descripcion}' agregado con éxito.")


def listar_instrumentos():
    with conexion_cursor() as (_, cursor):
        cursor.execute(
            "SELECT ins_id, ins_descripcion FROM instrumentos ORDER BY ins_id"
        )
        resultados = cursor.fetchall()

    print("\n--- LISTA DE INSTRUMENTOS ---")
    if not resultados:
        print("No hay instrumentos registrados.")
    else:
        for ins_id, descripcion in resultados:
            print(f"ID: {ins_id} | Descripción: {descripcion}")
    print("-----------------------------\n")


def actualizar_instrumento(ins_id, nueva_descripcion):
    nueva_descripcion = validar_descripcion(nueva_descripcion)
    with conexion_cursor() as (conexion, cursor):
        cursor.execute(
            "UPDATE instrumentos SET ins_descripcion = %s WHERE ins_id = %s",
            (nueva_descripcion, ins_id),
        )
        conexion.commit()
        if cursor.rowcount:
            print(f"Instrumento con ID {ins_id} actualizado.")
        else:
            print(f"No se encontró ningún instrumento con el ID {ins_id}.")


def eliminar_instrumento(ins_id):
    with conexion_cursor() as (conexion, cursor):
        cursor.execute("DELETE FROM instrumentos WHERE ins_id = %s", (ins_id,))
        conexion.commit()
        if cursor.rowcount:
            print(f"Instrumento con ID {ins_id} eliminado con éxito.")
        else:
            print(f"No se encontró ningún instrumento con el ID {ins_id}.")


def leer_id():
    try:
        return int(input("Ingresá el ID del instrumento: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return None


def menu():
    while True:
        print("\n=== MENÚ CRUD ARINC429 ===")
        print("1. Crear instrumento")
        print("2. Listar instrumentos")
        print("3. Modificar instrumento")
        print("4. Eliminar instrumento")
        print("5. Salir")

        opcion = input("Seleccioná una opción (1-5): ")

        if opcion == "1":
            descripcion = input("Ingresá la descripción del instrumento: ")
            try:
                crear_instrumento(descripcion)
            except ValueError as error:
                print(error)
        elif opcion == "2":
            listar_instrumentos()
        elif opcion == "3":
            ins_id = leer_id()
            if ins_id is not None:
                nueva_descripcion = input("Ingresá la nueva descripción: ")
                try:
                    actualizar_instrumento(ins_id, nueva_descripcion)
                except ValueError as error:
                    print(error)
        elif opcion == "4":
            ins_id = leer_id()
            if ins_id is not None:
                eliminar_instrumento(ins_id)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intentá de nuevo.")


if __name__ == "__main__":
    menu()
