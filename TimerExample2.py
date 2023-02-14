# https://flet.dev/docs/guides/python/user-controls/


import flet as ft
import time, threading


class Timer(ft.UserControl):
    def __init__(self, seconds, page: ft.Page):
        super().__init__()
        self.seconds = seconds
        self.page = page

    def did_mount(self):
        self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.th.start()

    def update_timer(self):
        seconds_left = self.seconds
        while self.seconds > 0:
            time.sleep(1)
            seconds_left -= 1
            if seconds_left == 0:
                self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
                self.page.update()
                seconds_left = self.seconds

    def build(self):
        return ft.Container()


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(Timer(2, page))


ft.app(target=main)