# -*- coding: utf-8 -*-
import sqlite3, json, argparse, sys, os
import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
from tkcalendar import Calendar
from datetime import datetime


# ФУНКЦИИ И ПЕРЕМЕННЫЕ

# ОПЕРАЦИИ С ЗАКАЗАМИ

def add_order():
    name = entry_o_name.get().strip()
    status_name = entry_status.get().strip()
    
    raw_date = entry_date.get_date() 

    d, m, y = raw_date.split(".")
    date = f"{y}-{m}-{d}"

    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("SELECT id_status FROM status WHERE name_status = ?;", (status_name, ))
    status_row = c.fetchone()
    status_id = status_row[0]

    c.execute("SELECT id_customer FROM customers WHERE name_customers = ?;", (name,))
    customer_row = c.fetchone()
    if not customer_row:
        messagebox.showerror("Ошибка", f"Клиент '{name}' не найден в базе!")
        db.close()
        return
    customer_id = customer_row[0]

    c.execute("""
        INSERT INTO orders (customer_id, date_orders, status_id, total_orders)
        VALUES (?, ?, ?, ?);
    """, (customer_id, date, status_id, 0.0))
    db.commit()
    
    new_order_id = c.lastrowid
    c.execute("""
        UPDATE orders 
        SET total_orders = COALESCE((
            SELECT SUM(quantity_order_items * price_order_items) 
            FROM order_items 
            WHERE order_id = ?
        ), 0.0)
        WHERE id_order = ?;
    """, (new_order_id, new_order_id))
    db.commit()
    db.close()

    entry_o_name.delete(0, tk.END)
    entry_o_name.insert(0, "Введите имя")
    entry_status.set("Новый")
    load_orders_list()
    messagebox.showinfo("Успех", "Новый заказ успешно добавлен!")


def update_order():
    selected_item = tree_orders.selection()
    if not selected_item:
        messagebox.showwarning("Внимание", "Пожалуйста, сначала выберите заказ в таблице!")
        return
        
    order_id = tree_orders.item(selected_item, "values")[0]

    customer_name = entry_o_name.get().strip()
    status_name = entry_status.get().strip()
    raw_date = entry_date.get_date()

    d, m, y = raw_date.split(".")
    date = f"{y}-{m}-{d}"

    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("SELECT id_status FROM status WHERE name_status = ?", (status_name,))
    status_row = c.fetchone()

    c.execute("SELECT id_customer FROM customers WHERE name_customers = ?", (customer_name,))
    customer_row = c.fetchone()

    c.execute("""
        UPDATE orders 
        SET customer_id = ?, date_orders = ?, status_id = ? 
        WHERE id_order = ?;
    """, (customer_row[0], date, status_row[0], order_id))
    
    db.commit()
    db.close()

    load_orders_list()
    entry_status.set("Новый")
    messagebox.showinfo("Успех", "Данные заказа успешно изменены!")

def delete_order():
    item_id = tree_orders.selection()[0]
    row_values = tree_orders.item(item_id, "values")
    order_id = row_values[0]
        
    if messagebox.askyesno("Подтверждение", f"Удалить заказ?"):
        db = sqlite3.connect("delivery_tables.db")
        c = db.cursor()
        c.execute("DELETE FROM orders WHERE id_order = ?;", (order_id))
        db.commit()
        db.close()
        messagebox.showinfo("Успех", "Заказ успешно удален")
        load_orders_list()
    else:
        messagebox.showwarning("Внимание", "Выберите строку в одной из таблиц!")

def load_orders_list():
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("""
        SELECT id_order, name_customers, date_orders, name_status, total_orders
        FROM orders
        left JOIN status ON status_id = id_status
        left join customers on id_customer = customer_id
    """)
    rows = c.fetchall()
    for item in tree_orders.get_children():
        tree_orders.delete(item)

    for row in rows:
        tree_orders.insert(parent="", index=tk.END, values=row)

    db.close()

    for item in tree_orders.get_children():
        tree_orders.delete(item)

    for row in rows:
        tree_orders.insert(parent="", index=tk.END, values=row)

def refresh_customers_list():
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("SELECT name_customers FROM customers;")
    customers = c.fetchall()
    customers_list = [row[0] for row in customers]
    
    entry_o_name.insert(0, customers_list[0])
    entry_o_name.config(values=customers_list)
    entry_o_name.set(customers_list[0])

def filter_orders_date(*args):
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    if combo_filter_date.get() == "От новых к старым":
        c.execute("""
            SELECT id_order, name_customers, date_orders, name_status, total_orders
            FROM orders
            LEFT JOIN status ON status_id = id_status
            LEFT JOIN customers ON id_customer = customer_id
            order by date_orders desc;
        """)
    else:
        c.execute("""
            SELECT id_order, name_customers, date_orders, name_status, total_orders
            FROM orders
            LEFT JOIN status ON status_id = id_status
            LEFT JOIN customers ON id_customer = customer_id
            order by date_orders asc;
        """)
    rows = c.fetchall()
    db.close()

