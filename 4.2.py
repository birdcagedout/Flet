import flet as ft
import os
import math
import time
import random
import logging
import ctypes
import pickle
from threading import *
import win32gui
from pynput import mouse as pynputMouse
from pynput import keyboard as pynputKeyboard


VER_MAJOR = "4"
VER_MINOR = "2"
VER = VER_MAJOR + "." + VER_MINOR


WIN_WIDTH = 350
WIN_HEIGHT = 420


HOME_DIR = r"C:\SickNTired"
SETTING_FILE = HOME_DIR + r"\sickntired.cfg"
LOG_FILE = HOME_DIR + r"\sickntired.log"


SUPERSPEED_DELAY = 0.1		# 작동 지연값(슈퍼스피드 모드 ON=0.1)
NORMALSPEED_DELAY = 0.3		# 작동 지연값(슈퍼스피드 모드 OFF=0.3)

DAY_NIGHT_PERIOD = 1.5		# 작동 중: 낮/밤 테마 바뀌는 주기
DAY_NIGHT_STEP = 0.1		# 작동 중: loop에서 한번 time.sleep()하는 시간

# 현재 컴퓨터의 IP 확인
# import socket
# print(socket.gethostbyname(socket.gethostname()))


# 현재 SCREEN의 실제 해상도 찾기
#import ctypes
#user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()		# 이 부분을 제외하면 배율이 1보다 클 때 낮은 해상도가 나온다(ex. 배율=1.25일때 3840/1.25 = 3072)
#[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


# 작업표시줄 height
#import win32api, ctypes
#user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()
#tray_height = win32api.GetSystemMetrics(1) - win32api.GetSystemMetrics(62)		# 4K모니터에서 42/ FHD모니터에서 24


# 인트로 스플래시 이미지 닫기(python3.9부터 importlib --> importlib.util로 바뀜)
#import importlib.util
#if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
#	import pyi_splash
#	#pyi_splash.update_text('UI Loaded ...')
#	pyi_splash.close()




