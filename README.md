PDF OCR Telegram Bot
This repository contains a Telegram bot that extracts text from PDF files. It supports:

- **Text-based PDFs** (direct text extraction)
- **Image-based PDFs** (OCR with [Tesseract](https://github.com/tesseract-ocr/tesseract))
Features
- Automatically detects if a PDF is text-based or image-based.
- Returns extracted text to the user in Telegram.
- Splits lengthy text into multiple messages to avoid Telegram size limits.
Requirements
- Python 3.8+ recommended
- [Tesseract](https://github.com/tesseract-ocr/tesseract) installed on your machine
- [Poppler](https://poppler.freedesktop.org/) (for the `pdf2image` Python package)
- A Telegram bot token
Installation & Setup
1. **Clone this repository**:
   ```bash
   git clone https://github.com/atheer92/pdf-ocr-telegram-bot.git
   cd pdf-ocr-telegram-bot
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Make sure Tesseract and Poppler are installed on your system and available in your PATH.

3. **Set your bot token**:
   - Create a new Telegram Bot via [BotFather](https://core.telegram.org/bots#3-how-do-i-create-a-bot) if you haven’t already.
   - Copy the token provided by BotFather (e.g., `1234567:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).
   - Set the `BOT_TOKEN` environment variable, for example:
     ```bash
     export BOT_TOKEN="YOUR_BOT_TOKEN"
     ```
   - Alternatively, store the token in a `.env` file and make sure `.env` is listed in your `.gitignore`.

4. **Run the Bot**:
   ```bash
   python bot.py
   ```
   The bot will run in polling mode until you stop it with `Ctrl + C`.
Usage
1. Open Telegram and find your bot (use the username BotFather assigned to it).
2. Send `/start` to receive a welcome message.
3. Send a PDF as a **Document**. The bot will determine if it’s text-based or image-based.
4. You will receive the extracted text in the chat. If the PDF is large, the bot will split the text into multiple messages.
Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes, commit, and push to your fork.
4. Submit a Pull Request describing your changes.
License
This project is licensed under the [MIT License](LICENSE).
Troubleshooting
- **No text extracted**: Verify that the PDF is not password-protected. Ensure Tesseract is installed correctly (`tesseract --version`).
- **Error during OCR**: Make sure Poppler is installed so `pdf2image` can convert PDF pages to images.
- **Large PDF**: Telegram limits message length. The bot splits messages to avoid exceeding Telegram’s size limits.

---

Happy OCRing!