def filter_orders_status(*args):
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    
    selected_status = combo_filter.get()
    c.execute("""
        SELECT id_order, name_customers, date_orders, name_status, total_orders
        FROM orders
        LEFT JOIN status ON status_id = id_status
        LEFT JOIN customers ON id_customer = customer_id;
    """)
    rows = c.fetchall()
    db.close()
    
    # 3. Полностью очищаем таблицу Treeview перед выводом отфильтрованных строк
    for item in tree_orders.get_children():
        tree_orders.delete(item)
        
    # 4. Выводим только те заказы, которые подходят под выбранный статус
    for row in rows:        
        order_status = row[3] # Индекс 3 — это текстовое название статуса в запросе
        
        # Если выбрано "Все", выводим каждую строку. Иначе — только совпадения.
        if selected_status == "Все" or order_status == selected_status:
            tree_orders.insert("", "end", values=row) 


    for item in tree_orders.get_children():
        tree_orders.delete(item)

    for row in rows:
        tree_orders.insert(parent="", index=tk.END, values=row)

def on_tree_orders_select(event):
    selected_items = tree_orders.selection()
    if selected_items:
        item_id = selected_items[0]
        row_values = tree_orders.item(item_id, "values")
        entry_o_name.set(row_values[1]) 
        
        entry_status.set(row_values[3])
        parts = row_values[2].split("-")
        year_val, month_val, day_val = int(parts[0]), int(parts[1]), int(parts[2])
        entry_date.selection_set(datetime(year_val, month_val, day_val))
    else:
        entry_o_name.set("Введите имя")
        entry_status.set("Новый")
        entry_date.selection_set(datetime.now())


# ОПЕРАЦИИ СО СПИСКОМ КЛИЕНТОВ

def add_customer():
    name = entry_o_name.get().strip()
    phone = entry_c_phone.get().strip()
    address = entry_c_address.get().strip()
    
    if not name or name == "Введите имя" or not phone or not address:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните все поля клиента!")
        return

    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute("""
        INSERT INTO customers (name_customers, phone_customers, address_customers)
        VALUES (?, ?, ?);
    """, (name, phone, address))    
    db.commit()
    db.close()

    entry_c_name.delete(0, tk.END)
    entry_c_name.insert(0, "Введите имя")
    entry_c_phone.delete(0, tk.END)
    entry_c_address.delete(0, tk.END)
    
    load_customers_list()
    messagebox.showinfo("Успех", "Новый клиент успешно добавлен!")
    refresh_customers_list()


