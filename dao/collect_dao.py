from db.db_pool import db_pool



def add_collect(good_id, user_id):
    with db_pool as cursor:
        try:
            sql = """
            INSERT INTO `collect` (user_id, goods_id)
            VALUES (%s, %s);
            """
            cursor.execute(sql, (user_id, good_id))
        except Exception as e:
            print("❌ add_collect:")
            print(e)


def delete_collect(good_id, user_id):
    with db_pool as cursor:
        try:
            sql = """
            DELETE FROM `collect`
            WHERE user_id = %s AND goods_id = %s;
            """
            cursor.execute(sql, (user_id, good_id))
        except Exception as e:
            print("❌ delete_collect:")
            print(e)


def get_user_collect(user_id, list_count=50):
    with db_pool as cursor:
        try:
            sql = """
            SELECT g.id, g.name, g.price, u.username, g.descr
            FROM `collect` c
            JOIN `goods` g
            ON g.id = c.goods_id
            JOIN `user` u
            ON u.id = g.user_id
            WHERE c.user_id = %s
            ORDER BY g.price
            LIMIT %s
            """
            cursor.execute(sql, (user_id, list_count))
            collects = cursor.fetchall()
            result = []
            for item in collects:
                good = (item["id"], item["name"], item["price"], item["username"], item["descr"])
                result.append(good)
            return result
        except Exception as e:
            print("❌ get_user_collect:")
            print(e)
            return []