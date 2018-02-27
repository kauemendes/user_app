import hashlib
import random
import string
import unicodedata



class StringKit:

    @staticmethod
    def random_key(size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    @staticmethod
    def has_any_substring(value, substrings: list):
        if not value:
            return False

        for substring in substrings:
            if value.find(substring) >= 0:
                return True

        return False

    @staticmethod
    def has_all_substring(value, substrings: list):
        if not value:
            return False

        for substring in substrings:
            if not value.find(substring) >= 0:
                return False

        return True

    @staticmethod
    def string_sha1(value: str):
        from app import app

        hash_to_make = hashlib.sha1()
        hash_to_make.update((value + app.config['SECRET_KEY']).encode())
        return hash_to_make.hexdigest()

    @staticmethod
    def string_sha2(value: str):
        from app import app

        hash_to_make = hashlib.sha256()
        hash_to_make.update((value + app.config['SECRET_KEY']).encode())
        return hash_to_make.hexdigest()

    @staticmethod
    def string_med5(value: str):
        from app import app

        hash_to_make = hashlib.md5()
        hash_to_make.update((value + app.config['SECRET_KEY']).encode())
        return hash_to_make.hexdigest()

    @staticmethod
    def normalize_string(text):
        return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')).lower()
