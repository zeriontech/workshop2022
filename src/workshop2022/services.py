from binascii import unhexlify
from typing import Any


class FeedService:
    async def get_statuses(self) -> list:
        # todo:
        return []

    async def process_updated_logs(self) -> None:
        print('todo')

    async def request_address_data_from_zerion_api(self) -> None:
        print('todo')

    async def process_received_address_portfolio(self, address_portfolio_data: dict[str, Any]) -> None:
        print('todo')

    @staticmethod
    def _parse_address(address_hash: str) -> str:
        return f'0x{address_hash[-40:]}'

    def _parse_text(self, text_hash: str) -> str:
        words = self._hash_to_words(text_hash)

        if len(words) == 1:
            return self._hash_to_string(words[0])

        if len(words) == 128 and len([word for word in words if self._hash_to_int(word) != 0]) == 1:
            return self._hash_to_string(words[0])

        # string position + dynamic size string (size + string)
        if self._hash_to_int(words[0]) == 32 and (len(words) != 2 or self._hash_to_int(words[1]) == 0):
            return self._words_to_string(words[1:])

        # dynamic size string (size + string)
        return self._words_to_string(words)

    @staticmethod
    def _hash_to_words(passed_hash: str) -> list[str]:
        passed_hash = passed_hash[2:] if passed_hash.startswith('0x') else passed_hash
        return [passed_hash[i:i + 64] for i in range(0, len(passed_hash), 64)]

    @staticmethod
    def _hash_to_string(passed_hash: str) -> str:
        encoded_string = passed_hash.rstrip('0')
        if len(encoded_string) % 2 != 0:
            encoded_string += '0'
        return unhexlify(encoded_string).decode()

    def _words_to_string(self, words: list[str]) -> str:
        string_length = self._hash_to_int(words[0]) * 2
        hex_string = ''.join(words[1:])
        result = unhexlify(hex_string[:string_length]).decode()
        return result.replace('\x00', '')

    @staticmethod
    def _hash_to_int(hex_str: str, unsigned: bool = True) -> int:
        hex_str = hex_str[:64]
        hex_str = hex_str.zfill(64)
        if not unsigned and int(hex_str[0], 16) >= 8:  # negative int
            return int(hex_str, 16) - 2**256
        return int(hex_str, 16)
