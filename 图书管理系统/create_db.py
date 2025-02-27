import pymysql

def create_database():
    # 连接MySQL（不指定数据库）
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456'
    )
    
    try:
        with conn.cursor() as cursor:
            # 创建数据库
            sql = "CREATE DATABASE IF NOT EXISTS library_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            cursor.execute(sql)
        print("Database created successfully!")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database() 