import queue
import pymysql
import threading
import time
from db.db_config import DB_CONFIG, POOL_CONFIG

class DataBasePool:
    _instance = None
    _single_lock = threading.Lock()

    def __new__(cls):
        # 防止重复初始化
        if not cls._instance:
            with cls._single_lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 只初始化一次
        if hasattr(self, "init_ok"):
            return
        self.init_ok = True
        print("连接池初始化完成")

        max_size = POOL_CONFIG["max_conn"]
        self.conn_queue = queue.Queue(maxsize=max_size)
        self.use_count_map = dict()  # 记录每个连接使用次数
        self.create_time_map = dict()  # 记录连接创建时间
        self._init_min_idle()
        self.thread_lock = threading.Lock()
        # 预先创建连接
    # 创建新数据库连接
    def _create_conn(self):
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset=DB_CONFIG["charset"]
        )
        self.use_count_map[conn] = 0
        self.create_time_map[conn] = time.time()
        return conn

    def _init_min_idle(self):
        for _ in range(POOL_CONFIG["min_idle_conn"]):
            conn = self._create_conn()
            self.conn_queue.put(conn)

        # 归还连接
    def return_conn(self, conn):
        if not conn:
            return
        try:
            # 异常连接直接关闭
            if not self._is_valid_conn(conn):
                self._close_single_conn(conn)
                return
            self.conn_queue.put(conn)
        except Exception:
            self._close_single_conn(conn)

    # 获取连接
    def get_conn(self):
        start_time = time.time()
        while True:
            # 等待超时判定
            if time.time() - start_time > POOL_CONFIG["wait_timeout"]:
                raise ConnectionError("数据库连接池无空闲连接，获取超时")
            try:
                conn = self.conn_queue.get(block=False)
            except queue.Empty:
                # 队列空，尝试新建
                if self.conn_queue.qsize() < POOL_CONFIG["max_conn"]:
                    conn = self._create_conn()
                else:
                    time.sleep(0.1)
                    continue
            # 连接无效则销毁重建
            if not self._is_valid_conn(conn):
                self._close_single_conn(conn)
                continue
            self.use_count_map[conn] += 1
            return conn

    def _is_valid_conn(self, conn) -> bool:
        now = time.time()
        # 超时过期
        if now - self.create_time_map.get(conn, 0) > POOL_CONFIG["conn_alive_timeout"]:
            return False
        # 超出最大使用次数
        if self.use_count_map.get(conn, 0) >= POOL_CONFIG["max_use_count"]:
            return False
        # 数据库ping检测
        try:
            conn.ping(reconnect=False)
            return True
        except Exception:
            return False

    # 关闭单个连接
    def _close_single_conn(self, conn):
        try:
            conn.close()
        except Exception:
            pass
        self.use_count_map.pop(conn, None)
        self.create_time_map.pop(conn, None)

    # 关闭所有连接，销毁连接池
    def close_all(self):
        while not self.conn_queue.empty():
            conn = self.conn_queue.get()
            self._close_single_conn(conn)
        self.use_count_map.clear()
        self.create_time_map.clear()

    # 上下文管理器
    def __enter__(self):
        self.conn = self.get_conn()
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.return_conn(self.conn)

db_pool = DataBasePool()