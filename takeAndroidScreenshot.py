from os import system 

def takeScreenshot(filename="./1.png"):
    """Take Screenshot with adb (assume in PATH)

    See https://stackoverflow.com/questions/20983351/taking-screenshot-on-emulator-from-android-studio
    """
    system("adb shell screencap -p /sdcard/screen.png")
    system("adb pull /sdcard/screen.png %s>NUL"%filename)
    system("adb shell rm /sdcard/screen.png")