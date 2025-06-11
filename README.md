# Image Steganography Application

A GUI application for encoding and decoding text messages in images using LSB (Least Significant Bit) and alpha channel steganography.

## Features

Functionality:
- LSB encoding (RGB channels)
- Alpha channel encoding
- Message decoding
- Image format validation
- Capacity calculation
- Image preview generation

Compatible Image Types:
- PNG
- BMP
- TIFF
- WEBP (RGB/RGBA only)

### User Interface
- **Modern Look and Feel:** The application sports a clean, dark theme for improved aesthetics.
- **Customizable Layout:** Features dockable widgets for the image preview, message input area, and encoding options, allowing you to arrange the workspace to your preference.

## Requirements
- Python 3.8+
- PyQt5
- Pillow
- NumPy

## Installation
1. Clone the repository
2. Install dependencies and package:
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in editable mode
   ```

## Quick Start (Ubuntu with Script)

For a fast setup on Ubuntu, a helper script is available. This script automates cloning/updating the repository, installing dependencies, and launching the application.

For detailed instructions on using this script, please see the `image_steganography/README.md` file.

## Usage
Run the application:
```bash
python main.py
```

### Encoding
1. Select an image
2. Choose encoding method
3. Enter your message
4. Click "Encode"
5. Save the encoded image

### Decoding
1. Select an encoded image
2. Choose the correct encoding method
3. Click "Decode"
4. View the decoded message

## Notes
- For LSB encoding, use lossless formats like PNG
- For alpha channel encoding, use images with transparency
- Larger images can store more data
- The application shows the maximum message capacity for the selected image and method

## License
MIT License
