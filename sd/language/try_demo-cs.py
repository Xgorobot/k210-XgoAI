'''
print("Clearing Cached Variables...", end="")
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
print(" Done\n")
import gc
import KPU as kpu
from Maix import utils
utils.gc_heap_size(0xAF000)#GC 500KB
print("utils.gc_heap_size():\t" + str(utils.gc_heap_size()))
'''

import os, Maix, lcd, image, sensor, gc, time, math
from Maix import FPIOA, GPIO
from fpioa_manager import *

try:
    from cocorobo import display_cjk_string, cocorobo_draw_text
except BaseException as e:
    print(str(e))
    pass

gc.enable()

count = 0

def gc_log():
    global count
    gc.collect()
    count = count + 1
    print(str(count) + ":" +str(gc.mem_free()/1000)+"kb")

buttonLeft, buttonRight, buttonDown = 9, 10, 11

fpiol = FPIOA()
fpior = FPIOA()
fpiod = FPIOA()

fpiol.set_function(buttonLeft,FPIOA.GPIO0)
fpior.set_function(buttonRight,FPIOA.GPIO1)
fpiod.set_function(buttonDown,FPIOA.GPIO2)

key_gpio_left=GPIO(GPIO.GPIO0,GPIO.IN)
key_gpio_right=GPIO(GPIO.GPIO1,GPIO.IN)
key_gpio_down=GPIO(GPIO.GPIO2,GPIO.IN)

ksl,ksr,ksd = 0, 0, 0

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)

color_splash_theme = (15,21,46)
color_blue = (31,61,185)
color_blue_lighter = (60,131,211)
color_white = (255,255,255)
color_gray = (60,73,126)
color_orange = (255,165,0)
color_red = (255,0,0)

splash = image.Image(size=(240, 240))
splash.clear()
splash.draw_rectangle(0,0,240,240,color=color_splash_theme,fill=True)

CATEGORY_ITEMS_DICT = {
    "null": (33, 3, 174, 30, 41, 8, '', "/sd/preset/images/icon_basics.jpg"),
    #"basics": (33, 3, 174, 30, 41, 8, '基础', "/sd/preset/images/icon_basics.jpg"),
    "vision": (33, 3, 174, 30, 41, 8, '视觉', "/sd/preset/images/icon_vision.jpg"),
    #"ml": (33, 3, 174, 30, 41, 10, '人工智能', "/sd/preset/images/icon_ml.jpg"),
    #"audiovideo": (33, 3, 174, 30, 41, 8, '多媒体', "/sd/preset/images/icon_av.jpg"),
    "voice": (33, 3, 174, 30, 41, 8, '声音', "/sd/preset/images/icon_av.jpg"),
    "movement": (33, 3, 174, 30, 41, 8, '运动学', "/sd/preset/images/icon_av.jpg")
}

MENU_LANGUAGE = "cs"
MENU_ITEM_PARENT_PATH = "/sd/preset/demos/"+MENU_LANGUAGE+"/"

