import mysql.connector

def conectar():
    """Establece la conexión con la base de datos MySQL."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Si tu usuario root tiene clave, escríbela aquí
        database="ARINC429_6A"
    )

def crear_instrumento(descripcion):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "INSERT INTO instrumentos (ins_descripcion) VALUES (%s)"
    cursor.execute(sql, (descripcion,))
    conexion.commit()
    print(f"✅ Instrumento '{descripcion}' agregado con éxito.")
    cursor.close()
    conexion.close()

def listar_instrumentos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM instrumentos")
    resultados = cursor.fetchall()
    
    print("\n--- LISTA DE INSTRUMENTOS ---")
    if not resultados:
        print("No hay instrumentos registrados.")
    else:
        for fila in resultados:
            print(f"ID: {fila[0]} | Descripción: {fila[1]}")
    print("-----------------------------\n")
    
    cursor.close()
    conexion.close()

def actualizar_instrumento(ins_id, nueva_descripcion):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "UPDATE instrumentos SET ins_descripcion = %s WHERE ins_id = %s"
    cursor.execute(sql, (nueva_descripcion, ins_id))
    conexion.commit()
    
    if cursor.rowcount > 0:
        print(f"✅ Instrumento con ID {ins_id} actualizado a '{nueva_descripcion}'.")
    else:
        print(f"⚠️ No se encontró ningún instrumento con el ID {ins_id}.")
        
    cursor.close()
    conexion.close()

def eliminar_instrumento(ins_id):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM instrumentos WHERE ins_id = %s"
    cursor.execute(sql, (ins_id,))
    conexion.commit()
    
    if cursor.rowcount > 0:
        print(f"🗑️ Instrumento con ID {ins_id} eliminado con éxito.")
    else:
        print(f"⚠️ No se encontró ningún instrumento con el ID {ins_id}.")
        
    cursor.close()
    conexion.close()

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
            desc = input("Ingresá la descripción del instrumento (ej. Altímetro): ")
            crear_instrumento(desc)
        elif opcion == "2":
            listar_instrumentos()
        elif opcion == "3":
            ins_id = input("Ingresá el ID del instrumento a modificar: ")
            nueva_desc = input("Ingresá la nueva descripción: ")
            actualizar_instrumento(ins_id, nueva_desc)
        elif opcion == "4":
            ins_id = input("Ingresá el ID del instrumento a eliminar: ")
            eliminar_instrumento(ins_id)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intentá de nuevo.")

if __name__ == "__main__":
    menu()
    