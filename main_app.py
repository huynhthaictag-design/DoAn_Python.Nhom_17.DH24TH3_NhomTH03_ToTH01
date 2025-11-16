# main_app.py

import tkinter as tk
from tkinter import ttk, Menu, messagebox
import sys

# Import modules
from database import conn, check_db_connection 
from hdv import HDVManager
from QLTDL import TuyenManager 
from diadiem import DiaDiemManager 
from datve import DatVeManager
from thongke import ThongKeManager

# --- Bảng màu (Color Palette) ---
# Đây là các màu từ hình ảnh của bạn
COLORS = {
    "background": "#fffffe",
    "headline": "#272343",      # Dùng cho Tiêu đề, Text Nút, Tab đang chọn
    "paragraph": "#2d334a",     # Dùng cho Text thông thường
    "button": "#ffd803",         # Nền nút
    "button_active": "#e6c200",  # Một màu tối hơn một chút cho (tự thêm)
    "secondary": "#e3f6f5",     # Nền tab không được chọn
    "tertiary": "#bae8e8"
}

# --- Helper Functions (Giữ nguyên) ---
def center_window(win, w=950, h=700):
    """Căn giữa cửa sổ ứng dụng."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# --- Hàm mở ứng dụng chính ---
def open_main_app(previous_window):
    if previous_window:
        previous_window.destroy()

    root = tk.Tk()
    root.title("HỆ THỐNG QUẢN TRỊ DU LỊCH (ADMIN)")
    center_window(root)
    root.resizable(True, True)
    
    # Cấu hình màu nền chính cho cửa sổ
    root.config(bg=COLORS["background"])

    if not check_db_connection(root):
        return 

    # --- Style Configuration (THÊM PHẦN NÀY) ---
    style = ttk.Style(root)
    
    # Sử dụng một theme 'clam' để cho phép tùy chỉnh màu sắc tốt hơn
    style.theme_use('clam')

    # Cấu hình chung
    # Nền cho tất cả widget, màu chữ (foreground)
    style.configure('.', 
                    background=COLORS["background"], 
                    foreground=COLORS["paragraph"])

    style.configure('TFrame', 
                    background=COLORS["background"])

    # Cấu hình cho Nút (TButton)
    style.configure('TButton', 
                    background=COLORS["button"], 
                    foreground=COLORS["headline"], 
                    font=('Arial', 10, 'bold'),
                    borderwidth=0)
    # Thay đổi màu khi di chuột hoặc nhấn
    style.map('TButton',
              background=[('active', COLORS["button_active"])])

    # Cấu hình cho Tab (TNotebook)
    style.configure('TNotebook', 
                    background=COLORS["background"], 
                    borderwidth=0)
                    
    style.configure('TNotebook.Tab',
                    background=COLORS["secondary"],  # Màu tab không được chọn
                    foreground=COLORS["paragraph"],
                    font=('Arial', 10),
                    padding=[10, 5]) # Thêm padding cho tab

    # Thay đổi màu cho tab đang được chọn (selected)
    style.map('TNotebook.Tab',
              background=[('selected', COLORS["background"])],
              foreground=[('selected', COLORS["headline"])])

    # --- Menu Bar ---
    menu = Menu(root)
    # Áp dụng màu cho Menu
    menu.config(bg=COLORS["background"], 
               fg=COLORS["paragraph"],
               activebackground=COLORS["button"],
               activeforeground=COLORS["headline"],
               relief=tk.FLAT)

    file_menu = Menu(menu, tearoff=0, 
                     bg=COLORS["background"], fg=COLORS["paragraph"],
                     activebackground=COLORS["button"], 
                     activeforeground=COLORS["headline"])
    file_menu.add_command(label='Exit', command=root.quit)
    menu.add_cascade(label='File', menu=file_menu)

    help_menu = Menu(menu, tearoff=0,
                     bg=COLORS["background"], fg=COLORS["paragraph"],
                     activebackground=COLORS["button"], 
                     activeforeground=COLORS["headline"])
    help_menu.add_command(label='About')
    menu.add_cascade(label='Help', menu=help_menu)
    root.config(menu=menu)

    # --- Notebook (Tab Control) ---
    tab_control = ttk.Notebook(root)
    
    # Các Frame này giờ sẽ tự động lấy màu nền từ style
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab4 = ttk.Frame(tab_control)
    tab5 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='Quản Lý Tuyến Du Lịch')
    tab_control.add(tab2, text='Quản Lý Hướng Dẫn Viên')
    tab_control.add(tab3, text='Quản Lý Địa Điểm') 
    tab_control.add(tab4, text='Quản Lý Đặt Vé') 
    tab_control.add(tab5, text='Thống Kê & Báo Cáo')
    tab_control.pack(expand=1, fill='both', padx=10, pady=10)

    # --- Khởi tạo các module quản lý ---
    # Các module này sẽ tự động sử dụng style đã định nghĩa
    tuyen_manager = TuyenManager(tab1)
    hdv_manager = HDVManager(tab2)
    diadiem_manager = DiaDiemManager(tab3)
    datve_manager = DatVeManager(tab4)
    thongke_manager = ThongKeManager(tab5) 

    root.mainloop()

    if conn and conn.is_connected():
        conn.close()

if __name__ == "__main__":
    open_main_app(None)