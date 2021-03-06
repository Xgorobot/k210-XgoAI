print("Clearing Cached Variables...", end="")
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
print(" Done")
import KPU as kpu
kpu.memtest()
from Maix import utils
import gc
gc.enable()
utils.gc_heap_size()

################# Done Init #################

import time

import machine, time
from fpioa_manager import fm

import lcd
import image
import sensor
import KPU as kpu
from fpioa_manager import *
from Maix import FPIOA, GPIO

_gp_side_buttons = [9, 10, 11]

FPIOA().set_function(_gp_side_buttons[0],FPIOA.GPIO0)
FPIOA().set_function(_gp_side_buttons[1],FPIOA.GPIO1)
FPIOA().set_function(_gp_side_buttons[2],FPIOA.GPIO2)

_gp_side_a = GPIO(GPIO.GPIO0,GPIO.IN,GPIO.PULL_UP)
_gp_side_b = GPIO(GPIO.GPIO1,GPIO.IN,GPIO.PULL_UP)
_gp_side_c = GPIO(GPIO.GPIO2,GPIO.IN,GPIO.PULL_UP)

import machine

fm.register(13,fm.fpioa.UART2_TX)
fm.register(14,fm.fpioa.UART2_RX)
robot_dog_setup_uart = machine.UART(machine.UART.UART2,115200,bits=8,parity=None,stop=1)

def add(a,b):
    num1 = a ^ b
    num2 = (a & b) << 1
    while num2 != 0:
        temp  = num1 ^ num2
        num2 = (num1 & num2) << 1
        num1 = temp
    return num1

def calculate_sum(a,b):
    bytearr = [9, 1, a, b]
    sum = 0
    for i in bytearr:
        sum = add(sum,i)
    calculated_cksum = bin(sum).replace("0b","")
    while len(calculated_cksum) < 8:
        calculated_cksum = "0" + calculated_cksum
    ReturningChecksum = ""
    for index in range(len(calculated_cksum)):
        if calculated_cksum[index] == "1":
            ReturningChecksum += "0"
        elif calculated_cksum[index] == "0":
            ReturningChecksum += "1"
    return bytes([int(hex(int(ReturningChecksum,2)),16)])

def mapping(input_value,i_min,i_max,o_min,o_max):
    if input_value < i_min:
        input_value = i_min
    if input_value > i_max:
        input_value = i_max
    dat=(input_value-i_min)/(i_max-i_min)*(o_max-o_min)+o_min
    return round(dat)

try:from cocorobo import display_cjk_string
except:pass

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        if font_size == 1 and scale != 1: font_size = scale
        else: font_size = font_size
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

_camera_x, _camera_y = 0, 0

task_customized_model = kpu.load("/sd/preset/models/rps/yolov2.kmodel")
anchor_customized_model = (1.9551, 4.6866, 2.3092, 5.4064, 2.7024, 5.7547, 3.2026, 4.4318, 3.3322, 5.6523)
a = kpu.init_yolo2(task_customized_model, 0.65, 0.1, 5, anchor_customized_model)

classes_customized_model = ["scissors", "paper", "rock"]



lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
_camera_x, _camera_y = 8, 8
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.skip_frames(30)
sensor.run(1)
sensor.set_windowing((224,224))
sensor.set_hmirror(True)
detime = time.ticks_ms()
while True:
    camera = sensor.snapshot()
    if time.ticks_ms() - detime >= 300:
        code_customized_model = kpu.run_yolo2(task_customized_model, camera)
        if code_customized_model is not None:
            if len(code_customized_model) == 1:
                for i in (code_customized_model):
                    if (classes_customized_model[i.classid()]) == "scissors":
                        canvas = image.Image("/sd/preset/images/rps/rock.jpg")
                    elif (classes_customized_model[i.classid()]) == "paper":
                        canvas = image.Image("/sd/preset/images/rps/scissors.jpg")
                    elif (classes_customized_model[i.classid()]) == "rock":
                        canvas = image.Image("/sd/preset/images/rps/paper.jpg")
                    _canvas_x, _canvas_y = 0, 0
                    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
                    robot_dog_setup_uart.write(bytes([57]))
                    time.sleep_ms(20)
                    time.sleep_ms(1000)
                    detime = time.ticks_ms()
                    lcd.clear(lcd.BLACK)
    lcd.display(camera, oft=(_camera_x,_camera_y))
    if _gp_side_c.value() == 1:
        old_time = time.ticks_ms()
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if time.ticks_ms() - old_time >= 1000:
                robot_dog_setup_uart.write(bytes([0]))
                time.sleep_ms(20)
                machine.reset()
