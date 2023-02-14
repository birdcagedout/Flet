import flet as ft

def main(page: ft.Page):
	page.theme_mode = ft.ThemeMode.LIGHT

	page.window_width = 400
	page.window_height = 400

	page.window_top = 500
	page.window_left = 1200

	page.title = 'Flet Example'

	# number = ft.TextField(value='테스트', height=32, border_width=0.5, border_radius=0)
	number = ft.TextField(value='테스트', border_radius=0, width=200)
	btn = ft.ElevatedButton(text="추가")

	entryRow = ft.Row(controls=[number, btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

	page.add(entryRow)

	page.update()


ft.app(target=main,)