def update_customer():
    selected_item = tree_customers.selection()
    if not selected_item:
        messagebox.showwarning("Внимание", "Пожалуйста, сначала выберите клиента в таблице!")
        return

    customer_id = tree_customers.item(selected_item, "values")[0]

    name = entry_c_name.get().strip()
    phone = entry_c_phone.get().strip()
    address = entry_c_address.get().strip()

    if not name or name == "Введите имя" or not phone or not address:
        messagebox.showwarning("Внимание", "Поля ввода не могут быть пустыми!")
        return

    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        UPDATE customers 
        SET name_customers = ?, phone_customers = ?, address_customers = ? 
        WHERE id_customer = ?;
    """, (name, phone, address, customer_id))
    
    db.commit()
    db.close()

    entry_c_name.delete(0, tk.END)
    entry_c_name.insert(0, "Введите имя")
    entry_c_phone.delete(0, tk.END)
    entry_c_address.delete(0, tk.END)
    
    load_customers_list()
    messagebox.showinfo("Успех", "Данные клиента успешно изменены!")
    refresh_customers_list()


def delete_customer():
    selected_items = tree_customers.selection()
    if not selected_items:
        messagebox.showwarning("Внимание", "Пожалуйста, сначала выберите клиента в таблице!")
        return
        
    item_id = selected_items[0]
    row_values = tree_customers.item(item_id, "values")
    customer_id = row_values[0]
    customer_name = row_values[1]
    if messagebox.askyesno("Подтверждение", f"Удалить клиента {customer_name}?"):
        db = sqlite3.connect("delivery_tables.db")
        c = db.cursor()
        c.execute("PRAGMA foreign_keys = ON;")
        
        try:
            c.execute("DELETE FROM customers WHERE id_customer = ?;", (customer_id,))
            db.commit()
            messagebox.showinfo("Успех", f"Клиент '{customer_name}' успешно удален")

            load_customers_list()
            load_orders_list()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", f"Нельзя удалить клиента {customer_name}, так как у него есть активные заказы!")
        finally:
            db.close()            

def load_customers_list():
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("""
        SELECT id_customer, name_customers, phone_customers, address_customers 
        FROM customers;
    """)
    rows = c.fetchall()

    db.close()

    for item in tree_customers.get_children():
        tree_customers.delete(item)

    for row in rows:
        tree_customers.insert(parent="", index=tk.END, values=row)

def on_tree_customers_select(event):
    selected_items = tree_customers.selection()
    if selected_items:
        item_id = selected_items[0]
        row_values = tree_customers.item(item_id, "values")
        entry_c_name.delete(0, tk.END)
        entry_c_phone.delete(0, tk.END)
        entry_c_address.delete(0, tk.END)
        entry_c_name.insert(0, row_values[1]) 
        entry_c_phone.insert(0, row_values[2])
        entry_c_address.insert(0, row_values[3])
    else:
        entry_c_name.delete(0, tk.END)
        entry_c_phone.delete(0, tk.END)
        entry_c_address.delete(0, tk.END)
        entry_c_name.insert(0, "Введите имя")
        entry_c_phone.insert(0, "Введите номер телефона")
        entry_c_address.insert(0, "Введите адрес")


# ОПЕРАЦИИ СО СПИСКОМ ТОВАРОВ

def load_items_list():
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("""
        SELECT id_order_items, name_order_items, order_id, quantity_order_items, price_order_items 
        FROM order_items;
    """)
    rows = c.fetchall()

    db.close()

    for item in tree_items.get_children():
        tree_items.delete(item)

    for row in rows:
        tree_items.insert(parent="", index=tk.END, values=row)
 

# ОПЕРАЦИИ СО СПИСКОМ ТОВАРОВ

def add_item():
    order_id = entry_item_order_id.get().strip()
    item_name = entry_item_name.get().strip()
    quantity = entry_item_quantity.get().strip()
    price = entry_item_price.get().strip()
    
    if not (order_id and item_name and quantity and price):
        messagebox.showwarning("Внимание", "Заполните все поля товара!")
        return
        
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    
    c.execute("""
        INSERT INTO order_items (order_id, name_order_items, quantity_order_items, price_order_items)
        VALUES (?, ?, ?, ?);
    """, (order_id, item_name, int(quantity), float(price)))
    
    c.execute("""
        UPDATE orders 
        SET total_orders = COALESCE((
            SELECT SUM(quantity_order_items * price_order_items) 
            FROM order_items 
            WHERE order_id = ?
        ), 0.0)
        WHERE id_order = ?;
    """, (order_id, order_id))
    
    db.commit()
    db.close()

    entry_item_name.delete(0, tk.END)
    entry_item_quantity.delete(0, tk.END)
    entry_item_price.delete(0, tk.END)
    
    load_orders_list()
    load_items_list()
    messagebox.showinfo("Успех", "Товар успешно добавлен к заказу, сумма пересчитана!")


# НИЖНИЕ КНОПКИ

def export_json():
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("""
        SELECT id_order, name_customers, date_orders, name_status, total_orders
        FROM orders
        left JOIN status ON status_id = id_status
        left join customers on id_customer = customer_id
""")
    rows = c.fetchall()
    db.close()
    
    json_data = []
    for row in rows:
        order_dict = {
            "id_order": row[0],
            "name_customers": row[1],
            "date_orders": row[2],
            "name_status": row[3],
            "total_orders": row[4]
            }
        json_data.append(order_dict)

    with open("export.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

def import_json():
    file_path = filedialog.askopenfilename(
        title="Выберите файл для импорта",
        filetypes=[("JSON файлы", "*.json")]
    )    
    if not file_path:
        return
        
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            imported_data = json.load(file)
            
        db = sqlite3.connect("delivery_tables.db")
        c = db.cursor()
        c.execute("PRAGMA foreign_keys = ON;")        
        success_count = 0

        for order in imported_data:
            c.execute("SELECT id_customers FROM customers WHERE name_customers = ?", (order["customer_name"],))
            customer_row = c.fetchone()            
            c.execute("SELECT id_status FROM status WHERE name_status = ?", (order["status"],))
            status_row = c.fetchone()

            if customer_row and status_row:
                c.execute("""
                    INSERT INTO orders (customer_id, date_orders, status_id, total_orders)
                    VALUES (?, ?, ?, ?);
                """, (customer_row[0], order["date"], status_row[0], order["total_price"]))
                success_count += 1                
        db.commit()
        db.close()        
        load_orders_list()        
        messagebox.showinfo("Успех", f"Импорт завершен!\nУспешно добавлено заказов: {success_count}")        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать файл или обновить базу данных.\nТехническая ошибка: {e}")

def show_report():
    report_text = f"ОТЧЁТ ЗА {datetime.now().strftime("%d.%m.%Y")}\n\n\u2730Топ-3 клиента по сумме заказов\u2730\n\n"
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    rows = c.fetchall()    

    c.execute("""
        SELECT '\u2730 id №'||customer_id||') '||name_customers||', '||SUM(total_orders)||';' 
        FROM orders 
        JOIN customers c ON customer_id = id_customer
        GROUP BY customer_id
        ORDER BY SUM(total_orders) DESC
        LIMIT 3;
    """)
    temp = c.fetchall()
    temp_list = [list(t) for t in temp]
    temp_list2 = []
    for t in temp_list:
        report_text += t[0] + "\n"

    report_text += "\n\n\u2730Количество заказов по статусам\u2730\n\nВсего: "
    c.execute("select count(*) from orders;")
    temp = c.fetchall()
    report_text += str(temp[0][0]) + "\n"
    c.execute("""
        SELECT name_status||': '||count(id_order)
        from status
        left join orders on id_status = status_id
        group by name_status
        order by count(id_order) desc, name_status
