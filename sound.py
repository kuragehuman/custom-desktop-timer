import winsound

# -----------------------------
# サウンド
# -----------------------------
def beep_repeated(app, times):

    if times > 0:
        winsound.MessageBeep()
        app.after(1000, lambda: beep_repeated(app, times - 1))
