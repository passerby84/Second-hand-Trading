from db.db_pool import db_pool


def get_goods_list(list_count=50):
    with db_pool as cursor:
        try:
            sql = """
            SELECT g.id, g.name, g.price, u.username, g.descr
            FROM `goods` g
            LEFT JOIN `user` u
            ON u.id = g.user_id
            WHERE g.status = 0
            ORDER BY g.price
            LIMIT %s;
            """
            cursor.execute(sql, (list_count, ))
            goods = cursor.fetchall()
            result = []
            for item in goods:
                good = (item["id"], item["name"], item["price"], item["username"], item["descr"])
                result.append(good)
            return result
        except Exception as e:
           print("❌ get_goods_list:")
           print(e)
           return


def search_items_by_key(keyword, list_count=50):
    with db_pool as cursor:
        try:
            sql = """
            SELECT g.id, g.name, g.price, u.username, g.descr
            FROM `goods` g
            LEFT JOIN `user` u
            ON u.id = g.user_id
            WHERE g.name LIKE %s AND g.status = 0
            ORDER BY g.price
            LIMIT %s;
            """
            cursor.execute(sql, (f"%{keyword}%", list_count))
            goods = cursor.fetchall()
            result = []
            for item in goods:
                good = (item["id"], item["name"], item["price"], item["username"], item["descr"])
                result.append(good)
            return result
        except Exception as e:
            print("❌ search_items_by_key:")
            print(e)
            return []

def set_goods_statu(good_id, statu=1):
    with db_pool as cursor:
        try:
            sql = """
            UPDATE `goods` 
            SET status = %s
            WHERE id = %s AND status = 0;
            """
            cursor.execute(sql, (statu, good_id))
        except Exception as e:
            print("❌ set_goods_statu:")
            print(e)
            return

def add_good(name, price, descr, user_id):
    with db_pool as cursor:
        try:
            sql = """
            INSERT INTO goods (name, price, descr, status, user_id)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (name, price, descr, 0, user_id))
        except Exception as e:
            print("❌ add_good:")
            print(e)
            return

def is_sell_user(good_id, user_id) -> bool:
    with db_pool as cursor:
        try:
            sql = "SELECT * FROM goods WHERE id = %s"
            cursor.execute(sql, (good_id, ))
            good = cursor.fetchone()
            if good["user_id"] == user_id:
                return True
            return False
        except Exception as e:
            print("❌ is_sell_user:")
            print(e)
            return True