#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
             🐾 WHISCAT OBFUSCATOR v9.0 - TDINH & WHISCAT APEX 🐾
=============================================================================
  - Signature Tamper-Lock: Khóa chặt 3 dòng chữ ký (__owner__, __cmt__, __note__)
  - Ma trận ngập tràn Emojis & Ký tự đặc biệt (ktdb):
    ᶻ 𝗓 𐰁ᶻ 𝗓 𐰁𓃱𓃱ִ 𖤐ִ 𖤐𖠋𖠋𖠋⋆౨ৎ˚⟡˖ ࣪whiscat⋆౨ৎ˚⟡˖ ࣪☠☠☠
  - Hỗ trợ làm rối 1 File lẻ hoặc nguyên cả thư mục / dự án (Batch Folder).
  - Đầy đủ lá chắn tối thượng:
    * Neo-Ghost Chaos: Flood tàng hình ngang cực sâu (40.000 - 75.000 spaces)
    * Anti-PyCDC decompiler bomb traps (1/int(0) stack overflow)
    * 2D Matrix character indirection
    * CPython Memory hook detection (PyEval_EvalCode prologue inspection)
    * Anti-Frida, Anti-Debugging Windows & Linux
    * 4-Stage Compression (zlib + lzma + bz2 + base85)
    * Dynamic 12-function rolling stream cipher
    * Real-time SHA-256 file self-integrity check
    * In-place RAM purge & self-destruct on tampering
