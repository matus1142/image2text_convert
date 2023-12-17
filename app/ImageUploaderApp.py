import os
from playsound import playsound
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageGrab
import io
import gtts
import pytesseract
import pykakasi
import pyperclip
kks = pykakasi.kakasi()


languageType = {
    'jpn_horizontal': {
        'config': '--psm 6 -l jpn',
        'lang': 'jpn',
        'audio': 'ja'
    },
    'jpn_vertical': {
        'config': '--psm 5 -l jpn_vert',
        'lang': 'jpn',
        'audio': 'ja'
    }
}


class ImageUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Text Convert")

        # UI components

        # Dropdown list for selecting image format
        self.format_label = tk.Label(root, text="Select image format:")
        self.format_label.grid(row=0, pady=5)

        self.language_formats = ["jpn_horizontal", "jpn_vertical"]
        self.selected_format = tk.StringVar(value=self.language_formats[0])

        self.format_dropdown = ttk.Combobox(
            root, textvariable=self.selected_format, values=self.language_formats)
        self.format_dropdown.grid(row=1, pady=5)
        # Add a callback for the <<ComboboxSelected>> event
        self.format_dropdown.bind(
            "<<ComboboxSelected>>", self.on_format_selected)

        # Image component
        self.image_label = tk.Label(root, text="Paste image from clipboard:")
        self.image_label.grid(row=2, pady=5)

        # Paste button component
        self.paste_button = tk.Button(
            root, text="Paste", command=self.paste_from_clipboard)
        self.paste_button.grid(row=3, pady=5)

        # Upload button component
        self.upload_button = tk.Button(
            root, text="Upload", command=self.upload_image)
        self.upload_button.grid(row=4, pady=5)

        # Translate image component
        self.upload_button = tk.Button(
            root, text="Read Image", command=self.readImage)
        self.upload_button.grid(column=0, row=5, pady=5)

        # Convert kanji to hiragana button
        self.hiragana_button = tk.Button(
            root, text="Hiragana", command=self.convertHiragana)
        self.hiragana_button.grid(column=1, row=5, pady=5)

        # Text field convert from image to text component
        self.read_image_text_field = tk.Text(root, width=50, height=7)
        self.read_image_text_field.grid(
            row=6, column=0, padx=20, pady=5)

        # Text field convert from kanji to hiragana component
        self.kanji2hiragana = tk.Text(root, width=50, height=7)
        self.kanji2hiragana.grid(
            row=6, column=1, padx=20, pady=5)

        # Audio text button component
        self.audio_button = tk.Button(
            root, text="Audio", command=self.textAudioPlay)
        self.audio_button.grid(row=7, pady=5)

        self.clipboard_image = None  # Store the clipboard image

    def paste_from_clipboard(self):
        try:
            # Get image from clipboard
            image = self.get_image_from_clipboard()

            # Save the clipboard image for later use
            self.clipboard_image = image

            # Display the image on the UI
            self.display_image(image)
        except Exception as e:
            print(f"Error pasting image: {e}")

    def get_image_from_clipboard(self):
        # Use Pillow to get the image from the clipboard
        image = ImageGrab.grabclipboard()

        if image:
            return image
        else:
            raise Exception("No image found in clipboard")

    def display_image(self, image):
        # Convert Pillow image to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(image)

        # Update the label with the new image
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def upload_image(self):
        if self.clipboard_image:
            # Ask the user to select a destination folder
            destination_folder = filedialog.askdirectory(
                title="Select Destination Folder")

            if destination_folder:
                # Generate a unique filename
                filename = "uploaded_image.png"

                # Save the original clipboard image to the destination folder
                file_path = tk.filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    initialdir=destination_folder,
                    initialfile=filename,
                    title="Save Image"
                )
                if file_path:
                    self.clipboard_image.save(file_path)
                    print(f"Image uploaded successfully to: {file_path}")
                else:
                    print("Upload canceled.")
            else:
                print("Upload canceled.")
        else:
            print("No image to upload. Please paste an image from the clipboard first.")

    def on_format_selected(self, event):
        # Callback function to print the selected format
        selected_format = self.selected_format.get()
        print(f"Selected format: {selected_format}")

    def readImage(self):
        if self.clipboard_image:
            # Optional: Display the image
            selected_format = self.selected_format.get()
            config = languageType[selected_format]['config']
            lang = languageType[selected_format]['lang']

            # Use pytesseract.image_to_string to extract text from the image
            text = pytesseract.image_to_string(
                self.clipboard_image, config=config, lang=lang)
            text = str(text).replace(" ", "")
            text = str(text).replace("\n", "")
            result = kks.convert(text)
            hiragana_sentence = ''
            for item in result:
                hiragana_sentence += item['hira']
            self.read_image_text_field.delete(1.0, tk.END)
            self.read_image_text_field.insert(tk.END, text)
            self.kanji2hiragana.delete(1.0, tk.END)
            self.kanji2hiragana.insert(tk.END, hiragana_sentence)

            # You can continue to perform other operations with the extracted text as needed
        else:
            print("No image found in the clipboard.")

    def textAudioPlay(self):
        if self.read_image_text_field:
            text = self.read_image_text_field.get("1.0", tk.END)
            selected_format = self.selected_format.get()
            mp3Name = 'temporarAudio.mp3'
            audio_language = languageType[selected_format]['audio']
            tts = gtts.gTTS(text, lang=audio_language)
            tts.save(mp3Name)
            playsound(mp3Name)
            os.remove(mp3Name)
        else:
            print("No text in field")

    def keyboardShortcutAudioPlay(self):
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            text = clipboard_text
            text = str(text).replace(" ", "")
            text = str(text).replace("\n", "")
            result = kks.convert(text)
            hiragana_sentence = ''
            for item in result:
                hiragana_sentence += item['hira']
            self.read_image_text_field.delete(1.0, tk.END)
            self.read_image_text_field.insert(tk.END, text)
            self.kanji2hiragana.delete(1.0, tk.END)
            self.kanji2hiragana.insert(tk.END, hiragana_sentence)
            selected_format = self.selected_format.get()
            mp3Name = 'temporarAudio.mp3'
            audio_language = languageType[selected_format]['audio']
            tts = gtts.gTTS(text, lang=audio_language)
            tts.save(mp3Name)
            playsound(mp3Name)
            os.remove(mp3Name)
        else:
            print("No clipboard found")

    def convertHiragana(self):
        if self.read_image_text_field:
            text = self.read_image_text_field.get("1.0", tk.END)
            text = str(text).replace(" ", "")
            text = str(text).replace("\n", "")
            result = kks.convert(text)
            hiragana_sentence = ''
            for item in result:
                hiragana_sentence += item['hira']
            self.kanji2hiragana.delete(1.0, tk.END)
            self.kanji2hiragana.insert(tk.END, hiragana_sentence)
        else:
            print("No text in field")
