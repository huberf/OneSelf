# This keylogger attempts to give useful insights into keyboard use

from pynput import keyboard
from threading import Timer
import time

DEBUG = False

log_file = open('records/keylogs.csv', 'a')

last_event = time.time()
MAX_PRESS_TIME = 0.5 # 0.5 seconds wait needed before save occurs
collected_events = []
scheduled_timer = None

def save_press(key):
    global scheduled_timer
    collected_events += [key]
    if scheduled_timer and not scheduled_timer.finished.is_set():
        scheduled_timer.cancel()
    scheduled_timer = Timer(MAX_PRESS_TIME, _full_key_save)
    scheduled_timer.start()

def _full_key_save():
    global collected_events
    keys = ''
    for i in collected_events:
        keys += i
    line = '{0},{1}\n'.format(time.time(), keys)
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
