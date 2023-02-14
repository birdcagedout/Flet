import flet as ft

def main(page: ft.Page):
	page.theme_mode = ft.ThemeMode.LIGHT

	page.floating_action_button = ft.FloatingActionButton(
		content=ft.Row(
			[ft.Icon(ft.icons.ADD), ft.Text("Add")], alignment="center", spacing=5
		),
		bgcolor=ft.colors.AMBER_300,
		shape=ft.RoundedRectangleBorder(radius=5),
		width=100,
		mini=True,
	)

	page.add(ft.Text("Just a text!"))

ft.app(target=main)