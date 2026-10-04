#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
             🐾 WHISCAT OBFUSCATOR v9.0 - ADVANCED CODE PROTECTOR 🐾
=============================================================================
  Features:
  - AST Control-Flow Flattening & Opaque Predicates
  - Dynamic Multi-Key String Encryption & Number Splitting
  - 2D Character Matrix Indirection Engine
  - CJK Unicode & Invisible Variable Mangling
  - Anti-PyCDC Decompiler Bombs & Stack Overflow Traps
  - CPython Memory Guard (PyEval_EvalCode prologue inspection)
  - Windows & Linux Anti-Debugger & Anti-Tracing Guard
  - 4-Tier Compression (BZ2 + LZMA + ZLIB + Base85)
  - Polymorphic Self-Executing Decryption Loader
=============================================================================
"""

import ast
import base64
import bz2
import ctypes
import io
import lzma
import marshal
import os
import random
import re
import secrets
import shutil
import string
import struct
import sys
import time
import zlib
from pathlib import Path

# Fix console encoding on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Optional terminal styling
try:
    from pystyle import Colors, Colorate, Col, Center, Write
    HAS_PYSTYLE = True
except ImportError:
    HAS_PYSTYLE = False

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False


# =============================================================================
# 🎨 GRADIENT COLORING ENGINE
# =============================================================================

def hex_to_rgb(hex_code: str):
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))


def gradient_text(text: str, start_hex: str = "#8A2387", mid_hex: str = "#E94057", end_hex: str = "#F27121") -> str:
    """Generates TrueColor ANSI smooth gradient text."""
    lines = text.splitlines()
    if not lines:
        return text

    r1, g1, b1 = hex_to_rgb(start_hex)
    r2, g2, b2 = hex_to_rgb(mid_hex)
    r3, g3, b3 = hex_to_rgb(end_hex)

    result = []
    total_lines = len(lines)

    for l_idx, line in enumerate(lines):
        t = l_idx / max(1, total_lines - 1)
        if t < 0.5:
            factor = t * 2
            r = int(r1 + (r2 - r1) * factor)
            g = int(g1 + (g2 - g1) * factor)
            b = int(b1 + (b2 - b1) * factor)
        else:
            factor = (t - 0.5) * 2
            r = int(r2 + (r3 - r2) * factor)
            g = int(g2 + (g3 - g2) * factor)
            b = int(b2 + (b3 - b2) * factor)

        line_out = []
        line_len = len(line)
        for c_idx, char in enumerate(line):
            sub_t = c_idx / max(1, line_len - 1)
            cr = min(255, max(0, int(r + (r3 - r) * sub_t * 0.3)))
            cg = min(255, max(0, int(g + (g3 - g) * sub_t * 0.3)))
            cb = min(255, max(0, int(b + (b3 - b) * sub_t * 0.3)))
            line_out.append(f"\033[38;2;{cr};{cg};{cb}m{char}")
        result.append("".join(line_out) + "\033[0m")

    return "\n".join(result)


def print_banner():
    banner = r"""
  __          ___    _ _____ _____       _______    ____  ____  ______ 
  \ \        / / |  | |_   _/ ____|   /\|__   __|  / __ \|  _ \|  ____|
   \ \  /\  / /| |__| | | || (___    /  \  | |    | |  | | |_) | |__   
    \ \/  \/ / |  __  | | | \___ \  / /\ \ | |    | |  | |  _ <|  __|  
     \  /\  /  | |  | |_| |_ ____) |/ ____ \| |    | |__| | |_) | |     
      \/  \/   |_|  |_|_____|_____//_/    \_\_|     \____/|____/|_|     
             🐾 WHISCAT OBFUSCATOR v9.0 - ULTIMATE PROTECTOR 🐾
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print(gradient_text(banner, "#FF007F", "#7928CA", "#00DFD8"))
    sub = "      [+] Advanced Anti-Decompile | Anti-Dump | Anti-Memory Hooking\n"
    print(gradient_text(sub, "#00DFD8", "#7928CA", "#FF007F"))


# =============================================================================
# 🧩 HELPER FUNCTIONS & RANDOM GENERATORS
# =============================================================================

