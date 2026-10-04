import ast
import random
import secrets
from typing import Dict, Tuple


def _random_ident(prefix: str = "_0x") -> str:
    chars = "abcdef0123456789"
    return prefix + "".join(secrets.choice(chars) for _ in range(8))


class StringEncryptor:
    """Multi-layer string encryptor with rolling keys and dynamic polymorphic decryptor."""

    def __init__(self):
        self.key = [random.randint(1, 254) for _ in range(random.randint(8, 16))]
        self.salt = random.randint(11, 233)
        self.decryptor_name = _random_ident("_str_")
        self.cache: Dict[str, bytes] = {}

    def encrypt_bytes(self, data: bytes) -> bytes:
        out = bytearray(len(data))
        klen = len(self.key)
        for i, b in enumerate(data):
            out[i] = (b ^ self.key[i % klen] ^ ((i * self.salt) & 0xFF)) & 0xFF
        return bytes(out)

    def encrypt_string(self, text: str) -> bytes:
        if text in self.cache:
            return self.cache[text]
        raw = text.encode("utf-8")
        encrypted = self.encrypt_bytes(raw)
        self.cache[text] = encrypted
        return encrypted

    def generate_decryptor_ast(self) -> ast.FunctionDef:
        """Generates an AST function definition for the decryptor."""
        # def <decryptor_name>(data: bytes) -> str:
        #     res = bytearray(len(data))
        #     k = [<key>]
        #     s = <salt>
        #     for i, b in enumerate(data):
        #         res[i] = (b ^ k[i % len(k)] ^ ((i * s) & 0xFF)) & 0xFF
        #     return res.decode('utf-8')
        code = f"""
def {self.decryptor_name}(data: bytes) -> str:
    _res = bytearray(len(data))
    _k = {self.key!r}
    _s = {self.salt}
    _l = len(_k)
    for _i, _b in enumerate(data):
        _res[_i] = (_b ^ _k[_i % _l] ^ ((_i * _s) & 0xFF)) & 0xFF
    return _res.decode('utf-8')
"""
        parsed = ast.parse(code.strip())
        return parsed.body[0]  # type: ignore

    def create_call_ast(self, encrypted_bytes: bytes) -> ast.Call:
        """Creates an AST Call node: <decryptor_name>(b'...')"""
        return ast.Call(
            func=ast.Name(id=self.decryptor_name, ctx=ast.Load()),
            args=[ast.Constant(value=encrypted_bytes)],
            keywords=[],
        )
