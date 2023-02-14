import flet as ft

def main(page):

	def slider_changed(e):
		t.value = f"Slider changed to {e.control.value}"
		page.update()

	t = ft.Text()
	page.add(
		ft.Text("Slider with 'on_change' event:"),
		ft.Slider(min=10, max=100, divisions=9, label="{value}%", on_change=slider_changed), t)

ft.app(target=main)