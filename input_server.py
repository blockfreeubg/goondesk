import asyncio
import json
import pyautogui
import websockets

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

async def handler(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get('type')
            print(f"Received: {msg_type}")

            if msg_type == 'mousemove':
                dx = data.get('dx', 0)
                dy = data.get('dy', 0)
                # Relative movement – instant, no duration
                pyautogui.moveRel(dx, dy, duration=0)

            elif msg_type == 'mousedown':
                button = data.get('button', 0)
                if button == 0:
                    pyautogui.mouseDown(button='left')
                elif button == 2:
                    pyautogui.mouseDown(button='right')
                else:
                    pyautogui.mouseDown(button='middle')

            elif msg_type == 'mouseup':
                button = data.get('button', 0)
                if button == 0:
                    pyautogui.mouseUp(button='left')
                elif button == 2:
                    pyautogui.mouseUp(button='right')
                else:
                    pyautogui.mouseUp(button='middle')

            elif msg_type == 'keydown':
                key = data.get('key', '')
                key_map = {
                    'ArrowUp': 'up', 'ArrowDown': 'down', 'ArrowLeft': 'left', 'ArrowRight': 'right',
                    'Enter': 'enter', 'Backspace': 'backspace', 'Tab': 'tab',
                    'Shift': 'shift', 'Control': 'ctrl', 'Alt': 'alt',
                    'Escape': 'esc', ' ': 'space',
                }
                pyautogui.keyDown(key_map.get(key, key))

            elif msg_type == 'keyup':
                key = data.get('key', '')
                key_map = {
                    'ArrowUp': 'up', 'ArrowDown': 'down', 'ArrowLeft': 'left', 'ArrowRight': 'right',
                    'Enter': 'enter', 'Backspace': 'backspace', 'Tab': 'tab',
                    'Shift': 'shift', 'Control': 'ctrl', 'Alt': 'alt',
                    'Escape': 'esc', ' ': 'space',
                }
                pyautogui.keyUp(key_map.get(key, key))

            else:
                print(f"Unknown command: {msg_type}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    print("Starting input server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
