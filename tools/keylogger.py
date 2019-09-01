# This keylogger attempts to give useful insights into keyboard use

from pynput import keyboard
import time

log_file = open('records/keylogs.csv', 'a')

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        line = '{0},{1}\n'.format(time.time(), key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        line = '{0},{1}\n'.format(time.time(), key)
    log_file.write(line)

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        log_file.close()
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
