import customtkinter as ctk
import winsound

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("デスクトップタイマー")
app.attributes("-topmost", True)

# タイトルバーを消す
# app.overrideredirect(True)

# ウィンドウサイズと右下固定
win_width, win_height = 300, 50
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = screen_width - win_width - 250
y = screen_height - win_height - 30
app.geometry(f"{win_width}x{win_height}+{x}+{y}")
app.grid_rowconfigure(0, weight=1)

timer_seconds = 0

# -----------------------------
# サウンドを繰り返す関数
# -----------------------------
def beep_repeated(times):
    if times > 0:
        winsound.MessageBeep()  # 1回鳴らす
        app.after(1000, lambda: beep_repeated(times - 1))  # 1秒後に次を鳴らす

# -----------------------------
# タイマー更新関数
# -----------------------------
def update_timer():
    global timer_seconds
    if timer_seconds >= 0:
        mins, secs = divmod(timer_seconds, 60)
        end_button.configure(text=f"{mins:02d}:{secs:02d}")
        
        # 残り時間で色を変える
        if timer_seconds <= 10:  # 残り10秒以下
            btn_color="red"
        elif timer_seconds <= 60:
            btn_color="orange"
        else:
            btn_color="yellow"
        
        end_button.configure(fg_color=btn_color, hover_color=btn_color)
        timer_seconds -= 1

        app.after(1000, update_timer)
    else:
        btn_color="yellow"
        end_button.configure(fg_color=btn_color, hover_color=btn_color)
        beep_repeated(3)
        # タイマー終了で終了ボタン非表示にして開始ボタンを戻す
        end_button.grid_remove()
        for btn in start_buttons:
            btn.grid()

# -----------------------------
# タイマー開始関数
# -----------------------------
def start_timer(minutes):
    global timer_seconds
    timer_seconds = minutes * 60
    # 開始ボタンを非表示
    for btn in start_buttons:
        btn.grid_remove()
    # 終了ボタンを表示
    end_button.grid(row=0, column=0, columnspan=5, pady=1, sticky="nswe")
    update_timer()

# 「n分」開始ボタン
buttons = [5, 10, 15, 20, 25]
start_buttons = []
for i, m in enumerate(buttons):
    btn = ctk.CTkButton(app, text=f"{m}:00", command=lambda m=m: start_timer(m), font=("Arial", 15))
    btn.grid(row=0, column=i, padx=5, pady=1, sticky="nswe")
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

end_button = ctk.CTkButton(app, text_color="black", text="00:00", command=stop_timer, font=("Arial", 20))
end_button.grid_remove()  # 最初は非表示

app.mainloop()