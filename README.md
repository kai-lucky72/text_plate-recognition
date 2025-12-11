Printed Text Scanner GUI (PyTesseract + Python GUI)

A simple GUI-based printed text scanner built using Python and PyTesseract.
This project was created as part of Week 13 – AI Without ML Assignment, and demonstrates how classical OCR works without machine learning models.

The application supports:

✅ Loading images
✅ Live camera input
✅ OCR using PyTesseract
✅ ROI (Region of Interest) selection
✅ Overlay preview of detected text
✅ Displaying extracted text inside the GUI

📸 Features
1. GUI Interface

A clean and simple window for interacting with the OCR tool.

2. Load an Image

Users can upload any printed-text image (JPG, PNG, etc.).

3. Live Camera Input

Allows capturing a frame directly from the laptop/PC camera.

4. Run OCR

Click a button to extract text.

5. ROI Selection

Select a region in the image before scanning.

6. Overlay Preview

Detected text appears on top of the image for visual verification.

7. Text Output

Extracted text is shown clearly in the GUI’s text area.

📦 Installation
1. Clone the Repository
git clone https://github.com/005murangwa/printed-text-scanner-gui.git
cd printed-text-scanner-gui

2. Install Requirements

Make sure Python 3.8+ is installed.

pip install -r requirements.txt

3. Install Tesseract OCR
Windows

Download installer:
https://github.com/UB-Mannheim/tesseract/wiki

After installing, add this to your PATH (usually done automatically):

C:\Program Files\Tesseract-OCR\tesseract.exe

macOS
brew install tesseract

Linux
sudo apt install tesseract-ocr

▶️ How to Run the App
python main.py


Your GUI window will open.

Your file names may differ depending on your code — this is just a clean structure for documentation.

🧠 How OCR Works in This Project

Image is loaded or captured

Converted to grayscale

Preprocessed (thresholding, noise removal, etc.)

ROI is extracted if selected

PyTesseract runs OCR

Detected text is displayed + overlay drawn

🧑‍💻 Author

Name: kagabo irene lucky
Class: Year 3d
Course: AI Without ML – Printed Text Scanner Assignment
