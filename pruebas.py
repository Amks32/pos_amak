import pandas as pd
import mysql.connector

# Leer el archivo Excel
file_path = r'C:\Users\bryan\Desktop\LIBRO EXPOR.xlsx'  # Usa una cadena de texto sin formato (raw string)
df = pd.read_excel(file_path)

# Conectar a la base de datos MySQL
db_connection = mysql.connector.connect(
    host='localhost',      # Reemplaza con tu host
    user='root',     # Reemplaza con tu usuario
    password='Superbryan12@',  # Reemplaza con tu contraseña
    database='pos_system'  # Reemplaza con tu base de datos
)
cursor = db_connection.cursor()

# Crear la tabla 'stock' (si no existe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(255),
    UNIDAD INT,
    PRECIO_DE_VENTA DECIMAL(10, 2),
    PRECIO_DE_COMPRA DECIMAL(10, 2),
    CATEGORIA VARCHAR(255),
    SUB_CATEGORIA VARCHAR(255),
    PROVEEDOR VARCHAR(255),
    precio_OFERTA1 DECIMAL(10, 2),
    precio_OFERTA2 DECIMAL(10, 2),
    precio_OFERTA3 DECIMAL(10, 2),
    COLUMNA_EXTRA1 VARCHAR(255),
    COLUMNA_EXTRA2 VARCHAR(255),
    COLUMNA_EXTRA3 VARCHAR(255),
    COLUMNA_EXTRA4 VARCHAR(255),
    COLUMNA_EXTRA5 VARCHAR(255)
)
''')

# Insertar los datos en la tabla 'stock'
for row in df.itertuples(index=False):
    cursor.execute('''
    INSERT INTO stock (descripcion, UNIDAD, PRECIO_DE_VENTA, PRECIO_DE_COMPRA, CATEGORIA, SUB_CATEGORIA, PROVEEDOR, precio_OFERTA1, precio_OFERTA2, precio_OFERTA3, COLUMNA_EXTRA1, COLUMNA_EXTRA2, COLUMNA_EXTRA3, COLUMNA_EXTRA4, COLUMNA_EXTRA5)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', row)

# Confirmar los cambios
db_connection.commit()

# Cerrar la conexión
cursor.close()
db_connection.close()

print("Datos migrados exitosamente a la tabla 'stock'.")

