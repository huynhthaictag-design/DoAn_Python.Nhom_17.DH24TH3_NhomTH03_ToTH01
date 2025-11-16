# user_app.py

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

from database import conn, check_db_connection 

# --- Định nghĩa màu sắc (Đã có trong code của bạn) ---
COLOR_BACKGROUND_MAIN = "#3da9fc" # Main Background / Button / Highlight
COLOR_HEADLINE = "#094067" # Headline / Stroke
COLOR_PARAGRAPH = "#5f6c7b" # Paragraph
COLOR_BUTTON_TEXT = "#fffffe" # Button text / Main
COLOR_SECONDARY = "#90b4ce" # Secondary
COLOR_TERTIARY = "#ef4565" # Tertiary (cho lỗi/cảnh báo)

class UserApp:
    """Giao diện chính cho Người dùng (User)"""
    def __init__(self, root):
        self.root = root
        self.root.title("Chào mừng Khách hàng")
        self.root.geometry("1100x700") 
        self.root.resizable(True, True)

        self.hovered_item = None
        
        # SỬA: Đổi tên các hàm khởi tạo
        self.tao_khung_chinh()
        self.tao_menu_trai()
        self.tao_khung_noi_dung()
        
        # Tải dữ liệu
        self.tai_bo_loc_diem_den() # Tải dữ liệu cho combobox lọc
        self.tai_du_lieu_tour() # Tải dữ liệu cho Treeview

    def tao_khung_chinh(self):
        """Tạo 2 khung chính: Menu (trái) và Nội dung (phải)"""
        # 1. Khung Menu bên trái
        self.menu_frame = tk.Frame(self.root, bg=COLOR_HEADLINE, width=200) # Nền xanh đậm
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)

        # 2. Khung Nội dung bên phải
        self.content_frame = tk.Frame(self.root, bg=COLOR_BUTTON_TEXT) # Nền trắng
        self.content_frame.pack(side="right", fill="both", expand=True)

    def tao_menu_trai(self):
        """Tạo các nút bấm hoạt động như Menu bên trái"""
        
        tk.Label(self.menu_frame, text="MENU", font=("Poppins", 16, "bold"),
                 bg=COLOR_HEADLINE, fg=COLOR_BUTTON_TEXT).pack(pady=20) 

        menu_items = [
            ("Xem Tours", self.hien_thi_tour),
            ("Đặt Vé", self.mo_cua_so_dat_ve), # SỬA: Đổi tên hàm
            ("Thoát", self.root.quit)
        ]

        for (text, command) in menu_items:
            btn = tk.Button(self.menu_frame, text=text, font=("Poppins", 11),
                            bg=COLOR_BACKGROUND_MAIN, fg=COLOR_BUTTON_TEXT, 
                            relief="flat", anchor="w",
                            padx=20, cursor="hand2")
            btn.config(command=command)
            btn.pack(fill="x", pady=5, padx=10)
            
            # Thay đổi màu khi hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_SECONDARY, fg=COLOR_HEADLINE)) 
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BACKGROUND_MAIN, fg=COLOR_BUTTON_TEXT))


    def tao_khung_noi_dung(self):
        """Tạo khu vực hiển thị Treeview (List view) và Bộ lọc"""
        
        lbl_title = tk.Label(self.content_frame, text="DANH SÁCH CÁC TOUR HIỆN CÓ", 
                             font=("Arial", 18, "bold"), fg=COLOR_HEADLINE, bg=COLOR_BUTTON_TEXT) 
        lbl_title.pack(pady=15)
        
        # --- KHUNG BỘ LỌC (MỚI) ---
        filter_frame = tk.Frame(self.content_frame, bg=COLOR_BUTTON_TEXT, padx=10)
        filter_frame.pack(fill="x", pady=5)
        
        # (Giữ nguyên các widget trong Khung Lọc)
        tk.Label(filter_frame, text="Loại Tour:", font=("Arial", 10), bg=COLOR_BUTTON_TEXT, fg=COLOR_PARAGRAPH).pack(side=tk.LEFT, padx=(5,2))
        self.combo_filter_loai = ttk.Combobox(filter_frame, width=12, state="readonly", values=["Tất cả", "Trong Nước", "Nước Ngoài"])
        self.combo_filter_loai.pack(side=tk.LEFT, padx=(0,10))
        self.combo_filter_loai.set("Tất cả")
        tk.Label(filter_frame, text="Điểm Đến:", font=("Arial", 10), bg=COLOR_BUTTON_TEXT, fg=COLOR_PARAGRAPH).pack(side=tk.LEFT, padx=(5,2))
        self.combo_filter_diemden = ttk.Combobox(filter_frame, width=15, state="readonly", values=["Tất cả"])
        self.combo_filter_diemden.pack(side=tk.LEFT, padx=(0,10))
        self.combo_filter_diemden.set("Tất cả")
        tk.Label(filter_frame, text="Giá từ:", font=("Arial", 10), bg=COLOR_BUTTON_TEXT, fg=COLOR_PARAGRAPH).pack(side=tk.LEFT, padx=(5,2))
        self.entry_filter_gia_tu = tk.Entry(filter_frame, width=12, relief="solid", bd=1, highlightcolor=COLOR_SECONDARY)
        self.entry_filter_gia_tu.pack(side=tk.LEFT, padx=(0,5))
        tk.Label(filter_frame, text="Giá đến:", font=("Arial", 10), bg=COLOR_BUTTON_TEXT, fg=COLOR_PARAGRAPH).pack(side=tk.LEFT, padx=(5,2))
        self.entry_filter_gia_den = tk.Entry(filter_frame, width=12, relief="solid", bd=1, highlightcolor=COLOR_SECONDARY)
        self.entry_filter_gia_den.pack(side=tk.LEFT, padx=(0,10))

        # Nút Lọc và Xóa Lọc
        btn_filter = tk.Button(filter_frame, text="Lọc", font=("Arial", 10, "bold"), 
                               bg=COLOR_BACKGROUND_MAIN, fg=COLOR_BUTTON_TEXT, 
                               command=self.tai_du_lieu_tour, relief="flat", cursor="hand2") # SỬA: Đổi tên hàm
        btn_filter.pack(side=tk.LEFT, padx=5)
        
        btn_clear_filter = tk.Button(filter_frame, text="Xóa Lọc", font=("Arial", 10), 
                                     bg=COLOR_SECONDARY, fg=COLOR_HEADLINE, 
                                     command=self.xoa_bo_loc, relief="flat", cursor="hand2") # SỬA: Đổi tên hàm
        btn_clear_filter.pack(side=tk.LEFT, padx=5)
        
        # --- KHUNG TREEVIEW ---
        tree_frame = tk.Frame(self.content_frame, padx=10, bg=COLOR_BUTTON_TEXT) # Nền trắng
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass 
        
        # (Giữ nguyên cấu hình Style)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=COLOR_SECONDARY, foreground=COLOR_HEADLINE)
        style.configure("Treeview", background=COLOR_BUTTON_TEXT, foreground=COLOR_PARAGRAPH, rowheight=25)
        style.map("Treeview", background=[('selected', COLOR_BACKGROUND_MAIN)], foreground=[('selected', COLOR_BUTTON_TEXT)])

        columns = ('maso', 'tentuyen', 'khoihanh', 'diemden', 'thoiluong', 'giatour_display', 'giatour_raw', 'hdv', 'loai', 'mota')
        self.tree_tours = ttk.Treeview(tree_frame, columns=columns, show='headings')

        self.tree_tours.tag_configure('normal', background=COLOR_BUTTON_TEXT, foreground=COLOR_PARAGRAPH)
        self.tree_tours.tag_configure('hover', background='#e0f2f7', foreground=COLOR_HEADLINE) 

        self.tree_tours.config(displaycolumns=('tentuyen', 'khoihanh', 'diemden', 'thoiluong', 'giatour_display', 'hdv', 'loai', 'mota'))

        # (Giữ nguyên cấu hình Headings)
        self.tree_tours.heading('tentuyen', text='Tên Tuyến'); self.tree_tours.column('tentuyen', width=180)
        self.tree_tours.heading('khoihanh', text='Khởi Hành'); self.tree_tours.column('khoihanh', width=120)
        self.tree_tours.heading('diemden', text='Điểm Đến'); self.tree_tours.column('diemden', width=120)
        self.tree_tours.heading('thoiluong', text='Thời Lượng'); self.tree_tours.column('thoiluong', width=80, anchor='center')
        self.tree_tours.heading('giatour_display', text='Giá Tour'); self.tree_tours.column('giatour_display', width=100, anchor='e')
        self.tree_tours.heading('hdv', text='HDV'); self.tree_tours.column('hdv', width=120)
        self.tree_tours.heading('loai', text='Loại'); self.tree_tours.column('loai', width=80, anchor='center')
        self.tree_tours.heading('mota', text='Mô Tả'); self.tree_tours.column('mota', width=200)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_tours.yview)
        self.tree_tours.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_tours.pack(fill="both", expand=True)
        
        # SỬA: Đổi tên hàm
        self.tree_tours.bind('<Motion>', self.khi_di_chuot_treeview)
        self.tree_tours.bind('<Leave>', self.khi_roi_chuot_treeview)
        self.tree_tours.bind('<Double-1>', self.mo_cua_so_dat_ve)

    def tai_bo_loc_diem_den(self):
        """Tải danh sách các điểm đến cho Combobox lọc."""
        if not check_db_connection(self.root): return
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT DISTINCT TenDiaDiem FROM DiaDiem ORDER BY TenDiaDiem")
                records = cursor.fetchall()
                diemden_list = ["Tất cả"] + [row[0] for row in records]
                self.combo_filter_diemden['values'] = diemden_list
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Bộ Lọc", f"Không thể tải danh sách điểm đến: {err}")

    def xoa_bo_loc(self):
        """Xóa tất cả các bộ lọc và tải lại dữ liệu."""
        self.combo_filter_loai.set("Tất cả")
        self.combo_filter_diemden.set("Tất cả")
        self.entry_filter_gia_tu.delete(0, tk.END)
        self.entry_filter_gia_den.delete(0, tk.END)
        self.tai_du_lieu_tour() # SỬA: Đổi tên hàm

    def tai_du_lieu_tour(self):
        """Tải dữ liệu Tour dựa trên các bộ lọc đã chọn."""
        if not check_db_connection(self.root): return
        for item in self.tree_tours.get_children(): self.tree_tours.delete(item)

        base_sql = """
        SELECT 
            T.maso, T.tentuyen, DD_KhoiHanh.TenDiaDiem AS DiemKhoiHanh,
            DD_Den.TenDiaDiem AS DiemDen, T.thoiluong, 
            CONCAT(FORMAT(T.giatour, 0), ' VNĐ') AS GiaTourDisplay,
            T.giatour, H.tenhdv AS TenHDV, T.loaitour, T.mota
        FROM tuyendulich AS T
        LEFT JOIN DiaDiem AS DD_KhoiHanh ON T.MaDiemKhoiHanh = DD_KhoiHanh.MaDiaDiem
        LEFT JOIN DiaDiem AS DD_Den ON T.MaDiemDen = DD_Den.MaDiaDiem
        LEFT JOIN huongdanvien AS H ON T.MaHDV = H.mahdv
        """
        
        where_clauses = []
        params = []
        
        try:
            # (Logic bên trong hàm này không thay đổi)
            loai_tour = self.combo_filter_loai.get()
            if loai_tour and loai_tour != "Tất cả":
                where_clauses.append("T.loaitour = %s")
                params.append(loai_tour)

            diem_den = self.combo_filter_diemden.get()
            if diem_den and diem_den != "Tất cả":
                where_clauses.append("DD_Den.TenDiaDiem = %s")
                params.append(diem_den)

            gia_tu_str = self.entry_filter_gia_tu.get()
            if gia_tu_str:
                try:
                    gia_tu = float(gia_tu_str)
                    where_clauses.append("T.giatour >= %s")
                    params.append(gia_tu)
                except ValueError:
                    messagebox.showwarning("Lỗi Dữ Liệu", "Giá TỪ phải là một con số.")
                    return

            gia_den_str = self.entry_filter_gia_den.get()
            if gia_den_str:
                try:
                    gia_den = float(gia_den_str)
                    where_clauses.append("T.giatour <= %s")
                    params.append(gia_den)
                except ValueError:
                    messagebox.showwarning("Lỗi Dữ Liệu", "Giá ĐẾN phải là một con số.")
                    return

            final_sql = base_sql
            if where_clauses:
                final_sql += " WHERE " + " AND ".join(where_clauses)
            final_sql += " ORDER BY T.tentuyen"

            with conn.cursor() as cursor:
                cursor.execute(final_sql, tuple(params))
                for record in cursor.fetchall():
                    self.tree_tours.insert('', tk.END, values=record, tags=('normal',))
                    
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu Tours", f"Lỗi: {err}")

    
    # --- Chức năng Đặt Vé ---
    
    def mo_cua_so_dat_ve(self, event=None):
        """Mở cửa sổ Toplevel để đặt vé cho tour đã chọn."""
        selected_item = self.tree_tours.focus()
        if not selected_item:
            messagebox.showwarning("Chưa chọn Tour", "Vui lòng chọn một tour từ danh sách để đặt vé.")
            return

        values = self.tree_tours.item(selected_item, 'values')
        
        try:
            ma_tuyen = int(values[0])
            ten_tuyen = values[1]
            gia_tour_raw = float(values[6])
        except (IndexError, ValueError):
            messagebox.showerror("Lỗi Dữ Liệu", "Không thể lấy thông tin tour. Dữ liệu bị lỗi.")
            return

        self.book_window = tk.Toplevel(self.root)
        self.book_window.title("Xác Nhận Đặt Vé")
        self.book_window.geometry("400x350")
        self.book_window.transient(self.root) 
        self.book_window.grab_set() 

        form_frame = tk.Frame(self.book_window, padx=20, pady=20, bg=COLOR_BUTTON_TEXT) 
        form_frame.pack(fill="both", expand=True)

        # (Giữ nguyên các widget trong cửa sổ đặt vé)
        tk.Label(form_frame, text="ĐẶT VÉ TOUR", font=("Arial", 16, "bold"), fg=COLOR_HEADLINE, bg=COLOR_BUTTON_TEXT).pack(pady=10)
        tk.Label(form_frame, text=f"Tour: {ten_tuyen}", font=("Arial", 11, "bold"), fg=COLOR_PARAGRAPH, bg=COLOR_BUTTON_TEXT).pack(anchor="w", pady=5)
        tk.Label(form_frame, text=f"Giá vé: {gia_tour_raw:,.0f} VNĐ/vé", font=("Arial", 10), fg=COLOR_PARAGRAPH, bg=COLOR_BUTTON_TEXT).pack(anchor="w")
        tk.Label(form_frame, text="Số lượng vé:", font=("Arial", 10), fg=COLOR_PARAGRAPH, bg=COLOR_BUTTON_TEXT).pack(anchor="w", pady=(10,0))
        entry_soluong = tk.Spinbox(form_frame, from_=1, to=50, width=10, font=("Arial", 10),
                                   bg=COLOR_BUTTON_TEXT, fg=COLOR_HEADLINE, highlightbackground=COLOR_SECONDARY) 
        entry_soluong.pack(anchor="w", fill="x", pady=5)
        
        submit_btn = ttk.Button(form_frame, text="Xác nhận Đặt Vé", 
                                style="TButton", 
                                command=lambda: self.xac_nhan_dat_ve( # SỬA: Đổi tên hàm
                                    ma_tuyen, 
                                    gia_tour_raw,
                                    entry_soluong.get()
                                ))
        submit_btn.pack(pady=20)

    def xac_nhan_dat_ve(self, ma_tuyen, gia_tour_mot_ve, so_luong_str):
        """Xử lý logic INSERT vào bảng DatVe."""
        try:
            so_luong = int(so_luong_str)
            if so_luong <= 0:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên dương.", parent=self.book_window)
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng không hợp lệ.", parent=self.book_window)
            return

        tong_tien = gia_tour_mot_ve * so_luong
        ngay_dat = date.today().strftime('%Y-%m-%d')

        if not check_db_connection(self.root): return

        try:
            with conn.cursor() as cursor:
                # (Logic bên trong không đổi)
                cursor.execute("SELECT MAX(MaVe) FROM DatVe")
                max_mave = cursor.fetchone()[0]
                new_mave = (max_mave if max_mave is not None else 0) + 1
                
                sql = "INSERT INTO DatVe (MaVe, MaTuyen, NgayDatVe, SoLuongVe, TongTien) VALUES (%s, %s, %s, %s, %s)"
                values = (new_mave, ma_tuyen, ngay_dat, so_luong, tong_tien)
                
                cursor.execute(sql, values)
                conn.commit()
                
                messagebox.showinfo("Thành Công", 
                                    f"Đặt vé thành công!\nMã vé của bạn là: {new_mave}\nTổng tiền: {tong_tien:,.0f} VNĐ",
                                    parent=self.book_window)
                
                self.book_window.destroy() 
                
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Không thể đặt vé: {err}", parent=self.book_window)

    def hien_thi_tour(self):
        # Chức năng này hiện không làm gì vì đã ở view tour
        pass 

    # --- Logic Hover ---
    def khi_di_chuot_treeview(self, event):
        item = self.tree_tours.identify_row(event.y)
        selected_item = self.tree_tours.selection()[0] if self.tree_tours.selection() else None
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_tours.item(self.hovered_item, tags=('normal',))
        if item and item != selected_item:
            self.tree_tours.item(item, tags=('hover',))
            self.hovered_item = item
        else: self.hovered_item = None
    
    def khi_roi_chuot_treeview(self, event):
        selected_item = self.tree_tours.selection()[0] if self.tree_tours.selection() else None
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_tours.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None

# --- SỬA: Đổi tên hàm toàn cục ---
def mo_ung_dung_user(previous_window):
    """
    Hàm được gọi từ login.py sau khi đăng nhập User thành công.
    """
    if previous_window:
        previous_window.destroy()
    root = tk.Tk()
    if not check_db_connection(root):
        return 
    app = UserApp(root)
    root.mainloop()
    if conn and conn.is_connected():
        conn.close()

if __name__ == "__main__":
    mo_ung_dung_user(None) # SỬA: Đổi tên hàm