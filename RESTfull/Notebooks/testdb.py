# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="sa",
#   password="icaiSQL2019",
#   database="master",
#   port="1433"
# )

# mycursor = mydb.cursor()

# mycursor.execute("SELECT * FROM bicimad")

# myresult = mycursor.fetchone()

# for x in myresult:
#   print(x)
import pyodbc
import pandas as pd

server = 'tcp:127.0.0.1'
database = 'master'
username = 'sa'
password = 'icaiSQL2019'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                        SERVER='+server+';DATABASE='+database+'; \
                            UID='+username+';PWD='+password)

df = pd.read_sql_query('SELECT * FROM bicimad',cnxn)

print(df.head())