import flet as ft
import os
import sys
import time
import logging
import ctypes
from threading import *
import win32gui, win32con
from pynput import mouse as pynputMouse
from pynput import keyboard as pynputKeyboard

VER = "4.0"




# 현재 컴퓨터의 IP 확인
# import socket
# print(socket.gethostbyname(socket.gethostname()))



# 인트로 스플래시 이미지 닫기(python3.9부터 importlib --> importlib.util로 바뀜)
import importlib.util
if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
	import pyi_splash
	#pyi_splash.update_text('UI Loaded ...')
	pyi_splash.close()



def main(page: ft.Page):
	page.title = f"귀찮다 v{VER}"
	page.window_width = 350
	page.window_height = 400
	page.window_maximizable = False
	page.window_minimizable = True
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window_always_on_top = True
	page.window_center()
	page.window_to_front()
	page.window_resizable = False
	page.padding = 15
	page.window_visible = True
	page.update()
	print(page.window_left, page.window_top)
	time.sleep(2)
	page.window_left = 1500
	page.window_top = 800
	page.update()
	print(page.window_left, page.window_top)





	# Appbar 이벤트 핸들러 : 개발자 정보
	def dev_info(e: ft.ControlEvent):
		if e.control.data == "dev_info":
			dlg = ft.AlertDialog(
				title=ft.Text(f"귀찮다 v{VER}", weight=ft.FontWeight.BOLD, size=30, text_align=ft.TextAlign.CENTER),
				content=ft.Text("김재형, 2022-2023\nAll rights reserved", size=18, text_align=ft.TextAlign.RIGHT),
				shape=ft.RoundedRectangleBorder(radius=10),
				on_dismiss=lambda e: print("Dialog dismissed!")
			)
			page.dialog = dlg
			dlg.open = True
			page.update()
	

	# RadioButton 선택시 이벤트 핸들러
	def radiogroup_changed(e: ft.ControlEvent):
		choice = int(e.control.value)
		#print(r2_container.content.value)
		page.snack_bar = ft.SnackBar(ft.Row([ft.Text(f"{preset_reasons[choice]}", color=ft.colors.YELLOW), ft.Text("을 선택하셨습니다")], spacing=0))
		page.snack_bar.open = True
		page.update()
	

	# Textfield 커서 받을 때 이벤트 핸들러 (텍스트필드의 값 = e.control.value = r2_container.content.value)
	def textfield_focused(e: ft.ControlEvent):
		choice = 5
		r2_container.content.value  = choice

		if preset_reasons[5].strip() == "":
			r3_container.content.value = None
			preset_reasons[5] = "직접 입력"

		page.snack_bar = ft.SnackBar(ft.Row([ft.Text(f"{preset_reasons[choice]}", color=ft.colors.YELLOW), ft.Text("을 선택하셨습니다")], expand=True, spacing=0))
		page.snack_bar.open = True
		page.update()

	# Textfield 변경될 때 이벤트 핸들러
	def textfield_changed(e: ft.ControlEvent):
		preset_reasons[5] = e.control.value
		print(preset_reasons)


	#========================================================================================================
	# 배너 부분
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
		content=ft.Text("자동차관리정보시스템이 시작되지 않았습니다.\r프로그램을 종료합니다.", color=ft.colors.BLACK),
		content_padding=ft.padding.only(left=10.0, top=20.0, right=10.0, bottom=4.0),
		actions=[
			ft.TextButton("Retry", on_click=banner_close),
			ft.TextButton("Ignore", on_click=banner_close),
			ft.TextButton("Cancel", on_click=banner_close),
		],
		force_actions_below=True
	)
	#========================================================================================================


	# 시작 버튼 클릭 ==> 애니메이션 1부(1.1배 커짐)
	def start_btn_animation_start(e: ft.ControlEvent):
		# 버튼UI 효과
		e.control.scale = 1.1
		e.control.content=ft.Row([
			ft.Icon(ft.icons.PAUSE, size=50),
			ft.Text("중지   ", size=30, weight=ft.FontWeight.BOLD)],
			alignment=ft.MainAxisAlignment.CENTER,
			spacing = 0
		)
		e.control.gradient.colors.reverse()
		page.update()

		# 로직 실행
		r2_container.content.value 

	

	# 시작 버튼 클릭 ==> 애니메이션 2부(원래크기)
	def start_btn_animation_end(e: ft.ControlEvent):
		e.control.scale = 1
		e.control.gradient.colors.reverse()
		#e.control.disabled = True
		page.update()
		

	# 변수 초기화 시작
	reason = None
	choice = 0
	preset_reasons = ["", "신규, 저당 등 업무대상자 확인", "이전, 변경 등 업무대상자 확인", "압류, 말소 등 업무대상자 확인", "소유자 확인", "직접 입력"]


	# 설정 파일이 있으면 "직접 입력한 사유"를 Textfield에 입력
	if os.path.exists("C:\sickntired.cfg") == True:
		with open("C:\sickntired.cfg", "r") as f:
			r3_container.content.value = f.read()

	







	# Part1. 최상단 AppBar (조회사유를 선택하세요)
	page.appbar = ft.AppBar(
		leading=ft.Icon(ft.icons.ANDROID_OUTLINED, size=80, color=ft.colors.GREEN_600, opacity=0.8),
		automatically_imply_leading=True,
		leading_width=40,
		
		title=ft.Column(controls=[
			ft.Text(" 자동으로 입력하실", font_family='Malgun Gothic', size=11, weight=ft.FontWeight.NORMAL, color=ft.colors.WHITE, opacity=1),
			ft.Text("조회사유를 선택하세요", font_family='Malgun Gothic', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, opacity=1),
		], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
		center_title=True,
		bgcolor="#59bdd5",
		toolbar_height=60,

		actions=[ft.IconButton(ft.icons.SETTINGS, icon_size=30, icon_color=ft.colors.BLACK54, tooltip="개발자 정보", on_click=dev_info, data="dev_info")]
	)	
	

	# Part2. 조회사유 Radiobutton 부분
	r2_container = ft.Container(
		content = ft.RadioGroup(
			content=ft.Column([
				ft.Radio(value="1", label="신규, 저당 등 업무대상자 확인", fill_color=ft.colors.LIGHT_BLUE_500, height=35),
				ft.Radio(value="2", label="이전, 변경 등 업무대상자 확인", fill_color=ft.colors.LIGHT_GREEN_600, height=35),
				ft.Radio(value="3", label="압류, 말소 등 업무대상자 확인", fill_color=ft.colors.DEEP_PURPLE_300, height=35),
				ft.Radio(value="4", label="소유자 확인", fill_color=ft.colors.PINK_200, height=35)],
				spacing=0, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
			on_change=radiogroup_changed),
		margin = 0,
		padding = ft.padding.only(left=30, right=30, top=-10, bottom=-5),
		alignment=ft.alignment.center
	)


	# Part3. 직접입력 부분
	# r3_container.content.value = "이전 사유 입력"
	r3_container = ft.Container(
		content = ft.TextField(label='직접 입력', width=230, text_size=14, bgcolor=ft.colors.TRANSPARENT, focused_bgcolor=ft.colors.AMBER_100, filled=True, dense=True,
			hint_text="(입력하신 내용은 자동으로 저장됩니다)", hint_style=ft.TextStyle(size=11, color=ft.colors.TEAL_300),
			on_focus=textfield_focused, on_change=textfield_changed,
		),
		padding = ft.padding.only(left=40, right=40, top=0, bottom=5),
		margin = 0,
		alignment=ft.alignment.center
	)


	# Part4. 시작 버튼 부분
	r4_container = ft.Container(
		# content = ft.FilledButton(icon=ft.icons.PLAY_ARROW_ROUNDED, text="시작", width=250),
		content = ft.Container(
			content = ft.Row([
				ft.Icon(ft.icons.PLAY_ARROW_ROUNDED, size=50),
				ft.Text("시작   ", size=30, weight=ft.FontWeight.BOLD)],
				alignment=ft.MainAxisAlignment.CENTER,
				spacing = 0,
			),
			width = 240,
			height = 70,
			bgcolor = ft.colors.LIGHT_BLUE_500,
			gradient = ft.LinearGradient(
				begin = ft.alignment.top_left,
				end = ft.alignment.bottom_right,
				colors = [ft.colors.LIGHT_BLUE_800, ft.colors.LIGHT_GREEN_300, ft.colors.DEEP_PURPLE_300, ft.colors.PINK_ACCENT_200]
			),
			border_radius=5,
			ink = True,
			margin = 0,
			alignment= ft.alignment.center,
			
			#on_hover=
			scale=ft.transform.Scale(scale=1),
			animate_scale=ft.animation.Animation(250, ft.AnimationCurve.EASE_IN_OUT_BACK),
			on_animation_end=start_btn_animation_end,
			
			on_click=start_btn_animation_start,
			data="start"
		),
		padding = ft.padding.only(left=30, right=30),
		#expand=True,
		alignment=ft.alignment.center
	)


	page.add(r2_container, r3_container, r4_container)
	

ft.app(target=main, view=ft.FLET_APP_HIDDEN)