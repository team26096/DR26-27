"""Use the SPIKE Prime hub buttons to position attachment motors."""

from pybricks.parameters import Button
from pybricks.tools import wait


# Check the hub buttons every 10 milliseconds so they feel quick to use.
BUTTON_CHECK_TIME_MS = 10


def _hold_all_attachments(attachments):
    """Keep every attachment at its current angle."""

    for label, motor, jog_speed_degrees_per_second in attachments:
        motor.hold()


def run_attachment_controller(hub, attachments):
    """Let the hub buttons position attachments before a mission starts.

    Each item in attachments has three parts:
    (display letter, motor, jog speed in degrees per second).
    """

    if not attachments:
        raise ValueError("Add at least one attachment motor.")

    # During setup, pressing center and Bluetooth together stops the program.
    # This lets us use the center button by itself to start the mission.
    hub.system.set_stop_button((Button.CENTER, Button.BLUETOOTH))

    # Start with the first attachment in the list.
    selected_index = 0
    bluetooth_was_pressed = False
    last_command = None
    selected_label, selected_motor, jog_speed_degrees_per_second = attachments[
        selected_index
    ]

    hub.display.char(selected_label)

    try:
        while True:
            pressed_buttons = hub.buttons.pressed()

            # The center button finishes setup and returns to the launcher.
            if Button.CENTER in pressed_buttons:
                _hold_all_attachments(attachments)

                # Wait until center is released so it does not stop the mission.
                while Button.CENTER in hub.buttons.pressed():
                    wait(BUTTON_CHECK_TIME_MS)
                return

            bluetooth_is_pressed = Button.BLUETOOTH in pressed_buttons

            # Change motors only once for each Bluetooth-button press.
            if bluetooth_is_pressed and not bluetooth_was_pressed:
                selected_motor.hold()

                # Add 1 list position, and wrap back to the first attachment.
                selected_index = (selected_index + 1) % len(attachments)
                selected_label, selected_motor, jog_speed_degrees_per_second = (
                    attachments[selected_index]
                )
                hub.display.char(selected_label)
                last_command = None

            bluetooth_was_pressed = bluetooth_is_pressed

            left_is_pressed = Button.LEFT in pressed_buttons
            right_is_pressed = Button.RIGHT in pressed_buttons

            if left_is_pressed and not right_is_pressed:
                command = "counterclockwise"
            elif right_is_pressed and not left_is_pressed:
                command = "clockwise"
            else:
                command = "hold"

            # Send a new motor command only when the button action changes.
            if command != last_command:
                if command == "counterclockwise":
                    selected_motor.run(-jog_speed_degrees_per_second)
                elif command == "clockwise":
                    selected_motor.run(jog_speed_degrees_per_second)
                else:
                    selected_motor.hold()
                last_command = command

            wait(BUTTON_CHECK_TIME_MS)
    finally:
        # Keep the attachments still if setup ends normally or with an error.
        _hold_all_attachments(attachments)

        # During the mission, center goes back to being the normal stop button.
        hub.system.set_stop_button(Button.CENTER)
