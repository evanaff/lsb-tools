import argparse
from PIL import Image
import string

def encode(input_image, secret_file, output_image):
    img = Image.open(input_image)
    img = img.convert("RGB")
    pixels = img.load()

    with open(secret_file, "r") as file:
        secret_message = file.read()

    secret_binary = "".join(format(ord(c), '08b') for c in secret_message)
    idx = 0
    width, height = img.size

    for y in range(height):
        for x in range(width):
            if idx >= len(secret_binary):
                break

            r, g, b = pixels[x, y]

            if idx < len(secret_binary):
                r = (r & ~1) | int(secret_binary[idx])
                idx += 1
            if idx < len(secret_binary):
                g = (g & ~1) | int(secret_binary[idx])
                idx += 1
            if idx < len(secret_binary):
                b = (b & ~1) | int(secret_binary[idx])
                idx += 1

            pixels[x, y] = (r, g, b)

        if idx >= len(secret_binary):
            break

    img.save(output_image)
    print(f"[+] Pesan berhasil disisipkan ke {output_image}")


def decode(input_image, output_file=None):
    img = Image.open(input_image)
    img = img.convert("RGB")

    allowed_chars = set(string.ascii_letters + string.digits + " \n")

    list_lsb = []
    extracted_lsb_bit = ""
    secret_message = ""

    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            for val in [r, g, b]:
                bit = val & 1
                if len(extracted_lsb_bit) < 8:
                    extracted_lsb_bit += str(bit)
                else:
                    list_lsb.append(extracted_lsb_bit)
                    extracted_lsb_bit = str(bit)

    if extracted_lsb_bit:
        list_lsb.append(extracted_lsb_bit)

    for bit in list_lsb:
        try:
            char = chr(int(bit, 2))
            if char in allowed_chars:
                secret_message += char
        except:
            pass

    if output_file:
        with open(output_file, "w") as f:
            f.write(secret_message)
        print(f"[+] Pesan berhasil diekstrak ke {output_file}")
    else:
        print("Secret Message:")
        print(secret_message)


def analyze(input_image, output_image):
    img = Image.open(input_image)
    img = img.convert("RGB")
    pixels = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))

            r_lsb = 255 if (r & 1) == 1 else 0
            g_lsb = 255 if (g & 1) == 1 else 0
            b_lsb = 255 if (b & 1) == 1 else 0

            pixels[x, y] = (r_lsb, g_lsb, b_lsb)

    img.save(output_image)
    print(f"[+] Hasil analisis LSB disimpan ke {output_image}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LSB Steganography Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encoder
    parser_encode = subparsers.add_parser("encode", help="Sisipkan pesan ke dalam gambar")
    parser_encode.add_argument("-i", "--input", required=True, help="Input image")
    parser_encode.add_argument("-s", "--secret", required=True, help="Secret text file")
    parser_encode.add_argument("-o", "--output", required=True, help="Output stego image")

    # Decoder
    parser_decode = subparsers.add_parser("decode", help="Ekstrak pesan dari gambar")
    parser_decode.add_argument("-i", "--input", required=True, help="Input stego image")
    parser_decode.add_argument("-o", "--output", help="Output text file (optional)")

    # Analyzer
    parser_analyze = subparsers.add_parser("analyze", help="Visualisasi LSB dari gambar")
    parser_analyze.add_argument("-i", "--input", required=True, help="Input image")
    parser_analyze.add_argument("-o", "--output", required=True, help="Output image hasil analisis")

    args = parser.parse_args()

    if args.command == "encode":
        encode(args.input, args.secret, args.output)
    elif args.command == "decode":
        decode(args.input, args.output)
    elif args.command == "analyze":
        analyze(args.input, args.output)
