from db.db_pool import db_pool

def buy_good(good_id, buyer_id):
    with db_pool as cursor:
        try:
            sql = """
            INSERT INTO `order` (goods_id, buy_user_id, sell_user_id, create_time)
            SELECT %(goods_id)s, %(buyer_id)s, user_id, NOW()
            FROM goods
            WHERE id = %(goods_id)s;
            """
            cursor.execute(sql, {
                "goods_id":good_id,
                "buyer_id":buyer_id
            })
            sql = """
            UPDATE `goods` 
            SET status = 1
            WHERE id = %s AND status = 0;
            """
            cursor.execute(sql, (good_id, ))
        except Exception as e:
            print("❌ set_goods_statu:")
            print(e)
            return
