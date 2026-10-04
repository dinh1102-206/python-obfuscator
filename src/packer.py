"""Polymorphic multi-layer runtime packer and encrypted payload generator."""

import marshal
import zlib
import base64
import random
import secrets
from typing import List
from .anti_analysis import generate_anti_analysis_code


def _random_ident(prefix: str = "_0x") -> str:
    chars = "abcdef0123456789"
    return prefix + "".join(secrets.choice(chars) for _ in range(8))


def _encrypt_payload(payload: bytes, key: List[int], salt: int) -> bytes:
    out = bytearray(len(payload))
    klen = len(key)
    for i, b in enumerate(payload):
        out[i] = (b ^ key[i % klen] ^ ((i * salt) & 0xFF)) & 0xFF
    return bytes(out)


def pack_code_to_standalone_script(
    source_code: str,
    enable_anti_analysis: bool = True,
    compression_level: int = 9,
) -> str:
    """Compiles source code into serialized bytecode, encrypts it,

    and packages it inside a polymorphic self-executing loader.
    """
    # 1. Compile to code object
    compiled = compile(source_code, "<encrypted>", "exec")
    serialized = marshal.dumps(compiled)

    # 2. Compress
    compressed = zlib.compress(serialized, level=compression_level)

    # 3. Generate dynamic key and salt
    key_length = random.randint(16, 32)
    key = [random.randint(1, 254) for _ in range(key_length)]
    salt = random.randint(13, 251)

    # 4. Multi-layer encryption
    encrypted_bytes = _encrypt_payload(compressed, key, salt)
    b85_payload = base64.b85encode(encrypted_bytes).decode("ascii")

    # 5. Polymorphic identifier generation
    anti_guard = generate_anti_analysis_code() if enable_anti_analysis else ""
    loader_fn = _random_ident("_ldr_")
    data_var = _random_ident("_dt_")
    key_var = _random_ident("_k_")
    salt_var = _random_ident("_s_")
    res_var = _random_ident("_buf_")
    exec_alias = _random_ident("_ex_")
    base64_alias = _random_ident("_b85_")
    zlib_alias = _random_ident("_zl_")
    marshal_alias = _random_ident("_ms_")

    # Obfuscate key representation with arithmetic
    key_repr = ", ".join(f"(0x{k:02x} ^ 0x00)" for k in key)

    loader_template = f"""# -*- coding: utf-8 -*-
# Protected by Python-Obfuscator
import base64 as {base64_alias}
import zlib as {zlib_alias}
import marshal as {marshal_alias}
import sys

{anti_guard}

def {loader_fn}():
    {data_var} = {base64_alias}.b85decode({b85_payload!r})
    {key_var} = [{key_repr}]
    {salt_var} = {salt}
    _l = len({key_var})
    {res_var} = bytearray(len({data_var}))
    for _i, _b in enumerate({data_var}):
        {res_var}[_i] = (_b ^ {key_var}[_i % _l] ^ ((_i * {salt_var}) & 0xFF)) & 0xFF
    _decompressed = {zlib_alias}.decompress(bytes({res_var}))
    _code = {marshal_alias}.loads(_decompressed)
    {exec_alias} = getattr(__builtins__, '\\x65\\x78\\x65\\x63')
    {exec_alias}(_code, globals())

try:
    {loader_fn}()
finally:
    # Cleanup frames
    try:
        del {loader_fn}
    except Exception:
        pass
"""
    return loader_template.strip()