MENU_ITEMS = [
    # movement
    ("表演模式", CATEGORY_ITEMS_DICT["movement"], MENU_ITEM_PARENT_PATH + "demo_dog_show" + ".py"),
    ("示教模式", CATEGORY_ITEMS_DICT["movement"], MENU_ITEM_PARENT_PATH + "demo_vision_show" + ".py"),
    # Machine Vision
    ("人脸检测", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_face_detection" + ".py"),
    ("人脸识别", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_facial_recognition" + ".py"),
    ("人脸跟随", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_face_tracking" + ".py"),
    #("人体跟随", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_person_tracking" + ".py"),
    ("口罩检测", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_mask_detection" + ".py"),
    ("猜拳游戏", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_finger_guessing" + ".py"),
    ("手势识别", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_hand_8gesture" + ".py"),
    #("手势识别", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_hand_gesture" + ".py"),
    ("手部跟随", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_hand_tracking" + ".py"),
    ("交通标志识别", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_trafficsign" + ".py"),
    ("红绿灯识别", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_trafficlight" + ".py"),
    ("物体分类", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_image_classification" + ".py"),
    ("骨头识别", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_dog_class_recognition" + ".py"),
    ("区域颜色分析", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_reginal_color_analyze" + ".py"),
    ("自动学习并寻找颜色", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_learn_track_color" + ".py"),
    ("色块追踪", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_vision_square_track" + ".py"),
    ("寻找二维码并解码", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_vision_decode_QR" + ".py"),
    #("读取关节", CATEGORY_ITEMS_DICT["vision"], MENU_ITEM_PARENT_PATH + "demo_vision_show" + ".py"),
    # voice
    ("普通话识别", CATEGORY_ITEMS_DICT["voice"], MENU_ITEM_PARENT_PATH + "demo_dog_mandarin_recognition" + ".py"),
    ("音频分析", CATEGORY_ITEMS_DICT["voice"], MENU_ITEM_PARENT_PATH + "demo_dog_sound_spectrum_analyze" + ".py"),
]

BASE_COORD = [3, 33, 3+10, 33+5]
MENU_ITEM_BOX_SIZE = (234, 30)

MENU_ITEM_COORD = [
    [BASE_COORD[0], BASE_COORD[1], BASE_COORD[2], BASE_COORD[3]],
    [BASE_COORD[0], BASE_COORD[1]+29*1, BASE_COORD[2], BASE_COORD[3]+29*1],
    [BASE_COORD[0], BASE_COORD[1]+29*2, BASE_COORD[2], BASE_COORD[3]+29*2],
    [BASE_COORD[0], BASE_COORD[1]+29*3, BASE_COORD[2], BASE_COORD[3]+29*3],
    [BASE_COORD[0], BASE_COORD[1]+29*4, BASE_COORD[2], BASE_COORD[3]+29*4],
    [BASE_COORD[0], BASE_COORD[1]+29*5, BASE_COORD[2], BASE_COORD[3]+29*5],
    [BASE_COORD[0], BASE_COORD[1]+29*6, BASE_COORD[2], BASE_COORD[3]+29*6],
    [BASE_COORD[0], BASE_COORD[1]+29*7, BASE_COORD[2], BASE_COORD[3]+29*7]
] 

MENU_TOTAL_ITEMS = len(MENU_ITEMS) - 1
MENU_CURRENT_SELECT = 0
MENU_PAGE_SWAP_COUNT = 0
MENU_PAGES_TOTAL = math.ceil((MENU_TOTAL_ITEMS+1) / 6)

if isinstance((MENU_TOTAL_ITEMS+1) / 6, int) == True:
    print("Total page "+ str((MENU_TOTAL_ITEMS+1) / 6)  +" is integer!")
elif isinstance((MENU_TOTAL_ITEMS+1) / 6, int) == False:
    print("Total page "+ str((MENU_TOTAL_ITEMS+1) / 6)  +" is not integer!")
    print(MENU_PAGES_TOTAL*6 - (MENU_TOTAL_ITEMS+1))
    for i in range(0,MENU_PAGES_TOTAL*6 - (MENU_TOTAL_ITEMS+1)+1,1):
        MENU_ITEMS.append(("",CATEGORY_ITEMS_DICT["null"],MENU_ITEM_PARENT_PATH + "" + ".py"))

def draw_nav(type):
    if type == "init":
        # Draw Left-side Up Arrow
        splash.draw_rectangle(3,3,30,30,color=color_blue,fill=True)
        splash.draw_rectangle(3,3,30,30,color=color_blue,fill=False)
        nav_up = image.Image("/sd/preset/images/arrow_up_filled.jpg")
        splash.draw_image(nav_up, 5, 5)
        # splash.draw_rectangle(5,5,26,26,color=color_white,fill=False)
        # Draw Right-side Down Arrow
        splash.draw_rectangle(207,3,30,30,color=color_blue,fill=True)
        splash.draw_rectangle(207,3,30,30,color=color_blue,fill=False)
        nav_down = image.Image("/sd/preset/images/arrow_down_filled.jpg")
        splash.draw_image(nav_down, 209, 5)
        # splash.draw_rectangle(209,5,26,26,color=color_white,fill=False)
    elif type == "left":
        # Draw Left-side Up Arrow
        splash.draw_rectangle(3,3,30,30,color=color_blue,fill=True)
        nav_up = image.Image("/sd/preset/images/arrow_up_pressed.jpg")
        splash.draw_image(nav_up, 5, 5)
        # splash.draw_rectangle(5,5,26,26,color=color_white,fill=True)
    elif type == "right":
        # Draw Right-side Down Arrow
        splash.draw_rectangle(207,3,30,30,color=color_blue,fill=True)
        nav_down = image.Image("/sd/preset/images/arrow_down_pressed.jpg")
        splash.draw_image(nav_down, 209, 5)
        #splash.draw_rectangle(209,5,26,26,color=color_white,fill=True)

def draw_ok(type):
    if type == "released":
        splash.draw_rectangle(MENU_ITEM_COORD[6][0],MENU_ITEM_COORD[6][1]+1,50,30,fill=True,color=color_blue_lighter,thickness=1)
        display_cjk_string(splash, MENU_ITEM_COORD[6][0]+6,MENU_ITEM_COORD[6][1]+8, "运行", font_size=1, color=color_splash_theme, background_color=color_blue_lighter)
    elif type == "pressed":
        splash.draw_rectangle(MENU_ITEM_COORD[6][0],MENU_ITEM_COORD[6][1]+1,50,30,fill=True,color=(26,81,143),thickness=1)
        display_cjk_string(splash, MENU_ITEM_COORD[6][0]+6,MENU_ITEM_COORD[6][1]+8, "运行", font_size=1, color=color_splash_theme, background_color=(26,81,143))

def draw_title_bar(index):
    splash.draw_rectangle(MENU_ITEMS[index][1][0],MENU_ITEMS[index][1][1],MENU_ITEMS[index][1][2],MENU_ITEMS[index][1][3], color=color_blue, fill=True)
    display_cjk_string(splash, MENU_ITEMS[index][1][4], MENU_ITEMS[index][1][5], MENU_ITEMS[index][1][6], font_size=1, color=color_white, background_color=color_blue)
    
    display_cjk_string(splash, 188,215, str(index) + "/" + str(MENU_TOTAL_ITEMS+1), font_size=1, color=color_splash_theme, background_color=color_splash_theme)
    display_cjk_string(splash, 188,215, str(index+2) + "/" + str(MENU_TOTAL_ITEMS+1), font_size=1, color=color_splash_theme, background_color=color_splash_theme)
    display_cjk_string(splash, 188,215, str(index+1) + "/" + str(MENU_TOTAL_ITEMS+1), font_size=1, color=color_white, background_color=color_splash_theme)

def draw_item(row, type, realindex):
    if type == "unselected":
        splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
        splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
        display_cjk_string(splash, MENU_ITEM_COORD[row][2]-4, MENU_ITEM_COORD[row][3]+2, MENU_ITEMS[realindex][0], font_size=1, color=color_gray, background_color=color_splash_theme)
    elif type == "selected":
        splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
        splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_white, fill=False, thickness=1)
        display_cjk_string(splash, MENU_ITEM_COORD[row][2]-4, MENU_ITEM_COORD[row][3]+2, MENU_ITEMS[realindex][0], font_size=1, color=color_white, background_color=color_splash_theme)
    elif type == "clearup":
        row = row - 1 
        splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
        splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
        display_cjk_string(splash, MENU_ITEM_COORD[row][2]-4, MENU_ITEM_COORD[row][3]+2, MENU_ITEMS[realindex][0], font_size=1, color=color_gray, background_color=color_splash_theme)
    elif type == "cleardown":
        row = row + 1 
        splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_splash_theme, fill=True, thickness=1)
        splash.draw_rectangle(MENU_ITEM_COORD[row][0], MENU_ITEM_COORD[row][1], MENU_ITEM_BOX_SIZE[0],MENU_ITEM_BOX_SIZE[1], color=color_gray, fill=False, thickness=1)
        display_cjk_string(splash, MENU_ITEM_COORD[row][2]-4, MENU_ITEM_COORD[row][3]+2, MENU_ITEMS[realindex][0], font_size=1, color=color_gray, background_color=color_splash_theme)

def draw_run(row, type, text):
    if type == "running":
        splash.draw_rectangle(MENU_ITEM_COORD[row][0]+1, MENU_ITEM_COORD[row][1]+1, MENU_ITEM_BOX_SIZE[0]-2,MENU_ITEM_BOX_SIZE[1]-2, color=color_orange, fill=True, thickness=1)
        display_cjk_string(splash, MENU_ITEM_COORD[row][2]-3, MENU_ITEM_COORD[row][3]+3, text, font_size=1, color=color_white, background_color=color_orange)
    elif type == "failed":
        splash.draw_rectangle(MENU_ITEM_COORD[row][0]+1, MENU_ITEM_COORD[row][1]+1, MENU_ITEM_BOX_SIZE[0]-2,MENU_ITEM_BOX_SIZE[1]-2, color=color_red, fill=True, thickness=1)
        display_cjk_string(splash, MENU_ITEM_COORD[row][2]-3, MENU_ITEM_COORD[row][3]+3, text, font_size=1, color=color_white, background_color=color_red)

draw_nav('init')
draw_title_bar(0)

for i in range(0,6,1):
    draw_item(i, 'unselected', i)
draw_item(0, 'selected', 0)

draw_ok('released')


while True:

    gc_log()
    # print(str(gc.mem_free()/1000)+"kb")

    key_state_left = key_gpio_left.value()
    key_state_right = key_gpio_right.value()
    key_state_down = key_gpio_down.value()


    """
    ██   ██ ███████ ██    ██      █████  
    ██  ██  ██       ██  ██      ██   ██ 
    █████   █████     ████       ███████ 
    ██  ██  ██         ██        ██   ██ 
    ██   ██ ███████    ██        ██   ██ 

    """

    if (key_state_left == 1 and ksl == 0):
        MENU_CURRENT_SELECT -= 1
        if MENU_CURRENT_SELECT <= 0: MENU_CURRENT_SELECT = 0

        # draw_item(MENU_CURRENT_SELECT)
        
        draw_nav('left')
        draw_title_bar(MENU_CURRENT_SELECT)

        if (MENU_CURRENT_SELECT % 6 > 0) and (MENU_CURRENT_SELECT % 6 < 5): 
            draw_item(MENU_CURRENT_SELECT % 6, "clearup", MENU_CURRENT_SELECT-1)
            draw_item(MENU_CURRENT_SELECT % 6, "cleardown", MENU_CURRENT_SELECT+1)
            draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)
        elif (MENU_CURRENT_SELECT % 6 == 0): 
            draw_item(MENU_CURRENT_SELECT % 6, "cleardown", MENU_CURRENT_SELECT+1)
            draw_item(5, "unselected", MENU_CURRENT_SELECT+5)
            draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)
        elif (MENU_CURRENT_SELECT % 6 >= 5): 
            draw_item(MENU_CURRENT_SELECT % 6, "clearup", MENU_CURRENT_SELECT-1)
            draw_item(0, "unselected", MENU_CURRENT_SELECT-5)
            draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)

        if ((MENU_CURRENT_SELECT % 6) == 0) and (MENU_CURRENT_SELECT != 0):
            MENU_PAGE_SWAP_COUNT -= 1 

        if ((MENU_CURRENT_SELECT % 6) == 5) and (MENU_CURRENT_SELECT != 0):
            for i in range(MENU_CURRENT_SELECT-5,MENU_CURRENT_SELECT+1,1):
                # print(str(MENU_CURRENT_SELECT-5)+","+str(MENU_CURRENT_SELECT))
                draw_item(i % 6, 'unselected', i)
            draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)

        print("Key A Pressed, Current Selection: " + str(MENU_CURRENT_SELECT) + ", \t"+ str(MENU_CURRENT_SELECT % 6) + ", "+ str(MENU_PAGE_SWAP_COUNT) + ", "+ str(MENU_PAGES_TOTAL))

        ksl = 1
    elif (key_state_left == 0 and ksl == 1): 
        draw_nav('init')
        ksl = 0





    '''
    ██   ██ ███████ ██    ██     ██████  
    ██  ██  ██       ██  ██      ██   ██ 
    █████   █████     ████       ██████  
    ██  ██  ██         ██        ██   ██ 
    ██   ██ ███████    ██        ██████  
                                         
    '''
    if (key_state_right == 1 and ksr == 0):
        MENU_CURRENT_SELECT += 1
        if MENU_CURRENT_SELECT >= MENU_TOTAL_ITEMS: MENU_CURRENT_SELECT = MENU_TOTAL_ITEMS
        # draw_item(MENU_CURRENT_SELECT)
        draw_nav('right')
        draw_title_bar(MENU_CURRENT_SELECT)

        if (MENU_CURRENT_SELECT % 6 > 0) and (MENU_CURRENT_SELECT % 6 < 5): 
            draw_item(MENU_CURRENT_SELECT % 6, "clearup", MENU_CURRENT_SELECT-1)
            draw_item(MENU_CURRENT_SELECT % 6, "cleardown", MENU_CURRENT_SELECT+1)
            draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)
        elif (MENU_CURRENT_SELECT % 6 == 0): 
            draw_item(MENU_CURRENT_SELECT % 6, "cleardown", MENU_CURRENT_SELECT+1)
            draw_item(5, "unselected", MENU_CURRENT_SELECT+5)
            draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)
        elif (MENU_CURRENT_SELECT % 6 >= 5): 
            draw_item(MENU_CURRENT_SELECT % 6, "clearup", MENU_CURRENT_SELECT-1)
            draw_item(0, "unselected", MENU_CURRENT_SELECT-5)
            draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)

        if ((MENU_CURRENT_SELECT % 6) == 0) and (MENU_CURRENT_SELECT != 0):
            MENU_PAGE_SWAP_COUNT += 1 
            for i in range(MENU_CURRENT_SELECT,MENU_CURRENT_SELECT+6,1):
                # print(str(MENU_CURRENT_SELECT)+","+str(MENU_CURRENT_SELECT+6))
                draw_item(i % 6, 'unselected', i)
            draw_item(MENU_CURRENT_SELECT % 6, 'selected', MENU_CURRENT_SELECT)

        print("Key B Pressed, Current Selection: " + str(MENU_CURRENT_SELECT) + ", \t"+ str(MENU_CURRENT_SELECT % 6) + ", "+ str(MENU_PAGE_SWAP_COUNT) + ", "+ str(MENU_PAGES_TOTAL))

        ksr = 1
    elif (key_state_right == 0 and ksr == 1): 
        draw_nav('init')
        ksr = 0






    '''
    ██   ██ ███████ ██    ██      ██████ 
    ██  ██  ██       ██  ██      ██      
    █████   █████     ████       ██      
    ██  ██  ██         ██        ██      
    ██   ██ ███████    ██         ██████ 
                                         
    '''
    if (key_state_down == 1 and ksd == 0):
        try:
            draw_ok('pressed')
            draw_run(MENU_CURRENT_SELECT % 6, "running", "打开程序中...")
            lcd.display(splash, oft=(0,0))
            print("Running: " + MENU_ITEMS[MENU_CURRENT_SELECT][2])
            time.sleep(1)

            exec(open(MENU_ITEMS[MENU_CURRENT_SELECT][2]).read())

        except BaseException as e:
            print(str(e))

            for name in dir():
                if not name.startswith('_') and not e:
                    del globals()[name]

            import lcd, image, machine
            try:from cocorobo import display_cjk_string
            except:pass

            def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
                try:
                    if font_size == 1 and scale != 1: font_size = scale
                    else: font_size = font_size
                    display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
                    return canvas
                except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

            splash = image.Image(size=(240, 240))
            splash.clear()
            splash.draw_rectangle(0,0,240,240,color=(15,21,46),fill=True)

            lcd_draw_string(splash, 10,10,"无法运行该示例, 错误原因:", color=(255,255,255), font_size=1)
            lcd_draw_string(splash, 10,35,str(e), color=(255,0,0), font_size=1)

            if "Reset Failed" == str(e) or "Sensor timeout!" == str(e):
                lcd_draw_string(splash, 10,60,"无法找到摄像头", color=(255,0,0), font_size=1)
            elif "ENOENT" in str(e):
                lcd_draw_string(splash, 10,60,"无法找到对应的图片或视频", color=(255,0,0), font_size=1)
            elif "kpu: load error:" in str(e) and "ERR_READ_FILE: read file failed" in str(e):
                lcd_draw_string(splash, 10,60,"无法找到kmodel模型文件", color=(255,0,0), font_size=1)

            lcd.display(splash)

            for sec in range(5,0,-1):
                splash.draw_rectangle(10,210,240,30,color=(15,21,46),fill=True)
                lcd_draw_string(splash, 10,210, str(sec)+"秒后重新启动...", color=(255,255,255), font_size=1)
                time.sleep(1)
                lcd.display(splash)

            machine.reset()
            # draw_run(MENU_CURRENT_SELECT % 6, "failed", "运行失败: " + str(e))

        print("Key C Pressed.")
        ksd = 1
    elif (key_state_down == 0 and ksd == 1): 
        draw_ok('released')
        ksd = 0 



    lcd.display(splash, oft=(0,0))
    