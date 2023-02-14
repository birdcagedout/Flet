import flet as ft

def main(page: ft.Page):
	page.window_width = 400
	page.window_height = 400
	page.window_center()

	def slider_changed(e):
		t.value = f"Slider changed to {e.control.value}"
		page.window_opacity = e.control.value / 100
		page.update()

	t = ft.Text()
	page.add(t)
	page.add(ft.Row(
			#visible=False,
			alignment="spaceBetween",
			vertical_alignment="center",
			controls=[
				ft.IconButton(
					icon=ft.icons.DIRECTIONS_BIKE,
					icon_color=ft.colors.GREEN,
					tooltip="동작속도를 느리게",
					disabled=True
					#on_click=self.save_clicked,
				),
				#ft.TextField(label="적어주세요"),
				ft.Slider(min=10, max=100, divisions=9, label="{value}%", expand = True, on_change_start=slider_changed, on_change=slider_changed),
		 		ft.IconButton(
					icon=ft.icons.ROCKET_LAUNCH,
					icon_color=ft.colors.RED,
					tooltip="동작속도를 빠르게",
					disabled=True
					#on_click=self.save_clicked,
				)
			]
		)
	)
	page.update()

ft.app(target=main)