import tkinter as tk
import pytesseract
from PIL import ImageGrab
from deep_translator import GoogleTranslator
import cv2
import numpy as np

# ХЭРЭВ WINDOWS АШИГЛАЖ БАЙГАА БОЛ TESSERACT-ИЙН ЗАМЫГ ЗААЖ ӨГӨХ ШААРДЛАГАТАЙ
# Доорх мөрийн чагтыг (comment) арилгаад өөрийн компьютерт суусан замыг бичнэ үү:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_and_translate():
    print("Дэлгэцийг уншиж байна. Түр хүлээнэ үү...")
    # 1. Дэлгэцийн зураг авах
    screen = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    # 2. Текст болон байршлыг олох (Англи хэл дээр)
    data = pytesseract.image_to_data(img, lang='eng', output_type=pytesseract.Output.DICT)
    translator = GoogleTranslator(source='en', target='mn')

    # 3. Дэлгэцэн дээр харуулах хагас нэвтрэх (overlay) цонх үүсгэх
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.65) # Нэвт харагдах хэмжээ (0.0 - 1.0)
    root.config(bg='black')

    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    # Гарах товч (Esc дарахад хаагдана)
    root.bind('<Escape>', lambda e: root.destroy())

    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60: # 60%-иас дээш нарийвчлалтай уншигдсан үгс
            word = data['text'][i].strip()
            # Зөвхөн үг байвал орчуулах
            if word and len(word) > 1:
                try:
                    # Үгийг орчуулах
                    translated_word = translator.translate(word)
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                    # Орчуулгыг дэлгэцэн дээр үүссэн хар хайрцагт цагаанаар бичих
                    canvas.create_rectangle(x, y, x+w, y+h, fill='#333333', outline='#555555')
                    canvas.create_text(x + w/2, y + h/2, text=translated_word, fill='white', font=('Arial', 10, 'bold'))
                except Exception as e:
                    print(f"Орчуулахад алдаа гарлаа: {word} - {e}")

    print("Орчуулж дууслаа. Цонхыг хаахын тулд ESC товчийг дарна уу.")
    root.mainloop()

if __name__ == "__main__":
    capture_and_translate()
