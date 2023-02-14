import flet as ft

def main(page: ft.Page):
	page.title = "Images Example"
	page.theme_mode = ft.ThemeMode.DARK

	page.window_width = 215
	page.window_height = 238
	page.padding = 0
	page.window_center()
	page.window_always_on_top = True
	page.window_to_front()

	img = ft.Image(
		src=f"smile.gif",
		# width=100,
		# height=100,
		fit=ft.ImageFit.CONTAIN,
	)

	

	page.add(img)

ft.app(target=main)