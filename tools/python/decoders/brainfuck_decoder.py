#!/usr/bin/env python3
"""
brainfuck_decoder.py

A small Brainfuck interpreter for decoding Brainfuck-encoded strings
commonly found in CTF challenges (e.g. flags hidden in esolang payloads).
Educational use only.

Usage:
   python3 brainfuck_decoder.py to run the script and when prompted to "Paste your Brainfuck code" simply paste your
   code and hit enter.
"""

import sys

def brainfuck(code):
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

bf_code = input("Paste your Brainfuck code: ").strip()
print("\nDecoded output:")
print(brainfuck(bf_code))