""")
    temp = c.fetchall()    
    temp_list2 = []
    for t in temp:
        for i in t:
            temp_list2.append(str(i))
            
    report_text += "\n".join(temp_list2) + "\n\n\u2730Общая выручка\u2730\n\nЗа неделю:\n"
    c.execute("""
        SELECT
            total_orders from orders
	    where status_id = 2 AND date_orders between date('now', '-7 days') and date('now');	
""")    
    rows = c.fetchall()
    prices = [row[0] for row in rows if row[0] is not None]
    if not prices: report_text += "0"
    elif len(prices) == 1: report_text += str(prices[0])
    else: report_text += f"{' + '.join(str(price) for price in prices)} = {sum(prices)}"
    report_text += "\n\nЗа месяц:\n"

    c.execute("""
        SELECT
            total_orders from orders
	    where status_id = 2 and date_orders between date('now', '-1 month') and date('now')	
    """)    
    rows = c.fetchall()
    prices = [row[0] for row in rows if row[0] is not None]
    if not prices: report_text += "0"
    elif len(prices) == 1: report_text += str(prices[0])
    else: report_text += f"{' + '.join(str(price) for price in prices)} = {sum(prices)}"
    report_text += "\n\nЗа год:\n"
    c.execute("""
        SELECT
            total_orders from orders
	    where status_id = 2 and date_orders between date('2025-12-31') and date('now')	
