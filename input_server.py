import asyncio
import json
import threading
import queue
import websockets as ws_library

try:
    import pydirectinput
    USE_DIRECTINPUT = True
except ImportError:
    USE_DIRECTINPUT = False

import pyautogui

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

KEY_MAP = {
    'ArrowUp': 'up', 'ArrowDown': 'down', 'ArrowLeft': 'left', 'ArrowRight': 'right',
    'Enter': 'enter', 'Backspace': 'backspace', 'Tab': 'tab',
    'Shift': 'shift', 'Control': 'ctrl', 'Alt': 'alt',
    'Escape': 'esc', ' ': 'space',
    'CapsLock': 'capslock', 'PageUp': 'pageup', 'PageDown': 'pagedown',
    'Home': 'home', 'End': 'end', 'Insert': 'insert', 'Delete': 'delete',
    'F1': 'f1', 'F2': 'f2', 'F3': 'f3', 'F4': 'f4',
    'F5': 'f5', 'F6': 'f6', 'F7': 'f7', 'F8': 'f8',
    'F9': 'f9', 'F10': 'f10', 'F11': 'f11', 'F12': 'f12',
    'Meta': 'win', 'Win': 'win',
}

def map_key(key):
    return KEY_MAP.get(key, key)

def perform_mouse_move(dx, dy):
    if USE_DIRECTINPUT:
        pydirectinput.moveRel(dx, dy, relative=True, duration=0)
    else:
        pyautogui.moveRel(dx, dy, duration=0, _pause=False)

def perform_mouse_down(button):
    if USE_DIRECTINPUT:
        if button == 0:
            pydirectinput.mouseDown(button='left')
        elif button == 2:
            pydirectinput.mouseDown(button='right')
        else:
            pydirectinput.mouseDown(button='middle')
    else:
        if button == 0:
            pyautogui.mouseDown(button='left', _pause=False)
        elif button == 2:
            pyautogui.mouseDown(button='right', _pause=False)
        else:
            pyautogui.mouseDown(button='middle', _pause=False)

def perform_mouse_up(button):
    if USE_DIRECTINPUT:
        if button == 0:
            pydirectinput.mouseUp(button='left')
        elif button == 2:
            pydirectinput.mouseUp(button='right')
        else:
            pydirectinput.mouseUp(button='middle')
    else:
        if button == 0:
            pyautogui.mouseUp(button='left', _pause=False)
        elif button == 2:
            pyautogui.mouseUp(button='right', _pause=False)
        else:
            pyautogui.mouseUp(button='middle', _pause=False)

def perform_key_down(key):
    mapped = map_key(key)
    if USE_DIRECTINPUT:
        pydirectinput.keyDown(mapped)
    else:
        pyautogui.keyDown(mapped, _pause=False)

def perform_key_up(key):
    mapped = map_key(key)
    if USE_DIRECTINPUT:
        pydirectinput.keyUp(mapped)
    else:
        pyautogui.keyUp(mapped, _pause=False)

# Command queue for non‑blocking processing
command_queue = queue.Queue()

def process_commands():
    while True:
        data = command_queue.get()
        if data is None:
            break
        msg_type = data.get('type')
        if msg_type == 'mousemove':
            perform_mouse_move(data.get('dx', 0), data.get('dy', 0))
        elif msg_type == 'mousedown':
            perform_mouse_down(data.get('button', 0))
        elif msg_type == 'mouseup':
            perform_mouse_up(data.get('button', 0))
        elif msg_type == 'keydown':
            perform_key_down(data.get('key', ''))
        elif msg_type == 'keyup':
            perform_key_up(data.get('key', ''))

# Start the processing thread
worker_thread = threading.Thread(target=process_commands, daemon=True)
worker_thread.start()

async def handler(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                continue
            command_queue.put(data)
    except Exception as e:
        print(f"Client disconnected: {e}")

async def main():
    PORT = 8765
    print(f"Starting ultra‑optimized input server on ws://localhost:{PORT}")
    if USE_DIRECTINPUT:
        print("Using pydirectinput for Windows DirectX input (best for games)")
    else:
        print("Using pyautogui (cross-platform)")

    async with ws_library.serve(handler, "localhost", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
