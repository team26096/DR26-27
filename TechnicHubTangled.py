from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color
from pybricks.tools import StopWatch


hub = TechnicHub()

# Gear list reads from the motor outward.
attachment_left = Motor(Port.B, gears=[[12, 20], [1, 24]])


# ---------- RESET ----------

hub.light.off()
attachment_left.reset_angle(0)

run_timer = StopWatch()


# ---------- RUN ----------

attachment_left.run_angle(speed=650, rotation_angle=-90)


# ---------- RESULT ----------

run_timer.pause()
elapsed = round(run_timer.time() / 1000, 1)
print("Total run time:", elapsed, "seconds")

# The Technic Hub has a status light instead of a display.
hub.light.on(Color.GREEN)
