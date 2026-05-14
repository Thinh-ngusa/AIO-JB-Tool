import os


if os.name == "nt":
    import msvcrt

    def get_key():
        key = msvcrt.getch().decode("utf-8", errors="ignore")
        print(key)
        return key

else:
    import sys
    import tty
    import termios

    def get_key():
        fd = sys.stdin.fileno()

        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            print(key)

        finally:
            termios.tcsetattr(
                fd,
                termios.TCSADRAIN,
                old_settings
            )

        return key