#!/usr/bin/env python3

import logging
import os
import tempfile

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Read the Bot Token from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN environment variable is not set.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "Hello! Send me a PDF document, and I'll extract the text for you."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when the /help command is issued."""
    await update.message.reply_text(
        "Send a PDF and I'll do my best to extract the text via OCR.\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - This help message"
    )

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming PDF files, extract text, and send it back."""
    document = update.message.document
    if not document:
        return

    # Only proceed if the file is indeed a PDF
    if document.mime_type != 'application/pdf':
        await update.message.reply_text("Please send a valid PDF file.")
        return

    # Download PDF to a temporary file
    with tempfile.TemporaryDirectory() as tmp_dir:
        pdf_path = os.path.join(tmp_dir, document.file_name)
        await document.get_file().download(pdf_path)

        extracted_text = ""

        # Step 1: Try extracting text directly (text-based PDF)
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
        except Exception as e:
            logging.error(f"Error reading PDF: {e}")

        # Step 2: If no text was found, attempt OCR (image-based PDF)
        if not extracted_text.strip():
            try:
                # Convert PDF to images
                pages = convert_from_path(pdf_path)
                for img_page in pages:
                    text = pytesseract.image_to_string(img_page)
                    extracted_text += text + "\n"
            except Exception as e:
                logging.error(f"Error during OCR process: {e}")
                await update.message.reply_text(
                    "Sorry, I couldn't process the PDF. Please try again."
                )
                return

        # Send extracted text back to the user
        if extracted_text.strip():
            # Some PDFs can be large, so we might want to chunk text
            max_length = 4096  # Telegram's max message length
            for i in range(0, len(extracted_text), max_length):
                await update.message.reply_text(extracted_text[i : i + max_length])
        else:
            await update.message.reply_text(
                "No text found. The PDF might be empty or unreadable."
            )

def main():
    """Start the bot."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # PDF handler
    application.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

    # Run the bot until you press Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
