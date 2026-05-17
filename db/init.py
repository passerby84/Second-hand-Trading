import pymysql

# 【重要】改成你自己的 MySQL 密码！！
MYSQL_PASSWORD = "Zbw_061010"

def init_database():
    # 1. 连接 MySQL 服务（不指定数据库，先建库）
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        charset="utf8mb4",
        port=3306,
    )
    cursor = conn.cursor()

    # 2. 创建数据库
    cursor.execute("CREATE DATABASE IF NOT EXISTS secondhand DEFAULT CHARACTER SET utf8mb4")
    print("✅ 数据库创建成功")

    # 3. 切换到该数据库
    conn.select_db("secondhand")

    # ===================== 建表 =====================
    # 用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL,
        name VARCHAR(50),
        phone VARCHAR(20)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    # 商品表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goods (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        price FLOAT NOT NULL,
        descr VARCHAR(500),
        status INT DEFAULT 0,  -- 0未出售 1已出售
        user_id INT NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    # 订单表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS `order` (
        id INT PRIMARY KEY AUTO_INCREMENT,
        goods_id INT NOT NULL,
        buy_user_id INT NOT NULL,
        sell_user_id INT NOT NULL,
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    # 收藏表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS collect (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        goods_id INT NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')

    print("✅ 所有表创建完成！")
    cursor.close()
    conn.close()

if __name__ == '__main__':
    init_database()