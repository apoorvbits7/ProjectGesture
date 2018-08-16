import os


def tv(action_type,channel=-1):
    os.system("adb shell am start -n com.tiqiaa.remote/com.tiqiaa.icontrol.BaseRemoteActivity")
    os.system("adb shell input tap 83 110")
    os.system("adb shell input tap 426 484")
    if action_type=='toggle':
        os.system("adb shell am start -n com.tiqiaa.remote/com.tiqiaa.icontrol.BaseRemoteActivity")
        os.system("adb shell input tap 173 473")
    if action_type=='volume_up':
        for i in range(5):
            os.system("adb shell input tap 964 718")
    if action_type=='volume_down':
        for i in range(5):
            os.system("adb shell input tap 940 1087")
    if action_type=='channel':
        os.system("adb shell input tap 159 1544")
        for n in channel:
            x = 229 + 300*((n-1)%3)
            y = 479 + 320*int(n/3.1)
            os.system("adb shell input tap "+str(x) + " " + str(y))
            os.system("adb shell input tap 541 1650")
    if action_type=='channel_up':
        os.system("adb shell input tap 143 693")
    if action_type=='channel_up':
        os.system("adb shell input tap 143 1065")
        


def ac(action_type,temp=-1):
    os.system("adb shell am start -n com.tiqiaa.remote/com.tiqiaa.icontrol.BaseRemoteActivity")
    os.system("adb shell input tap 83 110")
    os.system("adb shell input tap 426 667")
    if action_type=='toggle':
        os.system("adb shell input tap 168 546")
    if action_type=='temp':
        os.system("adb shell input tap 972 1654")
        for i in range(temp):
            os.system("adb shell input tap 355 599")
        os.system("adb shell input tap 541 1650")
    if action_type=='temp':
        os.system("adb shell input tap 972 1654")
        for i in range(temp):
            os.system("adb shell input tap 822 616")
        os.system("adb shell input tap 541 1650")
    if action_type=='temp_manual':
        os.system("adb shell input tap 417 823")
