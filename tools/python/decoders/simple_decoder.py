# Morse code decoder

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


def main():
    print("Morse Code Decoder")
    print("Separate letters with a space, and words with ' / '")
    print("Example: .... . .-.. .-.. --- / .-- --- .-. .-.. -..\n")

    user_input = input("Enter Morse code: ")
    result = decode_morse(user_input)
    print("Decoded message:", result)


if __name__ == "__main__":
    main()
