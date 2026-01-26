import tkinter as tk
from PIL import Image, ImageTk
import time


class FixedWindowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("流暢播放器 - 照片集優化版")

        # --- 初始視窗尺寸 ---
        self.win_width = 800
        self.win_height = 600
        self.update_window_geometry()
        self.root.resizable(False, False)
        self.root.configure(bg='black')

        # --- 檔案路徑設定 ---
        self.eye_gif_path = "eyes_look_and_blink.gif"
        self.video_gif_path = "tom_and_jerry.gif.gif"

        # 貓咪照片清單
        self.photo_list_cat = ["貓鼠1.jfif", "貓鼠2.jfif", "貓鼠3.jfif", "貓鼠4.jfif"]

        # 小狗照片清單 (已更新為您上傳的 .jfif 檔案)
        self.photo_list_dog = ["線條小狗1.jfif", "線條小狗2.jfif", "線條小狗3.jfif", "線條小狗4.jfif"]

        self.current_photo_list = []
        self.current_photo_idx = 0

        # 狀態控制
        self.last_activity_time = time.time()
        self.is_in_menu = False
        self.idle_limit = tk.IntVar(value=5)
        self.play_speed = tk.DoubleVar(value=1.0)
        self.eye_speed = tk.DoubleVar(value=1.0)

        # 快取
        self.current_video_obj = None
        self.photo_cache = None

        self.check_idle_time()
        self.show_animation_screen()

    def update_window_geometry(self):
        self.root.geometry(f"{self.win_width}x{self.win_height}")

    def get_scale_factor(self):
        raw_sf = self.win_width / 800
        return 0.85 if raw_sf < 1.0 else raw_sf

    def clear_screen(self):
        self.root.unbind("<Motion>")
        self.current_video_obj = None
        self.photo_cache = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def reset_timer(self, event=None):
        self.last_activity_time = time.time()

    def check_idle_time(self):
        if self.is_in_menu:
            elapsed_time = time.time() - self.last_activity_time
            if elapsed_time > self.idle_limit.get():
                self.is_in_menu = False
                self.show_animation_screen()
        self.root.after(500, self.check_idle_time)

    # --- 畫面 1：待機動畫 ---
    def show_animation_screen(self):
        self.is_in_menu = False
        self.clear_screen()
        self.display_label = tk.Label(self.root, bg='black', bd=0)
        self.display_label.pack(expand=True, fill="both")
        self.display_label.bind("<Button-1>", lambda e: self.show_main_menu())

        try:
            self.eye_gif = Image.open(self.eye_gif_path)
            self.eye_frame_idx = 0
            self.animate_eye()
        except:
            tk.Label(self.root, text="動畫加載失敗", fg="white", bg="black").pack(expand=True)

    def animate_eye(self):
        if not self.is_in_menu and hasattr(self, 'display_label') and self.display_label.winfo_exists():
            try:
                self.eye_gif.seek(self.eye_frame_idx)
                frame = self.eye_gif.resize((self.win_width, self.win_height), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(frame)
                self.display_label.config(image=self.photo)
                self.eye_frame_idx = (self.eye_frame_idx + 1) % self.eye_gif.n_frames
                delay = int(100 / self.eye_speed.get())
                self.root.after(max(10, delay), self.animate_eye)
            except:
                pass

    # --- 畫面 2：主選單 ---
    def show_main_menu(self):
        self.clear_screen()
        self.is_in_menu = True
        self.reset_timer()
        self.root.bind("<Motion>", self.reset_timer)
        self.root.configure(bg='#f0f0f0')

        sf = self.get_scale_factor()
        btn_params = {"font": ("微軟正黑體", int(16 * sf), "bold"), "width": 22, "height": 1, "cursor": "hand2"}

        container = tk.Frame(self.root, bg='#f0f0f0')
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="功能選單", font=("微軟正黑體", int(24 * sf), "bold"), bg='#f0f0f0').pack(pady=10)

        tk.Button(container, text="▶ 播放影片動畫", command=self.show_video_screen, **btn_params).pack(pady=5)
        tk.Button(container, text="🖼 播放照片集 (貓)", command=lambda: self.start_photo_album(self.photo_list_cat),
                  **btn_params).pack(pady=5)
        tk.Button(container, text="🐶 播放照片集 (狗)", command=lambda: self.start_photo_album(self.photo_list_dog),
                  **btn_params).pack(pady=5)
        tk.Button(container, text="⚙ 設定功能", command=self.show_settings_menu, **btn_params).pack(pady=5)

    # --- 照片播放邏輯 ---
    def start_photo_album(self, list_to_play):
        self.current_photo_list = list_to_play
        self.current_photo_idx = 0
        self.show_photo_album_screen()

    def show_photo_album_screen(self):
        self.is_in_menu = True
        self.clear_screen()
        self.root.configure(bg='black')

        self.album_label = tk.Label(self.root, bg='black', bd=0)
        self.album_label.pack(expand=True, fill="both")
        self.album_label.bind("<Button-1>", self.next_photo)

        sf = self.get_scale_factor()
        tk.Button(self.root, text="返回", command=self.show_main_menu,
                  bg="#444", fg="white", font=("微軟正黑體", int(14 * sf), "bold")).place(x=10, y=10)

        self.update_album_display()

    def next_photo(self, event=None):
        self.reset_timer()
        self.current_photo_idx = (self.current_photo_idx + 1) % len(self.current_photo_list)
        self.update_album_display()

    def update_album_display(self):
        try:
            img_path = self.current_photo_list[self.current_photo_idx]
            img = Image.open(img_path)
            # 關鍵：強制縮放至目前視窗大小 (win_width x win_height)
            img_resized = img.resize((self.win_width, self.win_height), Image.Resampling.LANCZOS)
            self.photo_cache = ImageTk.PhotoImage(img_resized)
            self.album_label.config(image=self.photo_cache)
        except Exception as e:
            print(f"載入失敗: {img_path}, 錯誤: {e}")

    # --- 其他功能 (影片/設定) ---
    def show_video_screen(self):
        self.is_in_menu = False
        self.clear_screen()
        try:
            self.current_video_obj = Image.open(self.video_gif_path)
            self.video_total_frames = self.current_video_obj.n_frames
            self.video_frame_idx = 0
            self.video_label = tk.Label(self.root, bg='black', bd=0)
            self.video_label.pack(expand=True, fill="both")
            self.video_label.bind("<Button-1>", lambda e: self.show_main_menu())
            self.animate_video()
        except:
            pass

    def animate_video(self):
        if not self.is_in_menu and self.current_video_obj:
            try:
                self.current_video_obj.seek(self.video_frame_idx)
                frame = self.current_video_obj.resize((self.win_width, self.win_height), Image.Resampling.NEAREST)
                self.photo_cache = ImageTk.PhotoImage(frame)
                self.video_label.config(image=self.photo_cache)
                self.video_frame_idx = (self.video_frame_idx + 1) % self.video_total_frames
                delay = int(33 / self.play_speed.get())
                self.root.after(max(5, delay), self.animate_video)
            except:
                pass

    def show_settings_menu(self):
        self.clear_screen()
        self.is_in_menu = True
        self.root.configure(bg='#e8e8e8')
        sf = self.get_scale_factor()
        container = tk.Frame(self.root, bg='#e8e8e8')
        container.place(relx=0.5, rely=0.5, anchor="center")
        btn_style = {"font": ("微軟正黑體", int(14 * sf), "bold"), "width": 20}

        tk.Label(container, text="設定選單", font=("微軟正黑體", int(20 * sf), "bold"), bg='#e8e8e8').pack(pady=10)
        tk.Button(container, text="📐 視窗大小", command=self.open_resize_dialog, **btn_style).pack(pady=3)
        tk.Button(container, text="⏲ 閒置時間", command=self.open_idle_time_dialog, **btn_style).pack(pady=3)
        tk.Button(container, text="⏩ 播放速度", command=self.open_speed_dialog, **btn_style).pack(pady=3)
        tk.Button(container, text="👁 待機動畫速度", command=self.open_eye_speed_dialog, **btn_style).pack(pady=3)
        tk.Button(container, text="⬅ 返回主頁", command=self.show_main_menu, bg="#bbb", **btn_style).pack(pady=10)

    # --- 對話框系列 ---
    def open_resize_dialog(self):
        win = tk.Toplevel(self.root);
        win.grab_set();
        win.geometry("300x300")
        tk.Label(win, text="選擇解析度", font=("微軟正黑體", 12, "bold")).pack(pady=10)
        for text, w, h in [("3.5吋 (480x320)", 480, 320), ("800x600 (預設)", 800, 600), ("1024x768", 1024, 768)]:
            tk.Button(win, text=text, width=20,
                      command=lambda _w=w, _h=h: [setattr(self, 'win_width', _w), setattr(self, 'win_height', _h),
                                                  self.update_window_geometry(), win.destroy(),
                                                  self.show_settings_menu()]).pack(pady=5)

    def open_speed_dialog(self):
        win = tk.Toplevel(self.root);
        win.grab_set();
        win.geometry("200x250")
        for v in [0.5, 1.0, 1.5, 2.0]:
            tk.Radiobutton(win, text=f"{v}x 速度", variable=self.play_speed, value=v).pack(pady=5)
        tk.Button(win, text="確定", command=win.destroy).pack(pady=10)

    def open_idle_time_dialog(self):
        win = tk.Toplevel(self.root);
        win.grab_set();
        win.geometry("200x250")
        for t in [5, 10, 30, 60]:
            tk.Radiobutton(win, text=f"{t} 秒", variable=self.idle_limit, value=t).pack(pady=5)
        tk.Button(win, text="確定", command=win.destroy).pack(pady=10)

    def open_eye_speed_dialog(self):
        win = tk.Toplevel(self.root);
        win.grab_set();
        win.geometry("200x250")
        for v in [0.5, 1.0, 1.5]:
            tk.Radiobutton(win, text=f"{v}x 速度", variable=self.eye_speed, value=v).pack(pady=5)
        tk.Button(win, text="確定", command=win.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FixedWindowApp(root)
    root.mainloop()