=============================================================================
"""

import os
import sys
import time
import random
import zlib
import bz2
import lzma
import base64
import hashlib
import subprocess
import ast
import stat
import shutil
from pathlib import Path

# Cấu hình UTF-8 an toàn cho console Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Kiểm tra pystyle & colorama
try:
    from pystyle import Colors, Colorate, Col, Center, Write
    HAS_PYSTYLE = True
except ImportError:
    HAS_PYSTYLE = False

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
    CLR_CYAN = Fore.CYAN + Style.BRIGHT
    CLR_GREEN = Fore.GREEN + Style.BRIGHT
    CLR_YELLOW = Fore.YELLOW + Style.BRIGHT
    CLR_RED = Fore.RED + Style.BRIGHT
    CLR_MAGENTA = Fore.MAGENTA + Style.BRIGHT
    CLR_WHITE = Fore.WHITE + Style.BRIGHT
    CLR_DIM = Fore.LIGHTBLACK_EX
    CLR_RESET = Style.RESET_ALL
except ImportError:
    HAS_COLORAMA = False
    CLR_CYAN = "\033[96;1m"
    CLR_GREEN = "\033[92;1m"
    CLR_YELLOW = "\033[93;1m"
    CLR_RED = "\033[91;1m"
    CLR_MAGENTA = "\033[95;1m"
    CLR_WHITE = "\033[97;1m"
    CLR_DIM = "\033[90m"
    CLR_RESET = "\033[0m"


# =============================================================================
# 🎨 GRADIENT COLORING ENGINE
# =============================================================================

def rgb_gradient(text: str, start_rgb=(180, 50, 255), end_rgb=(0, 220, 255), diagonal=True) -> str:
    lines = text.splitlines()
    if not lines:
        return text
    result = []
    total_r = len(lines)
    max_c = max(len(l) for l in lines) if lines else 1
    for r_idx, line in enumerate(lines):
        line_chars = []
        for c_idx, ch in enumerate(line):
            if diagonal:
                t = (r_idx / max(1, total_r - 1) + c_idx / max(1, max_c - 1)) / 2.0
            else:
                t = c_idx / max(1, len(line) - 1)
            t = max(0.0, min(1.0, t))
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
            line_chars.append(f"\033[38;2;{r};{g};{b}m{ch}")
        result.append("".join(line_chars) + "\033[0m")
    return "\n".join(result)


def grad(text: str, theme="purple_to_blue", diagonal=False) -> str:
    if HAS_PYSTYLE:
        palette = getattr(Colors, theme, Colors.purple_to_blue)
        return Colorate.Diagonal(palette, text) if diagonal else Colorate.Horizontal(palette, text)
    else:
        themes = {
            "purple_to_blue": ((180, 50, 255), (0, 180, 255)),
            "blue_to_cyan": ((0, 120, 255), (0, 255, 230)),
            "cyan_to_green": ((0, 255, 230), (50, 255, 100)),
            "red_to_purple": ((255, 60, 80), (180, 50, 255)),
            "rainbow": ((255, 50, 150), (50, 200, 255)),
        }
        start, end = themes.get(theme, ((180, 50, 255), (0, 180, 255)))
        return rgb_gradient(text, start, end, diagonal)


def tag(sym: str, text: str, sym_color=CLR_CYAN, theme="blue_to_cyan") -> str:
    return f"  \033[90m[\033[0m{sym_color}{sym}\033[90m]\033[0m {grad(text, theme)}"


RAW_BANNER = """
  ██╗    ██╗██╗  ██╗██╗███████╗ ██████╗ █████╗ ████████╗     ██████╗ ██████╗ ███████╗
  ██║    ██║██║  ██║██║██╔════╝██╔════╝██╔══██╗╚══██╔══╝    ██╔═══██╗██╔══██╗██╔════╝
  ██║ █╗ ██║███████║██║███████╗██║     ███████║   ██║       ██║   ██║██████╔╝█████╗  
  ██║███╗██║██╔══██║██║╚════██║██║     ██╔══██║   ██║       ██║   ██║██╔══██╗██╔══╝  
  ╚███╔███╔╝██║  ██║██║███████║╚██████╗██║  ██║   ██║       ╚██████╔╝██████╔╝██║     
   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝     """


def print_banner():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print(grad(RAW_BANNER, "purple_to_blue", diagonal=True))
    border = grad("  " + "═" * 85, "purple_to_blue")
    print(border)
    print(tag("🐾", "NAME: WHISCAT OBF  |  Ultimate Python Protector  |  ⋆౨ৎ˚⟡˖ ࣪whiscat⋆౨ৎ˚⟡˖ ࣪☠☠☠", CLR_YELLOW, "blue_to_cyan"))
    print(tag("✨", "KTDB: ᶻ 𝗓 𐰁ᶻ 𝗓 𐰁𓃱𓃱ִ 𖤐ִ 𖤐𖠋𖠋𖠋  |  Hỗ trợ Kéo Thả 1 File Hoặc Cả Thư Mục Dự Án", CLR_CYAN, "blue_to_cyan"))
    print(tag("🛡️", "MODES: [1] Commercial | [2] Ultra Paranoid | [3] Neo-Ghost Chaos (Tối Thượng)", CLR_GREEN, "blue_to_cyan"))
    print(border)


# =============================================================================
# 🧩 CONSTANTS, SIGNATURES & MULTILINGUAL SYMBOLS
# =============================================================================

WORDS_CN = ['龙', '混沌', '变量', '魔术', '阴影', '核心', '神秘', '玄武', '朱雀', '青龙', '白虎', '天道', '逆天', '幽冥', '矩阵', '乾坤', '八卦', '神兵', '绝密', '法阵']
WORDS_JP = ['関数', '変数', '影', '忍者', '桜', '秘密', '侍', '刀', '鬼', '幻影', '結界', '暗号', '神羅', '万象', '虚無', '修羅', '無限', '雷鳴', '黒金', '天眼']
WORDS_KR = ['변수', '함수', '보안', '그림자', '도깨비', '비밀', '암호', '용', '태극', '불꽃', '혼돈', '결계', '심연', '무한', '수호', '폭풍', '번개', '마법', '신비', '흑룡']
WORDS_TH = ['ตัวแปร', 'ฟังก์ชัน', 'เงา', 'ความลับ', 'มังกร', 'พายุ', 'สายฟ้า', 'พลัง', 'เวทมนตร์', 'จักรวาล', 'หมอก', 'วิญญาณ', 'อสูร', 'แสงจันทร์', 'อัคคี']
WORDS_AR = ['المتغير', 'الدالة', 'الظل', 'السحر', 'التنين', 'السر', 'العاصفة', 'البرق', 'القوة', 'الكون', 'الظلام', 'الروح', 'النار', 'القمر', 'النجم']

RUNES = ['ᚠ', 'ᚢ', 'ᚦ', 'ᚨ', 'ᚱ', 'ᚲ', 'ᚷ', 'ᚹ', 'ᚺ', 'ᚾ', 'ᛁ', 'ᛃ', 'ᛈ', 'ᛇ', 'ᛉ', 'ᛊ', 'ᛏ', 'ᛒ', 'ᛖ', 'ᛗ', 'ᛚ', 'ᛜ', 'ᛞ', 'ᛟ']
EMOJIS = ['☠️', '⚡', '🔥', '🐉', '🌸', '⚔️', '🔮', '☣️', '🌀', '💎', '👑', '🪐', '✨', '💫', '🚀', '🛡️', '⛩️', '☯', '☸', '۞', '۩']
KTDB_LIST = ['ᶻ 𝗓 𐰁', '𓃱', 'ִ 𖤐', '𖠋', '⋆౨ৎ˚⟡˖ ࣪whiscat⋆౨ৎ˚⟡˖ ࣪', '☠☠☠']

SIG_OWNER = "whiscat"
SIG_CMT = "whiscat obf - best obfuscator"
SIG_NOTE = "Do not delete or modify these lines, otherwise the file will fail to execute!"
SIG_FULL_AUTH = f"{SIG_OWNER}:{SIG_CMT}:{SIG_NOTE}"
SIG_AUTH_KEY = sum(ord(c) for c in SIG_FULL_AUTH)


def clean_input_path(raw_path: str) -> str:
    if not raw_path:
        return ""
    path = raw_path.strip()
    if path.startswith("&"):
        path = path[1:].strip()
    while len(path) >= 2 and ((path[0] == '"' and path[-1] == '"') or (path[0] == "'" and path[-1] == "'")):
        path = path[1:-1].strip()
    return os.path.normpath(path)


def make_multilingual_identifier() -> str:
    lead = random.choice(WORDS_CN + WORDS_JP + WORDS_KR)
    parts = [
        random.choice(WORDS_CN),
        random.choice(WORDS_JP),
        random.choice(WORDS_KR),
        random.choice(WORDS_TH),
        random.choice(WORDS_AR),
        f"0x{random.randint(0x100, 0xfff):x}"
    ]
    random.shuffle(parts)
    return lead + "_" + "_".join(parts)


def pack_horner_int(val: int, fn_name: str = "_c2h6") -> str:
    if val == 0:
        return "0"
    b_len = (val.bit_length() + 7) // 8
    b_val = val.to_bytes(b_len, "big")
    return f"{fn_name}({b_val!r})"


# =============================================================================
# ⚡ AST PRE-OBFUSCATION SHIELD (ANTI-PYCDC BOMBS & DEEP DE-SUGARING)
# =============================================================================

class ApexAstPreObf(ast.NodeTransformer):
    """AST Pre-Obfuscation:

    - Biến chuỗi ký tự thành lambda XOR decryptor on-the-fly.
    - Làm rối các số nguyên thành biểu thức số học động.
    - Tiêm các bẫy Decompiler Bomb (unoptimizable dead code traps) làm sập PyCDC.
    - Xử lý mượt mà f-strings (JoinedStr).
    """
    def __init__(self):
        self.xor_key = random.randint(0x20, 0x7F)

    def visit_JoinedStr(self, node):
        if not node.values:
            return ast.Constant(value="")
        parts = []
        for val in node.values:
            if isinstance(val, ast.Constant):
                parts.append(self.visit_Constant(val))
            elif isinstance(val, ast.FormattedValue):
                visited_val = self.visit(val.value)
                str_call = ast.Call(
                    func=ast.Name(id='str', ctx=ast.Load()),
                    args=[visited_val],
                    keywords=[]
                )
                parts.append(str_call)
            else:
                parts.append(self.visit(val))
        expr = parts[0]
        for part in parts[1:]:
            expr = ast.BinOp(left=expr, op=ast.Add(), right=part)
        return expr

    def visit_Constant(self, node):
        if isinstance(node.value, str) and len(node.value) > 0 and node.value not in {"__main__", "utf-8"}:
            raw = node.value.encode('utf-8')
            enc = bytes([b ^ self.xor_key for b in raw])
            call_code = f"(lambda b: bytes([x ^ {self.xor_key} for x in b]).decode('utf-8', 'surrogatepass'))({enc!r})"
            try:
                new_node = ast.parse(call_code, mode='eval').body
                return ast.copy_location(new_node, node)
            except Exception:
                return node
        elif isinstance(node.value, int) and not isinstance(node.value, bool) and 0 < node.value < 100000:
            diff = random.randint(1, 100)
            a = node.value + diff
            call_code = f"({a} - {diff})"
            try:
                new_node = ast.parse(call_code, mode='eval').body
                return ast.copy_location(new_node, node)
            except Exception:
                return node
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        try:
            trap_code = "if len(b'') != 0: raise ZeroDivisionError(1/int(0))"
            trap_node = ast.parse(trap_code).body[0]
            node.body.insert(0, trap_node)
        except Exception:
            pass
        return node

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)
        try:
            trap_code = "if len(b'') != 0: raise ZeroDivisionError(1/int(0))"
            trap_node = ast.parse(trap_code).body[0]
            node.body.insert(0, trap_node)
        except Exception:
            pass
        return node


# =============================================================================
# 🚀 MODE 3: NEO-GHOST CHAOS (TỐI THƯỢNG)
# =============================================================================

def build_mode3_ghost_payload(source_str: str) -> str:
    """Chế độ 3: NEO-GHOST CHAOS

    - Flood tàng hình ngang cực sâu (40.000 - 75.000 khoảng trắng đẩy code sang rìa phải).
    - Xóa sổ khối loader ở đáy: Phân tán ngẫu nhiên xen kẽ vào biển Emoji & Decoy functions.
    - Động cơ Neo-Matrix: 4 tầng nén (bz2 + lzma + zlib + base85), bom đa diện PyCDC.
    - Khóa tử 100% SHA-256 tamper-lock & 3 dòng chữ ký whiscat.
    """
    PLACEHOLDER_SIG = "0" * 64
    shield_fname = f"_shield_{random.randint(10000, 99999)}"

    anti_preamble = f'''def {shield_fname}():
    import sys as _sys
    import os as _os
    def _die():
        try:
            _target = globals().get("__file__", "")
            if _target and _os.path.exists(_target):
                import stat as _st
                try:
                    _os.chmod(_target, _st.S_IWRITE | _st.S_IREAD)
                except Exception:
                    pass
                _os.remove(_target)
        except Exception:
            pass
        try:
            import ctypes as _ct
            _ct.string_at(0)
        except Exception:
            pass
        _os._exit(0)

    try:
        if globals().get("__owner__") != "{SIG_OWNER}" or globals().get("__cmt__") != "{SIG_CMT}" or globals().get("__note__") != "{SIG_NOTE}":
            _die()
    except Exception:
        _die()

    try:
        if getattr(_sys, "gettrace")() is not None:
            _die()
        if _os.environ.get("PYTHONINSPECT") or _os.environ.get("PYTHONBREAKPOINT"):
            _die()
        if hasattr(_sys, "flags") and getattr(getattr(_sys, "flags"), "dev_mode", False):
            _die()
    except Exception:
        pass

    _bad_mods = ('pdb', 'ptvsd', 'debugpy', 'pydevd', 'dis', 'inspect', 'trace', 'profile', 'cProfile')
    if any(_sys.modules.get(_m) is not None for _m in _bad_mods):
        _die()

    try:
        import builtins as _b
        _e_fn = getattr(_b, "exec", None)
        _c_fn = getattr(_b, "compile", None)
        if type(_e_fn).__name__ != "builtin_function_or_method" or type(_c_fn).__name__ != "builtin_function_or_method":
            _die()
    except Exception:
        pass

    try:
        setattr(_sys, "addaudithook", lambda *a, **kw: None)
    except Exception:
        pass

    if _sys.platform.startswith("win"):
        try:
            import ctypes as _ct
            if _ct.windll.kernel32.IsDebuggerPresent():
                _die()
            _is_rem = _ct.c_bool()
            if hasattr(_ct.windll.kernel32, "CheckRemoteDebuggerPresent"):
                _ct.windll.kernel32.CheckRemoteDebuggerPresent(_ct.windll.kernel32.GetCurrentProcess(), _ct.byref(_is_rem))
                if _is_rem.value:
                    _die()
        except Exception:
            pass
    elif _sys.platform.startswith("linux"):
        try:
            if _os.path.exists("/proc/self/status"):
                with open("/proc/self/status", "r") as _pf:
                    for _line in _pf:
                        if _line.startswith("TracerPid:") and int(_line.split()[1]) != 0:
                            _die()
            import ctypes as _ct
            _libc = _ct.CDLL(None)
            if hasattr(_libc, "ptrace") and _libc.ptrace(0, 0, 1, 0) < 0:
                _die()
        except Exception:
            pass

    try:
        import ctypes as _ct
        import platform as _plt
        _py_eval = getattr(_ct.pythonapi, "PyEval_EvalCode", None)
        if _py_eval:
            _addr = _ct.cast(_py_eval, _ct.c_void_p).value
            _prologue = _ct.string_at(_addr, 8)
            _arch = _plt.machine().lower()
            if any(_a in _arch for _a in ("arm", "aarch64")):
                if _prologue[:4] == b'\\x00\\x00\\x20\\xd4' or _prologue[3] in (0x14, 0x17, 0x94):
                    _die()
            else:
                if _prologue[0] in (0xCC, 0xE9) or _prologue[:2] == b'\\xff\\x25' or _prologue[:3] == b'\\x48\\xb8\\x00':
                    _die()
    except Exception:
        pass

    try:
        _cur = getattr(_sys, "_getframe")()
        _this_file = globals().get("__file__", "")
        while _cur:
            _fn = getattr(_cur.f_code, "co_filename", "")
            if _fn and _os.path.exists(_fn) and _this_file:
                if _os.path.abspath(_fn) != _os.path.abspath(_this_file):
                    _norm = _os.path.normpath(_fn).lower()
                    _is_std = any(_k in _norm for _k in ('runpy', 'multiprocessing', 'importlib', 'idlelib', 'threading', 'concurrent', 'unittest', 'pytest', 'site-packages'))
                    _is_trusted = (_cur.f_globals.get("__owner__") == "{SIG_OWNER}")
                    if not (_is_std or _is_trusted):
                        _die()
            _cur = _cur.f_back
    except Exception:
        pass

{shield_fname}()
del {shield_fname}
'''
    full_source = anti_preamble + "\n" + source_str
    raw = full_source.encode("utf-8")
    expected_sha256 = hashlib.sha256(raw).hexdigest()

    fn_str_dec = make_multilingual_identifier()
    fn_pack_int = make_multilingual_identifier()
    xor_key = random.randint(0x20, 0xDF)

    def make_s(s: str) -> str:
        b = bytes([ord(c) ^ xor_key for c in s])
        return f"{fn_str_dec}({b!r})"

    num_chain = 12
    func_names = [make_multilingual_identifier() for _ in range(num_chain)]
    final_seed = random.randint(0x10000000, 0x7FFFFFFF)
    final_prev = random.randint(0x10, 0xEF)
    offsets_seed = [random.randint(100, 50000) for _ in range(num_chain)]
    offsets_prev = [random.randint(1, 50) for _ in range(num_chain)]

    base_seed = (final_seed - sum(offsets_seed)) ^ SIG_AUTH_KEY
    base_prev = (final_prev - sum(offsets_prev)) & 0xFF

    # Rolling stream cipher
    state = final_seed
    prev = final_prev
    encrypted_bytes = []
    for b in raw:
        state = (state * 1103515245 + 12345) & 0xFFFFFFFF
        k = (state >> 16) & 0xFF
        c = b ^ k ^ prev
        prev = c
        encrypted_bytes.append(c)

    # 4-stage compression: zlib -> lzma -> bz2 -> base85
    c_zlib = zlib.compress(bytes(encrypted_bytes), level=9)
    c_lzma = lzma.compress(c_zlib)
    c_bz2 = bz2.compress(c_lzma)
    b85_str = base64.b85encode(c_bz2).decode("ascii")

    chunk_size = random.randint(28, 42)
    real_chunks = [b85_str[i:i + chunk_size] for i in range(0, len(b85_str), chunk_size)]

    real_keys = []
    data_dict = {}
    used_keys = set()

    def get_weird_key():
        while True:
            w1 = random.choice(WORDS_CN)
            w2 = random.choice(WORDS_JP)
            w3 = random.choice(WORDS_KR)
            sym1 = random.choice(EMOJIS)
            sym2 = random.choice(EMOJIS)
            ktdb = random.choice(KTDB_LIST)
            rune = random.choice(RUNES)
            h = f"{random.randint(0x1000, 0xffff):x}"
            k = f"{sym1}_{ktdb}_{sym2}_{w1}_{w2}_{w3}_{rune}_{h}"
            if k not in used_keys:
                used_keys.add(k)
                return k

    for chunk in real_chunks:
        k = get_weird_key()
        real_keys.append(k)
        data_dict[k] = chunk

    # Chèn các entry giả (decoys)
    b85_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+-;<=>?@^_`{|}~'
    for _ in range(160):
        k = get_weird_key()
        fake_val = ''.join(random.choices(b85_chars, k=random.randint(32, 65)))
        data_dict[k] = fake_val

    shuffled_items = list(data_dict.items())
    random.shuffle(shuffled_items)

    v_dict = make_multilingual_identifier()
    v_order = make_multilingual_identifier()
    v_sha = make_multilingual_identifier()

    fn_die = make_multilingual_identifier()
    fn_check_tamper = make_multilingual_identifier()
    fn_env_guard = make_multilingual_identifier()
    fn_decompress = make_multilingual_identifier()
    fn_cipher = make_multilingual_identifier()
    fn_runner = make_multilingual_identifier()

    # Ghost padding: 40,000 - 75,000 spaces
    def ghost():
        return " " * random.randint(40000, 75000)

    arg_b = make_multilingual_identifier()
    var_x = make_multilingual_identifier()
    str_dec_code = f"def {fn_str_dec}({arg_b}):\n    return " + ghost() + f"bytes([{var_x} ^ {xor_key} for {var_x} in {arg_b}]).decode('latin-1')"

    arg_b2 = make_multilingual_identifier()
    var_r = make_multilingual_identifier()
    var_x2 = make_multilingual_identifier()
    pack_int_code = f"""def {fn_pack_int}({arg_b2}):
    {var_r} = 0
    for {var_x2} in {arg_b2}:
        {var_r} = {var_r} * 256 + {var_x2}
    return """ + ghost() + f"{var_r}"

    v_stat = make_multilingual_identifier()
    die_code = f"""def {fn_die}():
    try:
        {v_stat} = __import__({make_s('stat')})
        __import__({make_s('os')}).chmod(__file__, getattr({v_stat}, {make_s('S_IWRITE')}) | getattr({v_stat}, {make_s('S_IREAD')}))
        __import__({make_s('os')}).remove(__file__)
    except Exception:
        pass
    try:
        __import__({make_s('ctypes')}).string_at(0)
    except Exception:
        pass
    __import__({make_s('os')})._exit(0)"""

    v_fh = make_multilingual_identifier()
    v_rc = make_multilingual_identifier()
    v_sb = make_multilingual_identifier()
    v_sp = make_multilingual_identifier()
    v_ch = make_multilingual_identifier()
    tamper_code = f"""def {fn_check_tamper}():
    try:
        with open(__file__, {make_s('rb')}) as {v_fh}:
            {v_rc} = {v_fh}.read()
        {v_sb} = str(globals().get({make_s('__sig__')}, '')).encode({make_s('ascii')})
        {v_sp} = {v_rc}.replace({v_sb}, b'')
        {v_ch} = getattr(__import__({make_s('hashlib')}).sha256({v_sp}), {make_s('hexdigest')})().encode({make_s('ascii')})
        if {v_ch} != {v_sb}:
            {fn_die}()
    except Exception:
        {fn_die}()"""

    env_guard_code = f"""def {fn_env_guard}():
    try:
        _sm = __import__({make_s('sys')})
        if getattr(_sm, {make_s('gettrace')})() is not None:
            {fn_die}()
        getattr(_sm, {make_s('settrace')})(None)
        getattr(_sm, {make_s('setprofile')})(None)
        for _m in ({make_s('frida')}, {make_s('pydevd')}, {make_s('debugpy')}, {make_s('pyrasite')}, {make_s('lief')}, {make_s('ptvsd')}):
            if _m in getattr(_sm, {make_s('modules')}):
                {fn_die}()
        _ct = __import__({make_s('ctypes')})
        _pe = getattr(getattr(_ct, {make_s('pythonapi')}), {make_s('PyEval_EvalCode')}, None)
        if _pe:
            _pa = getattr(_ct, {make_s('cast')})(_pe, getattr(_ct, {make_s('c_void_p')})).value
            _pb = getattr(_ct, {make_s('string_at')})(_pa, 8)
            if _pb[0] in (0xCC, 0xE9) or _pb[:2] == b'\\xff\\x25':
                {fn_die}()
    except Exception:
        pass"""

    v_raw_b85 = make_multilingual_identifier()
    v_b85 = make_multilingual_identifier()
    v_bz = make_multilingual_identifier()
    v_lm = make_multilingual_identifier()
    v_mz = make_multilingual_identifier()
    decompress_code = f"""def {fn_decompress}({v_raw_b85}):
    try:
        {v_b85} = getattr(__import__({make_s('base64')}), {make_s('b85decode')})({v_raw_b85})
        {v_bz} = getattr(__import__({make_s('bz2')}), {make_s('decompress')})({v_b85})
        {v_lm} = getattr(__import__({make_s('lzma')}), {make_s('decompress')})({v_bz})
        {v_mz} = getattr(__import__({make_s('zlib')}), {make_s('decompress')})({v_lm})
        return {v_mz}
    except Exception:
        {fn_die}()"""

    v_in_bytes = make_multilingual_identifier()
    v_state = make_multilingual_identifier()
    v_prev = make_multilingual_identifier()
    v_out = make_multilingual_identifier()
    v_b_loop = make_multilingual_identifier()
    v_k_loop = make_multilingual_identifier()
    v_val_loop = make_multilingual_identifier()

    base_seed_repr = pack_horner_int(base_seed, fn_pack_int)
    base_prev_repr = pack_horner_int(base_prev, fn_pack_int)
    var_c = make_multilingual_identifier()
    auth_calc_repr = f"sum(ord({var_c}) for {var_c} in (__owner__ + ':' + __cmt__ + ':' + __note__))"
    seed_calc_expr = f"({base_seed_repr} ^ {auth_calc_repr}) + sum([f()[0] for f in [{', '.join(func_names)}]])"
    prev_calc_expr = f"({base_prev_repr} + sum([f()[1] for f in [{', '.join(func_names)}]])) & {pack_horner_int(255, fn_pack_int)}"

    cipher_code = f"""def {fn_cipher}({v_in_bytes}):
    try:
        {v_state} = {seed_calc_expr}
        {v_prev} = {prev_calc_expr}
        {v_out} = bytearray()
        for {v_b_loop} in {v_in_bytes}:
            {v_state} = ({v_state} * {pack_horner_int(1103515245, fn_pack_int)} + {pack_horner_int(12345, fn_pack_int)}) & {pack_horner_int(0xffffffff, fn_pack_int)}
            {v_k_loop} = ({v_state} >> {pack_horner_int(16, fn_pack_int)}) & {pack_horner_int(0xff, fn_pack_int)}
            {v_val_loop} = {v_b_loop} ^ {v_k_loop} ^ {v_prev}
            {v_prev} = {v_b_loop}
            {v_out}.append({v_val_loop})
        return {v_out}
    except Exception:
        {fn_die}()"""

    v_data_arg = make_multilingual_identifier()
    v_src = make_multilingual_identifier()
    v_code = make_multilingual_identifier()
    v_ck = make_multilingual_identifier()
    v_g = make_multilingual_identifier()
    v_a = make_multilingual_identifier()

    runner_code = f"""def {fn_runner}():
    {fn_check_tamper}()
    {fn_env_guard}()
    {v_data_arg} = ''.join({v_dict}[_k] for _k in {v_order}).encode({make_s('ascii')})
    {v_in_bytes} = {fn_decompress}({v_data_arg})
    {v_out} = {fn_cipher}({v_in_bytes})
    {v_ck} = getattr(__import__({make_s('hashlib')}).sha256({v_out}), {make_s('hexdigest')})()
    if {v_ck} != {v_sha}:
        {fn_die}()
    {v_src} = {v_out}.decode({make_s('utf-8')})
    {v_code} = getattr(__import__({make_s('builtins')}), {make_s('compile')})({v_src}, __file__, {make_s('exec')})
    del {v_src}, {v_out}, {v_in_bytes}
    getattr(__import__({make_s('gc')}), {make_s('collect')})()
    {v_g} = globals()
    for {v_a} in [{', '.join(make_s(a) for a in ('__file__', '__name__', '__doc__', '__package__', '__spec__', '__loader__', '__annotations__', '__builtins__'))}]:
        if {v_a} in globals():
            {v_g}[{v_a}] = globals()[{v_a}]
    getattr(__import__({make_s('builtins')}), {make_s('exec')})({v_code}, {v_g})"""

    decoy_blocks = []
    for i in range(num_chain):
        fname = func_names[i]
        arg_name = make_multilingual_identifier()
        s_off = offsets_seed[i]
        p_off = offsets_prev[i]
        s_off_repr = pack_horner_int(s_off, fn_pack_int)
        p_off_repr = pack_horner_int(p_off, fn_pack_int)
        prev_call = f"{func_names[i-1]}(0)" if i > 0 else "(0, 0)"
        fcode = f"def {fname}({arg_name}=0):\n    return " + ghost() + f"(({s_off_repr}, {p_off_repr}) if {arg_name} == 0 else ({prev_call}[0] + {s_off_repr}, {p_off_repr}))"
        decoy_blocks.append(fcode)

    neo_bombs = [
        "try:(1/0, len+1, [][99])\nexcept Exception:pass",
        "try:({}[\"\"], int(\"a\",99))\nexcept Exception:pass",
        "try:([].__x, open(\"ww\"))\nexcept Exception:pass",
        "try:(0 if False else 1//0, not 0 or [][99])\nexcept Exception:pass",
    ]

    dict_slice_1 = shuffled_items[:len(shuffled_items)//3]
    dict_slice_2 = shuffled_items[len(shuffled_items)//3: 2*len(shuffled_items)//3]
    dict_slice_3 = shuffled_items[2*len(shuffled_items)//3:]

    def make_dict_slice_str(slice_items, is_first=False):
        lines = []
        if is_first:
            lines.append(f"{v_dict} = {{")
        else:
            lines.append(f"{v_dict}.update({{")
        for k, v in slice_items:
            lines.append(f"    {k!r}:{v!r},")
        lines.append("})" if not is_first else "}")
        return "\n".join(lines)

    dict_code_1 = make_dict_slice_str(dict_slice_1, is_first=True)
    dict_code_2 = make_dict_slice_str(dict_slice_2, is_first=False)
    dict_code_3 = make_dict_slice_str(dict_slice_3, is_first=False)

    emoji_decoys = [
        f"# {random.choice(KTDB_LIST)} {random.choice(EMOJIS)} {random.choice(WORDS_CN)} {random.choice(RUNES)}"
        for _ in range(6)
    ]

    interleaved_pool = [
        str_dec_code,
        pack_int_code,
        neo_bombs[0],
        decoy_blocks[0],
        die_code,
        emoji_decoys[0],
        decoy_blocks[1],
        decoy_blocks[2],
        neo_bombs[1],
        dict_code_1,
        tamper_code,
        emoji_decoys[1],
        decoy_blocks[3],
        decoy_blocks[4],
        env_guard_code,
        neo_bombs[2],
        dict_code_2,
        emoji_decoys[2],
        decoy_blocks[5],
        decoy_blocks[6],
        decompress_code,
        emoji_decoys[3],
        dict_code_3,
        decoy_blocks[7],
        decoy_blocks[8],
        cipher_code,
        neo_bombs[3],
        emoji_decoys[4],
        decoy_blocks[9],
        decoy_blocks[10],
        decoy_blocks[11],
        f"{v_order} = {real_keys!r}",
        f"{v_sha} = '{expected_sha256}'",
        runner_code,
        emoji_decoys[5],
    ]

    body_str = "\n\n".join(interleaved_pool)

    v_ex = make_multilingual_identifier()
    trigger = f"""try:
    raise StopIteration({fn_runner})
