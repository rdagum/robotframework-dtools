# pylint: disable=missing-docstring
import json
import pathlib
import argparse
from cryptography.fernet import Fernet
import ast
from typing import Optional


# pylint: disable=too-few-public-methods
class Bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Encryption:
    def __init__(
        self, encryption_key: Optional[str] = None, key_file_path: Optional[str] = None
    ):
        if encryption_key:
            # Use the provided key directly
            self._key = encryption_key
            if isinstance(self._key, str):
                self._key = self._key.encode()
            self._encrypter = Fernet(self._key)
        else:
            # Load from configuration file (existing logic)
            try:
                key_path = key_file_path or self._get_default_key_path()
                with open(key_path, "r") as f:
                    key_data = json.load(f)
                encryption_key = key_data.get("encryption_key")
                if not encryption_key:
                    raise ValueError("encryption_key not found in configuration")
                self._key = ast.literal_eval(encryption_key)
                self._encrypter = Fernet(self._key)
            except FileNotFoundError:
                raise FileNotFoundError(f"Encryption key file not found: {key_path}")

    def decrypt(self, value: bytes) -> str:
        value = self._encrypter.decrypt(value)
        return value.decode()

    def encrypt(self, value: str) -> bytes:
        value = value.encode()
        return self._encrypter.encrypt(value)

    def _get_default_key_path(self):
        return str(pathlib.Path(__file__).parent.joinpath("configuration", "key.json"))


if __name__ == "__main__":
    encryption = Encryption()
    parser = argparse.ArgumentParser(description="Encrypt the provided value")
    parser.add_argument("--encrypt", action="store_true")
    parser.add_argument("--decrypt", action="store_true")
    parser.add_argument("value")
    args = parser.parse_args()
    if args.encrypt:
        print(Bcolors.OKCYAN + str(encryption.encrypt(args.value)) + Bcolors.ENDC)
    if args.decrypt:
        if args.value[:2] == "b'":
            print(
                Bcolors.FAIL
                + "   ERROR: Do not include b' in the string to decrypt"
                + Bcolors.ENDC
            )
        else:
            print(
                Bcolors.OKCYAN
                + encryption.decrypt(bytes(args.value, "utf-8"))
                + Bcolors.ENDC
            )
