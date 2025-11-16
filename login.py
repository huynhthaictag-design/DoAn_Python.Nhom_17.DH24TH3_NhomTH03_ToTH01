import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

import main_app as admin_app 
import user_app 

# --- Biến toàn cục ---
bg_photo = None
right_image_photo = None
COLOR_BACKGROUND_MAIN = "#3da9fc" 
COLOR_HEADLINE = "#094067" 
COLOR_PARAGRAPH = "#5f6c7b" 
COLOR_BUTTON_TEXT = "#fffffe" 
COLOR_SECONDARY = "#90b4ce" 
COLOR_TERTIARY = "#ef4565" 

def login_action():
    """
    Xử lý logic khi người dùng nhấn nút Đăng Nhập.
    """
    username = username_var.get()
    password = password_var.get()

    ADMIN_USER = "admin"
    ADMIN_PASS = "123"
    
    USER_USER = "user"
    USER_PASS = "123"

    status_label.config(text="")

    if not username or not password:
        status_label.config(text="Vui lòng nhập đầy đủ thông tin.", foreground=COLOR_TERTIARY, bg=COLOR_BUTTON_TEXT)
        return

    if username == ADMIN_USER and password == ADMIN_PASS:
        status_label.config(text="Đăng nhập Admin thành công!", foreground="#2E7D32", bg=COLOR_BUTTON_TEXT) 
        root.after(500, lambda: admin_app.open_main_app(root)) 
        
    elif username == USER_USER and password == USER_PASS:
        status_label.config(text="Đăng nhập User thành công!", foreground="#2E7D32", bg=COLOR_BUTTON_TEXT) 
        
        root.after(500, lambda: user_app.mo_ung_dung_user(root))
        
    else:
        status_label.config(text="Tên đăng nhập hoặc mật khẩu không đúng.", foreground=COLOR_TERTIARY, bg=COLOR_BUTTON_TEXT)

# --- Cửa sổ chính 
root = tk.Tk()
root.title("Đăng Nhập Hệ Thống")
root.geometry("950x600")
root.resizable(False, False)

username_var = tk.StringVar()
password_var = tk.StringVar()

# --- Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                font=("Poppins", 11, "bold"),
                padding=6,
                background=COLOR_BACKGROUND_MAIN, 
                foreground=COLOR_BUTTON_TEXT) 
style.map("TButton",
          background=[('active', COLOR_HEADLINE)], 
          foreground=[('active', COLOR_BUTTON_TEXT)])

# --- Khung trái: Form đăng nhập (Giữ nguyên) ---
left_frame = tk.Frame(root, bg=COLOR_HEADLINE, width=380) 
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

title = tk.Label(left_frame, text="Đăng Nhập", font=("Poppins", 26, "bold"),
                 bg=COLOR_HEADLINE, fg=COLOR_BUTTON_TEXT) 
title.pack(pady=(40, 10))
social_frame = tk.Frame(left_frame, bg=COLOR_HEADLINE)
social_frame.pack(pady=10)
for platform in ["G", "f", "in"]:
    tk.Button(social_frame, text=platform, font=("Arial", 12, "bold"),
              width=4, bg=COLOR_BUTTON_TEXT, fg=COLOR_HEADLINE, relief="flat", 
              cursor="hand2").pack(side="left", padx=6)
tk.Label(left_frame, text="-----------------or sign in with----------------", bg=COLOR_HEADLINE,
         fg=COLOR_BUTTON_TEXT, font=("Poppins", 10)).pack(pady=(10, 10)) 
tk.Label(left_frame, text="Email", bg=COLOR_HEADLINE,
         fg=COLOR_BUTTON_TEXT, anchor="w", font=("Poppins", 10)).pack(fill="x", padx=50) 
tk.Entry(left_frame, textvariable=username_var, width=30,
         font=("Poppins", 10), relief="flat", highlightthickness=1, 
         highlightbackground=COLOR_SECONDARY, 
         bg=COLOR_BUTTON_TEXT, fg=COLOR_HEADLINE).pack(pady=5, padx=50, fill="x") 
tk.Label(left_frame, text="Password", bg=COLOR_HEADLINE,
         fg=COLOR_BUTTON_TEXT, anchor="w", font=("Poppins", 10)).pack(fill="x", padx=50) 
tk.Entry(left_frame, textvariable=password_var, show="*", width=30,
         font=("Poppins", 10), relief="flat", highlightthickness=1, 
         highlightbackground=COLOR_SECONDARY, 
         bg=COLOR_BUTTON_TEXT, fg=COLOR_HEADLINE).pack(pady=5, padx=50, fill="x") 
remember_var = tk.BooleanVar()
tk.Checkbutton(left_frame, text="Remember password.", variable=remember_var,
               bg=COLOR_HEADLINE, fg=COLOR_BUTTON_TEXT, activebackground=COLOR_HEADLINE,
               selectcolor=COLOR_BACKGROUND_MAIN, 
               font=("Poppins", 9)).pack(pady=5)
btn_frame = tk.Frame(left_frame, bg=COLOR_HEADLINE)
btn_frame.pack(pady=20)
ttk.Button(btn_frame, text="Sign In", command=login_action).pack(side="left", padx=10)
ttk.Button(btn_frame, text="Sign Up").pack(side="left", padx=10)
tk.Label(left_frame, text="Quên Mật Khẩu", fg=COLOR_SECONDARY, bg=COLOR_HEADLINE,
         cursor="hand2", font=("Poppins", 9, "underline")).pack() 
status_label = tk.Label(left_frame, text="", bg=COLOR_HEADLINE, fg=COLOR_BUTTON_TEXT,
                         font=("Poppins", 9))
status_label.pack(pady=15)

# --- Khung phải: Ảnh minh hoa
right_frame = tk.Frame(root, bg=COLOR_BUTTON_TEXT) 
right_frame.pack(side="right", fill="both", expand=True)
try:
    image = Image.open("anh2.png") 
    image = image.resize((570, 600))
    right_image_photo = ImageTk.PhotoImage(image)
    img_label = tk.Label(right_frame, image=right_image_photo, bg=COLOR_BUTTON_TEXT)
    img_label.pack(expand=True, fill="both")
except Exception as e:
    tk.Label(right_frame,
             text="[Lỗi tải ảnh 'anh2.png']",
             bg=COLOR_BUTTON_TEXT, fg=COLOR_PARAGRAPH, 
             font=("Poppins", 12)).pack(expand=True)

root.bind('<Return>', lambda event=None: login_action())
root.mainloop()