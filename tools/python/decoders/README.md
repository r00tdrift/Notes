# Decoders

Scripts for decoding/encoding data commonly found in CTFs, logs, and recon output.

## Contents

*## Universal Decoder

A simple command-line tool that decodes strings encoded in one of 11 common formats.
Run the script, pick a decoder from the menu, then paste in your encoded string.

### Supported decoders

| # | Type | Example input |
|---|------|----------------|
| 1 | Morse Code | `.... . .-.. .-.. --- / .-- --- .-. .-.. -..` |
| 2 | Brainfuck | `++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.` |
| 3 | Base64 | `SGVsbG8=` |
| 4 | Binary | `01001000 01101001` |
| 5 | Hexadecimal | `48656c6c6f` |
| 6 | Caesar Cipher / ROT13 | `Uryyb` (shift 13) |
| 7 | URL Encoding | `Hello%20World%21` |
| 8 | ASCII / Decimal | `72 101 108 108 111` |
| 9 | Hex with `\x` Escapes | `\x48\x65\x6c\x6c\x6f` |
| 10 | Base32 | `JBSWY3DPEBLW64TMMQ======` |
| 11 | Atbash Cipher | `Svool` |

### Usage

\`\`\`bash
python3 simple_decoder.py
\`\`\`

You'll be prompted to:
1. Choose a decoder from the numbered menu
2. Enter your encoded string
3. View the decoded output printed to the console


## Ideas for future additions
- JWT decoder (header/payload, no verification)
- Multi-layer auto-decoder (detects and chains encodings)
