
from fpioa_manager import *
import os, Maix, lcd, image, sensor, gc, time, sys
from Maix import FPIOA, GPIO
import machine

try:
    from cocorobo import firmware_info
except BaseException as e:
    print(str(e))
    pass

try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True, background_color=(0,0,0)):
    try: display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
    except: canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

gc.enable()
gc.collect()

count = 0

def gc_log():
    global count
    gc.collect()
    count = count + 1
    # print(str(count) + ":" +str(gc.mem_free()/1000)+"kb")

def _GET_LIST_FROM_FILE(_path, _sep):
    f = open(_path, 'r')
    result = f.read().split(_sep)
    f.close()
    return result

ai_flash_freespace = (os.statvfs("/flash")[0]*os.statvfs("/flash")[3])/(1024*1024)
# ai_sd_freespace = (os.statvfs("/sd")[0]*os.statvfs("/sd")[3])/(1024*1024)

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

time.sleep(1)

lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)

ksl,ksr,ksd = 0, 0, 0

def main_program():
    global key_state_left, key_gpio_right, key_state_down, current_selection, ksl, ksr, ksd
    gc_log()

    key_state_left = key_gpio_left.value()
    key_state_right = key_gpio_right.value()
    key_state_down = key_gpio_down.value()

    if (key_state_left == 1 and ksl == 0):
        current_selection = current_selection - 1
        if current_selection == 0: current_selection = 2
        # print(str(current_selection))

        if current_selection == 1:
            splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
            lcd_draw_string(splash, btn_col[0]+7, btn_row+7, main_title[0], font_size=1, color=txt_selected, background_color=splash_theme_color)
            lcd_draw_string(splash, btn_col[0]+7, btn_row+27, main_title[1], font_size=1, color=txt_selected, background_color=splash_theme_color)

            splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
            lcd_draw_string(splash, btn_col[1]+7, btn_row+7, main_title[2], font_size=1, color=txt_unselected, background_color=splash_theme_color)
            lcd_draw_string(splash, btn_col[1]+7, btn_row+27, main_title[3], font_size=1, color=txt_unselected, background_color=splash_theme_color)
        elif current_selection == 2:
            splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
            lcd_draw_string(splash, btn_col[0]+7, btn_row+7, main_title[0], font_size=1, color=txt_unselected, background_color=splash_theme_color)
            lcd_draw_string(splash, btn_col[0]+7, btn_row+27, main_title[1], font_size=1, color=txt_unselected, background_color=splash_theme_color)

            splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
            lcd_draw_string(splash, btn_col[1]+7, btn_row+7, main_title[2], font_size=1, color=txt_selected, background_color=splash_theme_color)
            lcd_draw_string(splash, btn_col[1]+7, btn_row+27, main_title[3], font_size=1, color=txt_selected, background_color=splash_theme_color)

        ksl = 1
    elif (key_state_left == 0 and ksl == 1):
        ksl = 0


    if (key_state_right == 1 and ksr == 0):
        current_selection = current_selection + 1
        if current_selection > 2: current_selection = 1
        # print(str(current_selection))

        if current_selection == 1:
            splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
            lcd_draw_string(splash, btn_col[0]+7, btn_row+7, main_title[0], font_size=1, color=txt_selected, background_color=splash_theme_color)
            lcd_draw_string(splash, btn_col[0]+7, btn_row+27, main_title[1], font_size=1, color=txt_selected, background_color=splash_theme_color)

            splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
            lcd_draw_string(splash, btn_col[1]+7, btn_row+7, main_title[2], font_size=1, color=txt_unselected, background_color=splash_theme_color)
            lcd_draw_string(splash, btn_col[1]+7, btn_row+27, main_title[3], font_size=1, color=txt_unselected, background_color=splash_theme_color)
        elif current_selection == 2:
            splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
            lcd_draw_string(splash, btn_col[0]+7, btn_row+7, main_title[0], font_size=1, color=txt_unselected, background_color=splash_theme_color)
            lcd_draw_string(splash, btn_col[0]+7, btn_row+27, main_title[1], font_size=1, color=txt_unselected, background_color=splash_theme_color)

            splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
            lcd_draw_string(splash, btn_col[1]+7, btn_row+7, main_title[2], font_size=1, color=txt_selected, background_color=splash_theme_color)
            lcd_draw_string(splash, btn_col[1]+7, btn_row+27, main_title[3], font_size=1, color=txt_selected, background_color=splash_theme_color)

        ksr = 1
    elif (key_state_right == 0 and ksr == 1):
        ksr = 0


    if (key_state_down == 1 and ksd == 0):
        if current_selection == 1: 
            try:
                print("executing lastest code")
                splash.draw_rectangle(btn_col[0], btn_row-46,220,40, color=splash_theme_color, fill=True, thickness=1)
                lcd_draw_string(splash, btn_col[0], btn_row-25, splash_text[4], font_size=1, color=(0,255,255), background_color=splash_theme_color)
                lcd.display(splash, oft=(0,0))
                time.sleep(1)
                exec(open("user_latest_code.py").read())
                import machine
                machine.reset()
            except BaseException as e:
                try:
                    splash.draw_rectangle(btn_col[0], btn_row-46,220,40, color=splash_theme_color, fill=True, thickness=1)
                    if "ENOENT" in str(e):
                        # "Code not found."
                        lcd_draw_string(splash, btn_col[0], btn_row-25, splash_text[5], font_size=1, color=(255,0,0), background_color=splash_theme_color)
                    elif "invalid syntax" in str(e):
                        # "Error: invalid syntax."
                        lcd_draw_string(splash, btn_col[0], btn_row-25, splash_text[6], font_size=1, color=(255,0,0), background_color=splash_theme_color)
                        # splash.draw_string(btn_col[0], 30, str(e), color=(255,0,0), scale=1.332, mono_space=False)
                    else:
                        lcd_draw_string(splash, btn_col[0], btn_row-25, str(e), font_size=1, color=(255,0,0), background_color=splash_theme_color)
                        print(e)
                    lcd.display(splash, oft=(0,0))
                    print(str(e))
                    time.sleep_ms(2000)

                    # splash.draw_rectangle(btn_col[0], 30, 210, 20, color=splash_theme_color, fill=True, thickness=1)
                    # splash.draw_rectangle(btn_col[0], btn_row-22,210, 12, color=splash_theme_color, fill=True, thickness=1)
                    splash.draw_rectangle(btn_col[0], btn_row-46,240,40, color=splash_theme_color, fill=True, thickness=1)
                    #splash.draw_string(btn_col[0], btn_row-22, "Left key to Move, Right key to Choose:", color=txt_selected, scale=1.332, mono_space=False)
                    lcd_draw_string(splash, btn_col[0], btn_row-45, splash_text[2], font_size=1, color=txt_unselected, background_color=splash_theme_color)
                    lcd_draw_string(splash, btn_col[0], btn_row-25, splash_text[3], font_size=1, color=txt_unselected, background_color=splash_theme_color)

                    lcd.display(splash, oft=(0,0))
                except BaseException as e:
                    print(e)
                    import machine
                    machine.reset()
        if current_selection == 2: 
            try:
                splash.draw_rectangle(btn_col[0], btn_row-46,220,40, color=splash_theme_color, fill=True, thickness=1)
                lcd_draw_string(splash, btn_col[0], btn_row-25, splash_text[7], font_size=1, color=(0,255,255), background_color=splash_theme_color)
                lcd.display(splash, oft=(0,0))
                time.sleep(1)
                # __import__("try_demo")
                exec(open("/sd/language/try_demo-cs.py").read())
            except BaseException as e:
                print(str(e))
                splash.draw_rectangle(btn_col[0], btn_row-46,220,40, color=splash_theme_color, fill=True, thickness=1)
                lcd_draw_string(splash, btn_col[0], btn_row-25, splash_text[8], font_size=1, color=(255,0,0), background_color=splash_theme_color)
                lcd.display(splash, oft=(0,0))
                time.sleep_ms(2000)
                splash.draw_rectangle(btn_col[0], btn_row-46,220,40, color=splash_theme_color, fill=True, thickness=1)
                lcd_draw_string(splash, btn_col[0], btn_row-45, splash_text[2], font_size=1, color=txt_unselected, background_color=splash_theme_color)
                lcd_draw_string(splash, btn_col[0], btn_row-25, splash_text[3], font_size=1, color=txt_unselected, background_color=splash_theme_color)
                lcd.display(splash, oft=(0,0))

        print(str(current_selection) + " select")

        ksd = 1
    elif (key_state_down == 0 and ksd == 1):
        ksd = 0

    lcd.display(splash, oft=(0,0))


