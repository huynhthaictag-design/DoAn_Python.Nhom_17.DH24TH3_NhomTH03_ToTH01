# hdv_module.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import mysql.connector

# Import kết nối CSDL (Giả định file database.py và các biến conn, check_db_connection tồn tại)
from database import conn, check_db_connection 

class HDVManager:
    """Quản lý giao diện, dữ liệu và logic CRUD cho Tab Hướng Dẫn Viên."""

    def __init__(self, parent_tab):
        self.parent_tab = parent_tab
        self.root = parent_tab.winfo_toplevel() 
        
        # THÊM: Biến theo dõi hover
        self.hovered_item = None 

        self._create_widgets()
        self.load_data() # Tải dữ liệu khi Tab được khởi tạo

    def _create_widgets(self):
        """Thiết lập tất cả widgets trên tab2."""
        
        # 1. Tiêu đề và Khung Tìm kiếm
        # ... (Code giữ nguyên) ...
        lbl_title = tk.Label(self.parent_tab, text="CHI TIẾT HƯỚNG DẪN VIÊN", font=("Arial", 18, "bold"), fg="blue")
        lbl_title.pack(pady=10)
        frame_title_search_hdv = tk.Frame(self.parent_tab, padx=10)
        frame_title_search_hdv.pack(fill="x", pady=5)
        tk.Label(frame_title_search_hdv, text="Tìm Mã HDV:", font=("Arial", 10)).pack(side="left", padx=(10, 5))
        self.entry_search_mahdv = tk.Entry(frame_title_search_hdv, width=15)
        self.entry_search_mahdv.pack(side="left")
        tk.Button(frame_title_search_hdv, text="Tìm", command=self.search_by_mahdv, bg="#4da6ff", fg="white", font=("Arial", 9)).pack(side="left", padx=(6, 0))
        tk.Button(frame_title_search_hdv, text="Xem Tất Cả", command=self.load_data, bg="#99CCFF", fg="black", font=("Arial", 9)).pack(side="left", padx=(15, 0))

        # 2. Khung nhập thông tin (Entries)
        # ... (Code giữ nguyên) ...
        frame_info = tk.Frame(self.parent_tab, padx=20, pady=10, relief=tk.GROOVE, borderwidth=1)
        frame_info.pack(pady=5, padx=10, fill="x")
        frame_info.columnconfigure(1, weight=1); frame_info.columnconfigure(3, weight=1) 
        tk.Label(frame_info, text="Mã HDV:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_mahdv = tk.Entry(frame_info, width=30); 
        self.entry_mahdv.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Tên HDV:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_tenhdv = tk.Entry(frame_info, width=30); self.entry_tenhdv.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Số Điện Thoại:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_sdt = tk.Entry(frame_info, width=30); self.entry_sdt.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Email:", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.entry_email = tk.Entry(frame_info, width=30); self.entry_email.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Ngày Sinh:", font=("Arial", 10)).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.entry_ngaysinh = DateEntry(frame_info, width=12, date_pattern='dd/mm/yyyy', year=1990); self.entry_ngaysinh.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        tk.Label(frame_info, text="Kinh nghiệm (năm):", font=("Arial", 10)).grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.entry_kinhnghiem = tk.Spinbox(frame_info, from_=0, to=50, width=5); self.entry_kinhnghiem.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        self.entry_kinhnghiem.delete(0, tk.END); self.entry_kinhnghiem.insert(0, 0)
        
        # 3. Khung nút chức năng
        # ... (Code giữ nguyên) ...
        frame_buttons = tk.Frame(self.parent_tab, pady=10); frame_buttons.pack(pady=10)
        tk.Button(frame_buttons, text="Thêm", width=12, bg="#4CAF50", fg="white", command=self.add_hdv).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Sửa", width=12, bg="#FFC107", fg="black", command=self.update_hdv).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Xóa", width=12, bg="#F44336", fg="white", command=self.delete_hdv).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Làm Mới", width=12, command=self.clear_entries).pack(side=tk.LEFT, padx=10)

        # 4. Treeview 
        tree_frame = tk.Frame(self.parent_tab, padx=10); tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # --- SỬA LOGIC HOVER BẮT ĐẦU ---
        style = ttk.Style()
        try:
            # SỬA 1: Ép buộc theme 'clam'
            style.theme_use("clam")
        except tk.TclError:
            pass 

        # SỬA 2: Định nghĩa màu cho trạng thái 'selected'
        style.map("Treeview", 
                  background=[('selected', '#007bff')], # Xanh đậm
                  foreground=[('selected', 'white')])

        columns = ('mahdv', 'tenhdv', 'sodienthoai', 'email', 'ngaysinh', 'kinhnghiem')
        self.tree_hdv = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # SỬA 3: Cấu hình TAGS màu
        self.tree_hdv.tag_configure('normal', background='white', foreground='black')
        self.tree_hdv.tag_configure('hover', background='#e6f2ff', foreground='black') # Xanh nhạt

        # ... (Code headings và columns giữ nguyên)
        self.tree_hdv.heading('mahdv', text='Mã HDV'); self.tree_hdv.column('mahdv', width=60, anchor='center')
        self.tree_hdv.heading('tenhdv', text='Tên HDV'); self.tree_hdv.column('tenhdv', width=150)
        self.tree_hdv.heading('sodienthoai', text='SĐT'); self.tree_hdv.column('sodienthoai', width=100, anchor='center')
        self.tree_hdv.heading('email', text='Email'); self.tree_hdv.column('email', width=200)
        self.tree_hdv.heading('ngaysinh', text='Ngày Sinh'); self.tree_hdv.column('ngaysinh', width=100, anchor='center')
        self.tree_hdv.heading('kinhnghiem', text='Kinh Nghiệm'); self.tree_hdv.column('kinhnghiem', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_hdv.yview)
        self.tree_hdv.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_hdv.pack(fill="both", expand=True)
        
        # SỬA 4: Ràng buộc sự kiện
        self.tree_hdv.bind('<<TreeviewSelect>>', self.select_record)
        self.tree_hdv.bind('<Motion>', self._on_tree_hover)
        self.tree_hdv.bind('<Leave>', self._on_tree_leave)
        
        # --- SỬA LOGIC HOVER KẾT THÚC ---

    # --- THÊM: Logic Hover mới ---

    def _on_tree_hover(self, event):
        """Thay đổi tag của dòng khi di chuột qua."""
        item = self.tree_hdv.identify_row(event.y)
        
        selected_item = self.tree_hdv.selection()[0] if self.tree_hdv.selection() else None

        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_hdv.item(self.hovered_item, tags=('normal',))

        if item and item != selected_item:
            self.tree_hdv.item(item, tags=('hover',))
            self.hovered_item = item
        else:
            self.hovered_item = None 

    def _on_tree_leave(self, event):
        """Khôi phục màu của dòng khi chuột rời khỏi Treeview."""
        selected_item = self.tree_hdv.selection()[0] if self.tree_hdv.selection() else None
        
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_hdv.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None
            
    # --- CRUD Functions ---
    
    def clear_entries(self):
        """Làm sạch tất cả các trường nhập liệu."""
        self.entry_mahdv.delete(0, tk.END)
        self.entry_tenhdv.delete(0, tk.END)
        self.entry_sdt.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_ngaysinh.set_date(date.today()) 
        self.entry_kinhnghiem.delete(0, tk.END)
        self.entry_kinhnghiem.insert(0, 0)
        self.tree_hdv.selection_remove(self.tree_hdv.selection()) 
        self.entry_search_mahdv.delete(0, tk.END)
        
        # THÊM: Reset hover
        self._on_tree_leave(None)

    def load_data(self):
        """Tải dữ liệu hướng dẫn viên từ CSDL và hiển thị lên Treeview HDV."""
        if not check_db_connection(self.root): return
        for item in self.tree_hdv.get_children(): self.tree_hdv.delete(item)

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT mahdv, tenhdv, sodienthoai, email, DATE_FORMAT(ngaysinh, '%d/%m/%Y'), kinhnghiem FROM huongdanvien")
                for record in cursor.fetchall():
                    # SỬA: Thêm tag 'normal'
                    self.tree_hdv.insert('', tk.END, values=record, tags=('normal',))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu HDV", f"Lỗi: {err}")
            
    def search_by_mahdv(self):
        """Tìm kiếm hướng dẫn viên theo Mã HDV."""
        if not check_db_connection(self.root): return
        timkiem = self.entry_search_mahdv.get().strip()
        if not timkiem: return self.load_data()
        for item in self.tree_hdv.get_children(): self.tree_hdv.delete(item)

        try:
            mahdv_search = int(timkiem)
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Mã HDV phải là số nguyên."); return self.load_data()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT mahdv, tenhdv, sodienthoai, email, DATE_FORMAT(ngaysinh, '%d/%m/%Y'), kinhnghiem FROM huongdanvien WHERE mahdv = %s"
                cursor.execute(sql, (mahdv_search,))
                records = cursor.fetchall()
                if not records:
                    messagebox.showwarning("Không Tìm Thấy", f"Không tìm thấy HDV có Mã: {mahdv_search}"); self.load_data(); return
                for record in records:
                    # SỬA: Thêm tag 'normal'
                    self.tree_hdv.insert('', tk.END, values=record, tags=('normal',))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu", f"Lỗi: {err}")

    # ... (add_hdv, update_hdv, delete_hdv giữ nguyên) ...
    def add_hdv(self):
        if not check_db_connection(self.root): return
        mahdv_input = self.entry_mahdv.get().strip()
        tenhdv = self.entry_tenhdv.get().strip()
        sdt = self.entry_sdt.get().strip()
        email = self.entry_email.get().strip()
        ngaysinh_str = self.entry_ngaysinh.get_date().strftime('%Y-%m-%d')
        try: 
            kinhnghiem = int(self.entry_kinhnghiem.get())
            if kinhnghiem < 0:
                messagebox.showerror("Lỗi Dữ Liệu", "Kinh nghiệm không được là số âm."); return
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Kinh nghiệm phải là số nguyên."); return
        if not all([tenhdv, email]):
            messagebox.showerror("Lỗi Nhập Liệu", "Tên HDV và Email không được để trống."); return
        if mahdv_input:
            try:
                mahdv = int(mahdv_input)
            except ValueError:
                messagebox.showerror("Lỗi Dữ Liệu", "Mã HDV phải là số nguyên."); return
            sql = "INSERT INTO huongdanvien (mahdv, tenhdv, sodienthoai, email, ngaysinh, kinhnghiem) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (mahdv, tenhdv, sdt, email, ngaysinh_str, kinhnghiem) 
        else:
            sql = "INSERT INTO huongdanvien (tenhdv, sodienthoai, email, ngaysinh, kinhnghiem) VALUES (%s, %s, %s, %s, %s)"
            values = (tenhdv, sdt, email, ngaysinh_str, kinhnghiem) 
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()
                messagebox.showinfo("Thành Công", "Thêm hướng dẫn viên thành công.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.IntegrityError as err:
            messagebox.showerror("Lỗi SQL (Thêm HDV)", f"Lỗi: Email hoặc Mã HDV đã tồn tại hoặc dữ liệu không hợp lệ. Chi tiết: {err}")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Thêm HDV)", f"Lỗi: {err}")

    def update_hdv(self):
        if not check_db_connection(self.root): return
        mahdv_input = self.entry_mahdv.get().strip()
        try: 
            mahdv = int(mahdv_input)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã HDV không hợp lệ hoặc không được chọn."); return
        tenhdv = self.entry_tenhdv.get().strip()
        sdt = self.entry_sdt.get().strip()
        email = self.entry_email.get().strip()
        ngaysinh_str = self.entry_ngaysinh.get_date().strftime('%Y-%m-%d')
        try: 
            kinhnghiem = int(self.entry_kinhnghiem.get())
            if kinhnghiem < 0:
                messagebox.showerror("Lỗi Dữ Liệu", "Kinh nghiệm không được là số âm."); return
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Kinh nghiệm phải là số nguyên."); return
        if not all([tenhdv, email]):
            messagebox.showerror("Lỗi Nhập Liệu", "Tên và Email không được để trống."); return
        sql = "UPDATE huongdanvien SET tenhdv=%s, sodienthoai=%s, email=%s, ngaysinh=%s, kinhnghiem=%s WHERE mahdv=%s"
        values = (tenhdv, sdt, email, ngaysinh_str, kinhnghiem, mahdv)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Thành Công", "Cập nhật hướng dẫn viên thành công.")
                else:
                    messagebox.showwarning("Cảnh báo", f"Không tìm thấy HDV có Mã {mahdv} để cập nhật.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.IntegrityError as err:
            messagebox.showerror("Lỗi SQL (Sửa HDV)", "Lỗi: Email đã tồn tại cho một HDV khác.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Sửa HDV)", f"Lỗi: {err}")

    def delete_hdv(self):
        if not check_db_connection(self.root): return
        mahdv_input = self.entry_mahdv.get().strip()
        try: 
            mahdv = int(mahdv_input)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã HDV không hợp lệ hoặc không được chọn."); return
        if not messagebox.askyesno("Xác Nhận Xóa", f"Bạn có chắc chắn muốn xóa HDV có Mã {mahdv} không?"): return
        sql = "DELETE FROM huongdanvien WHERE mahdv = %s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (mahdv,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Thành Công", "Xóa hướng dẫn viên thành công.")
                else:
                    messagebox.showwarning("Cảnh báo", "Không tìm thấy HDV để xóa.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Xóa HDV)", f"Lỗi: {err}")


    def select_record(self, event):
        """Hiển thị dữ liệu của dòng được chọn lên các ô nhập liệu."""
        
        # SỬA: Khôi phục dòng hover trước đó về 'normal' khi chọn dòng mới
        selected_item = self.tree_hdv.focus()
        if self.hovered_item and self.hovered_item != selected_item:
             self.tree_hdv.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None

        # SỬA: Xóa thủ công các entry thay vì gọi clear_entries()
        self.entry_mahdv.delete(0, tk.END)
        self.entry_tenhdv.delete(0, tk.END)
        self.entry_sdt.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_kinhnghiem.delete(0, tk.END); self.entry_kinhnghiem.insert(0, 0)
        
        if not selected_item: 
            self.entry_ngaysinh.set_date(date.today())
            return
        
        values = self.tree_hdv.item(selected_item, 'values')
        
        if values:
            self.entry_mahdv.insert(0, values[0])
            self.entry_tenhdv.insert(0, values[1])
            self.entry_sdt.insert(0, values[2])
            self.entry_email.insert(0, values[3])
            
            try:
                # Chuyển đổi định dạng ngày tháng: 'dd/mm/YYYY' -> date object
                date_obj = datetime.strptime(values[4], '%d/%m/%Y').date()
                self.entry_ngaysinh.set_date(date_obj)
            except:
                self.entry_ngaysinh.set_date(date.today()) 
                
            self.entry_kinhnghiem.delete(0, tk.END)
            self.entry_kinhnghiem.insert(0, values[5])