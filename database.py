# database.py

import mysql.connector
from tkinter import messagebox
import sys

# --- Database Connection ---
def ket_noi_csdl():
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

# Tạo kết nối toàn cục
conn = ket_noi_csdl()

def kiem_tra_ket_noi(root_window):
    """Kiểm tra và thông báo nếu kết nối CSDL không khả dụng."""
    global conn
    # Nếu mất kết nối, thử kết nối lại
    if conn is None or not conn.is_connected():
        conn = ket_noi_csdl() 
        
    if conn is None:
        messagebox.showerror(
            "Lỗi CSDL", 
            "Kết nối CSDL không khả dụng. Vui lòng kiểm tra MySQL server, tên database và thông tin đăng nhập."
        )
        root_window.destroy() 
        sys.exit()
        return False
    return True