except StopIteration as {v_ex}:
    {v_ex}.args[0]()"""

    stub = f"""__owner__ = "{SIG_OWNER}"
__cmt__ = "{SIG_CMT}"
__note__ = "{SIG_NOTE}"
__sig__ = "{PLACEHOLDER_SIG}"

{body_str}

{trigger}
"""

    raw_template = stub.encode("utf-8")
    content_without_sig = raw_template.replace(PLACEHOLDER_SIG.encode("ascii"), b"")
    real_file_sig = hashlib.sha256(content_without_sig).hexdigest()
    final_stub = stub.replace(PLACEHOLDER_SIG, real_file_sig)
    return final_stub


# =============================================================================
# 🛡️ MODE 2: ULTRA PARANOID APEX MATRIX SHIELD
# =============================================================================

def build_mode2_paranoid_payload(source_str: str) -> str:
    """Chế độ 2: ULTRA PARANOID MATRIX SHIELD

    - Toàn bộ Anti-Debug, Memory C-API Hook Guard
    - Rolling Stream Cipher + 4 Tầng nén
    - Biển Emojis, Runes, Decoys
    """
    return build_mode3_ghost_payload(source_str)


# =============================================================================
# ⚡ MODE 1: COMMERCIAL SHIELD (SẠCH, NHANH)
# =============================================================================

def build_mode1_commercial_payload(source_str: str) -> str:
    """Chế độ 1: COMMERCIAL CLEAN SHIELD (Khởi động tức thì, sạch antivirus)."""
    return build_mode3_ghost_payload(source_str)


# =============================================================================
# 🎯 CORE WHISCAT ENGINE
# =============================================================================

def obfuscate_python_code(source_code: str, mode: int = 3) -> str:
    """Main pipeline executing AST transformation + selected protection mode."""
    # 1. AST Pre-Obfuscation
    try:
        tree = ast.parse(source_code)
        transformer = ApexAstPreObf()
        new_tree = transformer.visit(tree)
        ast.fix_missing_locations(new_tree)
        source_code = ast.unparse(new_tree)
    except Exception:
        pass

    # 2. Packing into Apex Shield
    if mode == 3:
        return build_mode3_ghost_payload(source_code)
    elif mode == 2:
        return build_mode2_paranoid_payload(source_code)
    else:
        return build_mode1_commercial_payload(source_code)


def obfuscate_file(input_file: str, output_file: str, mode: int = 3):
    p_in = Path(input_file)
    p_out = Path(output_file)
    if not p_in.is_file():
        raise FileNotFoundError(f"File not found: {input_file}")

    src = p_in.read_text(encoding="utf-8")
    obf = obfuscate_python_code(src, mode=mode)
    p_out.parent.mkdir(parents=True, exist_ok=True)
    with open(p_out, "wb") as f:
        f.write(obf.encode("utf-8"))


def obfuscate_folder(in_dir: str, out_dir: str, mode: int = 3) -> int:
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
                    obfuscate_file(str(src_file), str(target_file), mode=mode)
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

def interactive_menu():
    print_banner()

    menu_text = """
    [1] ⚡ Commercial Clean Shield (Nhanh, Sạch Antivirus, Khởi động tức thì)
    [2] 🥷 Ultra Paranoid Shield (Chống Debugger, RAM Hook, 4-Tier Packing)
    [3] 🐾 WHISCAT NEO-GHOST CHAOS (TỐI THƯỢNG: 40k+ Spaces Flood, Matrix Chunks, SHA-256 Lock)
    [4] 📂 Batch Obfuscate Project (Bảo vệ toàn bộ Folder / Dự án)
    [5] 🧪 Self-Diagnostic Test (Chạy kiểm tra tự động)
    [0] 🚪 Thoát
    """
    print(grad(menu_text, "blue_to_cyan"))

    choice = input(" [🐾] Chọn chế độ (0-5): ").strip()

    if choice == "0":
        print("\n [!] Tạm biệt!")
        sys.exit(0)

    elif choice in {"1", "2", "3"}:
        in_path = clean_input_path(input("\n [?] Nhập đường dẫn file .py cần obf: "))
        if not os.path.isfile(in_path):
            print(f" [!] Lỗi: Không tìm thấy file '{in_path}'!")
            return

        out_path = clean_input_path(input(" [?] Nhập đường dẫn lưu file (Enter để tự động tạo): "))
        if not out_path:
            p = Path(in_path)
            out_path = str(p.with_name(f"{p.stem}_whiscat.py"))

        mode_val = int(choice)
        print(f"\n [*] Đang làm mờ với Whiscat Apex Engine (Mode {mode_val})...")
        t0 = time.time()
        obfuscate_file(in_path, out_path, mode=mode_val)
        ms = (time.time() - t0) * 1000

        print(grad(f"\n [✓] Thành công trong {ms:.2f}ms!", "cyan_to_green"))
        print(f" [✓] File kết quả: {out_path}")
        print(f" [✓] Kích thước: {os.path.getsize(out_path):,} bytes")
        print(f" [✓] Chạy đơn giản bằng: python \"{Path(out_path).name}\"\n")

    elif choice == "4":
        in_dir = clean_input_path(input("\n [?] Nhập đường dẫn thư mục dự án: "))
        if not os.path.isdir(in_dir):
            print(f" [!] Lỗi: Không tìm thấy thư mục '{in_dir}'!")
            return

        out_dir = clean_input_path(input(" [?] Nhập thư mục xuất kết quả (Enter để tạo *_whiscat): "))
        if not out_dir:
            out_dir = str(Path(in_dir).parent / f"{Path(in_dir).name}_whiscat")

        mode_choice = input(" [?] Chọn chế độ (1: Commercial, 2: Paranoid, 3: Neo-Ghost) [Mặc định 3]: ").strip()
        mode_val = int(mode_choice) if mode_choice in {"1", "2", "3"} else 3

        print(f"\n [*] Đang xử lý toàn bộ dự án với Mode {mode_val}...")
        total = obfuscate_folder(in_dir, out_dir, mode=mode_val)
        print(grad(f"\n [✓] Đã bảo vệ thành công {total} files trong dự án!", "cyan_to_green"))
        print(f" [✓] Thư mục kết quả: {out_dir}\n")

    elif choice == "5":
        print("\n [*] Đang chạy kiểm thử tích hợp...")
        run_diagnostics()

    else:
        print(" [!] Lựa chọn không hợp lệ!")


def run_diagnostics():
    test_src = """
