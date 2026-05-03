"""Cortex - Morse Code Tool."""
from __future__ import annotations

from tools import BaseTool


MORSE = {"a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--", "z": "--..", "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----."}
REVERSE = {v: k for k, v in MORSE.items()}


class MorseCodeTool(BaseTool):
    name = "morse_code"
    description = "Encode or decode Morse code. Commands: encode <text> | decode <code>."
    usage_example = "morse_code encode sos"

    def run(self, input: str) -> str:
        cmd, _, text = input.strip().partition(" ")
        if cmd == "encode":
            return " ".join("/" if ch == " " else MORSE.get(ch.lower(), "") for ch in text)
        if cmd == "decode":
            return "".join(" " if token == "/" else REVERSE.get(token, "?") for token in text.split())
        return "[morse_code] Usage: encode <text> | decode <code>"
