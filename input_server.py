import asyncio
import json
import platform
import sys

# Try to import pydirectinput for Windows gaming performance
try:
    import pydirectinput
    USE_DIRECTINPUT = True
except ImportError:
    pydirectinput = None
    USE_DIRECTINPUT = False

# Fallback to pyautogui
import pyautogui

# Disable pyautogui's internal pause (we want zero delay)
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False  # allow moving to screen corners

# Optional: use pyautogui's fail-safe? Disabled for gaming.

# ----------------------------------------------------------------------
# Key mapping for special keys (same for both libraries)
# ----------------------------------------------------------------------
KEY_MAP = {
    'ArrowUp': 'up',
    'ArrowDown': 'down',
    'ArrowLeft': 'left',
    'ArrowRight': 'right',
    'Enter': 'enter',
    'Backspace': 'backspace',
    'Tab': 'tab',
    'Shift': 'shift',
    'Control': 'ctrl',
    'Alt': 'alt',
    'Escape': 'esc',
    ' ': 'space',
    'CapsLock': 'capslock',
    'PageUp': 'pageup',
    'PageDown': 'pagedown',
    'Home': 'home',
    'End': 'end',
    'Insert': 'insert',
    'Delete': 'delete',
    'F1': 'f1', 'F2': 'f2', 'F3': 'f3', 'F4': 'f4',
    'F5': 'f5', 'F6': 'f6', 'F7': 'f7', 'F8': 'f8',
    'F9': 'f9', 'F10': 'f10', 'F11': 'f11', 'F12': 'f12',
    'Meta': 'win',  # Windows key
    'Win': 'win',
}

def map_key(key):
    """Map a JavaScript key name to a library-specific key name."""
    return KEY_MAP.get(key, key)

def perform_mouse_move(dx, dy):
    """Move mouse relatively with zero delay."""
    if USE_DIRECTINPUT:
        # pydirectinput.moveRel is more reliable for games
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

# ----------------------------------------------------------------------
# WebSocket handler
# ----------------------------------------------------------------------
async def handler(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                print("Invalid JSON received")
                continue

            msg_type = data.get('type')
            # Optional: logging for debugging (disable for max speed)
            # print(f"Received: {msg_type}")

            if msg_type == 'mousemove':
                dx = data.get('dx', 0)
                dy = data.get('dy', 0)
                # Apply a sensitivity multiplier if desired (1.0 = default)
                # dx *= 1.0
                # dy *= 1.0
                perform_mouse_move(dx, dy)

            elif msg_type == 'mousedown':
                button = data.get('button', 0)
                perform_mouse_down(button)

            elif msg_type == 'mouseup':
                button = data.get('button', 0)
                perform_mouse_up(button)

            elif msg_type == 'keydown':
                key = data.get('key', '')
                perform_key_down(key)

            elif msg_type == 'keyup':
                key = data.get('key', '')
                perform_key_up(key)

            else:
                print(f"Unknown command: {msg_type}")

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Handler error: {e}")

async def main():
    port = 8765
    print(f"Starting ultra‑optimized input server on ws://localhost:{port}")
    if USE_DIRECTINPUT:
        print("Using pydirectinput for Windows DirectX input (best for games)")
    else:
        print("Using pyautogui (cross‑platform)")
    async with websockets.serve(handler, "localhost", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
