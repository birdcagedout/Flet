import math
import random
import threading
import time
import flet as ft

# 타이머 
class Timer(ft.UserControl):
	def __init__(self, seconds, page: ft.Page):
		super().__init__()
		self.seconds = seconds
		self.page = page

	def did_mount(self):
		self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
		self.th.start()

	def update_timer(self):
		print(self.page.width, self.page.height)
		seconds_left = self.seconds
		while self.seconds > 0:
			time.sleep(1)
			seconds_left -= 1
			if seconds_left == 0:
				self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
				self.page.update()
				seconds_left = self.seconds

	def build(self):
		return ft.Container()		# 더미 Control 하나 던져준다



def main(page: ft.Page):
	page.window_width = 350
	page.window_height = 400
	page.window_center()
	page.window_always_on_top = True
	page.window_to_front()
	page.padding=ft.padding.all(0)
	page.spacing = 0
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window_visible = True

	# 35가지 색상(0~33)
	colors = [
		#ft.colors.WHITE,
		ft.colors.RED,
		ft.colors.PINK,
		ft.colors.PURPLE,
		ft.colors.DEEP_PURPLE,
		ft.colors.INDIGO,
		ft.colors.BLUE,
		ft.colors.LIGHT_BLUE,
		ft.colors.CYAN,
		ft.colors.TEAL,
		ft.colors.GREEN,
		ft.colors.LIGHT_GREEN,
		ft.colors.LIME,
		ft.colors.YELLOW,
		ft.colors.AMBER,
		ft.colors.ORANGE,
		ft.colors.DEEP_ORANGE,
		ft.colors.BROWN,
		# ft.colors.BLUE_GREY,
		ft.colors.RED_ACCENT,
		ft.colors.PINK_ACCENT,
		ft.colors.PURPLE_ACCENT,
		ft.colors.DEEP_PURPLE_ACCENT,
		ft.colors.INDIGO_ACCENT,
		ft.colors.BLUE_ACCENT,
		ft.colors.LIGHT_BLUE_ACCENT,
		ft.colors.CYAN_ACCENT,
		# ft.colors.TEAL_ACCENT,
		ft.colors.GREEN_ACCENT,
		ft.colors.LIGHT_GREEN_ACCENT,
		ft.colors.LIME_ACCENT,
		ft.colors.YELLOW_ACCENT,
		ft.colors.AMBER_ACCENT,
		ft.colors.ORANGE_ACCENT,
		ft.colors.DEEP_ORANGE_ACCENT,
	]

	vertical_space_left = 363							# 주의: 절대 page.height깂을 넣지 말 것! ==> 682.4였다가 362.4로 변함
	print(page.height)
	stripes = []
	heights = []
	
	# 랜덤 10 ~ 100 : random.randint(a, b) includes both ends
	while vertical_space_left > 0:
		h = random.randint(5, 20) * random.randint(2, 5)
		if (vertical_space_left - h) >= 0:
			vertical_space_left -= h
		else:
			h = vertical_space_left
			vertical_space_left = 0
		heights.append(h)
	
	c = random.sample(colors, len(heights))

	for i in range(len(heights)):
		stripes.append(ft.ProgressBar(width=350, height=heights[i], opacity=1, rotate=ft.Rotate(angle= math.pi * (i % 2)), color=c[i], bgcolor=ft.colors.TRANSPARENT))
		page.add(stripes[i])
		time.sleep(0.1)
	
	page.add(Timer(2, page))
	page.overlay.append(ft.Container(content=ft.Text("작동 중", size=80, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center))
	
	page.theme_mode = ft.ThemeMode.LIGHT
	page.update()
	

ft.app(target=main, view=ft.FLET_APP_HIDDEN)