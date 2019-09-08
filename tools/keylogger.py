# This keylogger attempts to give useful insights into keyboard use

from pynput import keyboard
from threading import Timer
import time

DEBUG = False

log_file = open('records/keylogs.csv', 'a')

last_presses = [None, None, None] # Save a history of three presses

last_event = time.time()
MAX_PRESS_TIME = 0.5 # 0.5 seconds wait needed before save occurs
collected_events = []
scheduled_timer = None

def save_press(key):
    global scheduled_timer, collected_events
    collected_events += [key]
    if scheduled_timer and not scheduled_timer.finished.is_set():
        scheduled_timer.cancel()
    scheduled_timer = Timer(MAX_PRESS_TIME, _full_key_save)
    scheduled_timer.start()

def _full_key_save():
    global collected_events
    keys = ' '.join([str(i) for i in collected_events])
    line = '{0},\'{1}\'\n'.format(time.time(), keys)
    log_file.write(line)
    collected_events = []

def on_press(key):
    global last_presses
    try:
        if DEBUG:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        save_press(key.char)
        last_presses[1:2] = last_presses[:2]
        last_presses[0] = key.char
    except AttributeError:
        if DEBUG:
            print('special key {0} pressed'.format(
                key))
        save_press(key)
        last_presses[1:3] = last_presses[:2]
        last_presses[0] = key


def on_release(key):
    if DEBUG:
        print('{0} released'.format(
            key))
    if last_presses[2] == keyboard.Key.esc and \
            last_presses[1] == 'q' and \
            last_presses[0] == 'u':
        # Stop listener
        log_file.close()
        return False

print('To quit logging and properly save file, press: Esc q u')

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
print('Running...')
listener.start()
# Once we get past blocking listener, close the file
log_file.close()
