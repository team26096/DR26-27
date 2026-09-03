"""Position the run1_1 attachments, and then start the mission."""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port

from attachment_development import run_attachment_controller


# Each pair lists the teeth on two gears that touch each other.
# This gear train belongs only to the attachments used for run1_1.
RUN1_1_ATTACHMENT_GEARS = [[20, 12], [12, 36], [12, 20]]

# Jog each attachment at 50 degrees per second while an arrow is held.
RUN1_1_JOG_SPEED_DEGREES_PER_SECOND = 50


def main():
    """Run the attachment setup controls, and then start run1_1."""

    hub = PrimeHub()

    # Port B is the right attachment motor for this run.
    attachment_right = Motor(Port.B, gears=RUN1_1_ATTACHMENT_GEARS)

    # Port C is the left attachment motor for this run.
    attachment_left = Motor(Port.C, gears=RUN1_1_ATTACHMENT_GEARS)

    # The first item is selected first, so the hub starts by showing B.
    attachments = [
        ("B", attachment_right, RUN1_1_JOG_SPEED_DEGREES_PER_SECOND),
        ("C", attachment_left, RUN1_1_JOG_SPEED_DEGREES_PER_SECOND),
    ]

    try:
        run_attachment_controller(hub, attachments)
    finally:
        # Always close the development motors before another program uses them.
        attachment_right.close()
        attachment_left.close()

    # Importing run1_1 starts the existing mission program one time.
    import run1_1


if __name__ == "__main__":
    main()
