import win32gui, win32api, win32con
import time
from pynput import mouse as pynputMouse
from pynput import keyboard as pynputKeyboard


m = pynputMouse.Controller()
k = pynputKeyboard.Controller()

title_list = []
target_hWnd = None
child_hWnd = [] 
child_class_list = []
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
		#if title == '다운로드 사유 입력':
			global target_hWnd
			target_hWnd = hWnd




def childEnumHandler(hWnd, ctx):
	child_hWnd.append(hWnd)
	child_title = win32gui.GetWindowText(hWnd)
	child_title_list.append(child_title)
	child_class = win32gui.GetClassName(hWnd)
	child_class_list.append(child_class)

#	if child_title == "저장":
#		rect = win32gui.GetWindowRect(hWnd)
#		x = rect[0]
#		y = rect[1]
#		w = rect[2] - x
#		h = rect[3] - y
#		pos_x = x + int(w/2)
#		pos_y = y + int(h/2)
#		m.position = (pos_x, pos_y)
#		m.click(pynputMouse.Button.left, 1)
	
	
#	if child_title == "확인":
#		rect = win32gui.GetWindowRect(hWnd)
#		x = rect[0]
#		y = rect[1]
#		w = rect[2] - x
#		h = rect[3] - y
#		pos_x = x + int(w/2)
#		pos_y = y + int(h/2)
#		m.position = (pos_x, pos_y)
#		m.click(pynputMouse.Button.left, 1)


	
	#buf = " " * 255
	#buf_len = win32gui.SendMessage(hWnd, win32con.WM_GETTEXT, 255, buf)
	#child_title = buf[:buf_len]
	#child_title_list.append(child_title)
	

# 엑셀 다운로드: '다운로드 사유 입력' (엔터로 창 안 닫힘)
# 	

while True:
	win32gui.EnumWindows(winEnumHandler, None)
	print(title_list)
	title_list = []
	print('----------------------------------------------')

	if target_hWnd != None:
		win32gui.EnumChildWindows(target_hWnd, childEnumHandler, None)
	
	for i in range(len(child_hWnd)):
		print(f"[{i}] HWND: {child_hWnd[i]}\tCLASSNAME: {child_class_list[i]}\tTITLE: {child_title_list[i]}")
	print('==============================================')
	child_hWnd = []
	child_title_list = []
	time.sleep(1)


# 갑부 말소차량 중 고르기: '갑부열람차량관리번호'
