# lsb-tools

This project is a simple implementation of Least Significant Bit (LSB) steganography using Python.
With this tool, you can:

- Hide secret messages inside an image (encoder).

- Extract hidden messages from an image (decoder).

- Visualize the LSB layer of an image (visual analyzer).

## Installation

1. Clone the Repository
```bash
git clone https://github.com/username/lsb-steganography.git
cd lsb-tools
```

2. Create a virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install Dependencies
```
pip install -r requirements.txt
```
## Usage
Main script : `lsb_tools.py`

General Format :
```bash
python lsb_tool.py <mode> -i <input> -o <output> -s <secret>
```

1. Encode
```bash
python lsb_tool.py encode -i input.png -o stego.png -s secret.txt
```
- -i input.png : original cover image

- -o stego.png : output image containing hidden message

- -s secret.txt : text file containing the secret message

2. Decode
```bash
python lsb_tool.py decode -i stego.png -o extracted.txt
```
- -i stego.png → stego image with hidden data

- -o extracted.txt → output text file containing the extracted message

3. Visual Analyze
```bash
python lsb_tool.py analyze -i input.png -o lsb.png
```
- -i input.png → image to be analyzed

- -o lsb.png → black & white visualization of the LSB bits

## Notes
- Supports common image formats (PNG, JPG, etc). PNG is recommended to avoid compression artifacts.

- Messages are encoded character by character in 8-bit binary.

- Decoder only extracts alphanumeric characters, spaces, and newlines.
