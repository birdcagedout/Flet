import flet as ft

def main(page: ft.Page):
	page.window_width = 360				# page.width = 344.0
	page.window_height = 400			# page.height = 392.0
	page.window_resizable = False
	page.window_maximizable = False
	page.window_center()
	page.padding = 0
	page.window_title_bar_hidden = True
	page.window_title_bar_buttons_hidden = True

	def on_window_event(e: ft.ControlEvent):
		print(e.data)
		if e.data == "maximize":
			print("")
			return

	page.on_resize = on_window_event
	page.on_window_event = on_window_event
	
	#app_bar = ft.AppBar(
	#	leading=ft.Icon(ft.icons.ANDROID_OUTLINED, size=70, color=ft.colors.GREEN_600, opacity=0.8),
	#	automatically_imply_leading=True,
	#	leading_width=40,
		
	#	title=ft.Column(controls=[
	#		ft.Text(" 자동으로 입력하실", font_family='Malgun Gothic', size=11, weight=ft.FontWeight.NORMAL, color=ft.colors.WHITE, opacity=1),
	#		ft.Text("조회사유를 선택하세요", font_family='Malgun Gothic', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, opacity=1),
	#	], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
	#	center_title=True,
	#	bgcolor="#59bdd5",
	#	toolbar_height=50,

	#	actions=[ft.IconButton(ft.icons.INFO_OUTLINE, icon_size=30, icon_color=ft.colors.BLACK54, tooltip="개발자 정보", data="dev_info")]
	#)

	def win_event(e: ft.ControlEvent):
		if e.control.data == "minimize":
			page.window_minimized = True
			page.update()
		if e.control.data == "close":
			page.window_destroy()

	#title_bar = ft.WindowDragArea(ft.Container(ft.Text("Drag this area to move, maximize and restore application window."), bgcolor=ft.colors.TRANSPARENT, padding=50), expand=True)
	title_bar = ft.WindowDragArea(
		content=ft.Container(
			content=ft.Row([
				ft.Container(ft.Icon(ft.icons.ANDROID_OUTLINED, size=100, color=ft.colors.GREEN_600, opacity=0.8), width=50),
				ft.Container(ft.Column(controls=[
					ft.Text(" 자동으로 입력하실", font_family='Malgun Gothic', size=11, weight=ft.FontWeight.NORMAL, color=ft.colors.WHITE),
					ft.Text("조회사유를 선택하세요", font_family='Malgun Gothic', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, no_wrap=True),
				], spacing=1, alignment=ft.MainAxisAlignment.CENTER), width=230),
				ft.Container(
				#	ft.Row([
				#	ft.IconButton(ft.icons.MINIMIZE, icon_size=15, scale=1.5, on_click=win_event, data="minimize"),
				#	ft.IconButton(ft.icons.CLOSE, icon_size=15, scale=1.5, bgcolor=ft.colors.RED_ACCENT_400, on_click=win_event, data="close"),
				#], width=110, spacing=-20, alignment=ft.MainAxisAlignment.START)
					ft.Column([
						ft.Container(content=ft.Icon(ft.icons.CLOSE, size=30), bgcolor=ft.colors.RED_ACCENT_400, margin=0, expand=True, on_click=win_event, data="close"),
						ft.Container(content=ft.Icon(ft.icons.MINIMIZE, size=30), bgcolor=ft.colors.LIGHT_BLUE_300, margin=0, expand=True, on_click=win_event, data="minimize")
						],
						width=70, spacing=0, alignment=ft.MainAxisAlignment.SPACE_EVENLY, horizontal_alignment=ft.CrossAxisAlignment.STRETCH
				), ft.Column([ft.Text(" ")]),
				),
			],
			width=360,
			height=75,),
			bgcolor="#59bdd5",
		),
	)
	title_bar.margin=ft.margin.all(0)
		

	
	#st = ft.Stack([
	#	app_bar, title_bar
		#ft.Row(
		#	[
		#		title_bar,
		#		ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close())
		#	]
		#),
	#])
	
	#page.appbar = app_bar
	page.add(
		title_bar
	)

ft.app(target=main)