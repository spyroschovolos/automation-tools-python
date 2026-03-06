# Rockstar Launcher Auto-Retry Tool (Python Automation)

A practical automation script designed to resolve connectivity and launch issues with the Rockstar Games Launcher. This tool uses **Computer Vision (OCR)** and **UI Automation** to detect error states and automatically trigger retries until a successful launch is achieved.

## 🛠️ The Problem
The Rockstar Games Launcher often stops when downloading games (in my case it was GTA V), requiring the user to manually click "Retry" multiple times. This script automates this tedious process, ensuring the application launches without manual intervention.

## 🚀 Key Features

- **Visual Error Detection:** Utilizes **Pytesseract (OCR)** to "read" text from the screen and identify specific error messages.

- **Automated UI Interaction:** Uses **PyAutoGUI** to simulate mouse movements and clicks on the "Retry" button.

- **Smart Retrying Logic:** Implements a loop with randomized delays to mimic human behavior and avoid system flags.

- **Real-time Monitoring:** Provides feedback in the terminal about the current status of the launcher and detection results.

## 💻 Technical Stack

- **Python 3.x**
- **Pytesseract:** For Optical Character Recognition.
- **PyAutoGUI:** For cross-platform GUI automation.
- **Pillow (PIL):** For image processing and screen capturing.

## 📖 How it Works

1. The script takes a screenshot of the active launcher window.
2. It processes the image to extract text and searches for keywords like "Retry".
3. If an error state is detected, it moves the mouse to the button coordinates and performs a click.
4. The loop continues until the launcher moves past the error screen.

## 🔧 Requirements & Installation

```bash
pip install pytesseract pyautogui pillow
