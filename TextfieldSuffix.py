import flet as ft

def main(page: ft.Page):
	
	def erase(e: ft.ControlEvent):
		t2.value = None
		t2.update()

	t1 = ft.TextField(label="With prefix", prefix_text="https://")
	t2 = ft.TextField(label="With suffix", suffix=ft.IconButton(ft.icons.CANCEL, tooltip="모두 지움", on_click=erase))
	t3 = ft.TextField(
		label="With prefix and suffix", prefix_text="https://", suffix_text=".com"
	)
	t4 = ft.TextField(
		label="My favorite color",
		icon=ft.icons.FORMAT_SIZE,
		hint_text="Type your favorite color",
		helper_text="You can type only one color",
		counter_text="0 symbols typed",
		prefix_icon=ft.icons.COLOR_LENS,
		suffix_text="...is your color",
	)
	page.add(t1, t2, t3, t4)

ft.app(target=main)