# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your password",    # 这里替换为你得数据库密码
    "database": "secondhand",
    "charset": "utf8mb4"
}
# 连接池配置
POOL_CONFIG = {
    "max_conn": 5,          # 最大连接数
    "min_idle_conn": 2,      # 最小空闲连接
    "wait_timeout": 5,      # 无连接时等待秒数
    "conn_alive_timeout": 300,  # 连接空闲过期时间
    "max_use_count": 500     # 单个连接最大使用次数
}