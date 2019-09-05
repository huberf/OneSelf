# This keylogger attempts to give useful insights into keyboard use

from pynput import keyboard
import time

DEBUG = False

log_file = open('records/keylogs.csv', 'a')

last_event = time.time()
collected_events = []

def save_press(key):
    line = '{0},{1}\n'.format(time.time(), key)
    log_file.write(line)

def on_press(key):
    try:
        if DEBUG:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        save_press(line, key.char)
    except AttributeError:
        if DEBUG:
            print('special key {0} pressed'.format(
                key))
        save_press(key)

def on_release(key):
    if DEBUG:
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
print('Running...')
