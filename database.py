# database.py

import mysql.connector
from tkinter import messagebox
import sys

# --- Database Connection ---
def connect_db():
    """Thiết lập và trả về đối tượng kết nối CSDL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user='root',
            password='1234', 
            database="qltuyendulich"
        )
        if conn.is_connected():
            return conn
        return None
    except mysql.connector.Error as err:
        print(f"Lỗi Kết Nối CSDL: {err}")
        return None


conn = connect_db()

def check_db_connection(root_window):
    """Kiểm tra và thông báo nếu kết nối CSDL không khả dụng."""
    if not conn or not conn.is_connected():
        messagebox.showerror(
            "Lỗi CSDL", 
            "Kết nối CSDL không khả dụng. Vui lòng kiểm tra MySQL server, tên database và thông tin đăng nhập."
        )
        root_window.destroy() 
        sys.exit()
        return False
    return True

