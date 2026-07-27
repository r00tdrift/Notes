# Decoders

Scripts for decoding/encoding data commonly found in CTFs, logs, and recon output.

## Contents

- **simple_decoder.py** — Multi-format decoder supporting base64, hex, ROT13, URL-encoding, and binary.

### Usage

```bash
python simple_decoder.py --method base64 --input "SGVsbG8gd29ybGQ="
python simple_decoder.py --method hex --input "48656c6c6f"
echo "Uryyb" | python simple_decoder.py --method rot13
```

## Ideas for future additions

- Base32 / Base85 decoder
- Caesar cipher brute-forcer (all 25 shifts)
- Morse code decoder
- JWT decoder (header/payload, no verification)
- Multi-layer auto-decoder (detects and chains encodings)
