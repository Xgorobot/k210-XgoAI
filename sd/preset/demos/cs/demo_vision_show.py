import time

import lcd
import image
import machine, time
from fpioa_manager import fm
from machine import Timer

def _timer_on_timer(timer):
    global _timer_current_time_elapsed
    _timer_current_time_elapsed =  _timer_current_time_elapsed + 1

_timer_current_time_elapsed = 0
_timer_tim = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PERIODIC, period=1, callback=_timer_on_timer)

try:
	from xgo import XGO
except BaseException as e:
	print(str(e))
	pass

from fpioa_manager import *
from Maix import FPIOA, GPIO

_gp_side_buttons = [9, 10, 11]

FPIOA().set_function(_gp_side_buttons[0],FPIOA.GPIO0)
FPIOA().set_function(_gp_side_buttons[1],FPIOA.GPIO1)
FPIOA().set_function(_gp_side_buttons[2],FPIOA.GPIO2)

_gp_side_a = GPIO(GPIO.GPIO0,GPIO.IN,GPIO.PULL_UP)
_gp_side_b = GPIO(GPIO.GPIO1,GPIO.IN,GPIO.PULL_UP)
_gp_side_c = GPIO(GPIO.GPIO2,GPIO.IN,GPIO.PULL_UP)

try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        if font_size == 1 and scale != 1: font_size = scale
        else: font_size = font_size
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

fm.register(13,fm.fpioa.UART2_TX)
fm.register(14,fm.fpioa.UART2_RX)
robot_dog_setup_uart = machine.UART(machine.UART.UART2,115200,bits=8,parity=None,stop=1)
dog = XGO(machine.UART.UART2)

_canvas_x, _canvas_y = 0, 0



lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
servo = [11,12,13,21,22,23,31,32,33,41,42,43]
#my_list1 = [0,0,0,0,0,0,0,0,0,0,0,0]
#my_list2 = [0,0,0,0,0,0,0,0,0,0,0,0]
canvas = image.Image(size=(240, 240))
num = 0
isCollect = 0
n = 0
#m = 0
lcd_draw_string(canvas,50,20, "A键记录", color=(255,255,255), scale=2, mono_space=False)
lcd_draw_string(canvas,50,120, "B键结束", color=(255,255,255), scale=2, mono_space=False)
lcd_draw_string(canvas,50,210, "C键演示", color=(255,255,255), scale=2, mono_space=False)
lcd.display(canvas, oft=(_canvas_x,_canvas_y))
time.sleep(1)
canvas.clear()
data = [[],[],[],[],[],[],[],[],[],[],[],[]]
#全部舵机卸载
dog.unload_allmotor()

while True:
    
    _timer_tim.start()
    
    if _gp_side_a.value() == 1:
        while not (_gp_side_a.value() == 0):
            time.sleep_ms(1)
        time.sleep_ms(20)
        data[n] = dog.read_motor()
        #data_show = list(map(int, data[n]))
        #lcd_draw_string(canvas,0,0, (str(data_show)), color=(255,0,0), scale=1, mono_space=False)
        #lcd_draw_string(canvas,60,100, "动作"), color=(255,255,255), scale=2, mono_space=False)
        lcd_draw_string(canvas,70,100, "动作"+(str(n+1)), color=(255,255,255), scale=2, mono_space=False)
        lcd.display(canvas, oft=(_canvas_x,_canvas_y))
        time.sleep_ms(20)
        canvas.clear()
        n = n + 1        
    if _gp_side_b.value() == 1:
        while not (_gp_side_b.value() == 0):
            time.sleep_ms(1)
        time.sleep_ms(20)
        data[n] = dog.read_motor()
        dog.load_allmotor()
        #data_show_f = list(map(int, data[n]))
        #lcd_draw_string(canvas,5,5, (str(data_show_f)), color=(255,0,0), scale=1, mono_space=False)
        lcd_draw_string(canvas,40,100, "动作组就绪", color=(255,255,255), scale=2, mono_space=False)
        lcd.display(canvas, oft=(_canvas_x,_canvas_y))
        time.sleep_ms(20)
        canvas.clear()
    
    if _gp_side_c.value() == 1:
        #while not (_gp_side_c.value() == 0):
        #    time.sleep_ms(1)
        #time.sleep_ms(20)
        
        C_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - C_time >= 1000:
                robot_dog_setup_uart.write(bytes([0]))
                time.sleep_ms(20)
                machine.reset()
        
        lcd_draw_string(canvas,40,100, "动作组执行", color=(255,255,255), scale=2, mono_space=False)
        lcd.display(canvas, oft=(_canvas_x,_canvas_y))
        time.sleep_ms(20)
        canvas.clear()   
        dog.motor(servo,data[0])
        time.sleep_ms(800)
        dog.motor(servo,data[1])
        time.sleep_ms(800)
        dog.motor(servo,data[2])
        time.sleep_ms(800)
        dog.motor(servo,data[3])
        time.sleep_ms(800)
        dog.motor(servo,data[4])
        time.sleep_ms(800)
        dog.motor(servo,data[5])
        time.sleep_ms(800)
        dog.motor(servo,data[6])
        time.sleep_ms(800)
        dog.motor(servo,data[7]) 
        time.sleep_ms(800)
        dog.motor(servo,data[8])
        time.sleep_ms(800)
        dog.motor(servo,data[9])
        time.sleep_ms(800)
        dog.motor(servo,data[10])
        time.sleep_ms(800)
        dog.motor(servo,data[11]) 
        time.sleep_ms(800)

time.sleep_ms(20)
