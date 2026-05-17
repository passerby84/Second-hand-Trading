# 二手交易系统

一个基于 Python + MySQL 的简易二手交易系统，用于数据库知识的学习与实践。

## 项目结构

```
Second-hand Trading/
├── api/
│   └── app.py           # Tkinter GUI 应用入口
├── dao/
│   ├── user_dao.py      # 用户数据访问接口
│   ├── goods_dao.py     # 商品数据访问接口
│   ├── order_dao.py     # 订单数据访问接口
│   └── collect_dao.py   # 收藏数据访问接口
├── db/
│   ├── db_config.py     # 数据库与连接池配置
│   ├── db_pool.py       # 自定义数据库连接池实现
│   └── init.py          # 数据库初始化脚本
└── requirements.txt     # 项目依赖
```

---

## 数据库连接池

### 设计思路

`db/db_pool.py` 实现了一个自定义的数据库连接池，核心特性如下：

**1. 单例模式**
- 使用 `__new__` 方法配合双重检查锁定，确保全局只有一个连接池实例
- 避免重复创建连接浪费资源

**2. 连接池队列**
- 使用 `queue.Queue` 存储空闲连接
- 配置参数：
  - `max_conn`: 最大连接数上限
  - `min_idle_conn`: 初始化时预创建的最小空闲连接数
  - `wait_timeout`: 获取连接的超时等待时间
  - `conn_alive_timeout`: 连接的最大存活时间
  - `max_use_count`: 单个连接的最大使用次数

**3. 连接有效性检测**
- 空闲时间超时检测
- 使用次数超限检测
- `ping()` 方法检测连接是否断开

**4. 上下文管理器支持**
```python
with db_pool as cursor:
    sql = """
        ...
    """
    cursor.execute(sql, params)
    # 自动 commit 或 rollback（异常时）
    # 自动归还连接到池
```

---

## 数据访问层（DAO）

### user_dao.py - 用户接口

| 函数 | 说明 |
|------|------|
| `register(username, password, name, phone)` | 用户注册，密码使用 bcrypt 加密存储 |
| `check_register(username, ...)` | 检查用户名是否已存在 |
| `verify_login(username, password)` | 登录验证，返回用户 ID 或 None |

**密码安全处理：**
- `_encrypt_pwd(plain_pwd)` - 注册时加密，生成随机盐值
- `_check_pwd(plain_pwd, hash_pwd)` - 登录时校验

### goods_dao.py - 商品接口

| 函数 | 说明 |
|------|------|
| `get_goods_list(list_count)` | 获取可购买商品列表（status=0），按价格排序 |
| `search_items_by_key(keyword, list_count)` | 模糊搜索商品名称 |
| `add_good(name, price, descr, user_id)` | 发布新商品 |
| `set_goods_statu(good_id, statu)` | 更新商品状态（0=未出售，1=已出售） |
| `is_sell_user(good_id, user_id)` | 判断是否为商品发布者 |

### order_dao.py - 订单接口

| 函数 | 说明 |
|------|------|
| `buy_good(good_id, buyer_id)` | 购买商品，包含事务：创建订单 + 更新商品状态 |

**事务处理：**
两个 SQL 语句在同一上下文块中执行，异常时自动回滚，保证数据一致性。

### collect_dao.py - 收藏接口

| 函数 | 说明 |
|------|------|
| `add_collect(good_id, user_id)` | 添加收藏 |
| `delete_collect(good_id, user_id)` | 取消收藏 |
| `get_user_collect(user_id, list_count)` | 获取用户收藏列表 |

---

## 数据库表结构

### user 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键，自增 |
| username | VARCHAR(50) | 账号，唯一 |
| password | VARCHAR(100) | bcrypt 加密后的密码 |
| name | VARCHAR(50) | 昵称 |
| phone | VARCHAR(20) | 手机号 |

### goods 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键，自增 |
| name | VARCHAR(100) | 商品名称 |
| price | FLOAT | 价格 |
| descr | VARCHAR(500) | 商品描述 |
| status | INT | 状态：0=未出售，1=已出售 |
| user_id | INT | 发布者 ID |

### order 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键，自增 |
| goods_id | INT | 商品 ID |
| buy_user_id | INT | 买家 ID |
| sell_user_id | INT | 卖家 ID |
| create_time | DATETIME | 下单时间 |

### collect 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键，自增 |
| user_id | INT | 用户 ID |
| goods_id | INT | 商品 ID |

---

## 使用方式

**1. 初始化数据库**
```bash
python db/init.py
```

**2. 安装依赖**
```bash
pip install -r requirements.txt
```

**3. 运行应用**
```bash
python api/app.py
```

---

## 技术要点总结

- 自定义连接池：单例模式、队列管理、连接有效性检测、上下文管理器
- 密码安全：bcrypt 哈希加密，随机盐值
- 事务处理：上下文管理器自动 commit/rollback
- SQL 查询：JOIN 联表查询、LIKE 模糊搜索、参数化查询防注入