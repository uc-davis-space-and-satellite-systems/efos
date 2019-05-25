import pigpio
import time

ESC_PIN        = 12      # ESC_PIN to write to
PWM_RANGE_MAX  = 40000   # maximum writable pwm value
PWM_RANGE_MIN  = 26400   # minimum writable pwm value
PWM_FREQ       = 500     # frequency of pwm pulses (1000 pulses / s)
PWM_READ_DELAY = 2       # delay in seconds after setting duty cycle

pi = pigpio.pi()


class ESC:
    def __init__(self):
        pi.set_PWM_range(ESC_PIN, PWM_RANGE_MAX)
        pi.set_PWM_frequency(ESC_PIN, PWM_FREQ)
        self.init_sequence()

    def init_sequence(self):
        pi.set_PWM_dutycycle(ESC_PIN, 127)
        time.sleep(PWM_READ_DELAY)

    def set_dutycycle_percentage(self, percent):
        adjusted_dutycycle = (PWM_RANGE_MAX - PWM_RANGE_MIN) * percent / 100 + PWM_RANGE_MIN - 1
        pi.set_PWM_dutycycle(ESC_PIN, adjusted_dutycycle)
        time.sleep(PWM_READ_DELAY)


esc = ESC()
while True:
    try:
        percent = int(input("Enter duty cycle percentage: "))
        if percent < 0 or percent > 100:
            raise ValueError
        esc.set_dutycycle_percentage(percent)
    except ValueError:
        print("Error: percentage ranges from 0 to 100 inclusive.")
        break
pi.stop()
