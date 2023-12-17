import tkinter
from playsound import playsound
import pytesseract
from ImageUploaderApp import ImageUploaderApp
from pynput import keyboard
# Set the path to the Tesseract executable (replace with your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

if __name__ == "__main__":
    root = tkinter.Tk()
    app = ImageUploaderApp(root)
    with keyboard.GlobalHotKeys({'<ctrl>+<shift>+c': app.keyboardShortcutAudioPlay}) as h:
        root.mainloop()
