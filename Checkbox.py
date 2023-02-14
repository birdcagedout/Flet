import flet as ft



def main(page: ft.Page):
	page.title = "골라보셈 v4.0"
	page.window_width = 400
	page.window_height = 400
	page.window_maximizable = False
	page.window_minimizable = True
	page.window_center()
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window_always_on_top = True
	page.window_to_front()
	page.window_resizable = False
	
	
	def radiogroup_changed(e):
		text_result.value = f"Your favorite color is:  {e.control.value}"
		page.update()

	text_question = ft.Text("Select your favorite color:")
	radio_group = ft.RadioGroup(content=ft.Column(
		[
		ft.Radio(value="red", label="Red", fill_color={
			ft.MaterialState.HOVERED: ft.colors.RED,
			ft.MaterialState.DEFAULT: ft.colors.LIGHT_BLUE_500,
		}),
		ft.Radio(value="green", label="Green", fill_color={
			ft.MaterialState.HOVERED: ft.colors.RED,
			ft.MaterialState.DEFAULT: ft.colors.LIGHT_GREEN_500,
		}),
		ft.Radio(value="blue", label="Blue", fill_color={
			ft.MaterialState.HOVERED: ft.colors.RED,
			ft.MaterialState.DEFAULT: ft.colors.PINK_300,
		})
		]), on_change=radiogroup_changed)
	text_result = ft.Text()
  
	page.add(text_question, radio_group, text_result)

ft.app(target=main)