import time
from pysticks import get_controller
from djitellopy import Tello


# Connect to drone #9BA0DC
# drone = Tello(host='193.169.0.4')
drone = Tello()

drone.connect()
print('Battery')
drone.get_battery()
drone.streamon()

con = get_controller()
print('Battery: ', drone.get_battery())

drone_flying = False

# Init variables
previous_throttle = 0
previous_yaw = 0
previous_roll = 0
previous_pitch = 0

con.update()
previous_aux = con.getAux()

while True:

    try:

        con.update()

        #
        # Throttle <=> getYaw
        #
        #
        #


        # Throttle and Yaw are interchanged
        throttle = (((1 - con.getYaw()) * 100 / 2) - 50) * 2 # Between -100 and 100
        yaw = -con.getThrottle()
        roll = con.getRoll()
        pitch = con.getPitch()
        aux = con.getAux()

        if not drone_flying and throttle > 0:
            print('Takeoff')
            drone.takeoff()
            drone_flying = True
        elif drone_flying and throttle < -75:
            print('Land')
            drone.land()
            drone_flying = False
        else:
            if previous_aux != aux:
                print('Flip')
                try:
                    drone.send_rc_control(0,0, 0, 0)
                    drone.flip_forward()
                except Exception as e:
                    print('Flip failed')
                    pass

            if previous_roll != roll or previous_pitch != pitch or previous_yaw != yaw or previous_throttle != throttle:
                print('Send RC control', int(roll * 100), int(pitch * 100), 0, int(yaw * 100))
                drone.send_rc_control(int(roll * 100), int(pitch * 100),int(throttle), int(yaw * 100))


        # Store previous values
        previous_throttle = throttle
        previous_yaw = yaw
        previous_roll = roll
        previous_pitch = pitch
        previous_aux = aux

        time.sleep(0.001)

    except KeyboardInterrupt:
        # Emergency stop
        drone.emergency()

        break

    except Exception as e:
        # Emergency stop
        drone.emergency()

        print(e)
        break

drone.streamoff()