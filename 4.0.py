import flet as ft

VER = "4.0"

def main(page: ft.Page):
	page.title = f"귀찮다 v{VER}"
	page.window_width = 370
	page.window_height = 400
	page.window_maximizable = False
	page.window_minimizable = True
	page.window_center()
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window_always_on_top = True
	page.window_to_front()
	page.window_resizable = False
	page.padding = 15
	# page.spacing = 0
	# page.vertical_alignment = ft.MainAxisAlignment.START
	# page.horizontal_alignment = ft.CrossAxisAlignment.START
	#page.theme = ft.Theme(color_scheme_seed="red")
	

	# Appbar 이벤트 핸들러
	def check_item_clicked(e: ft.ControlEvent):
		print(e.control.data)
		if e.control.data == "checked":
			e.control.checked = not e.control.checked
			page.update()
	
	# 라디오버튼이 선택될 때 호출되는 이벤트 핸들러
	def radiogroup_changed(e: ft.ControlEvent):
		page.snack_bar = ft.SnackBar(ft.Row([ft.Text(f"{e.control.value}", color=ft.colors.YELLOW), ft.Text("을 선택하셨습니다")], spacing=0))
		page.snack_bar.open = True
		page.snack_bar.opacity = 0.5
		page.update()
	
	def textfield_focused(e: ft.ControlEvent):
		page.snack_bar = ft.SnackBar(ft.Row([ft.Text("직접 입력", color=ft.colors.YELLOW), ft.Text("을 선택하셨습니다")], spacing=0))
		page.snack_bar.open = True
		page.snack_bar.opacity = 0.5
		r2_container.content.value = None			# 직접 입력시 이전 라디오버튼 선택을 초기화한다.
		page.update()
	
	def textfield_changed(e: ft.ControlEvent):
		try:
			print(e.control.value)
		except UnicodeDecodeError:
			pass

	
	def banner_show(e):
		page.appbar.visible = False
		page.update()
		page.banner.open = True
		page.update()
	
	def banner_close(e):
		page.appbar.visible = True
		page.update()
		page.banner.open = False
		page.update()

	page.banner = ft.Banner(
		bgcolor=ft.colors.AMBER_200,
		leading=ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_600, size=40),
		leading_padding=8,
		content=ft.Text(
			"자동차관리정보시스템이 시작되지 않았습니다.\r프로그램을 종료합니다.", color=ft.colors.BLACK
		),
		content_padding=ft.padding.only(left=10.0, top=20.0, right=10.0, bottom=4.0),
		actions=[
			ft.TextButton("Retry", on_click=banner_close),
			ft.TextButton("Ignore", on_click=banner_close),
			ft.TextButton("Cancel", on_click=banner_close),
		],
		force_actions_below=True
	)

	page.appbar = ft.AppBar(
		#leading=ft.Icon(ft.icons.ROCKET_LAUNCH),
		#leading_width=30,
		

		title=ft.Text("자동입력할 조회사유를 선택하세요", font_family='Malgun Gothic', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, opacity=1),
		center_title=True,
		bgcolor=ft.colors.BLACK87,

		actions=[
			#ft.IconButton(ft.icons.INFO_OUTLINE, on_click=check_item_clicked, data="info"),
			#ft.IconButton(ft.icons.FILTER_3, on_click=check_item_clicked, data="filter3"),
			#ft.PopupMenuButton(
			#	items=[
			#		ft.PopupMenuItem(text="Item 1"),
			#		ft.PopupMenuItem(),  # divider
			#		ft.PopupMenuItem(
			#			text="Checked item", checked=False, on_click=check_item_clicked, data="checked"
			#		),
			#	]
			#),
		],
		
	)

	#r1_container = ft.Container(
	#	content = ft.Text("자동입력할 조회 사유를 선택해주세요", size=20, weight=ft.FontWeight.BOLD),
	#	bgcolor=ft.colors.LIGHT_GREEN_200,
	#	alignment = ft.alignment.center,
	#	width=page.window_max_width,
	#	#expand=True,
	#	margin=0
	#)
	
	

	r2_container = ft.Container(
		content = ft.RadioGroup(content=ft.Column([
		ft.Radio(value="신규, 저당 등 업무대상자 확인", label="신규, 저당 등 업무대상자 확인", fill_color=ft.colors.LIGHT_BLUE_500, height=35),
		ft.Radio(value="이전, 변경 등 업무대상자 확인", label="이전, 변경 등 업무대상자 확인", fill_color=ft.colors.LIGHT_GREEN_600, height=35),
		ft.Radio(value="압류, 말소 등 업무대상자 확인", label="압류, 말소 등 업무대상자 확인", fill_color=ft.colors.DEEP_PURPLE_300, height=35),
		ft.Radio(value="소유자 확인", label="소유자 확인", fill_color=ft.colors.PINK_200, height=35)
		], spacing=0), on_change=radiogroup_changed),
		padding = ft.padding.only(left=30, top=-5),
		margin = 0
	)
	

	r3_container = ft.Container(
		content = ft.TextField(label='직접 입력', width=230, text_size=14, bgcolor=ft.colors.TRANSPARENT, focused_bgcolor=ft.colors.AMBER_100, filled=True, dense=True, hint_text="(입력하신 내용은 자동으로 저장됩니다)", hint_style=ft.TextStyle(size=11, color=ft.colors.TEAL_300), on_focus=textfield_focused, on_change=textfield_changed),
		padding = ft.padding.only(left=40, right=40, top=0),
		margin = 0,
	)


	r4_container = ft.Row(
		controls = [
			ft.Container(
				margin=0,
				padding=0,
				expand=2,
				visible=False
			),
			ft.Container(
				content=ft.Row([
					ft.Icon(ft.icons.PLAY_ARROW_ROUNDED, size=50),
					ft.Text("시작", size=30, weight=ft.FontWeight.BOLD)]),
				width = 150,
				height = 60,
				bgcolor = ft.colors.LIGHT_BLUE_500,
				border_radius=5,
				ink = True,
				padding = ft.padding.only(left=50, right=50),
				margin = 0,
				expand=5,
				alignment= ft.alignment.center,
				on_click= lambda x: print("클릭")
			),
			ft.Container(
				margin=0,
				padding=0,
				expand=2,
				visible=False
			),
		])
		
	
	
	#page.add(r1_container, r2_container, r3_container)
	#page.add(ft.ElevatedButton("테스트 버튼", on_click=banner_show))
	page.add(r2_container, r3_container, r4_container)
	

ft.app(target=main)