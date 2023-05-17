import time
import random as rn
import cv2
import numpy as np
import pyautogui
import pytesseract


def click(x, y):
    pyautogui.moveTo(x, y)
    time.sleep(rn.uniform(0.05, 0.23))
    pyautogui.click(x, y, clicks=1, button="left")
    time.sleep(0.2)


def detect_screen_type(screenshot, templates):
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    threshold = 0.6
    matching_screens = []

    for template_path, screen_type in templates.items():
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        template_w, template_h = template.shape[::-1]
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            matching_screens.append(screen_type)

    return matching_screens


def searchForButton(buttonPath, threshold=0.6, minX=0, maxX=0, minY=0, maxY=0):
    buttonTemplate = cv2.imread(buttonPath, cv2.IMREAD_GRAYSCALE)
    if buttonTemplate is None:
        return None
    buttonW, buttonH = buttonTemplate.shape[::-1]
    screenshot = pyautogui.screenshot()
    screenshotGray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    ssim = cv2.matchTemplate(screenshotGray, buttonTemplate, cv2.TM_CCOEFF_NORMED)
    locations = np.where(ssim >= threshold)
    locations = list(zip(*locations[::-1]))
    if locations:
        buttonX, buttonY = locations[0]
        return buttonX + rn.randint(minX, maxX), buttonY + rn.randint(minY, maxY)
    else:
        return None


def clickOnButtonWithOffset(buttonPath, threshold=0.6, minX=0, maxX=0, minY=0, maxY=0):
    buttonLocation = searchForButton(buttonPath, threshold=0.6, minX=0, maxX=0, minY=0, maxY=0)
    if buttonLocation:
        buttonX, buttonY = buttonLocation
        buttonX += rn.randint(minX, maxX)
        buttonY += rn.randint(minY, maxY)
        click(buttonX, buttonY)
        return True
    return False


templates = {
    'gameNavigationReferences/MainMenu.png': 'main_menu',
    'gameNavigationReferences/ChooseYourDeck.png': 'deck_selection',
    'gameNavigationReferences/FindingOpponent.png': 'gameSearch',
    'gameNavigationReferences/VS.png': 'card_selection',
    'gameNavigationReferences/EnemyTurn.png': 'enemy_turn',
    'gameNavigationReferences/EndTurn.png': 'my_turn',
    'gameNavigationReferences/EndOfGame.png': 'end_game',
    'gameNavigationReferences/gameIssue.png': 'game_issue',
    'gameNavigationReferences/DesktopPlay.png': 'play_button_client',
    'gameNavigationReferences/DesktopBlizzard.png': 'blizzard_logo',
    'gameNavigationReferences/wildModeSelected.png': 'wild_mode_selected',
    'gameNavigationReferences/casualModeSelected.png': 'casual_mode_selected',
    'gameNavigationReferences/casualModeSelect.png': 'mode_select',
    'Buttons/PlayButton.png': 'gameplay_button'
}

screenshot = pyautogui.screenshot()
current_screen = detect_screen_type(screenshot, templates)


while True:
    time.sleep(0.8)
    screenshot = pyautogui.screenshot()
    current_screen = detect_screen_type(screenshot, templates)
    print(current_screen)

    if 'main_menu' in current_screen:
        clickOnButtonWithOffset('gameNavigationReferences/MainMenu.png', threshold=0.4, minX=50, maxX=90, minY=5, maxY=51)

    if 'wild_mode_selected' in current_screen:
        click(721,506)
        time.sleep(0.5)
        print("change game mode")
        time.sleep(0.3)
        clickOnButtonWithOffset('gameNavigationReferences/wildModeSelected.png', threshold=0.6, minX=50, maxX=90, minY=5, maxY=51)
    if 'mode_select' in current_screen:
        clickOnButtonWithOffset('gameNavigationReferences/casualModeSelect.png', threshold=0.6, minX=150, maxX=320,minY=50, maxY=220)
        print("clicking on casual")
        time.sleep(0.3)
    if 'casual_mode_selected' and 'gameplay_button' in current_screen:
        clickOnButtonWithOffset('Buttons/PlayButton.png', threshold=0.6, minX=150, maxX=180,minY=50, maxY=220)
        print("clicking on play button")
        time.sleep(0.3)
    if 'gameSearch' in current_screen:
        time.sleep(0.2)
        print("finding a game")





