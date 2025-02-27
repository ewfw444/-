import pymysql

def drop_database():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456'
    )
    
    try:
        with conn.cursor() as cursor:
            sql = "DROP DATABASE IF EXISTS library_db"
            cursor.execute(sql)
            print("Database dropped successfully!")
    finally:
        conn.close()

if __name__ == "__main__":
    drop_database() 