import win32gui, win32api, win32con
import time
from pynput import mouse as pynputMouse
from pynput import keyboard as pynputKeyboard


m = pynputMouse.Controller()
k = pynputKeyboard.Controller()

title_list = []
target_hWnd = None
child_hWnd = [] 
child_title_list = []

def winEnumHandler(hWnd, ctx):
	if win32gui.IsWindowVisible(hWnd):
		title = win32gui.GetWindowText(hWnd)

		if title != '' and 'Visual Studio Code' not in title and '검색어자동완성_Open' not in title and 'Microsoft Text Input Application' not in title and 'Program Manager' not in title and '노원다이어리 UC메신저' not in title and '저공해차량' not in title and '귀찮다' not in title and '새올' not in title:
			title_list.append(title)
		
		#if title == '오류':
		#	import win32api, win32com, win32con
		#	static_hwnd = win32gui.GetDlgItem(hWnd, 0x00FF)
		#	text = win32gui.GetWindowText(static_hwnd)
		#	print(text)

		# 갑부에서 말소차량 리스트 ==> 맨위 차량 선택 + 엔터
		#if title == '갑부열람차량관리번호':
		#	k.press(pynputKeyboard.Key.enter)
		#	k.release(pynputKeyboard.Key.enter)

		if title == '알림확인' or title =='오류':
			global target_hWnd
			target_hWnd = hWnd

def childEnumHandler(hWnd, ctx):
	child_hWnd.append(hWnd)
	child_title = win32gui.GetWindowText(hWnd)
	child_title_list.append(child_title)
	
	#buf = " " * 255
	#buf_len = win32gui.SendMessage(hWnd, win32con.WM_GETTEXT, 255, buf)
	#child_title = buf[:buf_len]
	#child_title_list.append(child_title)
	


while True:
	win32gui.EnumWindows(winEnumHandler, None)
	print(title_list)
	title_list = []
	print('----------------------------------------------')

	if target_hWnd != None:
		win32gui.EnumChildWindows(target_hWnd, childEnumHandler, None)
	
	for i in range(len(child_hWnd)):
		print(f"[{i}] {child_hWnd[i]}: {child_title_list[i]}")
	print('==============================================')
	child_hWnd = []
	child_title_list = []
	time.sleep(1)


# 갑부 말소차량 중 고르기: '갑부열람차량관리번호'
