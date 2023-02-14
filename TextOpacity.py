import flet as ft
import time

def main(page: ft.Page):

	title = ft.Text("this is title ",size=30,weight="bold")
	desc = ft.Text("Makes a control partially transparent. 0.0 - control is completely transparent, not painted at all. 1.0 (default) - a control is fully painted without any transparency.",
		width=300,
		animate_opacity=1000

		)

	def showme(e):
		desc.opacity = 0
		desc.update()
		time.sleep(desc.animate_opacity/1000)
		desc.visible = False
		page.update()
		
	page.add(
		title,
		desc,
		ft.ElevatedButton("showme", on_click=showme)
		)
	
ft.app(target=main)