import flet as ft

def main(page: ft.Page):
	page.window_width = 400
	page.window_height = 400
	page.window_center()
	
	def banner_show(e):
		page.banner.open = True
		page.update()
	
	def banner_close(e):
		page.banner.open = False
		page.update()

	page.banner = ft.Banner(
		bgcolor=ft.colors.AMBER_200,
		leading=ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_600, size=40),
		leading_padding=8,
		content=ft.Text(
			"자동차관리정보시스템이 시작되지 않았습니다.\r프로그램을 종료합니다.", color=ft.colors.BLACK
		),
		content_padding=ft.padding.only(left=16.0, top=24.0, right=16.0, bottom=4.0),
		actions=[
			ft.TextButton("Retry", on_click=banner_close),
			ft.TextButton("Ignore", on_click=banner_close),
			ft.TextButton("Cancel", on_click=banner_close),
		],
	)

	page.add(ft.ElevatedButton("Show Banner", on_click=banner_show))
	page.add(ft.ElevatedButton("Show Banner2", on_click=banner_show))
	page.add(ft.ElevatedButton("Show Banner3", on_click=banner_show))


ft.app(target=main)