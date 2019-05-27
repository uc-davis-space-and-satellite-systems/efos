import pigpio, time

PWM_RANGE_MAX  = 40000   # maximum writable pwm value
PWM_RANGE_MIN  = 26400   # minimum writable pwm value
PWM_FREQ       = 500     # frequency of pwm pulses (500 pulses / s)
PWM_READ_DELAY = 2       # delay in seconds after setting duty cycle

pi = pigpio.pi() # TODO should this be a global variable?

class ESC:
    def __init__(self, speed_pin, dir_pin1, dir_pin2):
        self.speed_pin = speed_pin
        self.dir_pin1 = dir_pin1
        self.dir_pin2 = dir_pin2

        pi.set_PWM_range(self.speed_pin, PWM_RANGE_MAX)
        pi.set_PWM_frequency(self.speed_pin, PWM_FREQ)

    def init_sequence(self):
        self.set_dutycycle_percentage(50) # this value is idle for the esc
        time.sleep(PWM_READ_DELAY) # wait a few seconds to make sure the ESC processes the command

        # TODO perform direction pin init here too

    def set_dutycycle_percentage(self, percent):
        adjusted_dutycycle = (PWM_RANGE_MAX - PWM_RANGE_MIN) * percent / 100 + PWM_RANGE_MIN - 1
        pi.set_PWM_dutycycle(self.speed_pin, adjusted_dutycycle)
        time.sleep(PWM_READ_DELAY)

    def set_direction(self, direction):
        pass

    def shutdown_sequence(self):
        pi.stop()

if __name__ == "__main__":
    esc = ESC(12, -1, -1) # direction not implemented yet
    esc.init_sequence()
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
