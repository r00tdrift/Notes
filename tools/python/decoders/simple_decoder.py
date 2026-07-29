# Universal Decoder
# Lets you pick which type of decoder you want to use, then decodes your string

# ---------- Morse Code Decoder ----------

MORSE_CODE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9'
}


def decode_morse(morse_code):
    # Words are separated by " / " and letters by spaces
    words = morse_code.strip().split(' / ')
    decoded_words = []

    for word in words:
        letters = word.split(' ')
        decoded_letters = []
        for letter in letters:
            if letter in MORSE_CODE:
                decoded_letters.append(MORSE_CODE[letter])
            else:
                decoded_letters.append('?')
        decoded_words.append(''.join(decoded_letters))

    return ' '.join(decoded_words)


# ---------- Brainfuck Decoder ----------

def decode_brainfuck(code):
    tape = [0] * 30000
    ptr = 0
    output = []
    code_ptr = 0
    loop_stack = []

    while code_ptr < len(code):
        cmd = code[code_ptr]
        if cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            output.append(chr(tape[ptr]))
        elif cmd == '[':
            if tape[ptr] == 0:
                depth = 1
                while depth != 0:
                    code_ptr += 1
                    if code[code_ptr] == '[':
                        depth += 1
                    elif code[code_ptr] == ']':
                        depth -= 1
            else:
                loop_stack.append(code_ptr)
        elif cmd == ']':
            if tape[ptr] != 0:
                code_ptr = loop_stack[-1]
            else:
                loop_stack.pop()
        code_ptr += 1

    return ''.join(output)


# ---------- Base64 Decoder ----------

import base64


def decode_base64(text):
    decoded_bytes = base64.b64decode(text)
    return decoded_bytes.decode("utf-8", errors="replace")


# ---------- Binary Decoder ----------

def decode_binary(text):
    # Splits on spaces, turns each 8-bit chunk into a character
    bits = text.strip().split(' ')
    letters = []
    for byte in bits:
        letters.append(chr(int(byte, 2)))
    return ''.join(letters)


# ---------- Hexadecimal Decoder ----------

def decode_hex(text):
    text = text.replace(' ', '')
    decoded_bytes = bytes.fromhex(text)
    return decoded_bytes.decode("utf-8", errors="replace")


# ---------- Caesar Cipher / ROT13 Decoder ----------

def decode_caesar(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)


# ---------- URL Decoder ----------

import urllib.parse


def decode_url(text):
    return urllib.parse.unquote(text)


# ---------- ASCII / Decimal Decoder ----------

def decode_ascii(text):
    # Splits on spaces, turns each decimal number into a character
    numbers = text.strip().split(' ')
    letters = []
    for num in numbers:
        letters.append(chr(int(num)))
    return ''.join(letters)


# ---------- Hex with \x Escapes Decoder ----------

def decode_hex_escaped(text):
    # Turns \x48\x65\x6c\x6c\x6f into normal hex, then decodes it
    text = text.replace('\\x', '')
    decoded_bytes = bytes.fromhex(text)
    return decoded_bytes.decode("utf-8", errors="replace")


# ---------- Base32 Decoder ----------

def decode_base32(text):
    decoded_bytes = base64.b32decode(text.upper())
    return decoded_bytes.decode("utf-8", errors="replace")


# ---------- Atbash Cipher Decoder ----------

def decode_atbash(text):
    result = []
    for char in text:
        if char.isupper():
            new_char = chr(ord('Z') - (ord(char) - ord('A')))
            result.append(new_char)
        elif char.islower():
            new_char = chr(ord('z') - (ord(char) - ord('a')))
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)


# ---------- Helper for pasting multi-line input ----------

import sys
import termios


