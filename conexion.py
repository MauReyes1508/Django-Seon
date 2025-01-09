import fdb

con = fdb.connect(
    dsn='localhost:/home/raul/bases/terceros.fdb',
    user='SYSDBA',
    password='123',
    charset='UTF8'
)

print("Conexión exitosa")
con.close()
