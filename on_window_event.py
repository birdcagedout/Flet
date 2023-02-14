import flet as ft

def main(page: ft.Page):
	page.title = "MyApp"

	def window_event(e: ft.ControlEvent):
		if e.data == "close":
			page.dialog = confirm_dialog
			confirm_dialog.open = True
			page.update()
		else:
			print(e.data)					# minimize, blur, focus, restore, maximize, unmaximize, moved, resized 등


	page.window_prevent_close = True
	page.on_window_event = window_event



	def yes_click(e):
		page.window_destroy()

	def no_click(e):
		confirm_dialog.open = False
		page.update()

	confirm_dialog = ft.AlertDialog(
		modal=True,
		title=ft.Text("Please confirm"),
		content=ft.Text("Do you really want to exit this app?"),
		actions=[
			ft.ElevatedButton("Yes", on_click=yes_click),
			ft.OutlinedButton("No", on_click=no_click),
		],
		actions_alignment=ft.MainAxisAlignment.END,
	)

	page.add(ft.Text('Try exiting this app by clicking window\'s "Close" button!'))

ft.app(target=main)