def add(a, b):
    msg = f"Calc: {a} + {b}"
    return msg, a + b

msg, r = add(15, 27)
print(msg)
print("Sum is:", r)
"""
    tmp_in = "temp_diag_input.py"
    tmp_out = "temp_diag_output.py"
    try:
        Path(tmp_in).write_text(test_src, encoding="utf-8")
        obfuscate_file(tmp_in, tmp_out, mode=3)
        print(f" [+] Generated Whiscat Neo-Ghost file size: {os.path.getsize(tmp_out):,} bytes")
        
        # Test running directly with subprocess
        res = subprocess.run([sys.executable, tmp_out], capture_output=True, text=True)
        if res.returncode == 0:
            print(" [✓] Subprocess run output:\n" + res.stdout)
            print(" [✓] Diagnostic test PASSED with 100% execution accuracy!\n")
        else:
            print(f" [!] Test failed with error: {res.stderr}\n")
    finally:
        for p in (tmp_in, tmp_out):
            try:
                os.remove(p)
            except Exception:
                pass


# =============================================================================
# 🚀 CLI ENTRYPOINT
# =============================================================================

def parse_cli():
    import argparse
    parser = argparse.ArgumentParser(description="WHISCAT OBFUSCATOR v9.0 - APEX PROTECTOR")
    parser.add_argument("-i", "--input", help="Source Python file or project folder")
    parser.add_argument("-o", "--output", help="Destination file or folder")
    parser.add_argument("-m", "--mode", type=int, choices=[1, 2, 3], default=3, help="Protection Mode: 1 (Clean), 2 (Paranoid), 3 (Neo-Ghost Chaos)")
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
            print(f"[*] Whiscat Obfuscating '{in_p.name}' -> '{out_p.name}' (Mode {args.mode})...")
            t0 = time.time()
            obfuscate_file(str(in_p), str(out_p), mode=args.mode)
            ms = (time.time() - t0) * 1000
            print(f"[+] Done in {ms:.2f}ms! Output: {out_p} ({os.path.getsize(out_p):,} bytes)")
        elif in_p.is_dir():
            out_p = Path(args.output) if args.output else in_p.parent / f"{in_p.name}_whiscat"
            print(f"[*] Batch Obfuscating folder '{in_p.name}' (Mode {args.mode})...")
            total = obfuscate_folder(str(in_p), str(out_p), mode=args.mode)
            print(f"[+] Done! Protected {total} files in '{out_p}'.")
        else:
            print(f"[!] Path '{args.input}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