# 타이머 
class Timer(ft.UserControl):
	def __init__(self, seconds, page: ft.Page):
		super().__init__()
		self.seconds = seconds
		self.page = page
		self.colors = [
			#ft.colors.WHITE,
			ft.colors.RED,
			ft.colors.PINK,
			ft.colors.PURPLE,
			ft.colors.DEEP_PURPLE,
			ft.colors.INDIGO,
			ft.colors.BLUE,
			ft.colors.LIGHT_BLUE,
			ft.colors.CYAN,
			ft.colors.TEAL,
			ft.colors.GREEN,
			ft.colors.LIGHT_GREEN,
			ft.colors.LIME,
			ft.colors.YELLOW,
			ft.colors.AMBER,
			ft.colors.ORANGE,
			ft.colors.DEEP_ORANGE,
			ft.colors.BROWN,
			# ft.colors.BLUE_GREY,
			ft.colors.RED_ACCENT,
			# ft.colors.PINK_ACCENT,
			ft.colors.PURPLE_ACCENT,
			# ft.colors.DEEP_PURPLE_ACCENT,
			# ft.colors.INDIGO_ACCENT,
			# ft.colors.BLUE_ACCENT,
			ft.colors.LIGHT_BLUE_ACCENT,
			# ft.colors.CYAN_ACCENT,
			# ft.colors.TEAL_ACCENT,
			# ft.colors.GREEN_ACCENT,
			# ft.colors.LIGHT_GREEN_ACCENT,
			# ft.colors.LIME_ACCENT,
			# ft.colors.YELLOW_ACCENT,
			ft.colors.AMBER_ACCENT,
			# ft.colors.ORANGE_ACCENT,
			# ft.colors.DEEP_ORANGE_ACCENT,
		]
		self.page.padding = ft.padding.all(0)
		self.page.spacing = 0
		self.page.theme_mode = ft.ThemeMode.LIGHT
		self.page.update()

		self.vertical_space_left = 381							# 주의: WIN_HEIGHT = 420일 때 380.8 ==> 380이면 1px 모자람
		self.stripes = []
		self.heights = []
		self.running = False
		random.seed()

	def did_mount(self):
		self.thread = Thread(target=self.update_timer, args=(), daemon=True)
		self.thread.start()
		self.running = True

	def will_unmount(self):
		self.running = False

	def update_timer(self):
		# 가로줄 높이 배정(높이 = 랜덤 10 ~ 90)
		while self.vertical_space_left > 0:

			h = random.randint(5, 15) * random.randint(2, 4)		# random.randint(a, b) includes both ends
			if (self.vertical_space_left - h) >= 0:
				self.vertical_space_left -= h
			else:
				h = self.vertical_space_left
				self.vertical_space_left = 0
			self.heights.append(h)
			
			# 가로줄의 개수가 color 개수보다 크면 처음부터 다시 가로줄 배정
			if self.vertical_space_left == 0 and len(self.heights) > len(self.colors):
				self.vertical_space_left = 381
				self.heights.clear()
				continue
		
		# 가로줄 개수만큼 컬러 배정
		c = random.sample(self.colors, len(self.heights))

		# 화면에 추가
		for i in range(len(self.heights)):
			self.stripes.append(ft.ProgressBar(width=self.page.width, height=self.heights[i], opacity=1, rotate=ft.Rotate(angle= math.pi * (i % 2)), color=c[i], bgcolor=ft.colors.TRANSPARENT))
			self.page.add(self.stripes[i])
			time.sleep(0.1 * random.randint(1, 3))
		
		# 정해진 시간이 되면 ft.ThemeMode를 서로 바꾼다
		seconds_left = self.seconds
		while (seconds_left > 0) and (self.running == True):
			time.sleep(DAY_NIGHT_STEP)
			seconds_left -= DAY_NIGHT_STEP
			
			if seconds_left <= 0:
				self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
				self.page.update()
				seconds_left = self.seconds

	def build(self):
		return ft.Container()		# 더미 Control 하나 던져준다





