
# Animation offset: https://flet.dev/docs/guides/python/animations

import flet as ft

def main(page: ft.Page):
	page.window_width = 400
	page.window_height = 400
	page.window_center()

	c1 = ft.Container(
		width=150,
		height=150,
		bgcolor="blue",
		border_radius=10,
		offset=ft.transform.Offset(-1, 0),
		animate_offset=ft.animation.Animation(1000),
	)

	c2 = ft.Container(
		width=150,
		height=150,
		bgcolor="red",
		border_radius=10,
		offset=ft.transform.Offset(-1, 0),
		animate_offset=ft.animation.Animation(1000),
	)

	c3 = ft.Container(
		width=10,
		height=150,
		left=0,
		top=10,
		bgcolor="white",
		border_radius=0,
	)

	def animate(e):
		c1.offset = ft.transform.Offset(0, 0)
		c2.offset = ft.transform.Offset(0, 0)
		page.update()

	page.add( ft.Row(controls=[c2, c1, c3], spacing=0, tight=True),
		ft.ElevatedButton("Reveal!", on_click=animate),
	)

ft.app(target=main)