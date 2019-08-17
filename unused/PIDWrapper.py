from PID import update
set_yaw = 0
current_yaw = 180
pid = update(value,achieve)
while True:
    # pid.setWindup(set_yaw) ##decide on what winup we should use, what is the maximal change that can occur in an ideal environment?
    print(pid.update())
while False:
    pid.clear()
##Start by modifying the KP constant and get the performance as good as you can before moving onto KD and then finally KI.
##If the motor adjustments are too aggressive, swinging between too fast and too slow, reduce the constant.
##   If the motor speed isn’t changing fast enough, increase the constant.
##  Make any change in small increments; even a very small change can have a dramatic effect.
