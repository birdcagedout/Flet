import flet as ft

#ft.icons.ROCKET_LAUNCH

VER = "4.0"

class TodoApp(ft.UserControl):
	def build(self):
		self.new_task = ft.TextField(label="자동입력할 사유를 적어주세요", expand=True)
		
		self.tasks = ft.Column()

		# application's root control (i.e. "view") containing all other controls
		return ft.Column(
			width=350,
			controls=[
				ft.Row(
					controls=[
						self.new_task,
						ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
					],
				),
				self.tasks,
			],
		)

	def add_clicked(self, e):
		self.tasks.controls.append(ft.Checkbox(label=self.new_task.value))
		self.new_task.value = ""
		self.update()


def main(page: ft.Page):
	page.title = f"귀찮다 v{VER}"
	#page.window_opacity = 0.5
	page.window_width = 400
	page.window_height = 400
	page.window_maximizable = False
	#page.vertical_alignment = ft.MainAxisAlignment.CENTER
	page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
	page.window_resizable = False

	page.window_to_front()
	page.update()

	def check_item_clicked(e: ft.ControlEvent):
		print(e.control.data)
		if e.control.data == "checked":
			e.control.checked = not e.control.checked
			page.update()

	page.appbar = ft.AppBar(
		leading=ft.Icon(ft.icons.ROCKET_LAUNCH),
		leading_width=40,

		title=ft.Text("사유를 적어주세요", size=20),
		center_title=False,
		bgcolor=ft.colors.LIGHT_GREEN_200,

		actions=[
			ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=check_item_clicked, data="sunny"),
			ft.IconButton(ft.icons.FILTER_3, on_click=check_item_clicked, data="filter3"),
			ft.PopupMenuButton(
				items=[
					ft.PopupMenuItem(text="Item 1"),
					ft.PopupMenuItem(),  # divider
					ft.PopupMenuItem(
						text="Checked item", checked=False, on_click=check_item_clicked, data="checked"
					),
				]
			),
		],
	)

	# create application instance
	todo = TodoApp()

	# add application's root control to the page
	page.add(todo)

ft.app(target=main)