# diadiem.py

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from database import conn, kiem_tra_ket_noi 
class QuanLyDiaDiem:
    """Quản lý giao diện, dữ liệu và logic CRUD cho Tab Địa Điểm."""

    def __init__(self, parent_tab):
        self.parent_tab = parent_tab
        self.root = parent_tab.winfo_toplevel() 
        
        self.hovered_item = None 

        self.taoGiaoDien()
        self.taiDuLieu() 

    def taoGiaoDien(self):
        """Thiết lập tất cả widgets trên tab3."""
        
        # 1. Tiêu đề và Khung Tìm kiếm
        lbl_title = tk.Label(self.parent_tab, text="CHI TIẾT ĐỊA ĐIỂM ĐẾN", font=("Arial", 18, "bold"), fg="#005b96")
        lbl_title.pack(pady=10)

        frame_search = tk.Frame(self.parent_tab, padx=10)
        frame_search.pack(fill="x", pady=5)

        tk.Label(frame_search, text="Tìm Mã Địa Điểm:", font=("Arial", 10)).pack(side="left", padx=(10, 5))
        self.entry_search_maDD = tk.Entry(frame_search, width=15)
        self.entry_search_maDD.pack(side="left")

        tk.Button(frame_search, text="Tìm", command=self.timTheoMa, bg="#4da6ff", fg="white", font=("Arial", 9)).pack(side="left", padx=(6, 0))
        tk.Button(frame_search, text="Xem Tất Cả", command=self.taiDuLieu, bg="#99CCFF", fg="black", font=("Arial", 9)).pack(side="left", padx=(15, 0))


        # 2. Khung nhập thông tin (Entries)
        frame_info = tk.LabelFrame(self.parent_tab, text="Thông tin địa điểm", font=("Arial", 13, "bold"), bg="#e3ecfa", fg="#2d5c88", bd=2)
        frame_info.pack(pady=5, padx=10, fill="x")
        frame_info.columnconfigure(1, weight=1); frame_info.columnconfigure(3, weight=1) 

        tk.Label(frame_info, text="Mã Địa Điểm:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_madiadiem = tk.Entry(frame_info, width=30); 
        self.entry_madiadiem.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Tên Địa Điểm:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_tendiadiem = tk.Entry(frame_info, width=30); self.entry_tendiadiem.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Địa Chỉ:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.entry_diachi = tk.Entry(frame_info, width=30); self.entry_diachi.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Loại Hình:", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.combo_loaihinh = ttk.Combobox(frame_info, width=28, state="readonly", 
                                           values=["Bãi biển", "Di tích lịch sử", "Núi", "Công viên giải trí", "Thành phố", "Khác"])
        self.combo_loaihinh.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.combo_loaihinh.set("Khác")
        tk.Label(frame_info, text="Mô Tả:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_mota = tk.Entry(frame_info, width=70); self.entry_mota.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="w")

        
        # 3. Khung nút chức năng
        frame_buttons = tk.Frame(self.parent_tab, pady=10); frame_buttons.pack(pady=10)
        tk.Button(frame_buttons, text="Thêm", width=12, bg="#4CAF50", fg="white", command=self.themDiaDiem).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Sửa", width=12, bg="#FFC107", fg="black", command=self.suaDiaDiem).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Xóa", width=12, bg="#F44336", fg="white", command=self.xoaDiaDiem).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Làm Mới", width=12, command=self.xoaThongTinNhap).pack(side=tk.LEFT, padx=10)

        # 4. Treeview 
        tree_frame = tk.Frame(self.parent_tab, padx=10); tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass 
        style.map("Treeview", 
                  background=[('selected', '#007bff')],
                  foreground=[('selected', 'white')])

        columns = ('madiadiem', 'tendiadiem', 'diachi', 'loaihinh', 'mota')
        self.tree_diadiem = ttk.Treeview(tree_frame, columns=columns, show='headings')
        #cái nào không chọn sẽ normal nền trắng chữ đen
        self.tree_diadiem.tag_configure('normal', background='white', foreground='black')
        self.tree_diadiem.tag_configure('hover', background='#e6f2ff', foreground='black')

        self.tree_diadiem.heading('madiadiem', text='Mã ĐĐ'); self.tree_diadiem.column('madiadiem', width=60, anchor='center')
        self.tree_diadiem.heading('tendiadiem', text='Tên Địa Điểm'); self.tree_diadiem.column('tendiadiem', width=150)
        self.tree_diadiem.heading('diachi', text='Địa Chỉ'); self.tree_diadiem.column('diachi', width=150)
        self.tree_diadiem.heading('loaihinh', text='Loại Hình'); self.tree_diadiem.column('loaihinh', width=100, anchor='center')
        self.tree_diadiem.heading('mota', text='Mô Tả'); self.tree_diadiem.column('mota', width=200)
        #tạo thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_diadiem.yview)
        self.tree_diadiem.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_diadiem.pack(fill="both", expand=True)
        #chọn hàng nào thì hàng đó hiện lên
        self.tree_diadiem.bind('<<TreeviewSelect>>', self.chonHang)
        #gán sự kiện di chuột vào bảng
        self.tree_diadiem.bind('<Motion>', self.khiDiChuotVaoBang)
        self.tree_diadiem.bind('<Leave>', self.khiRoiChuotKhoiBang)

    # --- Logic Hover ---
    def khiDiChuotVaoBang(self, event):
        # xác định ID của hàng con đang đang đưa vào tộ độ y
        item = self.tree_diadiem.identify_row(event.y)
        selected_item = self.tree_diadiem.selection()[0] if self.tree_diadiem.selection() else None
        # nếu có hàng hover và không phải hàng được chọn thì đổi về normal
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_diadiem.item(self.hovered_item, tags=('normal',))
        # nếu con trỏ chuột đang ở trên một hàng khác với hàng hover hiện tại và không phải hàng được chọn thì đổi hàng đó thành hover
        if item and item != selected_item:
            self.tree_diadiem.item(item, tags=('hover',))
            self.hovered_item = item
        else:
            self.hovered_item = None 

    def khiRoiChuotKhoiBang(self, event):
        selected_item = self.tree_diadiem.selection()[0] if self.tree_diadiem.selection() else None
        # nếu có hàng hover và không phải hàng được chọn thì đổi về normal
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_diadiem.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None
            
    # --- CRUD Functions ---
    
    def xoaThongTinNhap(self):
        """Làm sạch tất cả các trường nhập liệu."""
        self.entry_madiadiem.delete(0, tk.END)
        self.entry_tendiadiem.delete(0, tk.END)
        self.entry_diachi.delete(0, tk.END)
        self.entry_mota.delete(0, tk.END)
        self.combo_loaihinh.set("Khác") 
        self.tree_diadiem.selection_remove(self.tree_diadiem.selection()) 
        self.entry_search_maDD.delete(0, tk.END)
        self.khiRoiChuotKhoiBang(None) # Reset hover

    def taiDuLieu(self):
        """Tải dữ liệu địa điểm từ CSDL."""
        if not kiem_tra_ket_noi(self.root): return
        for item in self.tree_diadiem.get_children(): self.tree_diadiem.delete(item)

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT MaDiaDiem, TenDiaDiem, DiaChi, LoaiHinh, MoTa FROM DiaDiem")
                for record in cursor.fetchall():
                    self.tree_diadiem.insert('', tk.END, values=record, tags=('normal',))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu Địa Điểm", f"Lỗi: {err}")
            
    def timTheoMa(self):
        """Tìm kiếm địa điểm theo Mã."""
        if not kiem_tra_ket_noi(self.root): return
        timkiem = self.entry_search_maDD.get().strip()
        if not timkiem: return self.taiDuLieu()
        for item in self.tree_diadiem.get_children(): self.tree_diadiem.delete(item)

        try:
            madd_search = int(timkiem)
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Mã Địa Điểm phải là số nguyên."); return self.taiDuLieu()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT MaDiaDiem, TenDiaDiem, DiaChi, LoaiHinh, MoTa FROM DiaDiem WHERE MaDiaDiem = %s"
                cursor.execute(sql, (madd_search,))
                records = cursor.fetchall()
                if not records:
                    messagebox.showwarning("Không Tìm Thấy", f"Không tìm thấy Địa Điểm có Mã: {madd_search}"); self.taiDuLieu(); return
                for record in records:
                    self.tree_diadiem.insert('', tk.END, values=record, tags=('normal',))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu", f"Lỗi: {err}")

    def themDiaDiem(self):
        """Thêm một địa điểm mới."""
        if not kiem_tra_ket_noi(self.root): return
        
        madd_input = self.entry_madiadiem.get().strip()
        tendiadiem = self.entry_tendiadiem.get().strip()
        diachi = self.entry_diachi.get().strip()
        loaihinh = self.combo_loaihinh.get().strip()
        mota = self.entry_mota.get().strip()

        try:
            madd = int(madd_input)
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Mã Địa Điểm phải là số nguyên."); return
            
        if not tendiadiem:
            messagebox.showerror("Lỗi Nhập Liệu", "Tên Địa Điểm không được để trống."); return

        sql = "INSERT INTO DiaDiem (MaDiaDiem, TenDiaDiem, DiaChi, LoaiHinh, MoTa) VALUES (%s, %s, %s, %s, %s)"
        values = (madd, tendiadiem, diachi, loaihinh, mota) 
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()
                messagebox.showinfo("Thành Công", "Thêm địa điểm thành công.")
                self.xoaThongTinNhap()
                self.taiDuLieu()
        except mysql.connector.IntegrityError as err:
            messagebox.showerror("Lỗi SQL (Thêm Địa Điểm)", f"Lỗi: Mã Địa Điểm {madd} đã tồn tại.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Thêm Địa Điểm)", f"Lỗi: {err}")

    def suaDiaDiem(self):
        """Cập nhật thông tin địa điểm đã chọn."""
        if not kiem_tra_ket_noi(self.root): return
        
        madd_input = self.entry_madiadiem.get().strip()
        tendiadiem = self.entry_tendiadiem.get().strip()
        diachi = self.entry_diachi.get().strip()
        loaihinh = self.combo_loaihinh.get().strip()
        mota = self.entry_mota.get().strip()

        try: 
            madd = int(madd_input)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã Địa Điểm không hợp lệ hoặc không được chọn."); return
            
        if not tendiadiem:
            messagebox.showerror("Lỗi Nhập Liệu", "Tên Địa Điểm không được để trống."); return

        sql = "UPDATE DiaDiem SET TenDiaDiem=%s, DiaChi=%s, LoaiHinh=%s, MoTa=%s WHERE MaDiaDiem=%s"
        values = (tendiadiem, diachi, loaihinh, mota, madd)
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Thành Công", "Cập nhật địa điểm thành công.")
                else:
                    messagebox.showwarning("Cảnh báo", f"Không tìm thấy Địa Điểm có Mã {madd} để cập nhật.")
                self.xoaThongTinNhap()
                self.taiDuLieu()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Sửa Địa Điểm)", f"Lỗi: {err}")

    def xoaDiaDiem(self):
        """Xóa địa điểm đã chọn."""
        if not kiem_tra_ket_noi(self.root): return
        
        madd_input = self.entry_madiadiem.get().strip()
        try: 
            madd = int(madd_input)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã Địa Điểm không hợp lệ hoặc không được chọn."); return

        if not messagebox.askyesno("Xác Nhận Xóa", f"Bạn có chắc chắn muốn xóa Địa Điểm có Mã {madd} không?"): return
        
        sql = "DELETE FROM DiaDiem WHERE MaDiaDiem = %s"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (madd,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Thành Công", "Xóa địa điểm thành công.")
                else:
                    messagebox.showwarning("Cảnh báo", "Không tìm thấy địa điểm để xóa.")
                self.xoaThongTinNhap()
                self.taiDuLieu()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Xóa Địa Điểm)", f"Lỗi: {err}")

    def chonHang(self, event):
        """Hiển thị dữ liệu của dòng được chọn lên các ô nhập liệu."""
        
        selected_item = self.tree_diadiem.focus()
        if self.hovered_item and self.hovered_item != selected_item:
             self.tree_diadiem.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None

        self.entry_madiadiem.delete(0, tk.END)
        self.entry_tendiadiem.delete(0, tk.END)
        self.entry_diachi.delete(0, tk.END)
        self.entry_mota.delete(0, tk.END)
        
        if not selected_item: 
            self.combo_loaihinh.set("Khác")
            return
        
        values = self.tree_diadiem.item(selected_item, 'values')
        
        if values:
            self.entry_madiadiem.insert(0, values[0])
            self.entry_tendiadiem.insert(0, values[1])
            self.entry_diachi.insert(0, values[2])
            self.combo_loaihinh.set(values[3])
            self.entry_mota.insert(0, values[4])