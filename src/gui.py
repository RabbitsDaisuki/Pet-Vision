import tkinter as tk  # 匯入標準 GUI 庫
from PIL import Image, ImageTk  # 匯入影像處理庫（處理 GIF 與照片縮放）
import time  # 匯入時間庫（計算閒置時間）


class FixedWindowApp:
    def __init__(self, root):
        self.root = root  # 儲存主視窗物件
        self.root.title("寵物機器人")  # 設定視窗標題

        # --- 初始視窗尺寸設定 ---
        self.win_width = 800  # 預設寬度
        self.win_height = 600  # 預設高度
        self.update_window_geometry()  # 執行視窗尺寸更新
        self.root.resizable(False, False)  # 禁止使用者手動調整視窗大小
        self.root.configure(bg='black')  # 設定視窗背景顏色為黑色

        # --- 檔案路徑與資源設定 ---
        self.eye_gif_path = "eyes_look_and_blink.gif"  # 待機動畫路徑
        self.video_gif_path = "tom_and_jerry.gif.gif"  # 影片動畫路徑

        # 貓咪照片清單檔案路徑
        self.photo_list_cat = ["貓鼠1.jfif", "貓鼠2.jfif", "貓鼠3.jfif", "貓鼠4.jfif"]
        # 小狗照片清單檔案路徑
        self.photo_list_dog = ["線條小狗1.jfif", "線條小狗2.jfif", "線條小狗3.jfif", "線條小狗4.jfif"]

        self.current_photo_list = []  # 當前正在播放的照片清單（動態指定）
        self.current_photo_idx = 0  # 目前顯示的照片索引編號

        # --- 狀態與變數控制 ---
        self.last_activity_time = time.time()  # 紀錄最後一次操作的時間點
        self.is_in_menu = False  # 標記目前是否處於選單狀態（用於判斷閒置跳轉）
        self.idle_limit = tk.IntVar(value=5)  # 閒置跳轉秒數變數（預設 5 秒）
        self.play_speed = tk.DoubleVar(value=1.0)  # 影片播放速度倍率
        self.eye_speed = tk.DoubleVar(value=1.0)  # 待機眼睛動畫速度倍率

        # --- 快取變數 ---
        self.current_video_obj = None  # 儲存開啟的 GIF 物件
        self.photo_cache = None  # 儲存當前顯示的圖片物件（防止垃圾回收機制刪除圖片）

        # 啟動後台循環監測與初始畫面
        self.check_idle_time()  # 開始監控閒置時間
        self.show_animation_screen()  # 顯示初始待機畫面

    def update_window_geometry(self):
        """根據設定的寬高更新視窗實際尺寸"""
        self.root.geometry(f"{self.win_width}x{self.win_height}")

    def get_scale_factor(self):
        """計算縮放比例，若解析度太小則稍微縮小字體以防溢出"""
        raw_sf = self.win_width / 800
        return 0.85 if raw_sf < 1.0 else raw_sf

    def clear_screen(self):
        """切換畫面時，清除視窗內所有舊的元件與綁定事件"""
        self.root.unbind("<Motion>")  # 解除滑鼠移動監測
        self.current_video_obj = None  # 釋放影片資源
        self.photo_cache = None  # 釋放照片資源
        for widget in self.root.winfo_children():
            widget.destroy()  # 刪除視窗內所有元件

    def reset_timer(self, event=None):
        """當使用者有動作時，重設最後活動時間點"""
        self.last_activity_time = time.time()

    def check_idle_time(self):
        """後台循環函數：每 0.5 秒檢查一次是否因閒置過久而需跳回待機畫面"""
        if self.is_in_menu:  # 只有在選單或照片集模式下才偵測閒置
            elapsed_time = time.time() - self.last_activity_time
            if elapsed_time > self.idle_limit.get():  # 若超過設定秒數
                self.is_in_menu = False  # 關閉選單狀態標記
                self.show_animation_screen()  # 切換回待機畫面
        self.root.after(500, self.check_idle_time)  # 0.5秒後再次執行自我檢查

    # --- 畫面 1：待機眼睛動畫 ---
    def show_animation_screen(self):
        self.is_in_menu = False  # 待機畫面中不偵測閒置
        self.clear_screen()  # 清理螢幕
        self.display_label = tk.Label(self.root, bg='black', bd=0)  # 建立顯示容器
        self.display_label.pack(expand=True, fill="both")  # 填滿視窗
        self.display_label.bind("<Button-1>", lambda e: self.show_main_menu())  # 點擊左鍵進入選單

        try:
            self.eye_gif = Image.open(self.eye_gif_path)  # 開啟動畫檔案
            self.eye_frame_idx = 0  # 從第 0 幀開始播放
            self.animate_eye()  # 啟動動畫循環
        except:
            tk.Label(self.root, text="動畫加載失敗", fg="white", bg="black").pack(expand=True)

    def animate_eye(self):
        """循環播放眼睛 GIF 幀"""
        if not self.is_in_menu and hasattr(self, 'display_label') and self.display_label.winfo_exists():
            try:
                self.eye_gif.seek(self.eye_frame_idx)  # 移動到特定幀
                # 縮放該幀影像至視窗大小
                frame = self.eye_gif.resize((self.win_width, self.win_height), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(frame)  # 轉為 Tkinter 可讀格式
                self.display_label.config(image=self.photo)  # 更新標籤上的圖片
                self.eye_frame_idx = (self.eye_frame_idx + 1) % self.eye_gif.n_frames  # 計算下一幀編號
                delay = int(100 / self.eye_speed.get())  # 根據速度設定計算延遲
                self.root.after(max(10, delay), self.animate_eye)  # 預約下次更新
            except:
                pass

    # --- 畫面 2：主選單 ---
    def show_main_menu(self):
        self.clear_screen()
        self.is_in_menu = True  # 開啟閒置偵測
        self.reset_timer()  # 重設計時器
        self.root.bind("<Motion>", self.reset_timer)  # 滑鼠移動即視為活動
        self.root.configure(bg='#f0f0f0')  # 選單背景色

        sf = self.get_scale_factor()  # 取得縮放比例
        # 設定按鈕樣式
        btn_params = {"font": ("微軟正黑體", int(16 * sf), "bold"), "width": 22, "height": 1, "cursor": "hand2"}

        container = tk.Frame(self.root, bg='#f0f0f0')  # 建立置中容器
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="功能選單", font=("微軟正黑體", int(24 * sf), "bold"), bg='#f0f0f0').pack(pady=10)

        # 四大功能按鈕
        tk.Button(container, text="▶ 播放影片動畫", command=self.show_video_screen, **btn_params).pack(pady=5)
        tk.Button(container, text="🖼 播放照片集 (貓)", command=lambda: self.start_photo_album(self.photo_list_cat),
                  **btn_params).pack(pady=5)
        tk.Button(container, text="🐶 播放照片集 (狗)", command=lambda: self.start_photo_album(self.photo_list_dog),
                  **btn_params).pack(pady=5)
        tk.Button(container, text="⚙ 設定功能", command=self.show_settings_menu, **btn_params).pack(pady=5)

    # --- 照片播放邏輯 ---
    def start_photo_album(self, list_to_play):
        """指定要播放的照片集清單，並重置索引"""
        self.current_photo_list = list_to_play
        self.current_photo_idx = 0
        self.show_photo_album_screen()

    def show_photo_album_screen(self):
        """顯示照片播放畫面"""
        self.is_in_menu = True
        self.clear_screen()
        self.root.configure(bg='black')

        self.album_label = tk.Label(self.root, bg='black', bd=0)  # 照片容器
        self.album_label.pack(expand=True, fill="both")
        self.album_label.bind("<Button-1>", self.next_photo)  # 點擊照片切換下一張

        sf = self.get_scale_factor()
        # 返回主選單按鈕
        tk.Button(self.root, text="返回", command=self.show_main_menu,
                  bg="#444", fg="white", font=("微軟正黑體", int(14 * sf), "bold")).place(x=10, y=10)

        self.update_album_display()  # 顯示首張照片

    def next_photo(self, event=None):
        """切換到下一張照片並重時計時器"""
        self.reset_timer()
        self.current_photo_idx = (self.current_photo_idx + 1) % len(self.current_photo_list)
        self.update_album_display()

    def update_album_display(self):
        """更新當前照片，並強制縮放以填滿視窗"""
        try:
            img_path = self.current_photo_list[self.current_photo_idx]
            img = Image.open(img_path)
            # 核心邏輯：強制將圖片調整為目前視窗寬度與高度，使用 LANCZOS 確保縮放品質
            img_resized = img.resize((self.win_width, self.win_height), Image.Resampling.LANCZOS)
            self.photo_cache = ImageTk.PhotoImage(img_resized)
            self.album_label.config(image=self.photo_cache)
        except Exception as e:
            print(f"載入失敗: {img_path}, 錯誤: {e}")

    # --- 其他功能 (影片/設定) ---
    def show_video_screen(self):
        """啟動影片（GIF）播放畫面"""
        self.is_in_menu = False  # 影片播放時暫停閒置跳轉
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
        """循環播放影片 GIF 的每一幀"""
        if not self.is_in_menu and self.current_video_obj:
            try:
                self.current_video_obj.seek(self.video_frame_idx)
                # 影片縮放使用 NEAREST (效能優先)
                frame = self.current_video_obj.resize((self.win_width, self.win_height), Image.Resampling.NEAREST)
                self.photo_cache = ImageTk.PhotoImage(frame)
                self.video_label.config(image=self.photo_cache)
                self.video_frame_idx = (self.video_frame_idx + 1) % self.video_total_frames
                delay = int(33 / self.play_speed.get())  # 預設約 30 FPS
                self.root.after(max(5, delay), self.animate_video)
            except:
                pass

    def show_settings_menu(self):
        """顯示設定選單畫面"""
        self.clear_screen()
        self.is_in_menu = True
        self.root.configure(bg='#e8e8e8')
        sf = self.get_scale_factor()
        container = tk.Frame(self.root, bg='#e8e8e8')
        container.place(relx=0.5, rely=0.5, anchor="center")
        btn_style = {"font": ("微軟正黑體", int(14 * sf), "bold"), "width": 20}

        tk.Label(container, text="設定選單", font=("微軟正黑體", int(20 * sf), "bold"), bg='#e8e8e8').pack(pady=10)
        # 設定功能按鈕
        tk.Button(container, text="📐 視窗大小", command=self.open_resize_dialog, **btn_style).pack(pady=3)
        tk.Button(container, text="⏲ 閒置時間", command=self.open_idle_time_dialog, **btn_style).pack(pady=3)
        tk.Button(container, text="⏩ 播放速度", command=self.open_speed_dialog, **btn_style).pack(pady=3)
        tk.Button(container, text="👁 待機動畫速度", command=self.open_eye_speed_dialog, **btn_style).pack(pady=3)
        tk.Button(container, text="⬅ 返回主頁", command=self.show_main_menu, bg="#bbb", **btn_style).pack(pady=10)

    # --- 設定對話框對應的各種彈窗 ---
    def open_resize_dialog(self):
        """開啟解析度設定彈窗"""
        win = tk.Toplevel(self.root);
        win.grab_set();
        win.geometry("300x300")
        tk.Label(win, text="選擇解析度", font=("微軟正黑體", 12, "bold")).pack(pady=10)
        # 遍歷選項建立按鈕，點擊後更新尺寸並刷新選單
        for text, w, h in [("3.5吋 (480x320)", 480, 320), ("800x600 (預設)", 800, 600), ("1024x768", 1024, 768)]:
            tk.Button(win, text=text, width=20, command=lambda _w=w, _h=h: [
                setattr(self, 'win_width', _w),
                setattr(self, 'win_height', _h),
                self.update_window_geometry(),
                win.destroy(),
                self.show_settings_menu()
            ]).pack(pady=5)

    def open_speed_dialog(self):
        """開啟影片速度設定彈窗（使用單選框）"""
        win = tk.Toplevel(self.root);
        win.grab_set();
        win.geometry("200x250")
        for v in [0.5, 1.0, 1.5, 2.0]:
            tk.Radiobutton(win, text=f"{v}x 速度", variable=self.play_speed, value=v).pack(pady=5)
        tk.Button(win, text="確定", command=win.destroy).pack(pady=10)

    def open_idle_time_dialog(self):
        """開啟閒置秒數設定彈窗"""
        win = tk.Toplevel(self.root);
        win.grab_set();
        win.geometry("200x250")
        for t in [5, 10, 30, 60]:
            tk.Radiobutton(win, text=f"{t} 秒", variable=self.idle_limit, value=t).pack(pady=5)
        tk.Button(win, text="確定", command=win.destroy).pack(pady=10)

    def open_eye_speed_dialog(self):
        """開啟待機眼睛動畫速度彈窗"""
        win = tk.Toplevel(self.root);
        win.grab_set();
        win.geometry("200x250")
        for v in [0.5, 1.0, 1.5]:
            tk.Radiobutton(win, text=f"{v}x 速度", variable=self.eye_speed, value=v).pack(pady=5)
        tk.Button(win, text="確定", command=win.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()  # 啟動 Tkinter
    app = FixedWindowApp(root)  # 實例化應用程式
    root.mainloop()  # 開始主事件循環