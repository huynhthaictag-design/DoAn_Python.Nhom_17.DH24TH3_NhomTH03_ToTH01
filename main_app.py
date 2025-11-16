# main_app.py

import tkinter as tk
from tkinter import ttk, Menu, messagebox
import sys

from database import conn, kiem_tra_ket_noi 
from hdv import QuanLyHDV
from QLTDL  import QuanLyTuyen 
from diadiem import QuanLyDiaDiem 
from datve import QuanLyDatVe
from thongke import QuanLyThongKe


COLORS = {
    "background": "#fffffe",
    "headline": "#272343",      
    "paragraph": "#2d334a",     
    "button": "#ffd803",         
    "button_active": "#e6c200",  
    "secondary": "#e3f6f5",     
    "tertiary": "#bae8e8"
}

# --- Helper Functions 
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
    root.config(bg=COLORS["background"])

    # SỬA: Gọi hàm kiem_tra_ket_noi
    if not kiem_tra_ket_noi(root):
        return 

    # --- Style Configuration (Giữ nguyên) ---
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', 
                    background=COLORS["background"], 
                    foreground=COLORS["paragraph"])
    style.configure('TFrame', 
                    background=COLORS["background"])
    style.configure('TButton', 
                    background=COLORS["button"], 
                    foreground=COLORS["headline"], 
                    font=('Arial', 10, 'bold'),
                    borderwidth=0)
    style.map('TButton',
              background=[('active', COLORS["button_active"])])
    style.configure('TNotebook', 
                    background=COLORS["background"], 
                    borderwidth=0)
    style.configure('TNotebook.Tab',
                    background=COLORS["secondary"],  
                    foreground=COLORS["paragraph"],
                    font=('Arial', 10),
                    padding=[10, 5]) 
    style.map('TNotebook.Tab',
              background=[('selected', COLORS["background"])],
              foreground=[('selected', COLORS["headline"])])

    # --- Menu Bar  ---
    menu = Menu(root)
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

 
    tuyen_manager = QuanLyTuyen(tab1)
    hdv_manager = QuanLyHDV(tab2)
    diadiem_manager = QuanLyDiaDiem(tab3)
    datve_manager = QuanLyDatVe(tab4)
    thongke_manager = QuanLyThongKe(tab5) 

    root.mainloop()

    if conn and conn.is_connected():
        conn.close()

if __name__ == "__main__":
    open_main_app(None)