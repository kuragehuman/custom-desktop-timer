import customtkinter as ctk
import winsound

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("デスクトップタイマー")
app.attributes("-topmost", True)

# タイトルバーを消す
# app.overrideredirect(True)

# ウィンドウサイズと右下固定
win_width, win_height = 300, 100
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = screen_width - win_width - 12
y = screen_height - win_height - 82
app.geometry(f"{win_width}x{win_height}+{x}+{y}")

# 残り時間ラベル
time_label = ctk.CTkLabel(app, text="00:00", font=("Arial", 30))
time_label.grid(row=0, column=0, columnspan=5, pady=10)

timer_seconds = 0

# -----------------------------
# サウンドを繰り返す関数
# -----------------------------
def beep_repeated(times):
    if times > 0:
        winsound.MessageBeep()  # 1回鳴らす
        app.after(1000, lambda: beep_repeated(times - 1))  # 1秒後に次を鳴らす

# タイマー更新関数
def update_timer():
    global timer_seconds
    if timer_seconds >= 0:
        mins, secs = divmod(timer_seconds, 60)
        time_label.configure(text=f"{mins:02d}:{secs:02d}")
        timer_seconds -= 1
        app.after(1000, update_timer)
    else:
        time_label.configure(text="00:00")
        beep_repeated(3)
        # タイマー終了で終了ボタン非表示にして開始ボタンを戻す
        end_button.grid_remove()
        for btn in start_buttons:
            btn.grid()

# タイマー開始関数
def start_timer(minutes):
    global timer_seconds
    timer_seconds = minutes * 60
    # 開始ボタンを非表示
    for btn in start_buttons:
        btn.grid_remove()
    # 終了ボタンを表示
    end_button.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")
    update_timer()

# 「n分」開始ボタン
buttons = [5, 10, 15, 20, 25]
start_buttons = []
for i, m in enumerate(buttons):
    btn = ctk.CTkButton(app, text=f"{m}分", command=lambda m=m: start_timer(m))
    btn.grid(row=1, column=i, padx=5, pady=10, sticky="ew")
    start_buttons.append(btn)

# 列幅を均等に
for i in range(5):
    app.grid_columnconfigure(i, weight=1)

# 終了ボタン（最初は非表示）
def stop_timer():
    global timer_seconds
    timer_seconds = -1  # タイマー停止
    end_button.grid_remove()
    for btn in start_buttons:
        btn.grid()

end_button = ctk.CTkButton(app, text="終了", command=stop_timer)
end_button.grid_remove()  # 最初は非表示

app.mainloop()