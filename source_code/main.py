from machine import Pin, PWM
from machine import ADC, Pin
from time import sleep

led = Pin("LED", Pin.OUT)
led.value(0)

test_pin = Pin(4, Pin.OUT)
test_pin.value(0)

pwm0 = PWM(Pin(0))
pwm1 = PWM(Pin(1))
pwm2 = PWM(Pin(2))
pwm3 = PWM(Pin(3))

pwm0.freq(20000)
pwm1.freq(20000)
pwm2.freq(20000)
pwm3.freq(20000)

pwm0.duty_u16(0)
pwm1.duty_u16(0)
pwm2.duty_u16(0)
pwm3.duty_u16(0)

adc0 = ADC(Pin(26))
adc1 = ADC(Pin(27))
adc2 = ADC(Pin(28))

class PID:
    def __init__(self, p, i, d, inte, deri, preoffset):
        self.p = p
        self.i = i
        self.d = d
        self.inte = inte
        self.deri = deri
        self.preoffset = preoffset

# PID parameter for X axis
pid_x = PID(60, 0, 10, 0, 0, 0)

# PID parameter for Y axis
pid_y = PID(60, 0, 10, 0, 0, 0)

hall_sen_xbase = 0
hall_sen_ybase = 0
hall_sen_zbase = 0

MAX_INTE = 1000
MAX_OUTPUT = 60000
def PID_calculate(cur_offset, pid):
    pid.inte += cur_offset
    
    if pid.inte > MAX_INTE:
        pid.inte = MAX_INTE
    elif pid.inte < -MAX_INTE:
        pid.inte = -MAX_INTE
        
    output = pid.p * cur_offset + pid.i * pid.inte + pid.d * (cur_offset - pid.preoffset)
    
    if output > MAX_OUTPUT:
        output = MAX_OUTPUT
    elif output < -MAX_OUTPUT:
        output = -MAX_OUTPUT
        
    pid.preoffset = cur_offset
    
    return output

for count in range(50):
    hall_sen_xbase += adc0.read_u16()
    hall_sen_ybase += adc1.read_u16()
    hall_sen_zbase += adc2.read_u16()
    sleep(0.01)
hall_sen_xbase = hall_sen_xbase//50
hall_sen_ybase = hall_sen_ybase//50
hall_sen_zbase = hall_sen_zbase//50
print("xbase:%s ybase:%s zbase:%s" % (hall_sen_xbase, hall_sen_ybase, hall_sen_zbase))

while True:
    led.toggle()
    test_pin.toggle()
    offset_x = adc0.read_u16() - hall_sen_xbase# - 200
    offset_y = adc1.read_u16() - hall_sen_ybase# - 200
    #print("off_x:%6s off_y:%6s" % (offset_x, offset_y))
    #print("%s,%s" % (add_x, offset_x))
    output_x = PID_calculate(offset_x, pid_x)
    output_y = PID_calculate(offset_y, pid_y)
    #output_x = 60000
    #output_y = 60000
    #print("out_x:%6s out_y:%6s" % (output_x, output_y))
    if output_y > 0:
        pwm0.duty_u16(output_y)
        pwm1.duty_u16(0)
    else:
        pwm0.duty_u16(0)
        pwm1.duty_u16(-output_y)
        
    if output_x > 0:
        pwm2.duty_u16(output_x)
        pwm3.duty_u16(0)
    else:
        pwm2.duty_u16(0)
        pwm3.duty_u16(-output_x)
    #sleep(0.1)
    

