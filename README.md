# GoonDesk

A lightweight, static WebRTC-based screen sharing and remote control solution.

Broadcast your PC screen to any device and control it remotely with low latency.

---

## Credits

* **duderucool** – Project creator and developer
* **DeepSeek** – AI assistance in code implementation and optimization

---

## How It Works

* Uses **WebRTC** for peer-to-peer video streaming.
* Uses **PeerJS** for signaling (no backend required).
* Uses a local **Python input server** to inject mouse/keyboard events on the broadcaster PC.
* Supports pointer lock for gaming-like mouse control.

---

## Files

* `broadcaster.html` – Run on the PC you want to share/control.
* `viewer.html` – Run on any device to view and control.
* `input_server.py` – Local Python server for OS-level input injection.

---

## 🖥️ Setting Up the Home Computer (Broadcaster)

### Prerequisites

1. **Python 3.7+** installed.
2. A modern browser such as Chrome, Edge, Firefox, or Safari.

### Step 1: Install Python Dependencies

Open a terminal and run:

```bash
pip install websockets pyautogui pydirectinput
```

On macOS/Linux:

```bash
pip install websockets pyautogui
```

### Step 2: Start the Input Server

Navigate to the folder containing `input_server.py`, then run:

```bash
python input_server.py
```

Keep this terminal open while streaming.

### Step 3: Open the Broadcaster Page

#### Option A: Local File

Double-click `broadcaster.html`.

> **Note:** Some features may not work correctly from `file://`. Using a local server is recommended.

#### Option B: Local Server

Run one of the following commands:

```bash
npx serve
```

Or:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/broadcaster.html
```

#### Option C: Hosted Online

Upload the HTML files to a static hosting service such as GitHub Pages or Netlify, then open the broadcaster URL.

### Step 4: Start Sharing

1. Click **Start Sharing Screen**.
2. Choose **Entire Screen**.

   * For gaming, **borderless windowed mode** is recommended.
3. A preview will appear.
4. The broadcaster is now ready.

---

## 📺 Setting Up the Viewer Device

### Prerequisites

* Any modern browser on desktop or mobile.
* An internet connection if using hosted pages.
* The same local network if using a local server.

### Step 1: Open the Viewer Page

If using a local server, open:

```text
http://<broadcaster-ip>:8000/viewer.html
```

Replace `<broadcaster-ip>` with the broadcaster computer's local IP address.

If hosted online, open the hosted `viewer.html` URL.

### Step 2: Connect

1. Click **☰ Controls** in the top-left corner.
2. Click **🔗 Connect**.
3. Wait until the status says:

> **Connected (remote control ready)**

### Step 3: Start Remote Control

1. Click **🖱️ Enable Remote Control**.
2. Click on the video to lock the mouse pointer.
3. Use your mouse and keyboard normally.
4. Mouse clicks and keystrokes will be sent to the broadcaster.

Press **Esc** to unlock the mouse and disable remote control.

---

## ⛶ Fullscreen

Click **⛶ Fullscreen** to make the stream fill the viewer's entire screen.

---

## ❓ Troubleshooting

### Stream Is Black or Grey

Click the **▶ Play** button once.

Browsers may block autoplay until you interact with the page.

### Mouse/Keyboard Not Working on macOS

Grant **Accessibility** permissions to your terminal application:

**System Settings → Privacy & Security → Accessibility**

### Fullscreen Games Freeze

Use **borderless windowed mode**.

The broadcaster will automatically re-share if a freeze is detected.

### High Latency or Low Resolution

Reduce the capture resolution using URL parameters.

For example:

```text
broadcaster.html?width=1280&height=720
```

### Connection Fails Across the Internet

The free TURN server may be overloaded.

Try testing the connection on the **same local network** first.

---

## 🔑 Custom Peer ID

Add `?id=YourSecretKey` to both the broadcaster and viewer URLs to use a custom stream key.

### Example

**Broadcaster:**

```text
broadcaster.html?id=my-game-123
```

**Viewer:**

```text
viewer.html?id=my-game-123
```

Both devices must use the same ID.

---

## 🎮 Enjoy GoonDesk!

Made with **WebRTC**, **PeerJS**, and Python.
