from machine import Pin, PWM
from machine import ADC, Pin
from time import sleep

pwm0 = PWM(Pin(0))
pwm1 = PWM(Pin(1))
pwm2 = PWM(Pin(2))
pwm3 = PWM(Pin(3))

pwm0.freq(1000)
pwm1.freq(1000)
pwm2.freq(1000)
pwm3.freq(1000)

adc0 = ADC(Pin(26))
adc1 = ADC(Pin(27))
adc2 = ADC(Pin(28))

while True:
    duty0 = adc0.read_u16()
    pwm0.duty_u16(duty0)
    duty1 = adc1.read_u16()
    pwm1.duty_u16(duty1)
    duty2 = adc2.read_u16()
    pwm2.duty_u16(duty2)
    sleep(0.01)
    

