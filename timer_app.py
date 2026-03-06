import customtkinter as ctk
from monitor import get_work_area
from sound import beep_repeated
from tray import TrayIcon
import ctypes

WIN_WIDTH = 300
WIN_HEIGHT = 50
BUTTONS = [5, 10, 15, 20, 25]

class TimerApp:

    def __init__(self):

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("デスクトップタイマー")
        self.app.attributes("-topmost", True)
        self.app.overrideredirect(True)
        self.app.attributes("-alpha", 0.7)

        self.timer_seconds = 0

        self.setup_window()
        self.create_buttons()

        # ツールウィンドウ化
        self.app.update()
        self.make_tool_window()    

        self.app.bind("<Enter>", self.on_enter)
        self.app.bind("<Leave>", self.on_leave)
        
        self.tray = TrayIcon(self.app)
        self.tray.run()
        self.app.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.timer_job = None

        self.app.mainloop()

    # -----------------------------
    # ツールウィンドウ化
    # -----------------------------
    def make_tool_window(self):

        hwnd = ctypes.windll.user32.GetParent(self.app.winfo_id())

        GWL_EXSTYLE = -20
        WS_EX_TOOLWINDOW = 0x00000080

        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TOOLWINDOW)
        
    # -----------------------------
    # ウィンドウ配置
    # -----------------------------
    def setup_window(self):

        work = get_work_area()

        x = work.right - WIN_WIDTH - 1
        y = work.bottom - WIN_HEIGHT -1

        self.app.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+{x}+{y}")
        self.app.grid_rowconfigure(0, weight=1)

    # -----------------------------
    # UI生成
    # -----------------------------
    def create_buttons(self):

        self.start_buttons = []

        for i, m in enumerate(BUTTONS):

            btn = ctk.CTkButton(
                self.app,
                text=f"{m}:00",
                command=lambda m=m: self.start_timer(m),
                font=("Arial", 15),
            )

            btn.grid(row=0, column=i, padx=1, sticky="nswe")
            self.start_buttons.append(btn)

            self.app.grid_columnconfigure(i, weight=1)

        self.end_button = ctk.CTkButton(
            self.app,
            text="00:00",
            command=self.stop_timer,
            text_color="black",
            font=("Arial", 20),
        )

        self.end_button.grid_remove()

    # -----------------------------
    # 色判定
    # -----------------------------
    def get_timer_color(self, sec):

        if sec <= 10:
            return "red"
        elif sec <= 60:
            return "orange"

        return "yellow"

    # -----------------------------
    # タイマー更新
    # -----------------------------
    def update_timer(self):

        mins, secs = divmod(self.timer_seconds, 60)

        color = self.get_timer_color(self.timer_seconds)

        self.end_button.configure(
            text=f"{mins:02d}:{secs:02d}",
            fg_color=color,
            hover_color=color,
        )

        if self.timer_seconds == 0:

            beep_repeated(self.app, 3)

            self.end_button.grid_remove()

            for btn in self.start_buttons:
                btn.grid()

            self.timer_job = None
            return

        self.timer_seconds -= 1

        self.timer_job = self.app.after(1000, self.update_timer)

    # -----------------------------
    # タイマー開始
    # -----------------------------
    def start_timer(self, minutes):

        if self.timer_job:
            self.app.after_cancel(self.timer_job)
            self.timer_job = None
        
        self.timer_seconds = minutes * 60

        for btn in self.start_buttons:
            btn.grid_remove()

        self.end_button.grid(row=0, column=0, columnspan=5, sticky="nswe")

        self.update_timer()

    # -----------------------------
    # タイマー停止
    # -----------------------------
    def stop_timer(self):

        if self.timer_job:
            self.app.after_cancel(self.timer_job)
            self.timer_job = None
            
        self.timer_seconds = 0

        self.end_button.grid_remove()

        for btn in self.start_buttons:
            btn.grid()

    # -----------------------------
    # マウスカーソル有無による透明度の調整
    # -----------------------------
    def on_enter(self, event):
        self.app.attributes("-alpha", 1.0)

    def on_leave(self, event):
        self.app.attributes("-alpha", 0.7)

    # -----------------------------
    # ウィンドウ最小化
    # -----------------------------
    def hide_window(self):
        self.app.withdraw()