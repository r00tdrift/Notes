# Encoding Cheatsheet

Quick reference for encodings commonly encountered in CTFs, web testing, and log analysis.

## Base64

```bash
echo -n "Hello World" | base64          # SGVsbG8gV29ybGQ=
echo "SGVsbG8gV29ybGQ=" | base64 -d     # Hello World
```

## Hex

```bash
echo -n "Hello" | xxd -p                # 48656c6c6f
echo "48656c6c6f" | xxd -r -p           # Hello
```

## URL encoding

```bash
python3 -c "import urllib.parse; print(urllib.parse.quote('Hello World!'))"
python3 -c "import urllib.parse; print(urllib.parse.unquote('Hello%20World%21'))"
```

## ROT13 / Caesar

```bash
echo "Hello" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

## Binary / ASCII

```text
01001000 01100101 01101100 01101100 01101111  ->  Hello
```

## HTML entities

```text
&lt;script&gt;  ->  <script>
&#x3C;script&#x3E;  ->  <script>
```

## Unicode / punycode

```text
xn--80ak6aa92e.com  ->  аррӏе.com (IDN homograph — common in phishing)
```

## JWT (structure only — not encryption)

A JWT is three base64url segments separated by dots: `header.payload.signature`. The header and payload are just base64url-encoded JSON and can be decoded (not decrypted) directly:

```bash
echo -n "eyJhbGciOiJIUzI1NiJ9" | base64 -d
```

## Quick tips

- Base64 strings often end in `=` or `==` padding, use only `A-Za-z0-9+/`.
- Hex strings are pure `0-9a-f`.
- If output looks like readable text after one decode, you may be looking at multiple *layers* of encoding — try decoding again.
- CyberChef (https://gchq.github.io/CyberChef/) is invaluable for chaining these operations visually.