def get_encoded_string():
    print("Enter the encoded string: ", end="", flush=True)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    new_settings = termios.tcgetattr(fd)
    # Turn off canonical mode and echo so we can read raw keystrokes
    new_settings[3] = new_settings[3] & ~(termios.ICANON | termios.ECHO)
    termios.tcsetattr(fd, termios.TCSANOW, new_settings)

    # Tell the terminal to wrap pasted text in special markers instead
    # of sending it like normal typed characters/Enter presses
    sys.stdout.write("\x1b[?2004h")
    sys.stdout.flush()

    result = ""
    escape_buffer = ""
    in_paste = False

    try:
        while True:
            ch = sys.stdin.read(1)

            if ch == "\x1b" or escape_buffer:
                escape_buffer += ch
                if "\x1b[200~".startswith(escape_buffer):
                    if escape_buffer == "\x1b[200~":
                        in_paste = True
                        escape_buffer = ""
                    continue
                elif "\x1b[201~".startswith(escape_buffer):
                    if escape_buffer == "\x1b[201~":
                        in_paste = False
                        escape_buffer = ""
                    continue
                else:
                    escape_buffer = ""
                    continue

            if ch in ("\r", "\n"):
                if in_paste:
                    result += "\n"
                    continue
                else:
                    break

            if ch == "\x7f":  # backspace
                if result and not in_paste:
                    result = result[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue

            if ch == "\x03":  # Ctrl+C
                raise KeyboardInterrupt

            result += ch
            sys.stdout.write(ch)
            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\x1b[?2004l")
        sys.stdout.flush()
        print()

    # Strip out any newlines that were part of a pasted block
    return result.replace("\n", "")


# ---------- Main Menu ----------

def main():
    print("Universal Decoder")
    print("Which decoder do you want to use?")
    print("1. Morse Code")
    print("2. Brainfuck")
    print("3. Base64")
    print("4. Binary")
    print("5. Hexadecimal")
    print("6. Caesar Cipher / ROT13")
    print("7. URL Encoding")
    print("8. ASCII / Decimal")
    print("9. Hex with \\x Escapes")
    print("10. Base32")
    print("11. Atbash Cipher")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        print("\nSeparate letters with a space, and words with ' / '")
        print("Example: .... . .-.. .-.. --- / .-- --- .-. .-.. -..\n")
        user_input = get_encoded_string()
        result = decode_morse(user_input)
        print("Decoded message:", result)

    elif choice == "2":
        user_input = get_encoded_string()
        result = decode_brainfuck(user_input)
        print("Decoded message:", result)

    elif choice == "3":
        user_input = get_encoded_string()
        result = decode_base64(user_input)
        print("Decoded message:", result)

    elif choice == "4":
        print("\nSeparate each 8-bit byte with a space.")
        print("Example: 01001000 01101001\n")
        user_input = get_encoded_string()
        result = decode_binary(user_input)
        print("Decoded message:", result)

    elif choice == "5":
        user_input = get_encoded_string()
        result = decode_hex(user_input)
        print("Decoded message:", result)

    elif choice == "6":
        user_input = get_encoded_string()
        shift = int(input("Enter the shift number (13 for ROT13): "))
        result = decode_caesar(user_input, shift)
        print("Decoded message:", result)

    elif choice == "7":
        user_input = get_encoded_string()
        result = decode_url(user_input)
        print("Decoded message:", result)

    elif choice == "8":
        print("\nSeparate each number with a space.")
        print("Example: 72 101 108 108 111\n")
        user_input = get_encoded_string()
        result = decode_ascii(user_input)
        print("Decoded message:", result)

    elif choice == "9":
        print("\nExample: \\x48\\x65\\x6c\\x6c\\x6f\n")
        user_input = get_encoded_string()
        result = decode_hex_escaped(user_input)
        print("Decoded message:", result)

    elif choice == "10":
        user_input = get_encoded_string()
        result = decode_base32(user_input)
        print("Decoded message:", result)

    elif choice == "11":
        user_input = get_encoded_string()
        result = decode_atbash(user_input)
        print("Decoded message:", result)

    else:
        print("That is not a valid choice. Please pick a number from the menu.")


if __name__ == "__main__":
    main()