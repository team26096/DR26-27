def run(drive_base, attachment_left, attachment_right):
    # Flip the Rock. No attachments.

    # The robot starts facing backward, so negative drives toward the rock.
    drive_base.straight(-446)

    # Positive drives forward, back toward base.
    drive_base.straight(418)
