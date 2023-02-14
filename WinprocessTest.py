import win32gui, win32con

FOUND = False

# 현재 (보이는 윈도 중에서) 원하는 윈도 찾기 : "자동차관리정보시스템" 문자열 포함
def get_target_win():
	def winEnumHandler(hWnd, ctx):
		if win32gui.IsWindowVisible(hWnd):
			title = win32gui.GetWindowText(hWnd)
			if "자동차관리정보시스템" in title or "이륜차관리정보시스템" in title:
				global FOUND
				FOUND = True
	return win32gui.EnumWindows(winEnumHandler, None)

if __name__ == "__main__":
	get_target_win()
	if FOUND== True:
		print("성공")