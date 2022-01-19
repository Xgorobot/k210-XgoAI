import time

import machine, time
from fpioa_manager import fm
try:
	from xgo import XGO
except BaseException as e:
	print(str(e))
	pass

import lcd
import image

fm.register(13,fm.fpioa.UART2_TX)
fm.register(14,fm.fpioa.UART2_RX)
dog = XGO(machine.UART.UART2)

try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        if font_size == 1 and scale != 1: font_size = scale
        else: font_size = font_size
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

_canvas_x, _canvas_y = 0, 0
def robot_dog_get_servo_angle(index):
    global dog
    xgoAngle = dog.read_motor()
    return xgoAngle[index]



dog.unload_motor(1)
lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
canvas = image.Image(size=(240, 240))
num = 0
isCollect = 0
canvas.draw_rectangle(0,0, canvas.width(),canvas.height(), color=(255,0,0), thickness=1, fill=True)
lcd.display(canvas, oft=(_canvas_x,_canvas_y))
while True:
    lcd_draw_string(canvas,30,30, (str(robot_dog_get_servo_angle(2))), color=(255,255,255), scale=3, mono_space=False)
    time.sleep_ms(200)
    canvas.clear()
