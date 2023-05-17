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


def detectScreenType(screenshot, templates):
    screenshotGray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    threshold = 0.6
    matchingScreens = []

    for templatePath, screenType in templates.items():
        template = cv2.imread(templatePath, cv2.IMREAD_GRAYSCALE)
        templateW, templateH = template.shape[::-1]
        result = cv2.matchTemplate(screenshotGray, template, cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
        if maxVal >= threshold:
            matchingScreens.append(screenType)

    return matchingScreens


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
    "gameNavigationReferences/MainMenu.png": "mainMenu",
    "gameNavigationReferences/ChooseYourDeck.png": "deckSelection",
    "gameNavigationReferences/FindingOpponent.png": "gameSearch",
    "gameNavigationReferences/VS.png": "cardSelection",
    "gameNavigationReferences/EnemyTurn.png": "enemyTurn",
    "gameNavigationReferences/EndTurn.png": "myTurn",
    "gameNavigationReferences/EndOfGame.png": "endGame",
    "gameNavigationReferences/gameIssue.png": "gameIssue",
    "gameNavigationReferences/DesktopPlay.png": "playButtonClient",
    "gameNavigationReferences/DesktopBlizzard.png": "blizzardLogo",
    "gameNavigationReferences/wildModeSelected.png": "wildModeSelected",
    "gameNavigationReferences/casualModeSelected.png": "casualModeSelected",
    "gameNavigationReferences/casualModeSelect.png": "modeSelect",
    "Buttons/PlayButton.png": "gameplayButton"
}

screenshot = pyautogui.screenshot()
currentScreen = detectScreenType(screenshot, templates)


while True:
    time.sleep(0.8)
    screenshot = pyautogui.screenshot()
    currentScreen = detectScreenType(screenshot, templates)
    print(currentScreen)

    if "mainMenu" in currentScreen:
        clickOnButtonWithOffset("gameNavigationReferences/MainMenu.png", threshold=0.4, minX=50, maxX=90, minY=5, maxY=51)

    if "wildModeSelected" in currentScreen:
        click(721, 506)
        time.sleep(0.5)
        print("changeGameMode")
        time.sleep(0.3)
        clickOnButtonWithOffset("gameNavigationReferences/wildModeSelected.png", threshold=0.6, minX=50, maxX=90, minY=5, maxY=51)
    if "modeSelect" in currentScreen:
        clickOnButtonWithOffset("gameNavigationReferences/casualModeSelect.png", threshold=0.6, minX=150, maxX=320, minY=50, maxY=220)
        print("clickingOnCasual")
        time.sleep(0.3)
    if "casualModeSelected" and "gameplayButton" in currentScreen:
        clickOnButtonWithOffset("Buttons/PlayButton.png", threshold=0.6, minX=150, maxX=180, minY=50, maxY=220)
        print("clickingOnPlayButton")
        time.sleep(0.3)
    if "gameSearch" in currentScreen:
        time.sleep(0.2)
        print("findingAGame")