""")    
    rows = c.fetchall()
    prices = [row[0] for row in rows if row[0] is not None]
    if not prices: report_text += "0"
    elif len(prices) == 1: report_text += str(prices[0])
    else: report_text += f"{' + '.join(str(price) for price in prices)} = {sum(prices)}"
    
    db.close()
    with open("Отчёт.txt", "w", encoding="utf-8") as file:
        file.write(report_text)
    try:
        if hasattr(os, "startfile"):
            os.startfile("Отчёт.txt")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            import subprocess
            subprocess.call([opener, "Отчёт.txt"])
    except Exception as e:
        print(f"Не удалось автоматически открыть файл: {e}")
        

font1 = "Montserrat", 11, "bold"
font2 = "Montserrat", 10, "bold"
font_big = "Montserrat", 16, "bold"
COLOR_BG = "#F9B7CE"          
COLOR_CARD_BG = "#FFF0F5"     
COLOR_ACCENT = "#B93D6E"      
COLOR_TEXT_DARK = "#B93D6E"
COLOR_TEXT_LIGHT = "#FFFFFF"
status_options = ["Все", "Новый", "В доставке", "Выполнен", "Отменён"]

# ОСНОВНОЙ КОД

root = tk.Tk()
root.title("Быстрая доставка — Панель управления")
root.geometry("2000x900")  
root.configure(bg=COLOR_BG)

style = ttk.Style(root)
style.theme_use("clam")

root.grid_columnconfigure(0, weight=1, minsize=350)
root.grid_columnconfigure(1, weight=0, minsize=240)
root.grid_columnconfigure(2, weight=1, minsize=350)
root.grid_columnconfigure(3, weight=0, minsize=240)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)


# СПИСОК КЛИЕНТОВ

frame_customers = tk.LabelFrame(root, text=" Список клиентов / список товаров ", font=font1, padx=10, pady=10, background=COLOR_BG, foreground=COLOR_TEXT_DARK)
frame_customers.grid(row=0, column=0, padx=(15, 5), pady=15, sticky="nsew")

tree_customers = ttk.Treeview(frame_customers, columns=("id", "name", "phone", "address"), show="headings")
tree_customers.bind("<<TreeviewSelect>>", on_tree_customers_select)
tree_customers.heading("id", text="ID")
tree_customers.heading("name", text="Имя")
tree_customers.heading("phone", text="Телефон")
tree_customers.heading("address", text="Адрес")
tree_customers.pack(fill="both", expand=True)

load_customers_list()

tree_customers.column("id", width=10, minwidth=10, anchor="w")
tree_customers.column("name", width=90, minwidth=50, anchor="w")
tree_customers.column("phone", width=90, minwidth=50, anchor="w")
tree_customers.column("address", width=150, minwidth=100, anchor="e")

# СПИСОК ТОВАРОВ

tree_items = ttk.Treeview(frame_customers, columns=("id", "name", "order_id", "quantity", "price"), show="headings")
tree_items.heading("id", text="ID")
tree_items.heading("name", text="Название")
tree_items.heading("order_id", text="Заказ")
tree_items.heading("quantity", text="Количество")
tree_items.heading("price", text="Цена")
tree_items.pack(fill="both", expand=True)

load_items_list()

tree_items.column("id", width=90, minwidth=70, anchor="w")
tree_items.column("name", width=100, minwidth=90, anchor="w")
tree_items.column("order_id", width=90, minwidth=70, anchor="w")
tree_items.column("quantity", width=90, minwidth=70, anchor="w")
tree_items.column("price", width=90, minwidth=70, anchor="e")

# ПОЛЯ И КНОПКИ ДЛЯ ОПЕРАЦИЙ СО СПИСКОМ КЛИЕНТОВ

# Создаем фрейм клиентов
frame_ctrl_customers = tk.Frame(root, padx=10, pady=15, background=COLOR_CARD_BG)
frame_ctrl_customers.grid(row=0, column=1, padx=5, pady=15, sticky="nsew")

lbl_c_name = tk.Label(frame_ctrl_customers, text="Ввод имени", font=font1, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK)
lbl_c_name.pack(fill="x", anchor="center", pady=(7, 2))

entry_c_name = tk.Entry(frame_ctrl_customers, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK, insertbackground=COLOR_TEXT_DARK, highlightbackground=COLOR_ACCENT, highlightcolor=COLOR_ACCENT, highlightthickness=2, bd=0, font=font1, width=15)
entry_c_name.pack(fill="x", ipady=6, pady=(0, 5), padx=10)

lbl_c_phone = tk.Label(frame_ctrl_customers, text="Ввод номера телефона", font=font1, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK)
lbl_c_phone.pack(fill="x", anchor="center", pady=(0, 2))
entry_c_phone = tk.Entry(frame_ctrl_customers, font=font1, bd=0, highlightthickness=2, width=15)
entry_c_phone.pack(fill="x", ipady=6, pady=(0, 15), padx=10)

lbl_c_address = tk.Label(frame_ctrl_customers, text="Ввод адреса", font=font1, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK)
lbl_c_address.pack(fill="x", anchor="center", pady=(0, 2))

entry_c_address = tk.Entry(frame_ctrl_customers, font=font1, bd=0, highlightthickness=2, width=15)
entry_c_address.pack(fill="x", ipady=6, pady=(0, 15), padx=10)

btn_add = ttk.Button(frame_ctrl_customers, text="Добавить", style="Custom.TButton", command=add_customer)
btn_add.pack(fill="x", ipady=5, pady=(0, 7), padx=10)

lbl_separator = tk.Label(
    frame_ctrl_customers, 
    text="--------------------------------", 
    font=font_big, 
    fg=COLOR_TEXT_DARK,
    bg=COLOR_CARD_BG
) 
lbl_separator.pack(fill="x", pady=(15, 0), padx=10)

lbl_item_name = tk.Label(frame_ctrl_customers, text="Ввод названия", font=font1, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK)
lbl_item_name.pack(fill="x", anchor="center", pady=(10, 2))

entry_item_name = tk.Entry(frame_ctrl_customers, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK, insertbackground=COLOR_TEXT_DARK, 
                           highlightbackground=COLOR_ACCENT, highlightcolor=COLOR_ACCENT, highlightthickness=2, bd=0, font=font1, width=15)
entry_item_name.pack(fill="x", ipady=6, pady=(0, 5), padx=10)

lbl_item_order_id = tk.Label(frame_ctrl_customers, text="Выбор номера заказа", font=font1, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK)
lbl_item_order_id.pack(fill="x", anchor="center", pady=(0, 2))

entry_item_order_id = tk.Entry(frame_ctrl_customers, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK, insertbackground=COLOR_TEXT_DARK,
                               highlightbackground=COLOR_ACCENT, highlightcolor=COLOR_ACCENT, highlightthickness=2, bd=0, font=font1, width=15)
entry_item_order_id.pack(fill="x", ipady=6, pady=(0, 15), padx=10)


row_frame = tk.Frame(frame_ctrl_customers, bg=COLOR_CARD_BG)
row_frame.pack(fill="x", pady=(0, 7), padx=10)

row_frame.grid_columnconfigure(0, weight=1)
row_frame.grid_columnconfigure(1, weight=1)

lbl_item_quantity = tk.Label(row_frame, text="Ввод кол-ва", font=font1, fg=COLOR_TEXT_DARK, bg=COLOR_CARD_BG)
lbl_item_quantity.grid(row=0, column=0, pady=(0, 2), sticky="we")

entry_item_quantity = tk.Entry(row_frame, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK, font=font1, bd=0, highlightthickness=2, width=5)
entry_item_quantity.grid(row=1, column=0, ipady=6, padx=(0, 5), sticky="we")

lbl_item_price = tk.Label(row_frame, text="Ввод цены", font=font1, fg=COLOR_TEXT_DARK, bg=COLOR_CARD_BG)
lbl_item_price.grid(row=0, column=1, pady=(0, 2), sticky="we")

entry_item_price = tk.Entry(row_frame, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK, font=font1, bd=0, highlightthickness=2, width=5)
entry_item_price.grid(row=1, column=1, ipady=6, padx=(5, 0), sticky="we")

btn_add_item = ttk.Button(frame_ctrl_customers, text="Добавить товар", style="Custom.TButton", command=add_item)
btn_add_item.pack(fill="x", ipady=5, pady=(10, 7), padx=10)

# СПИСОК ЗАКАЗОВ

frame_orders = tk.LabelFrame(root, text=" Список заказов ", font=font1, padx=10, pady=10, background=COLOR_BG, foreground=COLOR_TEXT_DARK)
frame_orders.grid(row=0, column=2, padx=5, pady=15, sticky="nsew")

tree_orders = ttk.Treeview(frame_orders, columns=("id", "name", "date", "status", "total"), show="headings")
tree_orders.bind("<<TreeviewSelect>>", on_tree_orders_select)
tree_orders.heading("id", text="ID")
tree_orders.heading("name", text="Заказчик")
tree_orders.heading("date", text="Дата")
tree_orders.heading("status", text="Статус")
tree_orders.heading("total", text="Итого")
tree_orders.pack(fill="both", expand=True)

load_orders_list()

tree_orders.column("id", width=50, minwidth=40, anchor="w")
tree_orders.column("name", width=100, minwidth=70, anchor="w")
tree_orders.column("date", width=100, minwidth=50, anchor="w")
tree_orders.column("status", width=100, minwidth=50, anchor="w")
tree_orders.column("total", width=60, minwidth=50, anchor="e")

# ПОЛЯ И КНОПКИ ДЛЯ ОПЕРАЦИЙ СО СПИСКОМ ЗАКАЗОВ

frame_ctrl_orders = tk.Frame(root, padx=10, pady=15, background=COLOR_CARD_BG)
frame_ctrl_orders.grid(row=0, column=3, padx=(5, 15), pady=15, sticky="nsew")

lbl_filter = tk.Label(frame_ctrl_orders, text="Фильтровать по статусу/дате:", font=font1, fg=COLOR_TEXT_DARK, bg=COLOR_BG)
lbl_filter.pack(anchor="center", pady=(0, 2), ipadx = 120)

combo_filter_status = ttk.Combobox(frame_ctrl_orders, values=status_options, font=font1, state="readonly")
combo_filter_status.bind("<<ComboboxSelected>>", filter_orders_status)
combo_filter_status.pack(fill="x", ipady=6, pady=(0, 15), padx=10)
combo_filter_status.set(status_options[0])

combo_filter_date = ttk.Combobox(frame_ctrl_orders, values=["От новых к старым", "От старых к новым"], font=font1, state="readonly")
combo_filter_date.bind("<<ComboboxSelected>>", filter_orders_date)
combo_filter_date.pack(fill="x", ipady=6, pady=(0, 15), padx=10)
combo_filter_date.set("От новых к старым")

lbl_name = tk.Label(frame_ctrl_orders, text="Выбор заказчика", font=font1, fg=COLOR_TEXT_DARK, bg=COLOR_BG)
lbl_name.pack(fill="x", anchor="center", pady=(0, 2))

entry_o_name = ttk.Combobox(frame_ctrl_orders, font=font1, state="readonly", values=[])
entry_o_name.pack(fill="x", ipady=6, pady=(0, 15), padx=10)

refresh_customers_list()

lbl_c_date = tk.Label(frame_ctrl_orders, text="Ввод даты", font=font1, fg=COLOR_TEXT_DARK, bg=COLOR_BG)
lbl_c_date.pack(fill="x", anchor="center", pady=(0, 2))

entry_date = Calendar(frame_ctrl_orders, date_pattern='dd.mm.yyyy', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK, insertbackground=COLOR_TEXT_DARK, highlightbackground=COLOR_ACCENT, highlightcolor=COLOR_ACCENT, highlightthickness=2, bd=0, font=font1)
entry_date.pack(fill="x", ipady=6, pady=(0, 5), padx=6)

lbl_c_status = tk.Label(frame_ctrl_orders, text="Ввод статуса", font=font1, fg=COLOR_TEXT_DARK, bg=COLOR_BG)
lbl_c_status.pack(anchor="center", pady=(0, 2), ipadx=165)

entry_status = ttk.Combobox(frame_ctrl_orders, values=status_options, font=font1, state="readonly")       
entry_status.pack(fill="x", ipady=6, pady=(0, 5), padx=7)
entry_status.set("Новый")

style.configure(
    "Custom.TButton",
    background=COLOR_ACCENT,
    foreground=COLOR_TEXT_LIGHT,
    font=font1,
    borderwidth=0,
    focuscolor="none"
)

style.map(
    "Custom.TButton",
    background=[('active', '#962A54'), ('pressed', '#7D1E43')]
)

btn_add = ttk.Button(frame_ctrl_orders, text="Добавить", style="Custom.TButton", command=add_order)
btn_add.pack(fill="x", ipady=5, pady=(15, 7))

btn_edit = ttk.Button(frame_ctrl_orders, text="Редактировать", style="Custom.TButton", command=update_order)
btn_edit.pack(fill="x", ipady=5, pady=(0, 7))

btn_delete = ttk.Button(frame_ctrl_orders, text="Удалить", style="Custom.TButton", command=delete_order)
btn_delete.pack(fill="x", ipady=5)

frame_bottom = tk.Frame(root)
frame_bottom.grid(row=1, column=0, columnspan=4, padx=15, pady=(0, 25), sticky="we")
frame_bottom.grid_columnconfigure(0, weight=1)
frame_bottom.grid_columnconfigure(1, weight=1)

# НИЖНИЕ КНОПКИ

style.configure(
    "Big.TButton",
    background=COLOR_ACCENT,
    foreground=COLOR_TEXT_LIGHT,
    font=font_big,
    borderwidth=0,
    focuscolor="none"
)

style.map(
    "Big.TButton",
    background=[('active', '#962A54'), ('pressed', '#7D1E43')]
)

btn_report = ttk.Button(frame_bottom, text="Показать отчёт", style="Big.TButton", command=show_report)
btn_report.grid(row=0, column=0, columnspan=2, pady=(0, 10), ipady=8, sticky="we")

btn_import = ttk.Button(frame_bottom, text="Импорт json", style="Big.TButton", command=import_json)
btn_import.grid(row=1, column=0, padx=(0, 10), ipady=8, sticky="we")

btn_export = ttk.Button(frame_bottom, text="Экспорт json", style="Big.TButton", command=export_json)
btn_export.grid(row=1, column=1, padx=(10, 0), ipady=8, sticky="we")


# ФУНКЦИИ ДЛЯ CLI

def cli_add_customer():
        if not args.name:
            print("Ошибка: Для добавления клиента обязательно укажите --name")
            return
        db = sqlite3.connect("delivery_tables.db")
        c = db.cursor()
        c.execute(
            "INSERT INTO customers (name_customers, phone_customers, address_customers) VALUES (?, ?, ?);",
            (args.name, args.phone or "", args.address or ""),
        )
        db.commit()
        db.close()
        print(f" Успех: Клиент {args.name} успешно добавлен через CLI!")

def cli_update_customer():
            if not args.name:
                print("Ошибка: Для изменения клиента обязательно укажите --id_customer")
            return
            db = sqlite3.connect("delivery_tables.db")
            c = db.cursor()
            c.execute("PRAGMA foreign_keys = ON;")
            c.execute("""
                UPDATE customers 
                SET name_customers = ?, phone_customers = ?, address_customers = ? 
                WHERE id_customer = ?;
            """, (args.name, args.phone, args.address, args.id_customer))        
            db.commit()
            db.close()
            print(f" Успех: Информация о клиенте {args.name} успешно изменена через CLI!")
            
def cli_delete_customer():
            if not args.id_customer:
                print("Ошибка: Укажите --id_customer для удаления клиента")
            return
            db = sqlite3.connect("delivery_tables.db")
            c = db.cursor()
            c.execute("PRAGMA foreign_keys = ON;")

def cli_add_order(name, raw_date, status_name="Новый"):
    db = sqlite3.connect("delivery_tables.db")
    c = db.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute("SELECT id_status FROM status WHERE name_status = ?;", (status_name,))
    status_row = c.fetchone()
    if not status_row:
        print(f"Ошибка: Статус '{status_name}' не найден в базе данных!")
        db.close()
        return
    status_id = status_row[0]
    c.execute("SELECT id_customer FROM customers WHERE name_customers = ?;", (name,))
    customer_row = c.fetchone()
    if not customer_row:
        print(f"Ошибка: Клиент {name} не найден в базе! Сначала добавьте клиента.")
        db.close()
        return
    customer_id = customer_row[0]
    c.execute("""
        INSERT INTO orders (customer_id, date_orders, status_id, total_orders)
        VALUES (?, ?, ?, ?);
    """, (customer_id, date, status_id, 0.0))
    db.commit()
    new_order_id = c.lastrowid
    c.execute("""
        UPDATE orders 
        SET total_orders = COALESCE((
            SELECT SUM(quantity_order_items * price_order_items) 
            FROM order_items 
            WHERE order_id = ?
        ), 0.0)
        WHERE id_order = ?;
    """, (new_order_id, new_order_id))
    db.commit()
    db.close()

def cli_update_order(order_id, customer_name, raw_date, status_name):
        try:
            if "." in raw_date:
                d, m, y = raw_date.split(".")
                date = f"{y}-{m}-{d}"
            else:
                date = raw_date
        except Exception:
            print("Ошибка: Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return

        db = sqlite3.connect("delivery_tables.db")
        c = db.cursor()
        c.execute("PRAGMA foreign_keys = ON;")

        c.execute("SELECT id_order FROM orders WHERE id_order = ?;", (order_id,))
        if not c.fetchone():
            print(f"Ошибка: Заказ с ID {order_id} не найден в базе данных!")
            db.close()
            return

        c.execute("SELECT id_status FROM status WHERE name_status = ?;", (status_name,))
        status_row = c.fetchone()
        if not status_row:
            print(f"Ошибка: Статус '{status_name}' не найден!")
            db.close()
            return
        status_id = status_row[0]

        c.execute("SELECT id_customer FROM customers WHERE name_customers = ?;", (customer_name,))
        customer_row = c.fetchone()
        if not customer_row:
            print(f"Ошибка: Клиент '{customer_name}' не найден!")
            db.close()
            return
        customer_id = customer_row[0]

        c.execute("""
            UPDATE orders 
            SET customer_id = ?, date_orders = ?, status_id = ? 
            WHERE id_order = ?;
        """, (customer_id, date, status_id, order_id))        
        db.commit()
        db.close()

        print(f"Успех: Данные заказа №{order_id} успешно изменены через CLI!")

        
def cli_delete_order():
        if not args.order_id:
            print("Ошибка: Укажите --order_id для удаления заказа")
            return
        print(f"Успех: Заказ №{new_order_id} для клиента {name} успешно удалён через CLI!")

def cli_import_orders_from_json(file_path):

    if not os.path.exists(file_path):
        print(f"Ошибка: Файл по пути '{file_path}' не найден!")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            imported_data = json.load(file)
            
        db = sqlite3.connect("delivery_tables.db")
        c = db.cursor()
        c.execute("PRAGMA foreign_keys = ON;")
        
        success_count = 0

        for order in imported_data:
            c.execute("SELECT id_customer FROM customers WHERE name_customers = ?;", (order["customer_name"],))
            customer_row = c.fetchone()
            
            c.execute("SELECT id_status FROM status WHERE name_status = ?;", (order["status"],))
            status_row = c.fetchone()
            
            if customer_row and status_row:
                c.execute("""
                    INSERT INTO orders (customer_id, date_orders, status_id, total_orders)
                    VALUES (?, ?, ?, ?);
                """, (customer_row[0], order["date"], status_row[0], order["total_price"]))
                success_count += 1
                
        db.commit()
        db.close()
        
        print(f"Успех: Импорт завершен! Успешно добавлено заказов: {success_count}")
        
    except Exception as e:
        print(f"Ошибка при импорте: {e}")


def run_cli():
    parser = argparse.ArgumentParser(
        description="CLI управление системой доставки"
    )
    parser.add_argument(
        "--action",
        choices=["add_customer", "update_customer", "delete_customer", "add_order", "update_order", "delete_order", "import_json", "export_json"],
        help="Выберите действие для выполнения",
    )

    parser.add_argument(
        "--name", help="Имя клиента (используется при add_customer и update_customer)"
    )
    parser.add_argument(
        "--phone", help="Телефон клиента (используется при add_customer и update_customer)"
    )
    parser.add_argument(
        "--address", help="Адрес клиента (используется при add_customer и update_customer)"
    )
    parser.add_argument(
        "--id_customer", help="ID клиента (используется при delete_customer и update_customer)"
    )
    
    parser.add_argument(
        "--id_order", type=int, help="ID заказа (используется при delete_order и update_order)"
    )
    parser.add_argument(
        "--date_orders", help="Дата заказа (используется при add_order и update_order)"
    )
    parser.add_argument(
    "--name_status", help="Статус заказа (используется при add_order и update_order)"
    )

    parser.add_argument(
    "--file_path", help="Путь к файлу (используется при import_json)"
    )

    args = parser.parse_args()    

    match args.action:
        case "add_customer": cli_add_customer()
        case "update_customer": cli_update_customer()
        case "delete_customer": cli_delete_customer()
        case "add_order": cli_add_order()
        case "update_order": cli_update_order()
        case "delete_order": cli_delete_order()
        case "import_json": cli_import_json()
        case "export_json":
            cli_export_json()
            print(" Успех: Данные выгружены в orders_export.json!")


# ВХОД В ПРОГРАММУ

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        root.mainloop()