class WatcherThread(Thread):
	# 초기화
	def __init__(self, reason="", delay=SUPERSPEED_DELAY):
		super(WatcherThread, self).__init__(daemon=True)
		self.reason = reason
		self.delay = delay
		self.m = pynputMouse.Controller()
		self.k = pynputKeyboard.Controller()

	# 쓰레드 시작
	def run(self):

		# 이미 팝업창이 떠 있는 상태에서 실행된 경우 ==> 최상위 윈도가 현재 "귀찮다"이므로 팝업창 감지 안됨
		# 따라서 쓰레드 실행시 팝업창이 있다면 최상위로 올려주어 감지
		def winEnumHandler(hWnd, ctx):
			if win32gui.IsWindowVisible(hWnd):
				title = win32gui.GetWindowText(hWnd)
				if ("조회 사유 입력" in title) or ("개인정보 공개 열람사유입력" in title):
					# weird solution : SetForegroundWindow 전에 alt키 눌러야 동작한다.
					self.k.press(pynputKeyboard.Key.alt)
					self.k.release(pynputKeyboard.Key.alt)
					win32gui.SetForegroundWindow(hWnd)
		win32gui.EnumWindows(winEnumHandler, None)

		while True:
			# 팝업창 Title 찾기
			try:
				hWnd = win32gui.GetForegroundWindow()
				title = win32gui.GetWindowText(hWnd)
				rect = win32gui.GetWindowRect(hWnd)
				x = rect[0]
				y = rect[1]
				w = rect[2] - x
				h = rect[3] - y
			except Exception:
				time.sleep(0.1)
				continue

			# 둘 다 아닌 경우
			if (title != "조회 사유 입력") and (title != "개인정보 공개 열람사유입력"):
				time.sleep(0.1)
				continue

			# 조회 사유 입력창이 맞지만, 아직 창이 만들어지기도 전에 detect된 경우 ==> 기다려준다
			if w < 100:
				#print(f"[창이 너무 작습니다] x={x}, y={y}, w={w}, h={h}")
				time.sleep(0.1)
				continue
				
			# <경고: 입력장치 무력화 시작>=========================================================
			# 조회사유 입력 시작: 클릭 + 사유 입력
			ctypes.windll.user32.BlockInput(True)				# 마우스/키보드 입력 차단

			# 둘 중 하나는 발견한 경우: 너무 빠르니까 작동오류 발생 ==> 지연시간 추가: time.sleep(self.delay)
			# BUT 창이 제대로 만들어진 경우(w=386, h=246) 굳이 기다릴 필요가 없지만 ==> 다이얼로그에 Edit Control이 정상 작동할 수 있도록 0.1초만 기다림
			time.sleep(self.delay)

			(xPos, yPos) = self.m.position
			self.m.position = (x + int(w/2), y + int(h/2))
			self.m.click(pynputMouse.Button.left, 1)
			self.k.type(self.reason)
			time.sleep(0.1)
			self.k.press(pynputKeyboard.Key.enter)
			self.k.release(pynputKeyboard.Key.enter)
			self.m.position = (xPos, yPos)
			ctypes.windll.user32.BlockInput(False)				# 마우스/키보드 입력 차단 해제
			# 조회사유 입력 끝
			# <경고: 입력장치 무력화 끝>=========================================================
			

			###############################################################################
			# 창이 닫히지 않았는지 확인 ==> 닫히지 않았다면 문제 발생한 것
			time.sleep(1)
			try:
				hWnd = win32gui.GetForegroundWindow()
				title = win32gui.GetWindowText(hWnd)
				rect = win32gui.GetWindowRect(hWnd)
				x2 = rect[0]
				y2 = rect[1]
				w2 = rect[2] - x2
				h2 = rect[3] - y2
			except Exception:
				time.sleep(0.1)
				pass

			if (title == "조회 사유 입력") or (title == "개인정보 공개 열람사유입력"):
				# 로그 저장
				logger = logging.getLogger()
				logger.setLevel(logging.ERROR)
				formatter = logging.Formatter('%(asctime)s - %(message)s')
				file_handler = logging.FileHandler(LOG_FILE)
				file_handler.setFormatter(formatter)
				logger.addHandler(file_handler)
				logger.debug(f"[에러] 창 안닫힘: x={x}, y={y}, w={w}, h={h} ==> x2={x2}, y2={y2}, w2={w2}, h2={h2}\n")
			# 확인 끝
			###############################################################################

			time.sleep(1)