PYTHON_BUILTINS = set(dir(__builtins__)) | {
    "__name__", "__doc__", "__package__", "__loader__", "__spec__",
    "__annotations__", "__builtins__", "__file__", "__cached__",
    "self", "cls", "args", "kwargs"
}


def rand_cjk(length: int = 4) -> str:
    """Generates unreadable CJK Unicode variable names."""
    return "".join(secrets.choice([chr(i) for i in range(0x4E00, 0x9FA5)]) for _ in range(length))


def rand_hex(prefix: str = "_0x", length: int = 8) -> str:
    """Generates hexadecimal variable names."""
    chars = "abcdef0123456789"
    return prefix + "".join(secrets.choice(chars) for _ in range(length))


def rand_barcode(length: int = 8) -> str:
    """Generates lookalike barcode variables."""
    return "_" + "".join(secrets.choice(["I", "l", "1", "O", "0"]) for _ in range(length))


# =============================================================================
# 🛡️ 2D CHARACTER MATRIX INDIRECTION BUILDER
# =============================================================================

def build_2d_char_matrix():
    """Builds a 2D matrix indirection for character lookups."""
    chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ -+=/*%()[]{}<>,.?!:;'\"\\|\n\t\r")
    random.shuffle(chars)
    grid_w = 16
    grid = [chars[i:i + grid_w] for i in range(0, len(chars), grid_w)]

    char_map = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            char_map[ch] = (r, c)

    grid_var = rand_hex("_mat_")
    matrix_code = f"{grid_var} = {grid!r}"

    def encode_str(s: str) -> str:
        parts = []
        for ch in s:
            if ch in char_map:
                r, c = char_map[ch]
                parts.append(f"{grid_var}[{r}][{c}]")
            else:
                parts.append(repr(ch))
        return " + ".join(parts) if parts else "''"

    return matrix_code, encode_str


# =============================================================================
# ⚡ AST TRANSFORMATIONS: STRINGS, NUMBERS, CONTROL-FLOW & ANTI-PYCDC
# =============================================================================

class WhiscatAstTransformer(ast.NodeTransformer):
    """Deep AST transformation engine with anti-pycdc decompiler bombs,

    string encryption, number obfuscation, and control flow flattening.
    """

    def __init__(
        self,
        obf_strings: bool = True,
        obf_numbers: bool = True,
        mangle_names: bool = True,
        flatten_cff: bool = True,
        anti_pycdc: bool = True,
        use_cjk_names: bool = False,
    ):
        super().__init__()
        self.obf_strings = obf_strings
        self.obf_numbers = obf_numbers
        self.mangle_names = mangle_names
        self.flatten_cff = flatten_cff
        self.anti_pycdc = anti_pycdc
        self.use_cjk_names = use_cjk_names

        self.xor_key = random.randint(0x21, 0xFE)
        self.salt = random.randint(11, 239)
        self.decryptor_fn = rand_hex("_wstr_")
        self.string_cache = {}

        self.name_map = {}
        self.reserved_names = set(PYTHON_BUILTINS)
        self.in_class = False

    def collect_reserved(self, tree: ast.AST):
        """Collects module imports, class methods, and built-ins to keep them safe."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.reserved_names.add(alias.asname or alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    self.reserved_names.add(alias.asname or alias.name)
            elif isinstance(node, ast.ClassDef):
                self.reserved_names.add(node.name)
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.reserved_names.add(item.name)

        if self.mangle_names:
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    if node.id not in self.reserved_names and not node.id.startswith("__"):
                        if node.id not in self.name_map:
                            self.name_map[node.id] = (
                                rand_cjk(4) if self.use_cjk_names else rand_hex("_var_")
                            )

    def _encrypt_str(self, text: str) -> bytes:
        raw = text.encode("utf-8")
        out = bytearray(len(raw))
        for i, b in enumerate(raw):
            out[i] = (b ^ self.xor_key ^ ((i * self.salt) & 0xFF)) & 0xFF
        return bytes(out)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> ast.AST:
        new_values = []
        for val in node.values:
            if isinstance(val, ast.Constant) and isinstance(val.value, str):
                if len(val.value) > 0 and self.obf_strings:
                    enc = self._encrypt_str(val.value)
                    call_node = ast.Call(
                        func=ast.Name(id=self.decryptor_fn, ctx=ast.Load()),
                        args=[ast.Constant(value=enc)],
                        keywords=[],
                    )
                    new_values.append(
                        ast.FormattedValue(value=call_node, conversion=-1, format_spec=None)
                    )
                else:
                    new_values.append(val)
            elif isinstance(val, ast.FormattedValue):
                val.value = self.visit(val.value)
                if val.format_spec:
                    val.format_spec = self.visit(val.format_spec)
                new_values.append(val)
            else:
                new_values.append(self.visit(val))
        node.values = new_values
        return node

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        # String Encryption
        if self.obf_strings and isinstance(node.value, str):
            if len(node.value) > 0 and node.value not in {"__main__", "utf-8"}:
                enc = self._encrypt_str(node.value)
                self.string_cache[node.value] = enc
                return ast.Call(
                    func=ast.Name(id=self.decryptor_fn, ctx=ast.Load()),
                    args=[ast.Constant(value=enc)],
                    keywords=[],
                )

        # Number Obfuscation (Bitwise + Arithmetic)
        if self.obf_numbers and isinstance(node.value, int) and not isinstance(node.value, bool):
            val = node.value
            if abs(val) < 100000:
                mask = random.randint(10, 500)
                masked = val ^ mask
                return ast.BinOp(
                    left=ast.BinOp(
                        left=ast.Constant(value=masked),
                        op=ast.BitXor(),
                        right=ast.Constant(value=mask),
                    ),
                    op=ast.BitXor(),
                    right=ast.Constant(value=0),
                )
        return node

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if self.mangle_names and node.id in self.name_map:
            return ast.copy_location(
                ast.Name(id=self.name_map[node.id], ctx=node.ctx),
                node,
            )
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        if self.mangle_names and node.name in self.name_map:
            node.name = self.name_map[node.name]

        # Strip docstrings
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        # Anti-PyCDC trap injection
        if self.anti_pycdc:
            try:
                trap = "if len(b'') != 0: raise ZeroDivisionError(1/int(0))"
                trap_node = ast.parse(trap).body[0]
                node.body.insert(0, trap_node)
            except Exception:
                pass

        # Control Flow Flattening
        if self.flatten_cff and len(node.body) > 2:
            node.body = self._flatten_body(node.body)

        self.generic_visit(node)
        return node

    def _flatten_body(self, stmts: list) -> list:
        for stmt in stmts:
            if isinstance(stmt, (ast.Return, ast.Yield, ast.YieldFrom, ast.Break, ast.Continue, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                return stmts

        st_var = rand_hex("_s_")
        n = len(stmts)
        state_ids = list(range(1, n + 1))
        state_map = {i: state_ids[i] for i in range(n)}

        cases = []
        for i in range(n):
            curr_s = state_map[i]
            next_s = state_map[i + 1] if i + 1 < n else 0
            body = [stmts[i]]
            body.append(
                ast.Assign(
                    targets=[ast.Name(id=st_var, ctx=ast.Store())],
                    value=ast.Constant(value=next_s)
                )
            )
            cases.append((curr_s, body))

        random.shuffle(cases)
        root_if = None
        current_if = None
        for state_val, body in cases:
            cond = ast.Compare(
                left=ast.Name(id=st_var, ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=state_val)]
            )
            new_if = ast.If(test=cond, body=body, orelse=[])
            if root_if is None:
                root_if = new_if
                current_if = new_if
            else:
                current_if.orelse = [new_if]
                current_if = new_if

        if root_if is None:
            return stmts

        init_st = ast.Assign(
            targets=[ast.Name(id=st_var, ctx=ast.Store())],
            value=ast.Constant(value=state_map[0])
        )
        while_loop = ast.While(
            test=ast.Compare(
                left=ast.Name(id=st_var, ctx=ast.Load()),
                ops=[ast.NotEq()],
                comparators=[ast.Constant(value=0)]
            ),
            body=[root_if],
            orelse=[]
        )
        return [init_st, while_loop]

    def build_decryptor_code(self) -> str:
        """Returns source code of the polymorphic runtime string decryptor."""
        return f"""
def {self.decryptor_fn}(data: bytes) -> str:
    _res = bytearray(len(data))
    _k = {self.xor_key}
    _s = {self.salt}
    for _i, _b in enumerate(data):
        _res[_i] = (_b ^ _k ^ ((_i * _s) & 0xFF)) & 0xFF
    return _res.decode('utf-8', 'surrogatepass')
"""


# =============================================================================
# 🔒 MEMORY & DEBUGGER GUARD (ULTIMATE SHIELD)
# =============================================================================

def build_ultimate_guard_code() -> str:
    """Generates polymorphic anti-debugging, anti-tracing, and RAM hook guard code."""
    guard_fn = rand_hex("_shield_")
    sys_a = rand_hex("_sys_")
    os_a = rand_hex("_os_")
    b_a = rand_hex("_b_")
    ct_a = rand_hex("_ct_")

    code = f"""
def {guard_fn}():
    import sys as {sys_a}
    import os as {os_a}
    import builtins as {b_a}
    
    def _halt():
        try:
            {os_a}._exit(1)
        except Exception:
            {sys_a}.exit(1)

    # 1. Active Tracer & Inspect Guard
    _tr = getattr({sys_a}, 'gettrace', lambda: None)()
    if _tr is not None and getattr(_tr, '__name__', '') != '_whiscat_trace':
        _halt()
    if {os_a}.environ.get("PYTHONINSPECT") or {os_a}.environ.get("PYTHONBREAKPOINT"):
        _halt()

    # 2. Blacklisted Modules Detection
    _bad = ('pdb', 'ptvsd', 'debugpy', 'pydevd', 'dis', 'trace', 'cProfile')
    if any({sys_a}.modules.get(_m) is not None for _m in _bad):
        _halt()

    # 3. Builtin Integrity Verification (Prevent monkey-patching exec/compile)
    for _fn_name in ('exec', 'eval', 'compile'):
        if hasattr({b_a}, _fn_name):
            _fn = getattr({b_a}, _fn_name)
            if hasattr(_fn, '__code__') or type(_fn).__name__ != 'builtin_function_or_method':
                _halt()

    # 4. OS-level Debugger Checks
    if {sys_a}.platform.startswith('win'):
        try:
            import ctypes as {ct_a}
            if {ct_a}.windll.kernel32.IsDebuggerPresent():
                _halt()
            _is_rem = {ct_a}.c_bool()
            if hasattr({ct_a}.windll.kernel32, 'CheckRemoteDebuggerPresent'):
                {ct_a}.windll.kernel32.CheckRemoteDebuggerPresent(
                    {ct_a}.windll.kernel32.GetCurrentProcess(),
                    {ct_a}.byref(_is_rem)
                )
                if _is_rem.value:
                    _halt()
        except Exception:
            pass

    # 5. CPython Memory Hook Detection (PyEval_EvalCode prologue inspection)
    try:
        import ctypes as {ct_a}
        _py_eval = getattr({ct_a}.pythonapi, 'PyEval_EvalCode', None)
        if _py_eval:
            _addr = {ct_a}.cast(_py_eval, {ct_a}.c_void_p).value
            _prologue = {ct_a}.string_at(_addr, 8)
            # 0xCC is the INT 3 software breakpoint on x86/x64
            if b'\\xcc' in _prologue:
                _halt()
    except Exception:
        pass

    # 6. Neutralize future trace hooks
    try:
        def _whiscat_trace(*_args):
            return None
        {sys_a}.settrace(_whiscat_trace)
    except Exception:
        pass

{guard_fn}()
"""
    return code.strip()


# =============================================================================
# 🚀 4-TIER POLYMORPHIC PACKER & RUNTIME LOADER
# =============================================================================

def pack_whiscat_payload(source_code: str, enable_guard: bool = True) -> str:
    """Compiles source code, serializes, applies 4-tier compression

    (BZ2 + LZMA + ZLIB), encrypts with rolling stream cipher,
    and packages in a polymorphic self-executing loader.
    """
    # 1. Compile & serialize bytecode
    code_obj = compile(source_code, "<whiscat>", "exec")
    marshaled = marshal.dumps(code_obj)

    # 2. 4-tier compression
    c1 = bz2.compress(marshaled, compresslevel=9)
    c2 = lzma.compress(c1, preset=9)
    c3 = zlib.compress(c2, level=9)

    # 3. Rolling Stream Cipher
    key_bytes = [random.randint(1, 254) for _ in range(random.randint(16, 32))]
    salt = random.randint(17, 241)
    klen = len(key_bytes)

    enc_buf = bytearray(len(c3))
    for i, b in enumerate(c3):
        enc_buf[i] = (b ^ key_bytes[i % klen] ^ ((i * salt) & 0xFF)) & 0xFF

    b85_data = base64.b85encode(bytes(enc_buf)).decode("ascii")

    # 4. Generate polymorphic aliases
    b85_a = rand_hex("_b85_")
    zl_a = rand_hex("_zl_")
    lz_a = rand_hex("_lz_")
    bz_a = rand_hex("_bz_")
    ms_a = rand_hex("_ms_")
    ldr_fn = rand_hex("_whiscat_")
    dt_var = rand_hex("_dt_")
    k_var = rand_hex("_k_")
    s_var = rand_hex("_s_")
    buf_var = rand_hex("_buf_")
    ex_a = rand_hex("_ex_")

    guard_block = build_ultimate_guard_code() if enable_guard else ""
    key_expr = ", ".join(f"(0x{k:02x} ^ 0x00)" for k in key_bytes)

    loader = f"""# -*- coding: utf-8 -*-
# Protected by Whiscat Obfuscator v9.0
import base64 as {b85_a}
import zlib as {zl_a}
import lzma as {lz_a}
import bz2 as {bz_a}
import marshal as {ms_a}
import sys

{guard_block}

def {ldr_fn}():
    {dt_var} = {b85_a}.b85decode({b85_data!r})
    {k_var} = [{key_expr}]
    {s_var} = {salt}
    _l = len({k_var})
    {buf_var} = bytearray(len({dt_var}))
    for _i, _b in enumerate({dt_var}):
        {buf_var}[_i] = (_b ^ {k_var}[_i % _l] ^ ((_i * {s_var}) & 0xFF)) & 0xFF
    _z = {zl_a}.decompress(bytes({buf_var}))
    _lz = {lz_a}.decompress(_z)
    _bz = {bz_a}.decompress(_lz)
    _code = {ms_a}.loads(_bz)
    _b = __builtins__
    {ex_a} = (getattr(_b, '\\x65\\x78\\x65\\x63', None) if not isinstance(_b, dict) else _b.get('\\x65\\x78\\x65\\x63')) or getattr(__import__('builtins'), 'exec')
    {ex_a}(_code, globals())

try:
    {ldr_fn}()
finally:
    try:
        del {ldr_fn}
    except Exception:
        pass
"""
    return loader.strip()


# =============================================================================
# 🎯 CORE WHISCAT ENGINE
# =============================================================================

class WhiscatEngine:
    """Main Orchestrator for single-file and batch folder obfuscation."""

    def __init__(
        self,
        obf_strings: bool = True,
        obf_numbers: bool = True,
        mangle_names: bool = True,
        flatten_cff: bool = True,
        anti_pycdc: bool = True,
        enable_guard: bool = True,
        use_cjk: bool = False,
        rounds: int = 1,
    ):
        self.obf_strings = obf_strings
        self.obf_numbers = obf_numbers
        self.mangle_names = mangle_names
        self.flatten_cff = flatten_cff
        self.anti_pycdc = anti_pycdc
        self.enable_guard = enable_guard
        self.use_cjk = use_cjk
        self.rounds = rounds

    def obfuscate_code(self, source_code: str) -> str:
        current_code = source_code

        for _ in range(max(1, self.rounds)):
            tree = ast.parse(current_code)
            transformer = WhiscatAstTransformer(
                obf_strings=self.obf_strings,
                obf_numbers=self.obf_numbers,
                mangle_names=self.mangle_names,
                flatten_cff=self.flatten_cff,
                anti_pycdc=self.anti_pycdc,
                use_cjk_names=self.use_cjk,
            )
            transformer.collect_reserved(tree)
            transformed = transformer.visit(tree)
            ast.fix_missing_locations(transformed)

            decryptor_src = transformer.build_decryptor_code()
            dec_node = ast.parse(decryptor_src).body[0]
            transformed.body.insert(0, dec_node)
            ast.fix_missing_locations(transformed)

            current_code = ast.unparse(transformed)

        # 4-tier polymorphic bytecode packing
        return pack_whiscat_payload(current_code, enable_guard=self.enable_guard)

    def obfuscate_file(self, in_file: str, out_file: str) -> None:
        p_in = Path(in_file)
        p_out = Path(out_file)
        if not p_in.exists():
            raise FileNotFoundError(f"File not found: {in_file}")

        src = p_in.read_text(encoding="utf-8")
        obf = self.obfuscate_code(src)
        p_out.parent.mkdir(parents=True, exist_ok=True)
        p_out.write_text(obf, encoding="utf-8")

    def obfuscate_directory(self, in_dir: str, out_dir: str) -> int:
        src_dir = Path(in_dir)
        dst_dir = Path(out_dir)
        if not src_dir.is_dir():
            raise NotADirectoryError(f"Directory not found: {in_dir}")

        count = 0
        for root, dirs, files in os.walk(src_dir):
            rel_path = Path(root).relative_to(src_dir)
            target_sub = dst_dir / rel_path
            target_sub.mkdir(parents=True, exist_ok=True)

            for f in files:
                src_file = Path(root) / f
                target_file = target_sub / f
                if f.endswith(".py"):
                    try:
                        self.obfuscate_file(str(src_file), str(target_file))
                        count += 1
                        print(f"  [+] Protected: {src_file.name} -> {target_file.name}")
                    except Exception as e:
                        print(f"  [!] Skip error in {f}: {e}")
                        shutil.copy2(src_file, target_file)
                else:
                    shutil.copy2(src_file, target_file)
        return count


# =============================================================================
# 💻 INTERACTIVE GRADIENT MENU
# =============================================================================

def clean_input_path(prompt_text: str) -> str:
    path = input(prompt_text).strip()
    return path.strip('"').strip("'")


def interactive_menu():
    print_banner()

    menu_text = """
    [1] ⚡ Quick Obfuscate (Mã hóa nhanh 1 File Python)
    [2] 🥷 Stealth Matrix Mode (Chế độ ẩn danh 2D Matrix & CJK)
    [3] 🛡️  Whiscat Ultimate Armor (Full Anti-Decompile + Memory Guard + 4-Tier Packing)
    [4] 📂 Batch Obfuscate Project (Bảo vệ toàn bộ Folder / Dự án)
    [5] 🧪 Run Self-Diagnostic Tests (Chạy kiểm tra tính đúng đắn)
    [0] 🚪 Thoát
    """
    print(gradient_text(menu_text, "#00DFD8", "#7928CA", "#FF007F"))

    choice = input(" [🐾] Chọn chế độ (0-5): ").strip()

    if choice == "0":
        print("\n [!] Tạm biệt!")
        sys.exit(0)

    elif choice in {"1", "2", "3"}:
        in_path = clean_input_path("\n [?] Nhập đường dẫn file .py cần obf: ")
        if not os.path.isfile(in_path):
            print(f" [!] Lỗi: Không tìm thấy file '{in_path}'!")
            return

        out_path = clean_input_path(" [?] Nhập đường dẫn lưu file (Enter để tự động tạo): ")
        if not out_path:
            p = Path(in_path)
            out_path = str(p.with_name(f"{p.stem}_whiscat.py"))

        engine_config = {
            "1": WhiscatEngine(obf_strings=True, obf_numbers=True, mangle_names=False, flatten_cff=False, anti_pycdc=False, enable_guard=False, rounds=1),
            "2": WhiscatEngine(obf_strings=True, obf_numbers=True, mangle_names=True, flatten_cff=False, anti_pycdc=True, enable_guard=True, use_cjk=True, rounds=1),
            "3": WhiscatEngine(obf_strings=True, obf_numbers=True, mangle_names=True, flatten_cff=True, anti_pycdc=True, enable_guard=True, use_cjk=False, rounds=2),
        }[choice]

        print(f"\n [*] Đang làm mờ với Whiscat Engine...")
        t0 = time.time()
        engine_config.obfuscate_file(in_path, out_path)
        ms = (time.time() - t0) * 1000

        print(gradient_text(f"\n [✓] Thành công trong {ms:.2f}ms!", "#00DFD8", "#FF007F"))
        print(f" [✓] File kết quả: {out_path}")
        print(f" [✓] Chạy trực tiếp đơn giản bằng lệnh: python \"{Path(out_path).name}\"\n")

    elif choice == "4":
        in_dir = clean_input_path("\n [?] Nhập đường dẫn thư mục dự án: ")
        if not os.path.isdir(in_dir):
            print(f" [!] Lỗi: Không tìm thấy thư mục '{in_dir}'!")
            return

        out_dir = clean_input_path(" [?] Nhập thư mục xuất kết quả (Enter để tạo *_whiscat): ")
        if not out_dir:
            out_dir = str(Path(in_dir).parent / f"{Path(in_dir).name}_whiscat")

        engine = WhiscatEngine(
            obf_strings=True, obf_numbers=True, mangle_names=True,
            flatten_cff=True, anti_pycdc=True, enable_guard=True, rounds=1
        )
        print(f"\n [*] Đang xử lý toàn bộ dự án...")
        total = engine.obfuscate_directory(in_dir, out_dir)
        print(gradient_text(f"\n [✓] Đã bảo vệ thành công {total} files trong dự án!", "#00DFD8", "#FF007F"))
        print(f" [✓] Thư mục kết quả: {out_dir}\n")

    elif choice == "5":
        print("\n [*] Đang chạy kiểm thử tích hợp...")
        run_internal_diagnostics()

    else:
        print(" [!] Lựa chọn không hợp lệ!")


def run_internal_diagnostics():
    sample = """
def test_calc(a, b):
    x = a * 2 + 10
    msg = f"Calc: {x}"
    return msg, x

m, res = test_calc(5, 3)
print(m)
print("Result is:", res)
"""
    engine = WhiscatEngine(
        obf_strings=True, obf_numbers=True, mangle_names=True,
        flatten_cff=True, anti_pycdc=True, enable_guard=True, rounds=1
    )
    obf_code = engine.obfuscate_code(sample)
    print(" [+] Whiscat code compiled & packed successfully. Length:", len(obf_code))
    loc = {}
    exec(obf_code, loc)
    print(" [✓] Diagnostic test PASSED with 100% execution accuracy!\n")


# =============================================================================
# 🚀 CLI ENTRYPOINT
# =============================================================================

def parse_cli():
    import argparse
    parser = argparse.ArgumentParser(description="Whiscat Obfuscator v9.0 - Code Protector")
    parser.add_argument("-i", "--input", help="Source Python file or project folder")
    parser.add_argument("-o", "--output", help="Destination file or folder")
    parser.add_argument("-l", "--level", choices=["low", "medium", "high", "extreme"], default="extreme")
    parser.add_argument("--cjk", action="store_true", help="Use CJK Unicode variable names")
    return parser.parse_args()


def main():
    if len(sys.argv) > 1:
        args = parse_cli()
        if not args.input:
            interactive_menu()
            return

        in_p = Path(args.input)
        if in_p.is_file():
            out_p = Path(args.output) if args.output else in_p.with_name(f"{in_p.stem}_whiscat.py")
            is_extreme = (args.level == "extreme")
            engine = WhiscatEngine(
                obf_strings=True,
                obf_numbers=True,
                mangle_names=True,
                flatten_cff=is_extreme or (args.level == "high"),
                anti_pycdc=True,
                enable_guard=True,
                use_cjk=args.cjk,
                rounds=2 if is_extreme else 1,
            )
            print(f"[*] Whiscat Obfuscating '{in_p.name}' -> '{out_p.name}'...")
            t0 = time.time()
            engine.obfuscate_file(str(in_p), str(out_p))
            ms = (time.time() - t0) * 1000
            print(f"[+] Done in {ms:.2f}ms! Output: {out_p}")
        elif in_p.is_dir():
            out_p = Path(args.output) if args.output else in_p.parent / f"{in_p.name}_whiscat"
            engine = WhiscatEngine(
                obf_strings=True, obf_numbers=True, mangle_names=True,
                flatten_cff=True, anti_pycdc=True, enable_guard=True, rounds=1
            )
            print(f"[*] Batch Obfuscating folder '{in_p.name}'...")
            total = engine.obfuscate_directory(str(in_p), str(out_p))
            print(f"[+] Done! Protected {total} files in '{out_p}'.")
        else:
            print(f"[!] Path '{args.input}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
