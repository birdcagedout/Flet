import time
import ctypes
import flet as ft


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()		# 이 부분을 제외하면 배율이 1보다 클 때 낮은 해상도가 나온다(ex. 배율=1.25일때 3840/1.25 = 3072)
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

def main(page: ft.Page):
	page.title = f"Window 창 이동 가능한지 테스트"
	page.window_width = 350
	page.window_height = 400
	page.window_maximizable = False
	page.window_minimizable = True
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window_always_on_top = True
	page.window_center()
	page.window_to_front()
	page.window_resizable = False
	page.padding = 15
	page.window_visible = True
	page.update()

	for i in range(10):
		page.window_left = (w/2) - (350/2) + (i*50)
		page.window_top = (h/2) - (400/2) + (i*10)
		page.update()
		time.sleep(0.5)



ft.app(target=main, view=ft.FLET_APP_HIDDEN)