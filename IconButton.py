import flet as ft

from flet import icons

def main(page: ft.Page):
	page.title = "Outlined buttons with icons"

	def btn_event(e: ft.ControlEvent):
		#if e.control.data == "Icon Button":
		#	page.window_minimized = True
		#	page.update()
		#else:
		#	page.window_maximized = True
		#	page.update()
		pass

	
	page.add(
		ft.ElevatedButton("Icon Button", icon=ft.icons.LIGHTBULB_OUTLINE_SHARP, icon_color=ft.colors.BLACK45,
			style=ft.ButtonStyle(
				bgcolor={
					ft.MaterialState.DEFAULT: ft.colors.LIGHT_BLUE,
					ft.MaterialState.HOVERED: ft.colors.BLUE,
					ft.MaterialState.FOCUSED: ft.colors.BLUE,
					ft.MaterialState.PRESSED: ft.colors.PINK
				},
				color={
					ft.MaterialState.DEFAULT: ft.colors.WHITE54,
					ft.MaterialState.HOVERED: ft.colors.WHITE,
					ft.MaterialState.FOCUSED: ft.colors.WHITE,
					ft.MaterialState.PRESSED: ft.colors.WHITE
				},
				shape=ft.RoundedRectangleBorder(radius=8),
			),
			on_click=btn_event, data="Icon Button"
		),
		ft.OutlinedButton("Icon Button with color", icon=ft.icons.EMOJI_OBJECTS_OUTLINED, icon_color=ft.colors.YELLOW_700, on_click=btn_event, data="Icon Button with color")
	)

ft.app(target=main)