#=====================================================================================================================================================
# Flet App: Entry Point
def main(page: ft.Page):
	page.title = f"귀찮다 v{VER}"
	page.window_width = WIN_WIDTH
	page.window_height = WIN_HEIGHT
	page.window_maximizable = False
	page.window_minimizable = True
	page.window_resizable = False
	#page.padding = 15
	page.padding = 0
	#page.spacing = 10
	page.spacing = 0
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window_center()
	page.window_visible = True
	page.update()



	#=====================================================================================================================================================
	# 초기화 시작
	choice = None
	reason = None
	preset_reasons = ["", "신규 저당 등 업무대상자 확인", "이전 변경 등 업무대상자 확인", "압류 말소 등 업무대상자 확인", "소유자 확인", ""]

	setting_autosave = True					# 설정 자동 저장 여부
	setting_minimize = True					# 작동 후 최소화 여부
	setting_transparency = 0.0				# 투명도 값
	setting_superspeed = True 				# 슈퍼스피드 모드
	setting_delay = SUPERSPEED_DELAY		# 작동 지연값(슈퍼스피드 모드 ON=0.1, OFF=0.35)

	car_system_launched = False

	# "자동차(이륜차)관리정보시스템" 윈도 찾기
	def check_car_system():
		def winEnumHandler(hWnd, ctx):
			if win32gui.IsWindowVisible(hWnd):
				title = win32gui.GetWindowText(hWnd)
				if "자동차관리정보시스템" in title or "이륜차관리정보시스템" in title:
					nonlocal car_system_launched
					car_system_launched = True
		win32gui.EnumWindows(winEnumHandler, None)


	# 설정 파일이 있으면 로딩
	if os.path.exists(SETTING_FILE) == True:
		with open(SETTING_FILE, "rb") as f:
			setting = pickle.load(f)

			# 사유/설정 자동저장값이 True일 때만 설정파일 반영
			if setting['setting_autosave'] == True:
				setting_autosave = setting['setting_autosave']
				setting_minimize = setting['setting_minimize']
				setting_transparency = setting['setting_transparency']
				setting_delay = setting['setting_delay']
				choice = setting['setting_choice']
				preset_reasons[5] = setting['setting_reason']

				try:
					setting_superspeed = setting['setting_superspeed']
					setting_delay = SUPERSPEED_DELAY if setting_superspeed == True else NORMALSPEED_DELAY
				except KeyError:
					setting_superspeed = True
					setting_delay = SUPERSPEED_DELAY
	# 초기화 끝
	#=====================================================================================================================================================


	#=====================================================================================================================================================
	# Setting 버튼 클릭시 이벤트 핸들러
	def on_setting(e: ft.ControlEvent):

		# 설정1 - 조회사유 자동저장 (switch)
		def switch_autosave(e: ft.ControlEvent):
			nonlocal setting_autosave
			setting_autosave = e.control.value		# OFF로 바뀌면 False, ON으로 바뀌면 True
			if e.control.value == True:
				r3_container.content.hint_text = "(입력하신 내용은 자동으로 저장됩니다)"
			else:
				r3_container.content.hint_text = "(입력하신 내용은 저장되지 않습니다)"

		# 설정2 - 작동 후 최소화 여부 (switch)
		def switch_minimize(e: ft.ControlEvent):
			nonlocal setting_minimize
			setting_minimize = e.control.value		# ON: 작동 후 창을 최소화
		
		# 설정3 - 투명도 조절 (slider)
		def slider_transparency(e: ft.ControlEvent):
			if e.control.value is None:
				e.control.value = 0
			
			nonlocal setting_transparency
			setting_transparency = round(e.control.value / 100, 1)
			page.window_opacity = round(1 - setting_transparency, 1)
			# print(f"e.control.value: {e.control.value}, setting_transparency: {setting_transparency}, page.window_opacity: {page.window_opacity}")
			page.update()

		# 설정4 - 슈퍼스피드 모드 (checkbox)
		def checkbox_delay(e: ft.ControlEvent):
			nonlocal setting_superspeed
			nonlocal setting_delay
			if e.control.value == True:
				setting_superspeed = True
				setting_delay = SUPERSPEED_DELAY
			else:
				setting_superspeed = False
				setting_delay = NORMALSPEED_DELAY
		
		# 확인 버튼 
		def dlg_ok(e: ft.ControlEvent):
			nonlocal dlg_setting
			dlg_setting.open = False
			page.update()

		# "설정" 클릭시 modal dialog (2개의 tab)
		dlg_setting = ft.AlertDialog(
			modal = True,
			shape=ft.RoundedRectangleBorder(radius=5),
			title_padding= ft.padding.all(0),
			content_padding=ft.padding.only(left=25, right=25, top=20, bottom=0),
			actions_padding=ft.padding.only(left=33, right=33, top=0, bottom=20),

			content=ft.Tabs(
				selected_index=0,
				animation_duration=200,
				tabs=[
					ft.Tab(
						text="설정  ",
						icon=ft.icons.TUNE_OUTLINED,
						content=ft.Column([
							ft.Container(content= ft.Switch(label="  사유/설정 자동저장", value=setting_autosave, tooltip="조회사유와 설정값을 자동으로 저장합니다", on_change=switch_autosave), padding=ft.padding.only(top=5)),
							ft.Container(content=ft.Switch(label="  작동 후 창 최소화", value=setting_minimize, tooltip="작동 후 창을 최소화합니다", on_change=switch_minimize), padding=ft.padding.only(top=5)),
							ft.Container(content=ft.Row([
								ft.Text("  투명도", text_align=ft.TextAlign.START, tooltip="투명도: 0% ~ 90%", expand=4),
								ft.Slider(min=0, max=90, divisions=9, label="{value}%", value=int(setting_transparency*100), on_change_start=slider_transparency, on_change=slider_transparency, expand=10),
	       					], spacing=0, expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=ft.padding.only(top=0, bottom=-5),
							),
						    ft.Container(content=ft.Row([
								ft.Checkbox(label="슈퍼스피드 모드", value=setting_superspeed, tooltip="슈퍼스피드 모드: 동작지연 0.1초\n노멀스피드 모드: 동작지연 0.3초", on_change=checkbox_delay)
								#ft.Text("  동작지연", text_align=ft.TextAlign.START, tooltip="똥컴일수록 큰값으로 설정", expand=5),
								#ft.Slider(min=0.3, max=0.45, divisions=3, label="{value}", value=setting_delay, on_change_start=slider_delay, on_change=slider_delay, expand=10),
	       					], spacing=0, expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=ft.padding.only(top=0, bottom=0),
							),
						], spacing=0, tight=True, alignment=ft.MainAxisAlignment.CENTER),
					),
					ft.Tab(
						text="정보  ",
						icon=ft.icons.INFO,
						content=ft.Column([
							ft.Container(content=ft.Text(f"귀찮다 v{VER}", weight=ft.FontWeight.BOLD, size=30, text_align=ft.TextAlign.CENTER), alignment=ft.alignment.center),
							ft.Container(content=ft.Text("   노원구청 교통행정과\n   김재형 © 2022-2023\n       무단배포 대환영!\n", size=17, text_align=ft.TextAlign.CENTER), alignment=ft.alignment.bottom_center),
						], alignment=ft.MainAxisAlignment.SPACE_AROUND, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
					),
				],
				expand=True,
			),
			actions=[
				ft.ElevatedButton("확인", icon=ft.icons.DONE_SHARP, icon_color=ft.colors.GREEN_400, on_click=dlg_ok)
        	],
        	actions_alignment=ft.MainAxisAlignment.END,
		)
		page.dialog = dlg_setting
		dlg_setting.open = True
		page.update()
	#=< on_setting() 끝 >====================================================================================================================================================
	

	# RadioButton 선택시 이벤트 핸들러
	def radiogroup_changed(e: ft.ControlEvent):
		nonlocal choice
		choice = int(e.control.value)
		#print(r2_container.content.value)
		colors = [ft.colors.WHITE, ft.colors.LIGHT_BLUE_500, ft.colors.LIGHT_GREEN_600, ft.colors.DEEP_PURPLE_300, ft.colors.PINK_200]
		page.snack_bar = ft.SnackBar(ft.Row([ft.Text(f"{preset_reasons[choice]}", size=12.5, color=colors[choice], weight=ft.FontWeight.BOLD), ft.Text("을 선택하셨습니다", size=12.5)], spacing=0))
		page.snack_bar.open = True
		page.update()
	

	# Textfield 커서 받을 때 이벤트 핸들러 (텍스트필드의 값 = e.control.value = r2_container.content.value)
	def textfield_focused(e: ft.ControlEvent):
		nonlocal choice
		choice = 5
		r2_container.content.value  = str(choice)

		if preset_reasons[5].strip() == "":			# 입력했다가 모두 지웠거나, 공백문자만 입력한 경우 ==> "직접 입력"으로 바꾸기
			r3_container.content.value = ""
			page.snack_bar = ft.SnackBar(ft.Row([ft.Text(f"직접 입력", size=12.5, color=ft.colors.YELLOW, weight=ft.FontWeight.BOLD), ft.Text("을 선택하셨습니다", size=12.5)], spacing=0))
		else:
			r3_container.content.value = preset_reasons[5]
			page.snack_bar = ft.SnackBar(ft.Row([ft.Text(f"{preset_reasons[choice]}", size=12.5, color=ft.colors.YELLOW, weight=ft.FontWeight.BOLD), ft.Text("을(를) 선택하셨습니다", size=12.5)], spacing=0, wrap=True))
		page.snack_bar.open = True
		page.update()


	# Textfield 변경될 때 이벤트 핸들러
	def textfield_changed(e: ft.ControlEvent):
		preset_reasons[5] = e.control.value.strip()
		#print(preset_reasons)


	#========================================================================================================
	# 시작 버튼 hover: in=1.1배 커짐 / out=원래대로
	def start_btn_hover(e: ft.ControlEvent):
		# hover in
		if e.data == 'true':
			e.control.scale = 1.1
		# hover out
		else:
			e.control.scale = 1
		e.control.gradient.colors.reverse()
		e.control.update()


	#========================================================================================================
	# 시작 버튼 클릭 ==> 애니메이션(1.2배 커졌다가 1배로 작아짐)
	def start_btn(e: ft.ControlEvent):

		# 자동차/이륜차 시스템 실행되지 않은 경우
		check_car_system()
		def dlg_alert_carsystem(e: ft.ControlEvent):
			dlg_alert_carsystem.open = False
			page.update()
		
		if car_system_launched == False:
			dlg_alert_carsystem = ft.AlertDialog(
				modal=True,
				title=ft.Row([
					ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_600, size=35),
					ft.Text("실행 전에", size=25),
					ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_600, size=35),
				], spacing=5, alignment=ft.MainAxisAlignment.START),
				title_padding=ft.padding.only(top=24, left=24, right=24, bottom=0),

				content=ft.Text("자동차 관리정보시스템을\n먼저 실행해주세요.", size=16),
				content_padding=ft.padding.only(top=20, left=24, right=24, bottom=24),

				actions=[ft.TextButton("돌아가기", on_click=dlg_alert_carsystem)],
				actions_padding=ft.padding.only(top=0, left=24, right=24, bottom=20),
				actions_alignment=ft.MainAxisAlignment.END,
			)
			page.dialog = dlg_alert_carsystem
			dlg_alert_carsystem.open = True
			page.update()
			return


		# 아무것도 선택하지 않은 경우
		def dlg_alert_noneselected_close(e: ft.ControlEvent):
			dlg_alert_noneselected.open = False
			page.update()
		
		if choice == None:
			dlg_alert_noneselected = ft.AlertDialog(
				modal=True,
				title=ft.Row([
					ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_600, size=35),
					ft.Text("조회사유는", size=25, weight=ft.FontWeight.BOLD),
					ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_600, size=35),
				], spacing=0, alignment=ft.MainAxisAlignment.START),
				title_padding=ft.padding.only(top=24, left=24, right=24, bottom=0),

				content=ft.Text("필수 입력 사항입니다.\n다시 선택해주세요.", size=16),
				content_padding=ft.padding.only(top=20, left=24, right=24, bottom=24),

				actions=[ft.TextButton("돌아가기", on_click=dlg_alert_noneselected_close)],
				actions_padding=ft.padding.only(top=0, left=24, right=24, bottom=20),
				actions_alignment=ft.MainAxisAlignment.END,
			)
			page.dialog = dlg_alert_noneselected
			dlg_alert_noneselected.open = True
			page.update()
			return
		 
		
		# "직접 입력" 선택시 4글자 이상인지 확인
		def dlg_alert_short_close(e: ft.ControlEvent):
			dlg_alert_short.open = False
			page.update()
			r3_container.content.focus()
		
		if choice == 5:
			if len(r3_container.content.value.strip()) < 4:
				dlg_alert_short = ft.AlertDialog(
					modal=True,
					title=ft.Row([
						ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_600, size=35),
						ft.Text("조회사유는", size=25, weight=ft.FontWeight.BOLD),
						ft.Icon(ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_600, size=35),
					], spacing=0, alignment=ft.MainAxisAlignment.START),
					title_padding=ft.padding.only(top=24, left=24, right=24, bottom=0),

					content=ft.Text("4글자 이상이어야 합니다.\n다시 입력해주세요.", size=16),
					content_padding=ft.padding.only(top=20, left=24, right=24, bottom=24),

					actions=[ft.TextButton("돌아가기", on_click=dlg_alert_short_close)],
					actions_alignment=ft.MainAxisAlignment.END,
					actions_padding=ft.padding.only(top=0, left=24, right=24, bottom=20),
				)
				page.dialog = dlg_alert_short
				dlg_alert_short.open = True
				page.update()
				return
				

		# 버튼 비활성화
		e.control.disabled = True

		
		# 사유 입력: choice는 무조건 1 ~ 5
		nonlocal reason
		reason = preset_reasons[choice]


		# 설정/사유 저장(setting_autosave==True)
		if setting_autosave == True:
			# 폴더가 없으면 만들고
			if os.path.isdir(HOME_DIR) == False:
				os.mkdir(HOME_DIR)
			# 파일 쓰기
			with open(SETTING_FILE, "wb") as f:
				setting = { 'setting_version': VER,
							'setting_autosave': setting_autosave,
							'setting_minimize': setting_minimize, 
							'setting_transparency': setting_transparency,
							'setting_superspeed': setting_superspeed,
							'setting_delay': setting_delay,
							'setting_choice': choice, 
							'setting_reason': preset_reasons[5]}
				pickle.dump(setting, f)
		# 설정/사유 저장(setting_autosave==False)
		else:
			if os.path.exists(SETTING_FILE) == True:
				os.remove(SETTING_FILE)


		# 버튼 애니메이션 1부
		e.control.scale = 1.2
		e.control.content = ft.Row([
		 	ft.Icon(ft.icons.ROCKET_LAUNCH_SHARP, size=40, rotate=math.pi*(-0.25)),
		 	ft.Text("뾰로롱~", size=30, weight=ft.FontWeight.BOLD)],
		 	alignment=ft.MainAxisAlignment.CENTER,
		 	spacing = 0
		 )
		e.control.gradient.colors.reverse()
		page.update()
		time.sleep(0.3)


		# 버튼 애니메이션 2부
		e.control.scale = 1
		e.control.gradient.colors.reverse()
		page.update()
		time.sleep(0.3)

		# 화면 없애고 "작동중"
		page.appbar = None
		page.clean()
		page.update()
		page.add(Timer(DAY_NIGHT_PERIOD, page))
		page.overlay.append(ft.Container(content=ft.Text("작동 중", size=80, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center))

		# 쓰레드 시작
		worker = WatcherThread(reason=reason, delay=setting_delay)
		worker.start()

		# 작동 후 최소화
		if setting_minimize == True:
			page.window_minimized = True
			page.update()
		
		

	# Part1. 최상단 AppBar (조회사유를 선택하세요)
	r1_appbar = ft.AppBar(
		leading=ft.Icon(ft.icons.ANDROID_OUTLINED, size=80, color=ft.colors.GREEN_600, opacity=1),
		leading_width=40,
		
		title=ft.Column(
			controls=[
			ft.Text(" 자동으로 입력하실", font_family='Malgun Gothic', size=11, weight=ft.FontWeight.NORMAL, color=ft.colors.WHITE),
			ft.Text("조회사유를 선택하세요", font_family='Malgun Gothic', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
			], 
			spacing=2, 
			alignment=ft.MainAxisAlignment.CENTER
		),
		center_title=True,
		bgcolor="#59bdd5",
		toolbar_height=58,

		actions=[
			ft.Container(
				content=ft.Row([
					ft.IconButton(ft.icons.SETTINGS, icon_size=30, icon_color=ft.colors.BLACK54, tooltip="설정",  on_click=on_setting), 
					ft.Text("", size=1)
				],
				spacing=5)
			)
		]
	)

	# Part1.5 Appbar 하단에 shadow 추가
	r1_appbar_shdow = ft.Column([
		ft.Divider(height=1, color=ft.colors.BLACK45),
		ft.Divider(height=1, color=ft.colors.BLACK38),
		ft.Divider(height=1, color=ft.colors.BLACK26),
		ft.Divider(height=1, color=ft.colors.BLACK12)
		],
		spacing=0
	)

	

	# Part2. 조회사유 Radiobutton 부분
	r2_container = ft.Container(
		content = ft.RadioGroup(
			content=ft.Column([
				ft.Radio(value="1", label="신규 저당 등 업무대상자 확인", fill_color=ft.colors.LIGHT_BLUE_500, height=30),
				ft.Radio(value="2", label="이전 변경 등 업무대상자 확인", fill_color=ft.colors.LIGHT_GREEN_600, height=30),
				ft.Radio(value="3", label="압류 말소 등 업무대상자 확인", fill_color=ft.colors.DEEP_PURPLE_300, height=30),
				ft.Radio(value="4", label="소유자 확인", fill_color=ft.colors.PINK_200, height=30)],
				spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
			value=choice, on_change=radiogroup_changed),
		margin = 0,
		padding = ft.padding.only(left=45, right=45, top=9, bottom=5),
		alignment=ft.alignment.center
	)


	# Part3. 직접입력 부분
	# r3_container.content.value = "이전 사유 입력"
	r3_container = ft.Container(
		content = ft.TextField(label='직접 입력', label_style=ft.TextStyle(size=14), width=230, text_size=13, bgcolor="#fef0c8", focused_bgcolor=ft.colors.AMBER_200, border=ft.InputBorder.OUTLINE, border_color=ft.colors.AMBER_500, border_radius=5, filled=True, dense=True,
			hint_text="(입력하신 내용은 자동으로 저장됩니다)", hint_style=ft.TextStyle(size=11.5, color=ft.colors.WHITE70),
			value=preset_reasons[5],
			on_focus=textfield_focused,
			on_change=textfield_changed
		),
		padding = ft.padding.only(left=40, right=40, top=0, bottom=5),
		margin = 0,
		alignment=ft.alignment.center
	)


	# Part4. 시작 버튼 부분
	r4_container = ft.Container(
		content = ft.Row([
				ft.Icon(ft.icons.ROCKET_SHARP, size=40),
				ft.Text("시작  ", size=30, weight=ft.FontWeight.BOLD)
				],
				alignment=ft.MainAxisAlignment.CENTER,
				spacing = 0,
			),
		gradient = ft.LinearGradient(
			begin = ft.alignment.top_left,
			end = ft.alignment.bottom_right,
			colors = [ft.colors.LIGHT_BLUE_900, ft.colors.LIGHT_GREEN_500, ft.colors.DEEP_PURPLE_400, ft.colors.PINK_ACCENT_400]
		),
		#border=ft.border.only(right=ft.BorderSide(width=2, color=ft.colors.BLACK26), bottom=ft.BorderSide(width=2, color=ft.colors.BLACK26)),
		#border=ft.border.all(width=1, color=ft.colors.YELLOW),
		border_radius=5,
		ink = True,
		margin = ft.margin.only(left=40, right=40, top=7, bottom=3),
		expand=True,
		
		scale=ft.transform.Scale(scale=1),
		animate_scale=ft.animation.Animation(250, ft.AnimationCurve.EASE_IN_OUT_BACK),
		on_click=start_btn,
		on_hover=start_btn_hover,
		
		data="start",
		alignment= ft.alignment.center,
	)

	# Part5. 개발자 정보 맨밑 한줄
	r5_container = ft.Container(
		content=ft.Text("Developed by 김재형, 2022-2023", size=12),
		alignment=ft.alignment.center_right,
		margin = ft.margin.only(left=40, right=40, top=3, bottom=20),
	)

	page.appbar = r1_appbar
	page.add(r1_appbar_shdow, r2_container, r3_container, r4_container, r5_container)

	if choice == 5:
		r3_container.content.focus()
	

ft.app(target=main, view=ft.FLET_APP_HIDDEN)