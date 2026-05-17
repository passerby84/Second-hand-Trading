import bcrypt

# 密码加密
def _encrypt_pwd(plain_pwd: str) -> str:
    # 转字节
    pwd_bytes = plain_pwd.encode("utf-8")
    # 生成盐值
    salt = bcrypt.gensalt()
    # 加密
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")

# 密码校验（登录用）
def _check_pwd(plain_pwd: str, hash_pwd: str) -> bool:
    pwd_bytes = plain_pwd.encode("utf-8")
    hash_bytes = hash_pwd.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hash_bytes)


from db.db_pool import db_pool

def register(username, password, name, phone):
    with db_pool as cursor:
        try:
            sql = "INSERT INTO `user` (username, password, name, phone) VALUES (%s, %s, %s, %s);"
            cursor.execute(sql, (username, _encrypt_pwd(password), name, phone))
            print("✅ 注册成功！")
        except Exception as e:
            print("❌ 注册失败，账号已存在！")
            print(e)

def check_register(username, password,nickname , phone) -> bool:
    with db_pool as cursor:
        try:
            sql = "SELECT * FROM `user` WHERE username=%s;"
            cursor.execute(sql, (username, ))
            user = cursor.fetchone()
            if not user:
                print("当前用户不存在")
                return True
            return False
        except Exception as e:
           print("❌ 查找当前账户是否存在出错：")
           print(e)
           return False

def verify_login(username, password) -> int:
    with db_pool as cursor:
        sql = "SELECT * FROM `user` WHERE username=%s;"
        cursor.execute(sql, (username,))
        user = cursor.fetchone()
        if user:
            if _check_pwd(password, user["password"]):
                return user["id"]
        return None
