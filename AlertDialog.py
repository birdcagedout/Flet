import flet as ft



def main(page: ft.Page):
	page.title = "AlertDialog examples"
	page.theme_mode = ft.ThemeMode.LIGHT


	def yes_click(e: ft.ControlEvent):
		page.window_close()
	
	def no_click(e: ft.ControlEvent):
		# print(type(e) is ft.ControlEvent)
		dlg_modal.open = False
		page.update()

	dlg_modal = ft.AlertDialog(
		modal=True,
		title=ft.Text("Please confirm"),
		content=ft.Text("Do you really want to exit?"),
		actions=[
			ft.TextButton("Yes", on_click=yes_click),
			ft.TextButton("No", on_click=no_click),
		],
		actions_alignment=ft.MainAxisAlignment.END
	)

	def open_dlg_modal(e: ft.ControlEvent):
		page.dialog = dlg_modal
		dlg_modal.open = True
		page.update()

	page.add(
		ft.ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
	)

ft.app(target=main)

