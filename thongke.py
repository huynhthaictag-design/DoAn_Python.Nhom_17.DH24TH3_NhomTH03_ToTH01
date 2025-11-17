# thongke.py

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from database import conn, kiem_tra_ket_noi
class QuanLyThongKe:
    """Quản lý giao diện và logic cho Tab Thống Kê."""

    # --- HÀM KHỞI TẠO 
    def __init__(self, parent_tab):
        self.parent_tab = parent_tab
        self.root = parent_tab.winfo_toplevel()
        
        self.stats_widgets = {} # Nơi lưu trữ các Label
        
      
        self.taoGiaoDien()
        self.taiThongKe()

    def taoGiaoDien(self):
        """Thiết lập các widget hiển thị."""
        
        main_frame = tk.Frame(self.parent_tab, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        tk.Label(main_frame, text="BÁO CÁO & THỐNG KÊ", font=("Arial", 18, "bold"), fg="#005b96").pack(pady=10)
        
        tk.Button(main_frame, text="Làm mới Dữ liệu", command=self.taiThongKe, bg="#007bff", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
        
        stats_frame = tk.Frame(main_frame, relief=tk.GROOVE, borderwidth=1, padx=15, pady=15)
        stats_frame.pack(fill="x", pady=10)
        stats_frame.columnconfigure(1, weight=1)

        stat_items = [
            ("tong_doanh_thu", "Tổng Doanh Thu:"),
            ("tong_ve_ban", "Tổng Số Vé Đã Bán:"),
            ("tong_luot_dat", "Tổng Số Lượt Đặt:"),
            ("tong_so_tour", "Tổng Số Tour Hiện Có:"),
            ("tong_so_hdv", "Tổng Số Hướng Dẫn Viên:"),
            ("tong_so_diadiem", "Tổng Số Địa Điểm:"),
            ("tour_pho_bien", "Tour Phổ Biến Nhất:")
        ]

        for i, (key, text) in enumerate(stat_items):
            tk.Label(stats_frame, text=text, font=("Arial", 11, "bold")).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            lbl_data = tk.Label(stats_frame, text="Đang tải...", font=("Arial", 11), fg="#0056b3")
            lbl_data.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            self.stats_widgets[key] = lbl_data

    def taiThongKe(self):
        """Tải dữ liệu thống kê từ CSDL và cập nhật giao diện."""
        if not kiem_tra_ket_noi(self.root): return
        
        try:
            with conn.cursor() as cursor:
                
                # 1. Tổng doanh thu
                cursor.execute("SELECT SUM(TongTien) FROM DatVe")
                doanh_thu = cursor.fetchone()[0] or 0
                self.stats_widgets["tong_doanh_thu"].config(text=f"{doanh_thu:,.0f} VNĐ")

                # 2. Tổng vé và lượt đặt
                cursor.execute("SELECT COUNT(*), SUM(SoLuongVe) FROM DatVe")
                result = cursor.fetchone()
                luot_dat = result[0] or 0
                so_ve = result[1] or 0
                self.stats_widgets["tong_luot_dat"].config(text=f"{luot_dat} lượt")
                self.stats_widgets["tong_ve_ban"].config(text=f"{so_ve} vé")

                # 3. Tổng Tour, HDV, Địa điểm
                cursor.execute("SELECT COUNT(*) FROM tuyendulich")
                so_tour = cursor.fetchone()[0] or 0
                self.stats_widgets["tong_so_tour"].config(text=f"{so_tour} tours")
                
                cursor.execute("SELECT COUNT(*) FROM huongdanvien")
                so_hdv = cursor.fetchone()[0] or 0
                self.stats_widgets["tong_so_hdv"].config(text=f"{so_hdv} HDV")

                cursor.execute("SELECT COUNT(*) FROM DiaDiem")
                so_diadiem = cursor.fetchone()[0] or 0
                self.stats_widgets["tong_so_diadiem"].config(text=f"{so_diadiem} địa điểm")

                # 4. Tour phổ biến nhất
                sql_top_tour = """
                SELECT T.tentuyen, COUNT(DV.MaTuyen) AS SoLanDat 
                FROM DatVe AS DV 
                JOIN tuyendulich AS T ON DV.MaTuyen = T.maso 
                GROUP BY T.tentuyen 
                ORDER BY SoLanDat DESC 
                LIMIT 1
                """
                cursor.execute(sql_top_tour)
                top_tour_result = cursor.fetchone()
                if top_tour_result:
                    top_tour_text = f"{top_tour_result[0]} (với {top_tour_result[1]} lượt đặt)"
                else:
                    top_tour_text = "Chưa có dữ liệu"
                self.stats_widgets["tour_pho_bien"].config(text=top_tour_text)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi Tải Thống Kê", f"Lỗi: {err}")