import flet as ft
from flet.border import BorderSide
from flet.buttons import RoundedRectangleBorder

def main(page: ft.Page):
	page.theme_mode = ft.ThemeMode.LIGHT
	
	page.add(
		ft.ElevatedButton(
			"Styled button 1",
			style=ft.ButtonStyle(
				color={
					#ft.MaterialState.HOVERED: ft.colors.WHITE,
					ft.MaterialState.FOCUSED: ft.colors.BLUE,
					ft.MaterialState.DEFAULT: ft.colors.BLACK,
				},
				bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": ft.colors.YELLOW},
				#padding={ft.MaterialState.HOVERED: 20},
				overlay_color=ft.colors.TRANSPARENT,
				elevation={"pressed": 0, "": 1},
				animation_duration=500,
				side={
					ft.MaterialState.DEFAULT: BorderSide(1, ft.colors.BLUE),
					#ft.MaterialState.HOVERED: BorderSide(2, ft.colors.BLUE),
				},
				shape={
					#ft.MaterialState.HOVERED: RoundedRectangleBorder(radius=20),
					ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=2),
				},
			),
		)
	)

ft.app(target=main)