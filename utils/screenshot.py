import base64
from io import BytesIO

def capture_screen(delay_seconds=3):
    """Captura a tela e retorna como base64 PNG. delay_seconds: espera antes de capturar."""
    if delay_seconds > 0:
        import time
        time.sleep(delay_seconds)

    screenshot = None
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
    except Exception:
        pass

    if screenshot is None:
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
        except Exception:
            raise RuntimeError("Nao foi possivel capturar a tela. Pillow ou pyautogui necessario.")

    from PIL import Image
    if screenshot.size[0] > 1280:
        ratio = 1280.0 / screenshot.size[0]
        new_w = 1280
        new_h = int(screenshot.size[1] * ratio)
        try:
            screenshot = screenshot.resize((new_w, new_h), Image.ANTIALIAS)
        except AttributeError:
            screenshot = screenshot.resize((new_w, new_h), Image.LANCZOS)

    buffer = BytesIO()
    screenshot.save(buffer, format="PNG", optimize=True)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def capture_screen_pil():
    """Captura a tela e retorna objeto PIL Image."""
    try:
        from PIL import ImageGrab
        return ImageGrab.grab()
    except Exception:
        pass
    try:
        import pyautogui
        return pyautogui.screenshot()
    except Exception:
        raise RuntimeError("Nao foi possivel capturar a tela.")

def pil_to_base64(img, max_width=1280):
    """Converte PIL Image para base64 PNG, redimensionando se necessario."""
    from PIL import Image
    if img.size[0] > max_width:
        ratio = float(max_width) / img.size[0]
        new_h = int(img.size[1] * ratio)
        try:
            img = img.resize((max_width, new_h), Image.ANTIALIAS)
        except AttributeError:
            img = img.resize((max_width, new_h), Image.LANCZOS)
    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def pil_to_thumbnail(img, max_w=400, max_h=300):
    """Retorna thumbnail PIL Image."""
    from PIL import Image
    thumb = img.copy()
    try:
        thumb.thumbnail((max_w, max_h), Image.ANTIALIAS)
    except AttributeError:
        thumb.thumbnail((max_w, max_h), Image.LANCZOS)
    return thumb
