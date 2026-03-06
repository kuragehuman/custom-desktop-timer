import pystray
from PIL import Image, ImageDraw
import threading


def create_image():
    # 簡単なアイコン生成
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="black")
    return image


class TrayIcon:

    def __init__(self, app):
        self.app = app
        self.icon = pystray.Icon(
            "desktop_timer",
            create_image(),
            "Desktop Timer",
            menu=pystray.Menu(
                pystray.MenuItem("表示", self.show_window),
                pystray.MenuItem("終了", self.quit_app)
            )
        )

    def run(self):
        threading.Thread(target=self.icon.run, daemon=True).start()

    def show_window(self):
        self.app.after(0, self.app.deiconify)

    def quit_app(self, icon, item):
        self.icon.stop()
        self.app.quit()