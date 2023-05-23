import mysql.connector  # Mysql 資料庫
def sql_connect():
    connection = mysql.connector.connect(
        host = 'localhost',
        port = '3306',
        user = 'root',
        password = '12345',
        database = '111_2_data_structure'
    )
    return connection