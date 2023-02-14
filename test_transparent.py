import flet as ft

def main(page: ft.Page):
	page.window_width = 350
	page.window_height = 400
	page.window_center()

	page.window_bgcolor = ft.colors.TRANSPARENT
	page.bgcolor = ft.colors.TRANSPARENT
	page.window_title_bar_hidden = True
	page.window_frameless = True
	
	page.add(ft.ElevatedButton("I'm a floating button!"))

ft.app(target=main)