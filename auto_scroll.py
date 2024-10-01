import pyautogui
import time


class AutoScroll():
    def myinit(self):
        self.acrive_browser()
    def go(self):
        # return self.auto_scroll_komiflo()
        return self.auto_scroll_dmm()
    def acrive_browser(self):
        # ブラウザをactiveに
        # pyautogui.moveTo(540, 5, duration=0.5)
        pyautogui.moveTo(700, 5, duration=0.5)
        pyautogui.click()
        # 中央に移動
        pyautogui.moveTo(540, 960, duration=0.5)
        time.sleep(0.5)

    def auto_scroll_komiflo(self):
        # 開始
        # 前準備
        self.acrive_browser()

    def auto_scroll_komiflo(self):
        self.get_screenshot()
        try:
            x, y = pyautogui.locateCenterOnScreen('tweet.png',confidence=0.5)
            try:
                # 最後のページか？
                x, y = pyautogui.locateCenterOnScreen('komi_end.png',confidence=0.5)
                # 終わる
                #self.event_button_auto(1)
                self.flag_auto = False
                self.get_screenshot()
                return False
            except:
                pass
            # 次の話へ移動
            #self.flag_screenshot_ok = False
            pyautogui.moveTo(200, 960, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(540, 960, duration=0.5)
            #self.flag_screenshot_ok = True
            time.sleep(0.5)
        except:
            # 基本は見つからないのでスクロール
            pyautogui.scroll(-10)
            #print("no found...")
        time.sleep(0.3)
        return True

    def auto_scroll_dmm(self):
        self.get_screenshot()
        try:
            # 最後のページか？
            x, y = pyautogui.locateCenterOnScreen('dmm_end.png',confidence=0.9)
            # 終わる
            #self.event_button_auto(1)
            self.flag_auto = False
            return
        except:
            # 基本は見つからないのでスクロール
            pyautogui.scroll(-10)
            #print("no found...")
        time.sleep(0.3)

