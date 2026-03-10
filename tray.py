import pystray
from PIL import Image, ImageDraw
import threading


def create_image():
    size = 64

    image = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(image)

    # 時計の外枠
    draw.ellipse(
        (8, 8, 56, 56),
        outline="black",
        width=4
    )

    # 中心点
    center = (32, 32)

    # 長針（分）
    draw.line(
        (center[0], center[1], center[0], 16),
        fill="black",
        width=4
    )

    # 短針（時）
    draw.line(
        (center[0], center[1], 44, 32),
        fill="black",
        width=4
    )

    # 中心
    draw.ellipse(
        (29, 29, 35, 35),
        fill="black"
    )

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