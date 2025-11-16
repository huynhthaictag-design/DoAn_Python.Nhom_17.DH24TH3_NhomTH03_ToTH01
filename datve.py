# datve_module.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import mysql.connector

# Import kết nối CSDL (Giả định file database.py và các biến conn, check_db_connection tồn tại)
from database import conn, check_db_connection 

class DatVeManager:
    """Quản lý giao diện, dữ liệu và logic CRUD cho Tab Đặt Vé."""

    def init(self, parent_tab):
        self.parent_tab = parent_tab
        self.root = parent_tab.winfo_toplevel() 
        
       
        self.hovered_item = None 

        self._create_widgets()
        self.load_data() 

    def _create_widgets(self):
        """Thiết lập tất cả widgets trên tab Đặt Vé."""
        
        # 1. Tiêu đề và Khung Tìm kiếm
        lbl_title = tk.Label(self.parent_tab, text="QUẢN LÝ ĐẶT VÉ DU LỊCH", font=("Arial", 18, "bold"), fg="#007bff")
        lbl_title.pack(pady=10)

        frame_search = tk.Frame(self.parent_tab, padx=10)
        frame_search.pack(fill="x", pady=5)

        tk.Label(frame_search, text="Tìm Mã Vé:", font=("Arial", 10)).pack(side="left", padx=(10, 5))
        self.entry_search_mave = tk.Entry(frame_search, width=15)
        self.entry_search_mave.pack(side="left")

        tk.Button(frame_search, text="Tìm", command=self.search_by_mave, bg="#4da6ff", fg="white", font=("Arial", 9)).pack(side="left", padx=(6, 0))
        tk.Button(frame_search, text="Xem Tất Cả", command=self.load_data, bg="#99CCFF", fg="black", font=("Arial", 9)).pack(side="left", padx=(15, 0))


        # 2. Khung nhập thông tin (Entries)
        frame_info = tk.LabelFrame(self.parent_tab, text="Thông tin đặt vé", font=("Arial", 13, "bold"), bg="#e6f7ff", fg="#0056b3", bd=2)
        frame_info.pack(pady=5, padx=10, fill="x")
        frame_info.columnconfigure(1, weight=1); frame_info.columnconfigure(3, weight=1) 

        tk.Label(frame_info, text="Mã Vé:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=7, sticky="w")
        self.entry_mave = tk.Entry(frame_info, width=25); 
        self.entry_mave.grid(row=0, column=1, padx=10, pady=7, sticky="w")
        
        tk.Label(frame_info, text="Mã Tuyến:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=7, sticky="w")
        self.entry_matuyen = tk.Entry(frame_info, width=25); 
        self.entry_matuyen.grid(row=1, column=1, padx=10, pady=7, sticky="w")
        
        tk.Label(frame_info, text="Ngày Đặt Vé:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=7, sticky="w")
        self.entry_ngaydatve = DateEntry(frame_info, width=22, date_pattern='dd/mm/yyyy'); 
        self.entry_ngaydatve.grid(row=2, column=1, padx=10, pady=7, sticky="w")

        tk.Label(frame_info, text="Số Lượng Vé:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=7, sticky="w")
        self.spin_soluongve = tk.Spinbox(frame_info, from_=1, to=100, width=23); 
        self.spin_soluongve.grid(row=0, column=3, padx=10, pady=7, sticky="w")
        
        tk.Label(frame_info, text="Tổng Tiền:", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=10, pady=7, sticky="w")
        self.entry_tongtien = tk.Entry(frame_info, width=25); 
        self.entry_tongtien.grid(row=1, column=3, padx=10, pady=7, sticky="w")

        
        # 3. Khung nút chức năng
        frame_buttons = tk.Frame(self.parent_tab, pady=10); frame_buttons.pack(pady=10)
        tk.Button(frame_buttons, text="Thêm Vé", width=12, bg="#28a745", fg="white", command=self.add_datve).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Sửa Vé", width=12, bg="#ffc107", fg="black", command=self.update_datve).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Xóa Vé", width=12, bg="#dc3545", fg="white", command=self.delete_datve).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Làm Mới", width=12, command=self.clear_entries).pack(side=tk.LEFT, padx=10)

        # 4. Treeview 
        tree_frame = tk.Frame(self.parent_tab, padx=10); tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Logic Hover
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass 
        style.map("Treeview", 
                  background=[('selected', '#007bff')],
                  foreground=[('selected', 'white')])

        columns = ('mave', 'matuyen', 'ngaydatve', 'soluongve', 'tongtien')
        self.tree_datve = ttk.Treeview(tree_frame, columns=columns, show='headings')

        self.tree_datve.tag_configure('normal', background='white', foreground='black')
        self.tree_datve.tag_configure('hover', background='#e6f2ff', foreground='black')

        self.tree_datve.heading('mave', text='Mã Vé'); self.tree_datve.column('mave', width=60, anchor='center')
        self.tree_datve.heading('matuyen', text='Mã Tuyến'); self.tree_datve.column('matuyen', width=80, anchor='center')
        self.tree_datve.heading('ngaydatve', text='Ngày Đặt'); self.tree_datve.column('ngaydatve', width=100, anchor='center')
        self.tree_datve.heading('soluongve', text='Số Lượng'); self.tree_datve.column('soluongve', width=80, anchor='center')
        self.tree_datve.heading('tongtien', text='Tổng Tiền'); self.tree_datve.column('tongtien', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_datve.yview)
        self.tree_datve.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_datve.pack(fill="both", expand=True)
        
        self.tree_datve.bind('<<TreeviewSelect>>', self.select_record)
        self.tree_datve.bind('<Motion>', self._on_tree_hover)
        self.tree_datve.bind('<Leave>', self._on_tree_leave)

    # --- Logic Hover ---

    def _on_tree_hover(self, event):
        item = self.tree_datve.identify_row(event.y)
        selected_item = self.tree_datve.selection()[0] if self.tree_datve.selection() else None
        
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_datve.item(self.hovered_item, tags=('normal',))
            
        if item and item != selected_item:
            self.tree_datve.item(item, tags=('hover',))
            self.hovered_item = item
        else:
            self.hovered_item = None 

    def _on_tree_leave(self, event):
        selected_item = self.tree_datve.selection()[0] if self.tree_datve.selection() else None
        
        if self.hovered_item and self.hovered_item != selected_item:
            self.tree_datve.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None
            
    # --- CRUD Functions ---
    
    def clear_entries(self):
        """Làm sạch tất cả các trường nhập liệu."""
        self.entry_mave.delete(0, tk.END)
        self.entry_matuyen.delete(0, tk.END)
        self.entry_ngaydatve.set_date(date.today())
        self.spin_soluongve.delete(0, tk.END); self.spin_soluongve.insert(0, 1)
        self.entry_tongtien.delete(0, tk.END)
        
        self.tree_datve.selection_remove(self.tree_datve.selection()) 
        self.entry_search_mave.delete(0, tk.END)
        self._on_tree_leave(None) # Reset hover

    def load_data(self):
        """Tải dữ liệu đặt vé từ CSDL."""
        if not check_db_connection(self.root): return
        for item in self.tree_datve.get_children(): self.tree_datve.delete(item)

        try:
            with conn.cursor() as cursor:
                # Định dạng NgayDatVe sang dd/mm/YYYY để hiển thị
                sql = "SELECT MaVe, MaTuyen, DATE_FORMAT(NgayDatVe, '%d/%m/%Y'), SoLuongVe, TongTien FROM DatVe"
                cursor.execute(sql)
                for record in cursor.fetchall():
                    self.tree_datve.insert('', tk.END, values=record, tags=('normal',))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu Đặt Vé", f"Lỗi: {err}")
            
    def search_by_mave(self):
        """Tìm kiếm vé theo Mã Vé."""
        if not check_db_connection(self.root): return
        timkiem = self.entry_search_mave.get().strip()
        if not timkiem: return self.load_data()
        for item in self.tree_datve.get_children(): self.tree_datve.delete(item)

        try:
            mave_search = int(timkiem)
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Mã Vé phải là số nguyên."); return self.load_data()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT MaVe, MaTuyen, DATE_FORMAT(NgayDatVe, '%d/%m/%Y'), SoLuongVe, TongTien FROM DatVe WHERE MaVe = %s"
                cursor.execute(sql, (mave_search,))
                records = cursor.fetchall()
                if not records:
                    messagebox.showwarning("Không Tìm Thấy", f"Không tìm thấy Vé có Mã: {mave_search}"); self.load_data(); return
                for record in records:
                    self.tree_datve.insert('', tk.END, values=record, tags=('normal',))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Dữ Liệu", f"Lỗi: {err}")

    def _validate_input(self):
        """Kiểm tra dữ liệu đầu vào và trả về tuple data."""
        mave_str = self.entry_mave.get().strip()
        matuyen_str = self.entry_matuyen.get().strip()
        ngaydat_str = self.entry_ngaydatve.get_date().strftime('%Y-%m-%d')
        soluong_str = self.spin_soluongve.get().strip()
        tongtien_str = self.entry_tongtien.get().strip()

        if not all([mave_str, matuyen_str, soluong_str, tongtien_str]):
            messagebox.showerror("Lỗi Nhập Liệu", "Mã Vé, Mã Tuyến, Số Lượng và Tổng Tiền không được để trống."); return None
        
        try:
            mave = int(mave_str)
            matuyen = int(matuyen_str)
            soluong = int(soluong_str)
            tongtien = float(tongtien_str)
            
            if soluong <= 0:
                messagebox.showerror("Lỗi Dữ Liệu", "Số lượng vé phải lớn hơn 0."); return None
                
        except ValueError:
            messagebox.showerror("Lỗi Dữ Liệu", "Mã Vé, Mã Tuyến, Số Lượng, Tổng Tiền phải là số."); return None

        return (mave, matuyen, ngaydat_str, soluong, tongtien)

    def add_datve(self):
        """Thêm một vé mới."""
        if not check_db_connection(self.root): return
        
        data = self._validate_input()
        if not data: return
        
        sql = "INSERT INTO DatVe (MaVe, MaTuyen, NgayDatVe, SoLuongVe, TongTien) VALUES (%s, %s, %s, %s, %s)"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, data)
                conn.commit()
                messagebox.showinfo("Thành Công", "Thêm vé thành công.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.IntegrityError as err:
            if err.errno == 1062: # Lỗi trùng lặp Khóa chính
                messagebox.showerror("Lỗi SQL (Thêm Vé)", f"Lỗi: Mã Vé '{data[0]}' đã tồn tại.")
            elif err.errno == 1452: # Lỗi Khóa ngoại
                messagebox.showerror("Lỗi SQL (Thêm Vé)", f"Lỗi: Mã Tuyến '{data[1]}' không tồn tại trong bảng Tuyến Du Lịch.")
            else:
                 messagebox.showerror("Lỗi SQL (Thêm Vé)", f"Lỗi: {err}")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Thêm Vé)", f"Lỗi: {err}")

    def update_datve(self):
        """Cập nhật thông tin vé đã chọn."""
        if not check_db_connection(self.root): return
        
        # Lấy MaVe từ entry (không thể thay đổi)
        mave_str = self.entry_mave.get().strip()
        if not mave_str:
             messagebox.showerror("Lỗi", "Vui lòng chọn vé cần sửa."); return
             
        data = self._validate_input()
        if not data: return
        
        # data[0] là MaVe, nhưng chúng ta cần nó ở cuối cho lệnh UPDATE
        # (MaTuyen, NgayDatVe, SoLuongVe, TongTien, MaVe)
        update_data = data[1:] + (data[0],) 

        sql = "UPDATE DatVe SET MaTuyen=%s, NgayDatVe=%s, SoLuongVe=%s, TongTien=%s WHERE MaVe=%s"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, update_data)
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Thành Công", "Cập nhật vé thành công.")
                else:
                    messagebox.showwarning("Cảnh báo", f"Không tìm thấy Vé có Mã {data[0]} để cập nhật.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.IntegrityError as err:
             if err.errno == 1452: # Lỗi Khóa ngoại
                messagebox.showerror("Lỗi SQL (Sửa Vé)", f"Lỗi: Mã Tuyến '{data[1]}' không tồn tại trong bảng Tuyến Du Lịch.")
             else:
                 messagebox.showerror("Lỗi SQL (Sửa Vé)", f"Lỗi: {err}")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Sửa Vé)", f"Lỗi: {err}")

    def delete_datve(self):
        """Xóa vé đã chọn."""
        if not check_db_connection(self.root): return
        
        mave_input = self.entry_mave.get().strip()
        try: 
            mave = int(mave_input)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã Vé không hợp lệ hoặc không được chọn."); return

        if not messagebox.askyesno("Xác Nhận Xóa", f"Bạn có chắc chắn muốn xóa Vé có Mã {mave} không?"): return
        
        sql = "DELETE FROM DatVe WHERE MaVe = %s"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (mave,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Thành Công", "Xóa vé thành công.")
                else:
                    messagebox.showwarning("Cảnh báo", "Không tìm thấy vé để xóa.")
                self.clear_entries()
                self.load_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi SQL (Xóa Vé)", f"Lỗi: {err}")

    def select_record(self, event):
        """Hiển thị dữ liệu của dòng được chọn lên các ô nhập liệu."""
        
        selected_item = self.tree_datve.focus()
        if self.hovered_item and self.hovered_item != selected_item:
             self.tree_datve.item(self.hovered_item, tags=('normal',))
        self.hovered_item = None

        # Xóa thủ công
        self.entry_mave.delete(0, tk.END)
        self.entry_matuyen.delete(0, tk.END)
        self.spin_soluongve.delete(0, tk.END)
        self.entry_tongtien.delete(0, tk.END)
        
        if not selected_item: 
            self.entry_ngaydatve.set_date(date.today())
            self.spin_soluongve.insert(0, 1)
            return
        
        values = self.tree_datve.item(selected_item, 'values')
        
        if values:
            self.entry_mave.insert(0, values[0])
            self.entry_matuyen.insert(0, values[1])
            
            # Xử lý ngày tháng (định dạng dd/mm/YYYY)
            try:
                date_obj = datetime.strptime(values[2], '%d/%m/%Y').date()
                self.entry_ngaydatve.set_date(date_obj)
            except:
                self.entry_ngaydatve.set_date(date.today()) 
                
            self.spin_soluongve.insert(0, values[3])
            self.entry_tongtien.insert(0, values[4])