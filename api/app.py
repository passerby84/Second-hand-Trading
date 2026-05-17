import time
import tkinter as tk
from tkinter import ttk, messagebox
from db.db_pool import db_pool
import dao.user_dao as db_user
import dao.goods_dao as db_goods
import dao.order_dao as db_order

class LoginFrame(tk.Frame):
    """登录界面"""

    def __init__(self, master, on_login_success, on_register):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.on_register = on_register
        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_label = tk.Label(self, text="二手交易系统", font=("Arial", 24, "bold"))
        title_label.pack(pady=40)

        # 登录框容器
        login_frame = tk.Frame(self)
        login_frame.pack(pady=20)

        # 用户名
        tk.Label(login_frame, text="用户名:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(login_frame, width=25, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # 密码
        tk.Label(login_frame, text="密码:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(login_frame, width=25, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # 登录按钮
        login_btn = tk.Button(login_frame, text="登 录", width=20, height=2,
                              font=("Arial", 11), command=self.handle_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # 注册按钮
        register_btn = tk.Button(login_frame, text="注册新账户", width=20,
                                 font=("Arial", 10), command=self.on_register)
        register_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # 绑定回车键
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码")
            return

        # TODO: 在此处添加API验证逻辑
        user_id = db_user.verify_login(username, password)
        if user_id:
            self.on_login_success(username, user_id)
        else:
            messagebox.showwarning("提示", "用户名或密码错误")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()
            return



class RegisterFrame(tk.Frame):
    """注册界面"""

    def __init__(self, master, on_register_success, on_back_to_login):
        super().__init__(master)
        self.on_register_success = on_register_success
        self.on_back_to_login = on_back_to_login
        self.create_widgets()

    def create_widgets(self):
        # 标题
        title_label = tk.Label(self, text="注册新账户", font=("Arial", 24, "bold"))
        title_label.pack(pady=30)

        # 注册框容器
        register_frame = tk.Frame(self)
        register_frame.pack(pady=10)

        # 账户名（必填）
        tk.Label(register_frame, text="账户名:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=8, sticky="e")
        self.account_entry = tk.Entry(register_frame, width=25, font=("Arial", 12))
        self.account_entry.grid(row=0, column=1, padx=10, pady=8)
        tk.Label(register_frame, text="*必填", font=("Arial", 9), fg="gray").grid(row=0, column=2, sticky="w")

        # 密码（必填）
        tk.Label(register_frame, text="密码:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=8, sticky="e")
        self.password_entry = tk.Entry(register_frame, width=25, font=("Arial", 12), show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=8)
        tk.Label(register_frame, text="*必填", font=("Arial", 9), fg="gray").grid(row=2, column=2, sticky="w")

        # 确认密码（必填）
        tk.Label(register_frame, text="确认密码:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=8, sticky="e")
        self.confirm_password_entry = tk.Entry(register_frame, width=25, font=("Arial", 12), show="*")
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=8)
        tk.Label(register_frame, text="*必填", font=("Arial", 9), fg="gray").grid(row=3, column=2, sticky="w")

        # 昵称（选填）
        tk.Label(register_frame, text="昵称:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=8, sticky="e")
        self.nickname_entry = tk.Entry(register_frame, width=25, font=("Arial", 12))
        self.nickname_entry.grid(row=1, column=1, padx=10, pady=8)
        tk.Label(register_frame, text="可选", font=("Arial", 9), fg="gray").grid(row=1, column=2, sticky="w")

        # 手机号（可选）
        tk.Label(register_frame, text="手机号:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=8, sticky="e")
        self.phone_entry = tk.Entry(register_frame, width=25, font=("Arial", 12))
        self.phone_entry.grid(row=4, column=1, padx=10, pady=8)
        tk.Label(register_frame, text="可选", font=("Arial", 9), fg="gray").grid(row=4, column=2, sticky="w")

        # 按钮区域
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        # 注册按钮
        register_btn = tk.Button(btn_frame, text="注 册", width=15, height=2,
                                 font=("Arial", 11), command=self.handle_register)
        register_btn.grid(row=0, column=0, padx=10)

        # 返回登录按钮
        back_btn = tk.Button(btn_frame, text="返回登录", width=15,
                             font=("Arial", 10), command=self.on_back_to_login)
        back_btn.grid(row=0, column=1, padx=10)

        # 绑定回车键
        self.confirm_password_entry.bind("<Return>", lambda e: self.handle_register())

    def handle_register(self):
        """处理注册"""
        account = self.account_entry.get().strip()
        nickname = self.nickname_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # 验证必填字段
        if not account:
            messagebox.showwarning("提示", "请输入账户名")
            self.account_entry.focus()
            return

        if not password:
            messagebox.showwarning("提示", "请输入密码")
            self.password_entry.focus()
            return

        if not confirm_password:
            messagebox.showwarning("提示", "请确认密码")
            self.confirm_password_entry.focus()
            return

        # 验证密码一致性
        if password != confirm_password:
            messagebox.showwarning("提示", "两次输入的密码不一致")
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.password_entry.focus()
            self.confirm_password_entry.delete(0, tk.END)
            return

        if nickname:
            if len(nickname) > 10:
                messagebox.showwarning("提示", "昵称名称大于10个字")
                self.nickname_entry.focus()
                self.nickname_entry.delete(0, tk.END)
                return

        # 验证手机号格式（如果填写了）
        if phone:
            if not phone.isdigit() or len(phone) != 11:
                messagebox.showwarning("提示", "请输入正确的11位手机号")
                self.phone_entry.focus()
                self.phone_entry.delete(0, tk.END)
                return

        # TODO: 在此处添加API注册逻辑
        if db_user.check_register(account, password, nickname, phone):
            db_user.register(account, password, nickname, phone)
            messagebox.showinfo("注册成功", f"账户名: {account}")
        else:
            messagebox.showinfo("账号名已存在", "请更换账户名")
            return

        # 暂时直接通过，后续替换为API注册
        self.on_register_success(account)


class MainFrame(tk.Frame):
    """主界面 - 二手交易系统"""

    def __init__(self, master, username, userid, on_logout):
        super().__init__(master)
        self.username = username
        self.userid = userid
        self.on_logout = on_logout
        self.current_mode = "buy"  # 默认为购买模式
        self.create_widgets()

    def create_widgets(self):
        # 顶部栏
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        # 用户信息
        tk.Label(top_frame, text=f"欢迎, {self.username}", font=("Arial", 12)).pack(side=tk.LEFT)

        # 模式切换按钮
        self.mode_btn = tk.Button(top_frame, text="出售", font=("Arial", 10),
                                   command=self.toggle_mode)
        self.mode_btn.pack(side=tk.LEFT, padx=20)

        # 登出按钮
        tk.Button(top_frame, text="退出登录", font=("Arial", 10),
                  command=self.on_logout).pack(side=tk.RIGHT)

        # 分隔线
        ttk.Separator(self, orient="horizontal").pack(fill=tk.X, pady=5)

        # 内容区域
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 默认显示购买界面
        self.show_buy_panel()

    def toggle_mode(self):
        """切换购买/出售模式"""
        if self.current_mode == "buy":
            self.current_mode = "sell"
            self.mode_btn.config(text="购买")
            self.show_sell_panel()
        else:
            self.current_mode = "buy"
            self.mode_btn.config(text="出售")
            self.show_buy_panel()

    def clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_buy_panel(self):
        """显示购买面板"""
        self.clear_content()

        # 标题
        tk.Label(self.content_frame, text="可购买商品榜单", font=("Arial", 16, "bold")).pack(pady=10)

        # 搜索框
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(fill=tk.X, pady=5)

        tk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="搜索", command=self.search_items).pack(side=tk.LEFT)

        # 商品列表
        list_frame = tk.Frame(self.content_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 创建Treeview
        columns = ("id", "name", "price", "seller", "description")
        self.item_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        self.item_tree.heading("id", text="编号")
        self.item_tree.heading("name", text="商品名称")
        self.item_tree.heading("price", text="价格")
        self.item_tree.heading("seller", text="卖家")
        self.item_tree.heading("description", text="描述")

        self.item_tree.column("id", width=0, stretch=False)
        self.item_tree.column("name", width=150)
        self.item_tree.column("price", width=80)
        self.item_tree.column("seller", width=100)
        self.item_tree.column("description", width=200)

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=scrollbar.set)

        self.item_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 操作按钮
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="刷新列表", command=self.refresh_buy_list).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="购买选中", command=self.buy_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="查看详情", command=self.view_detail).pack(side=tk.LEFT, padx=5)

        # 加载示例数据
        self.load_buy_items()

    def show_sell_panel(self):
        """显示出售面板"""
        self.clear_content()

        # 标题
        tk.Label(self.content_frame, text="发布商品出售", font=("Arial", 16, "bold")).pack(pady=10)

        # 表单
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)

        # 商品名称
        tk.Label(form_frame, text="商品名称:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.sell_name_entry = tk.Entry(form_frame, width=30, font=("Arial", 11))
        self.sell_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # 价格
        tk.Label(form_frame, text="价格:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.sell_price_entry = tk.Entry(form_frame, width=30, font=("Arial", 11))
        self.sell_price_entry.grid(row=1, column=1, padx=10, pady=10)

        # 商品描述
        tk.Label(form_frame, text="商品描述:", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=10, sticky="ne")
        self.sell_desc_text = tk.Text(form_frame, width=35, height=5, font=("Arial", 11))
        self.sell_desc_text.grid(row=2, column=1, padx=10, pady=10)

        # 分类
        tk.Label(form_frame, text="分类:", font=("Arial", 11)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.category_var = tk.StringVar(value="电子产品")
        categories = ["电子产品", "书籍", "服装", "生活用品", "其他"]
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var,
                                            values=categories, state="readonly", width=28)
        self.category_combo.grid(row=3, column=1, padx=10, pady=10)

        # 提交按钮
        tk.Button(self.content_frame, text="发布商品", width=20, height=2,
                  font=("Arial", 11), command=self.submit_sell).pack(pady=20)

    # ========== 业务方法 (后续添加API调用) ==========

    def load_buy_items(self):
        """加载可购买商品列表"""
        # TODO: 调用API获取商品列表
        goods_data = db_goods.get_goods_list(50)
        for item in goods_data:
            self.item_tree.insert("", tk.END, values=item)

    def refresh_buy_list(self):
        """刷新商品列表"""
        # 清空现有数据
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        # TODO: 调用API重新加载
        time.sleep(0.2)
        self.load_buy_items()

    def search_items(self):
        """搜索商品"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.refresh_buy_list()
            return

        # TODO: 调用API搜索
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        goods_data = db_goods.search_items_by_key(keyword, 50)
        for item in goods_data:
            self.item_tree.insert("", tk.END, values=item)

        # messagebox.showinfo("搜索", f"搜索: {keyword}\n(后续添加API)")

    def buy_selected(self):
        """购买选中商品"""
        selected = self.item_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择商品")
            return
        item = self.item_tree.item(selected[0])
        # TODO: 调用购买API
        if db_goods.is_sell_user(item['values'][0], self.userid):
            messagebox.showinfo("购买", f"不可购买自己发布的商品\n{item['values'][1]}")
        else:
            # db_goods.set_goods_statu(item['values'][0], 1)  # 多线程时易错，应使用事务
            db_order.buy_good(item['values'][0], self.userid)
            messagebox.showinfo("购买", f"购买{item['values'][1]}\n成功")
        self.refresh_buy_list()

    def view_detail(self):
        """查看商品详情"""
        selected = self.item_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择商品")
            return
        item = self.item_tree.item(selected[0])
        # TODO: 打开详情窗口
        messagebox.showinfo("商品详情", f"名称: {item['values'][1]}\n"
                                        f"价格: {item['values'][2]}元\n"
                                        f"卖家: {item['values'][3]}\n"
                                        f"描述: {item['values'][4]}")

    def submit_sell(self):
        """提交出售商品"""
        name = self.sell_name_entry.get().strip()
        price = self.sell_price_entry.get().strip()
        desc = self.sell_desc_text.get("1.0", tk.END).strip()
        category = self.category_var.get()

        if not name or not price:
            messagebox.showwarning("提示", "请填写商品名称和价格")
            return

        try:
            float(price)
        except ValueError:
            messagebox.showwarning("提示", "价格必须是数字")
            return

        # TODO: 调用API提交
        db_goods.add_good(name, price, desc, self.userid)
        messagebox.showinfo("发布成功", f"商品: {name}\n价格: {price}元\n分类: {category}")

        # 清空表单
        self.sell_name_entry.delete(0, tk.END)
        self.sell_price_entry.delete(0, tk.END)
        self.sell_desc_text.delete("1.0", tk.END)


class SecondHandApp(tk.Tk):
    """主应用程序"""

    def __init__(self):
        super().__init__()
        self.title("二手交易系统")
        self.geometry("700x600")
        self.resizable(True, True)

        # 显示登录界面
        self.show_login()

    def show_login(self):
        """显示登录界面"""
        self.clear_window()
        self.login_frame = LoginFrame(self, self.on_login_success, self.show_register)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_register(self):
        """显示注册界面"""
        self.clear_window()
        self.register_frame = RegisterFrame(self, self.on_register_success, self.show_login)
        self.register_frame.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self, username, userid):
        """登录成功回调"""
        self.clear_window()
        self.main_frame = MainFrame(self, username, userid, self.logout)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def on_register_success(self, account):
        """注册成功回调，返回登录界面"""
        self.show_login()

    def logout(self):
        """登出"""
        self.show_login()

    def clear_window(self):
        """清空窗口"""
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = SecondHandApp()
    def close_dbp():
        db_pool.close_all()
    app.protocol("WM_DELETE_WINDOW", close_dbp)
    app.mainloop()
