import win32gui
import time
from pynput import mouse as pynputMouse
from pynput import keyboard as pynputKeyboard


m = pynputMouse.Controller()
k = pynputKeyboard.Controller()

title_list = []

def winEnumHandler(hWnd, ctx):
	if win32gui.IsWindowVisible(hWnd):
		title = win32gui.GetWindowText(hWnd)
		if title != '' and 'Visual Studio Code' not in title and '검색어자동완성_Open' not in title and 'Microsoft Text Input Application' not in title and 'Program Manager' not in title and '노원다이어리 UC메신저' not in title and '저공해차량' not in title and '귀찮다' not in title and '새올' not in title:
			title_list.append(title)

		# 갑부에서 말소차량 리스트 ==> 맨위 차량 선택 + 엔터
		#if title == '갑부열람차량관리번호':
		#	k.press(pynputKeyboard.Key.enter)
		#	k.release(pynputKeyboard.Key.enter)

while True:
	win32gui.EnumWindows(winEnumHandler, None)
	print(title_list)
	title_list = []
	print('----------------------------------------------')
	time.sleep(1)


# 갑부 말소차량 중 고르기: '갑부열람차량관리번호'
