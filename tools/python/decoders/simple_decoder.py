#!/usr/bin/env python3
"""
simple_decoder.py

A small multi-format decoder for common CTF / recon encodings.
Educational use only.

Usage:
    python simple_decoder.py --method base64 --input "SGVsbG8gd29ybGQ="
    python simple_decoder.py --method hex --input "48656c6c6f"
    python simple_decoder.py --method rot13 --input "Uryyb"
    python simple_decoder.py --method url --input "Hello%20World"
    python simple_decoder.py --method binary --input "01001000 01101001"
    echo "SGVsbG8=" | python simple_decoder.py --method base64
"""

import argparse
import base64
import codecs
import sys
import urllib.parse


def decode_base64(data: str) -> str:
    # Add padding if missing
    padded = data + "=" * (-len(data) % 4)
    return base64.b64decode(padded).decode("utf-8", errors="replace")


def decode_hex(data: str) -> str:
    cleaned = data.replace(" ", "").replace("0x", "").replace(",", "")
    return bytes.fromhex(cleaned).decode("utf-8", errors="replace")


def decode_rot13(data: str) -> str:
    return codecs.decode(data, "rot_13")


def decode_url(data: str) -> str:
    return urllib.parse.unquote(data)


def decode_binary(data: str) -> str:
    bits = data.split()
    return "".join(chr(int(b, 2)) for b in bits)


METHODS = {
    "base64": decode_base64,
    "hex": decode_hex,
    "rot13": decode_rot13,
    "url": decode_url,
    "binary": decode_binary,
}


def main():
    parser = argparse.ArgumentParser(description="Decode common encodings used in CTFs/recon.")
    parser.add_argument(
        "--method",
        choices=METHODS.keys(),
        required=True,
        help="Decoding method to use.",
    )
    parser.add_argument(
        "--input",
        help="String to decode. If omitted, reads from stdin.",
    )
    args = parser.parse_args()

    data = args.input if args.input is not None else sys.stdin.read().strip()

    try:
        result = METHODS[args.method](data)
    except Exception as exc:
        print(f"[!] Failed to decode with method '{args.method}': {exc}", file=sys.stderr)
        sys.exit(1)

    print(result)


if __name__ == "__main__":
    main()