if key_gpio_left.value() == 1 and key_gpio_right.value() == 0:
    try:
        lcd.clear(lcd.BLACK)
        lcd.draw_string(10,10, "Entering test mode...", lcd.WHITE, lcd.BLACK)
        time.sleep(1)
        exec(open("/sd/device_test.py").read())
        gc_log()
    except BaseException as e:
        gc.collect()
        lcd.clear(lcd.BLACK)
        lcd.draw_string(10,10,str(e), lcd.RED, lcd.BLACK)
        sys.exit(0)
        gc_log()
else:
    try:
        import machine, time

        is_config_there = False

        try:
            f = open("/sd/config.cfg", "r")
            is_config_there = True
        except: pass

        if is_config_there == True:
            check_if_load_last_code_directly = _GET_LIST_FROM_FILE("/sd/config.cfg", '\r\n')[0].strip("\n").split("=")[1].split(" ")[1]

            try:
                if check_if_load_last_code_directly == '1':
                    exec(open("user_latest_code.py").read())
                elif check_if_load_last_code_directly == '0':
                    pass
            except Exception as e:
                lcd.clear(lcd.BLACK)
                lcd.draw_string(10,10, "Config.cfg Error: " +str(e), lcd.WHITE, lcd.BLACK)
                # print("Proccess config.cfg Error: ", e)
                time.sleep(2)
                machine.reset()

    except Exception as e:
        print("Error: ", e)
        pass

    if "board_type.cfg" not in os.listdir("/sd"):
        with open("board_type.cfg", "w") as f:
            f.write("ai")

    btn_selected = (255,255,255)
    btn_unselected = (76,86,127)
    txt_selected = (255,255,255)
    txt_unselected = (76,86,127)

    # gc.threshold(800000)
    # print("before splash")
    gc_log()
    splash = image.Image(size=(240, 240))
    # splash = image.Image("/sd/preset/images/splash_bg.jpg")
    # print("after splash")
    splash_theme_color = (15,21,46)
    # del splash
    gc_log()

    splash.clear()
    splash.draw_rectangle(0,0,240,240,color=splash_theme_color,fill=True)
    # splash.draw_string(btn_col, 7, "", color=(255,255,255), scale=2, mono_space=False)

    btn_width = 114
    btn_height = 52

    btn_y_base = 5
    btn_col = (btn_y_base, btn_y_base+btn_width, btn_y_base+152)
    btn_row = 180

    main_title = (
        "运行",
        "上次程序",
        "打开",
        "样例菜单"
    )

    splash_text = (
        "固件版本: ",
        "固件版本: 未知",
        "按下A或B键移动选项,",
        "按下C键进行选择",
        "正在打开上次上传的程序...",
        "无法找到该程序",
        "程序语法错误",
        "正在打开样例菜单...",
        "无法找到样例菜单文件"
    )

    gc_log()

    try:
        os.listdir("/sd")
        # print("[CocoRobo] SD Card Successfully Initiated.")
    except BaseException as e:
        print(str(e))
        splash.draw_rectangle(0,0,240,240,color=(0,0,0), fill=True)
        # splash.draw_string(btn_col[0]+40, 70, b"Cannot Load", color=(200,0,0), scale=3, mono_space=False)
        # splash.draw_string(btn_col[0]+43, 100, b"The SD Card", color=(200,0,0), scale=3, mono_space=False)
        splash.draw_line(101,66,75,92,color=(200,0,0),thickness=4)
        splash.draw_line(75,92,75,174,color=(200,0,0),thickness=4)
        splash.draw_line(75,174,165,174,color=(200,0,0),thickness=4)
        splash.draw_line(165,174,165,66,color=(200,0,0),thickness=4)
        splash.draw_line(165,66,101,66,color=(200,0,0),thickness=4)
        splash.draw_string(btn_col[0]+108, 85, "?", color=(200,0,0), scale=7, mono_space=False)
        # lcd_draw_string(splash, btn_col[0]+20, 70, "无法读取SD卡", font_size=2, color=(0,255,255), auto_wrap=False)
        lcd.display(splash, oft=(0,0))
        print("[CocoRobo] SD Card Initiate Failed. Please Reset Now")
        sys.exit(0)
        # machine.reset()

    try:
        title_logo_text = image.Image("/sd/preset/images/cocorobo_text.jpg")
        splash.draw_image(title_logo_text, btn_col[0]+3, 10)
    except:
        splash.draw_string(btn_col[0]+1, 7, "CocoRobo AI Module", color=(255,255,255), scale=2, mono_space=False)

    try:
        lcd_draw_string(splash, btn_col[0], 40, splash_text[0] + str(firmware_info.ai()), color=(0,255,255), background_color=splash_theme_color)
    except BaseException as e:
        lcd_draw_string(splash, btn_col[0], 40, splash_text[1], font_size=1, color=(0,255,255), background_color=splash_theme_color)
        pass


    lcd_draw_string(splash, btn_col[0], btn_row-45, splash_text[2], font_size=1, color=txt_unselected, background_color=splash_theme_color)
    lcd_draw_string(splash, btn_col[0], btn_row-25, splash_text[3], font_size=1, color=txt_unselected, background_color=splash_theme_color)
    # splash.draw_string(btn_col[0], btn_row-22, "Key A & B to Move, Key C to Choose:", color=txt_selected, scale=1.332, mono_space=False)

    splash.draw_rectangle(btn_col[0], btn_row, btn_width, btn_height, color=btn_selected, fill=False, thickness=1)
    lcd_draw_string(splash, btn_col[0]+7, btn_row+7, main_title[0], font_size=1, color=txt_selected, background_color=splash_theme_color)
    lcd_draw_string(splash, btn_col[0]+7, btn_row+27, main_title[1], font_size=1, color=txt_selected, background_color=splash_theme_color)

    splash.draw_rectangle(btn_col[1], btn_row, btn_width, btn_height, color=btn_unselected, fill=False, thickness=1)
    lcd_draw_string(splash, btn_col[1]+7, btn_row+7, main_title[2], font_size=1, color=txt_unselected, background_color=splash_theme_color)
    lcd_draw_string(splash, btn_col[1]+7, btn_row+27,  main_title[3], font_size=1, color=txt_unselected, background_color=splash_theme_color)

    lcd.display(splash, oft=(0,0))

    current_selection = 1

    # _thread.start_new_thread(main_program,()) 
    try:
        pass
        # main_program()
    except KeyboardInterrupt:
        print("exit")

gc_log()

while True:
    main_program()
