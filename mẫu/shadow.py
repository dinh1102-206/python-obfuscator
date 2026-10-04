#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
  SHADOW-OBFUSCATOR v8.0 - TDINH SPECIAL EDITION ⋆౨ৎ˚⟡˖ ࣪☠☠☠
=============================================================================
- Owner: tdinh | Comment: best obfuscator
- Signature Tamper-Lock: Khóa chặt 3 dòng chữ ký (__owner__, __cmt__, __note__).
  Nếu bị xóa hoặc sửa dù chỉ 1 ký tự -> NameError / Giải mã sai / Tự dừng ngay!
- Ma trận ngập tràn Emojis & Ký tự đặc biệt (ktdb):
  ᶻ 𝗓 𐰁ᶻ 𝗓 𐰁𓃱𓃱ִ 𖤐ִ 𖤐𖠋𖠋𖠋⋆౨ৎ˚⟡˖ ࣪tdinh⋆౨ৎ˚⟡˖ ࣪☠☠☠
- HỖ TRỢ LÀM RỐI CẢ THƯ MỤC / TOÀN BỘ DỰ ÁN (BATCH FOLDER OBFUSCATION):
  Kéo thả 1 file .py lẻ hoặc nguyên cả thư mục dự án -> Tự động xử lý toàn bộ!
- Đầy đủ lá chắn tối thượng: Anti-PyCDC, 2D Matrix, Caller Stack Check,
  Anti-Debug đa nền tảng, Rolling Stream Cipher, SHA-256, In-Place RAM Purge.
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
from colorama import init, Fore, Back, Style

# Cấu hình UTF-8 an toàn cho console Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

init(autoreset=True)

# Kiểm tra pystyle (Tsunami & Pymeomeo engine)
try:
    from pystyle import Colors, Colorate, Col, Center, Write
    HAS_PYSTYLE = True
except ImportError:
    HAS_PYSTYLE = False

# Bảng màu Colorama ANSI chuẩn
CLR_CYAN = Fore.CYAN + Style.BRIGHT
CLR_GREEN = Fore.GREEN + Style.BRIGHT
CLR_YELLOW = Fore.YELLOW + Style.BRIGHT
CLR_RED = Fore.RED + Style.BRIGHT
CLR_MAGENTA = Fore.MAGENTA + Style.BRIGHT
CLR_WHITE = Fore.WHITE + Style.BRIGHT
CLR_DIM = Fore.LIGHTBLACK_EX
CLR_RESET = Style.RESET_ALL

def rgb_gradient(text: str, start_rgb=(180, 50, 255), end_rgb=(0, 220, 255), diagonal=True) -> str:
    """Fallback tự sinh dải màu TrueColor 24-bit ANSI khi môi trường không có pystyle."""
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
    """Tạo gradient neon rực rỡ phong cách Pymeomeo / Tsunami."""
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
    """Format thẻ thông tin có biểu tượng và gradient neon."""
    return f"  \033[90m[\033[0m{sym_color}{sym}\033[90m]\033[0m {grad(text, theme)}"

RAW_BANNER = """
  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗     ██████╗ ██████╗ ███████╗
  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║    ██╔═══██╗██╔══██╗██╔════╝
  ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║    ██║   ██║██████╔╝█████╗  
  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║    ██║   ██║██╔══██╗██╔══╝  
  ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝    ╚██████╔╝██████╔╝██║     
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝      ╚═════╝ ╚═════╝ ╚═╝     """

def print_banner():
    print(grad(RAW_BANNER, "purple_to_blue", diagonal=True))
    border = grad("  " + "═" * 85, "purple_to_blue")
    print(border)
    print(tag("👑", "OWNER: tdinh  |  best obfuscator  |  ⋆౨ৎ˚⟡˖ ࣪tdinh⋆౨ৎ˚⟡˖ ࣪☠☠☠", CLR_YELLOW, "blue_to_cyan"))
    print(tag("✨", "KTDB: ᶻ 𝗓 𐰁ᶻ 𝗓 𐰁𓃱𓃱ִ 𖤐ִ 𖤐𖠋𖠋𖠋  |  Hỗ trợ Kéo Thả 1 File Hoặc Cả Thư Mục Dự Án", CLR_CYAN, "blue_to_cyan"))
    print(tag("🛡️", "PROFILES: [1] Commercial | [2] Ultra Paranoid | [3] Neo-Ghost Chaos", CLR_GREEN, "blue_to_cyan"))
    print(border)

BANNER = grad(RAW_BANNER, "purple_to_blue", diagonal=True)


WORDS_CN = ['龙', '混沌', '变量', '魔术', '阴影', '核心', '神秘', '玄武', '朱雀', '青龙', '白虎', '天道', '逆天', '幽冥', '矩阵', '乾坤', '八卦', '神兵', '绝密', '法阵']
WORDS_JP = ['関数', '変数', '影', '忍者', '桜', '秘密', '侍', '刀', '鬼', '幻影', '結界', '暗号', '神羅', '万象', '虚無', '修羅', '無限', '雷鳴', '黒金', '天眼']
WORDS_KR = ['변수', '함수', '보안', '그림자', '도깨비', '비밀', '암호', '용', '태극', '불꽃', '혼돈', '결계', '심연', '무한', '수호', '폭풍', '번개', '마법', '신비', '흑룡']
WORDS_TH = ['ตัวแปร', 'ฟังก์ชัน', 'เงา', 'ความลับ', 'มังกร', 'พายุ', 'สายฟ้า', 'พลัง', 'เวทมนตร์', 'จักรวาล', 'หมอก', 'วิญญาณ', 'อสูร', 'แสงจันทร์', 'อัคคี']
WORDS_AR = ['المتغير', 'الدالة', 'الظل', 'السحر', 'التنين', 'السر', 'العاصفة', 'البرق', 'القوة', 'الكون', 'الظلام', 'الروح', 'النار', 'القمر', 'النجم']
WORDS_ID = ['bayangan', 'rahasia', 'kekuatan', 'hantu', 'kutukan', 'badai', 'petir', 'keabadian', 'alam_semesta', 'kegelapan', 'sang_naga', 'batu_mistis']

RUNES = ['ᚠ', 'ᚢ', 'ᚦ', 'ᚨ', 'ᚱ', 'ᚲ', 'ᚷ', 'ᚹ', 'ᚺ', 'ᚾ', 'ᛁ', 'ᛃ', 'ᛈ', 'ᛇ', 'ᛉ', 'ᛊ', 'ᛏ', 'ᛒ', 'ᛖ', 'ᛗ', 'ᛚ', 'ᛜ', 'ᛞ', 'ᛟ']
EMOJIS = ['☠️', '⚡', '🔥', '🐉', '🌸', '⚔️', '🔮', '☣️', '🌀', '💎', '👑', '🪐', '✨', '💫', '🚀', '🛡️', '⛩️', '☯', '☸', '۞', '۩']
KTDB_LIST = ['ᶻ 𝗓 𐰁', '𓃱', 'ִ 𖤐', '𖠋', '⋆౨ৎ˚⟡˖ ࣪tdinh⋆౨ৎ˚⟡˖ ࣪', '☠☠☠']

# Thông tin chữ ký độc quyền của tdinh
SIG_OWNER = "tdinh"
SIG_CMT = "best obfuscator"
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

def build_2d_matrix_builder():
    chars_needed = set("abcdefghijklmnopqrstuvwxyz0123456789_")
    char_list = list(chars_needed)
    random.shuffle(char_list)
    grid_w = 8
    grid = [char_list[i:i + grid_w] for i in range(0, len(char_list), grid_w)]
    
    char_map = {}
    for r_idx, row in enumerate(grid):
        for c_idx, ch in enumerate(row):
            char_map[ch] = (r_idx, c_idx)
            
    def get_repr(s: str, grid_var: str) -> str:
        parts = [f"{grid_var}[{char_map[c][0]}][{char_map[c][1]}]" for c in s]
        return " + ".join(parts)
        
    return grid, get_repr

def make_unreadable_var(prefix: str = "") -> str:
    bc1 = "".join(random.choices(["I", "l"], k=random.randint(2, 4)))
    word = random.choice(WORDS_CN + WORDS_JP + WORDS_KR + WORDS_TH + WORDS_AR)
    bc2 = "".join(random.choices(["I", "l"], k=random.randint(2, 4)))
    h = f"0x{random.randint(0x100, 0xfff):x}"
    if prefix:
        return f"_{prefix}_{bc1}_{word}_{bc2}_{h}"
    return f"_{bc1}_{word}_{bc2}_{h}"

def pack_horner_int(val: int, fn_name: str = "_c2h6") -> str:
    if val == 0:
        return "0"
    b_len = (val.bit_length() + 7) // 8
    b_val = val.to_bytes(b_len, "big")
    return f"{fn_name}({b_val!r})"

class ApexAstPreObf(ast.NodeTransformer):
    """
    TẦNG BẢO VỆ AST TRƯỚC KHI NÉN (AST PRE-OBFUSCATION SHIELD):
    - Biến toàn bộ chuỗi ký tự (strings) thành dynamic lambda XOR decoders on-the-fly.
    - Làm rối các số nguyên (ints) thành biểu thức số học động.
    - Tiêm các bẫy Decompiler Bomb (unoptimizable dead code traps) vào hàm để làm sập PyCDC.
    - Giữ nguyên 100% logic của JoinedStr (f-strings) và các cấu trúc cú pháp Python.
    """
    def __init__(self):
        self.xor_key = random.randint(0x20, 0x7f)

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
        if isinstance(node.value, str) and len(node.value) > 0:
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

def build_mode3_ghost_payload(source_str: str) -> str:
    """Chế độ 3: NEO-GHOST CHAOS
    - Flood tàng hình ngang cực sâu (40.000 - 80.000 khoảng trắng đẩy code sang rìa phải mấy trăm KB).
    - Xóa sổ khối loader ở đáy: Toàn bộ hàm giải mã, decompressor, tamper-check, env-guard
      được trà trộn và phân tán ngẫu nhiên xen kẽ vào biển Emoji & Decoy functions.
    - Động cơ Neo-Matrix: 4 tầng nén (bz2 + lzma + zlib + base85), bom đa diện PyCDC, sys.monitoring.
    - Khóa tử 100% SHA-256 tamper-lock & 3 dòng chữ ký tdinh.
    """
    PLACEHOLDER_SIG = "0" * 64
    shield_fname = f"_shield_{random.randint(10000, 99999)}"

    # Full shield: Anti-Debug, Anti-Inspect, Stack Frame Caller
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
            import winreg as _wr
            _key = _wr.OpenKey(_wr.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings")
            _val, _ = _wr.QueryValueEx(_key, "ProxyServer")
            if _val and ("127.0.0.1" in _val or "8001" in _val or "8888" in _val):
                _die()
        except Exception:
            pass
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
    xor_key = random.randint(0x20, 0xdf)

    def make_s(s: str) -> str:
        b = bytes([ord(c) ^ xor_key for c in s])
        return f"{fn_str_dec}({b!r})"

    num_chain = 12
    func_names = [make_multilingual_identifier() for _ in range(num_chain)]
    final_seed = random.randint(0x10000000, 0x7fffffff)
    final_prev = random.randint(0x10, 0xef)
    offsets_seed = [random.randint(100, 50000) for _ in range(num_chain)]
    offsets_prev = [random.randint(1, 50) for _ in range(num_chain)]

    base_seed = (final_seed - sum(offsets_seed)) ^ SIG_AUTH_KEY
    base_prev = (final_prev - sum(offsets_prev)) & 0xff

    # Rolling stream cipher
    state = final_seed
    prev = final_prev
    encrypted_bytes = []
    for b in raw:
        state = (state * 1103515245 + 12345) & 0xffffffff
        k = (state >> 16) & 0xff
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

    # Decoy dictionary entries
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

    # Ghost padding helper: 40,000 - 75,000 spaces pushing code hundreds of KB to the right
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
        try:
            _mn = getattr(_sm, {make_s('monitoring')}, None)
            if _mn:
                for _ev in getattr(_mn, {make_s('get_events')})().values():
                    if _ev:
                        {fn_die}()
        except Exception:
            pass
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

def build_tdinh_apex_payload(source_str: str, mode: int = 1, target_kb: int = None) -> str:
    # 0. Áp dụng bộ làm rối AST tiền xử lý (AST Pre-Obfuscation Shield)
    try:
        if hasattr(ast, "unparse"):
            tree = ast.parse(source_str)
            transformer = ApexAstPreObf()
            new_tree = transformer.visit(tree)
            ast.fix_missing_locations(new_tree)
            source_str = ast.unparse(new_tree)
    except Exception:
        pass

    if mode == 3:
        return build_mode3_ghost_payload(source_str)

    if target_kb is None:
        target_kb = 45 if mode == 1 else 280

    PLACEHOLDER_SIG = "0" * 64
    shield_fname = f"_shield_{random.randint(10000, 99999)}"

    if mode == 1:
        # Chế độ Thương Mại: Sạch Antivirus, không API nhạy cảm, khởi động tức thì
        anti_preamble = f'''def {shield_fname}():
    import sys as _sys
    import os as _os
    def _die():
        try:
            _target = globals().get("__file__", "")
            if _target and _os.path.exists(_target):
                _os.remove(_target)
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
    else:
        # Chế độ Ultra Paranoid Shield: Full phòng thủ kernel & memory
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
            import winreg as _wr
            _rk = _wr.OpenKey(_wr.HKEY_CURRENT_USER, r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Internet Settings")
            _px_en, _ = _wr.QueryValueEx(_rk, "ProxyEnable")
            if bool(_px_en):
                _srv, _ = _wr.QueryValueEx(_rk, "ProxyServer")
                if any(_p in str(_srv) for _p in ("8001", "8888", "8080", "127.0.0.1", "localhost")):
                    _die()
            _wr.CloseKey(_rk)
        except Exception:
            pass

    if _sys.platform.startswith("win"):
        try:
            import ctypes as _ct
            if hasattr(_ct, "windll") and hasattr(_ct.windll, "kernel32"):
                _k32 = _ct.windll.kernel32
                if _k32.IsDebuggerPresent() != 0:
                    _die()
                _is_rem = _ct.c_bool()
                _k32.CheckRemoteDebuggerPresent(_k32.GetCurrentProcess(), _ct.byref(_is_rem))
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

    # Chống Frida & C-API Dynamic Hooking trên PyEval_EvalCode đa nền tảng (x86/x64/ARM64)
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
        if _sys.platform.startswith("win"):
            _k32 = getattr(_ct, "windll", None)
            if _k32 and hasattr(_k32, "kernel32"):
                for _mod in (b"frida-agent.dll", b"frida-gadget.dll", b"frida-agent-64.dll", b"frida-agent-32.dll"):
                    if _k32.kernel32.GetModuleHandleA(_mod):
                        _die()
        elif _sys.platform.startswith("linux"):
            if _os.path.exists("/proc/self/maps"):
                with open("/proc/self/maps", "r") as _mf:
                    _maps = _mf.read().lower()
                    if any(_f in _maps for _f in ("frida", "gadget", "linjector")):
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
    
    # 1. Bảng ma trận ký tự 2D
    grid_var = f"_0xM{random.randint(1000, 9999):x}"
    grid_data, get_grid_repr = build_2d_matrix_builder()
    
    str_zlib = get_grid_repr("zlib", grid_var)
    str_base64 = get_grid_repr("base64", grid_var)
    str_builtins = get_grid_repr("builtins", grid_var)
    str_sys = get_grid_repr("sys", grid_var)
    str_os = get_grid_repr("os", grid_var)
    str_time = get_grid_repr("time", grid_var)
    str_gc = get_grid_repr("gc", grid_var)
    str_ctypes = get_grid_repr("ctypes", grid_var)
    str_hashlib = get_grid_repr("hashlib", grid_var)
    str_decomp = get_grid_repr("decompress", grid_var)
    str_b85 = get_grid_repr("b85decode", grid_var)
    str_sha = get_grid_repr("sha256", grid_var)
    str_hex = get_grid_repr("hexdigest", grid_var)
    str_exec = get_grid_repr("exec", grid_var)
    str_compile = get_grid_repr("compile", grid_var)
    
    # 2. Sinh mạng lưới hàm đa ngôn ngữ liên hoàn
    fn_str_dec = make_unreadable_var("str")
    fn_pack_int = make_unreadable_var("num")

    num_chain = 12
    func_names = [make_multilingual_identifier() for _ in range(num_chain)]
    
    final_seed = random.randint(0x10000000, 0x7fffffff)
    final_prev = random.randint(0x10, 0xef)
    
    offsets_seed = [random.randint(100, 50000) for _ in range(num_chain)]
    offsets_prev = [random.randint(1, 50) for _ in range(num_chain)]
    
    # KHÓA TỬ THẦN CHO 3 DÒNG CHỮ KÝ:
    base_seed = (final_seed - sum(offsets_seed)) ^ SIG_AUTH_KEY
    base_prev = (final_prev - sum(offsets_prev)) & 0xff
    
    chain_funcs_code = []
    for i in range(num_chain):
        fname = func_names[i]
        arg_name = make_unreadable_var("a")
        matrix = [pack_horner_int(random.randint(100, 9999), fn_pack_int) for _ in range(8)]
        s_off = offsets_seed[i]
        p_off = offsets_prev[i]
        s_off_repr = pack_horner_int(s_off, fn_pack_int)
        p_off_repr = pack_horner_int(p_off, fn_pack_int)
        mat_var = make_unreadable_var("m")
        dummy_var = make_unreadable_var("d")
        x_var = make_unreadable_var("x")
        
        prev_call = f"{func_names[i-1]}(0)" if i > 0 else "(0, 0)"
        
        fcode = f"""def {fname}({arg_name}=0):
    {mat_var} = [{', '.join(matrix)}]
    {dummy_var} = sum({x_var} ^ {pack_horner_int(random.randint(10, 255), fn_pack_int)} for {x_var} in {mat_var})
    return ({s_off_repr}, {p_off_repr}) if {arg_name} == 0 else ({prev_call}[0] + {s_off_repr}, {p_off_repr})
"""
        chain_funcs_code.append(fcode)
        
    # 3. Mã hóa Rolling Stream Cipher đa hình
    state = final_seed
    prev = final_prev
    encrypted_bytes = []
    for b in raw:
        state = (state * 1103515245 + 12345) & 0xffffffff
        k = (state >> 16) & 0xff
        c = b ^ k ^ prev
        prev = c
        encrypted_bytes.append(c)
        
    compressed = zlib.compress(bytes(encrypted_bytes), level=9)
    b85_str = base64.b85encode(compressed).decode("ascii")
    
    chunk_size = random.randint(28, 40)
    real_chunks = [b85_str[i:i + chunk_size] for i in range(0, len(b85_str), chunk_size)]
    
    target_bytes = target_kb * 1024
    if mode == 1:
        needed_decoys = max(20, int((target_bytes * 0.35) / 130))
    else:
        needed_decoys = max(350, int((target_bytes * 0.72) / 220))
    
    real_keys = []
    data_dict = {}
    used_keys = set()
    
    # Tạo key từ điển ngập tràn Emoji & Ký tự đặc biệt (ktdb)
    def get_weird_key():
        while True:
            w1 = random.choice(WORDS_CN)
            w2 = random.choice(WORDS_JP)
            w3 = random.choice(WORDS_KR)
            w4 = random.choice(WORDS_TH)
            w5 = random.choice(WORDS_AR)
            w6 = random.choice(WORDS_ID)
            sym1 = random.choice(EMOJIS)
            sym2 = random.choice(EMOJIS)
            ktdb = random.choice(KTDB_LIST)
            rune = random.choice(RUNES)
            h = f"{random.randint(0x1000, 0xffff):x}"
            k = f"{sym1}_{ktdb}_{sym2}_{w1}_{w2}_{w3}_{w4}_{w5}_{w6}_{rune}_{h}"
            if k not in used_keys:
                used_keys.add(k)
                return k

    for chunk in real_chunks:
        k = get_weird_key()
        real_keys.append(k)
        data_dict[k] = chunk
        
    b85_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+-;<=>?@^_`{|}~'
    for _ in range(needed_decoys):
        k = get_weird_key()
        fake_val = ''.join(random.choices(b85_chars, k=random.randint(32, 75)))
        data_dict[k] = fake_val

    shuffled_items = list(data_dict.items())
    random.shuffle(shuffled_items)
    
    v_dict = f"混沌_マトリックス_비밀_{random.choice(WORDS_TH)}_{random.choice(WORDS_AR)}_0x{random.randint(1000, 9999):x}"
    v_order = f"ลำดับ_الترتيب_순서_秩序_0x{random.randint(1000, 9999):x}"
    v_sha = f"تجزئة_แฮช_해시_検証_0x{random.randint(1000, 9999):x}"
    v_loader = make_multilingual_identifier()
    
    dict_repr_lines = []
    dict_repr_lines.append(f"{v_dict} = {{")
    for k, v in shuffled_items:
        p_sp = " " * (random.randint(10, 25) if mode == 1 else random.randint(250, 450))
        dict_repr_lines.append(f"    {k!r}:{p_sp}{v!r},")
    dict_repr_lines.append("}")
    dict_repr_str = "\n".join(dict_repr_lines)
    
    decoy_code_str = "\n".join(chain_funcs_code)
    
    # Biểu thức tính toán hạt giống khóa: bắt buộc phải có __owner__, __cmt__, __note__
    base_seed_repr = pack_horner_int(base_seed, fn_pack_int)
    base_prev_repr = pack_horner_int(base_prev, fn_pack_int)
    var_c = make_unreadable_var("c")
    auth_calc_repr = f"sum(ord({var_c}) for {var_c} in (__owner__ + ':' + __cmt__ + ':' + __note__))"
    seed_calc_expr = f"({base_seed_repr} ^ {auth_calc_repr}) + sum([f()[0] for f in [{', '.join(func_names)}]])"
    prev_calc_expr = f"({base_prev_repr} + sum([f()[1] for f in [{', '.join(func_names)}]])) & {pack_horner_int(255, fn_pack_int)}"
    
    pycdc_divisions = "1/int(0)," * (60 if mode == 1 else 1500)
    pad_grid = " " * (random.randint(20, 50) if mode == 1 else random.randint(800, 1200))
    pad_order = " " * (random.randint(20, 50) if mode == 1 else random.randint(800, 1200))
    pad_sha = " " * (random.randint(20, 50) if mode == 1 else random.randint(800, 1200))
    
    xor_key = random.randint(0x20, 0xdf)
    def make_s(s: str) -> str:
        b = bytes([ord(c) ^ xor_key for c in s])
        return f"{fn_str_dec}({b!r})"
    
    # Tên biến unreadable hỗn độn cho helper và loader
    arg_b = make_unreadable_var("b")
    var_x = make_unreadable_var("x")
    arg_b2 = make_unreadable_var("b")
    var_r = make_unreadable_var("r")
    var_x2 = make_unreadable_var("x")
    v_trap = make_unreadable_var("tr")

    v_os = make_unreadable_var("os")
    v_time = make_unreadable_var("tm")
    v_ct = make_unreadable_var("ct")
    v_b = make_unreadable_var("bi")
    v_t_start = make_unreadable_var("ts")
    v_z = make_unreadable_var("z")
    v_b85 = make_unreadable_var("b8")
    v_e = make_unreadable_var("ex")
    v_c = make_unreadable_var("cp")
    v_hash = make_unreadable_var("hs")
    v_data = make_unreadable_var("dt")
    v_decomp = make_unreadable_var("dc")
    v_ex_mem = make_unreadable_var("em")
    v_st = make_unreadable_var("st")
    v_state = make_unreadable_var("se")
    v_prev = make_unreadable_var("pv")
    v_bytearray = make_unreadable_var("ba")
    v_decrypted = make_unreadable_var("dy")
    v_byte = make_unreadable_var("bt")
    v_k = make_unreadable_var("k")
    v_val = make_unreadable_var("vl")
    v_check_sha = make_unreadable_var("cs")
    v_src_text = make_unreadable_var("sc")
    v_code_obj = make_unreadable_var("co")
    v_s_id = make_unreadable_var("id")
    v_raw_mem = make_unreadable_var("rm")
    v_first_bytes = make_unreadable_var("fb")
    v_offset = make_unreadable_var("of")
    v_g = make_unreadable_var("gl")
    v_attr = make_unreadable_var("at")
    v_ex_stop = make_unreadable_var("es")
    v_xt = make_unreadable_var("xt")
    v_ex_sys = make_unreadable_var("ey")
    v_run_init = make_unreadable_var("ri")
    v_k_loop = make_unreadable_var("kl")

    # Biến kiểm tra tính toàn vẹn 100% của toàn bộ file
    v_fh = make_unreadable_var("fh")
    v_rc = make_unreadable_var("rc")
    v_sb = make_unreadable_var("sb")
    v_sp = make_unreadable_var("sp")
    v_ch = make_unreadable_var("ch")
    v_die_ldr = make_unreadable_var("die")
    v_stat = make_unreadable_var("stt")

    if mode == 1:
        die_impl = f'''    def {v_die_ldr}():
        try:
            {v_os}.remove(__file__)
        except Exception:
            pass
        {v_os}._exit(0)'''
        mem_clean_impl = f'''    del {v_decrypted}
    del {v_decomp}
    del {v_data}
    del {v_src_text}
    getattr(__import__({make_s('gc')}), {make_s('collect')})()'''
        hook_check_impl = ""
        timeout_limit = f"{pack_horner_int(6, fn_pack_int)}"
    else:
        die_impl = f'''    def {v_die_ldr}():
        try:
            {v_stat} = __import__({make_s('stat')})
            {v_os}.chmod(__file__, getattr({v_stat}, {make_s('S_IWRITE')}) | getattr({v_stat}, {make_s('S_IREAD')}))
            {v_os}.remove(__file__)
        except Exception:
            pass
        try:
            __import__({make_s('ctypes')}).string_at(0)
        except Exception:
            pass
        {v_os}._exit(0)'''
        mem_clean_impl = f'''    try:
        {v_s_id} = id({v_src_text})
        {v_raw_mem} = getattr({v_ct}, {make_s('string_at')})({v_s_id}, {pack_horner_int(128, fn_pack_int)})
        {v_first_bytes} = {v_src_text}[:min({pack_horner_int(8, fn_pack_int)}, len({v_src_text}))].encode({make_s('utf-8')})
        {v_offset} = {v_raw_mem}.find({v_first_bytes})
        if {v_offset} != -1:
            getattr({v_ct}, {make_s('memset')})({v_s_id} + {v_offset}, 0, len({v_src_text}.encode({make_s('utf-8')})))
    except Exception:
        pass
    {v_decrypted}[:] = b'\\\\x00' * len({v_decrypted})
    del {v_decrypted}
    del {v_decomp}
    del {v_data}
    del {v_src_text}
    getattr(__import__({make_s('gc')}), {make_s('collect')})()'''
        hook_check_impl = f'''    try:
        _pe = getattr(getattr({v_ct}, {make_s('pythonapi')}), {make_s('PyEval_EvalCode')}, None)
        if _pe:
            _pa = getattr({v_ct}, {make_s('cast')})(_pe, getattr({v_ct}, {make_s('c_void_p')})).value
            _pb = getattr({v_ct}, {make_s('string_at')})(_pa, 8)
            if _pb[0] in (0xCC, 0xE9) or _pb[:2] == b'\\\\xff\\\\x25':
                {v_die_ldr}()
    except Exception:
        pass'''
        timeout_limit = f"{pack_horner_int(2, fn_pack_int)}"

    stub = f"""__owner__ = "{SIG_OWNER}"
__cmt__ = "{SIG_CMT}"
__note__ = "{SIG_NOTE}"
__sig__ = "{PLACEHOLDER_SIG}"

try:
    {v_trap} = ({pycdc_divisions})
except Exception:
    pass

def {fn_str_dec}({arg_b}):
    return bytes([{var_x} ^ {xor_key} for {var_x} in {arg_b}]).decode('latin-1')

def {fn_pack_int}({arg_b2}):
    {var_r} = 0
    for {var_x2} in {arg_b2}:
        {var_r} = {var_r} * 256 + {var_x2}
    return {var_r}

{grid_var}{pad_grid}={pad_grid}{grid_data!r}

{decoy_code_str}

{dict_repr_str}

{v_order}{pad_order}={pad_order}{real_keys!r}
{v_sha}{pad_sha}={pad_sha}'{expected_sha256}'

def {v_loader}():
    {v_b} = __import__({make_s('builtins')})
    {v_os} = __import__({make_s('os')})
    {v_hash} = getattr(__import__({make_s('hashlib')}), {make_s('sha256')})

{die_impl}

    try:
        with open(__file__, {make_s('rb')}) as {v_fh}:
            {v_rc} = {v_fh}.read()
        {v_sb} = str(globals().get({make_s('__sig__')}, '')).encode({make_s('ascii')})
        {v_sp} = {v_rc}.replace({v_sb}, b'')
        {v_ch} = getattr({v_hash}({v_sp}), {make_s('hexdigest')})().encode({make_s('ascii')})
        if {v_ch} != {v_sb}:
            {v_die_ldr}()
    except Exception:
        {v_die_ldr}()

    {v_time} = __import__({make_s('time')})
    {v_ct} = __import__({make_s('ctypes')})
    {v_t_start} = getattr({v_time}, {make_s('perf_counter')})()
    
    {v_z} = getattr(__import__({make_s('zlib')}), {make_s('decompress')})
    {v_b85} = getattr(__import__({make_s('base64')}), {make_s('b85decode')})
    {v_e} = getattr({v_b}, {make_s('exec')})
    {v_c} = getattr({v_b}, {make_s('compile')})

    if type({v_e}).__name__ != {make_s('builtin_function_or_method')} or type({v_c}).__name__ != {make_s('builtin_function_or_method')}:
        {v_die_ldr}()
    
    {v_data} = ''.join({v_dict}[{v_k_loop}] for {v_k_loop} in {v_order}).encode({make_s('ascii')})
    {v_decomp} = {v_z}({v_b85}({v_data}))
    
    if (getattr({v_time}, {make_s('perf_counter')})() - {v_t_start}) > {timeout_limit}:
        {v_die_ldr}()
        
    {v_ex_mem} = getattr({v_b}, {make_s('MemoryError')})
    try:
        raise {v_ex_mem}({seed_calc_expr}, {prev_calc_expr})
    except {v_ex_mem} as {v_st}:
        {v_state}, {v_prev} = {v_st}.args[0], {v_st}.args[1]
    
    {v_bytearray} = getattr({v_b}, {make_s('bytearray')})
    {v_decrypted} = {v_bytearray}()
    for {v_byte} in {v_decomp}:
        {v_state} = ({v_state} * {pack_horner_int(1103515245, fn_pack_int)} + {pack_horner_int(12345, fn_pack_int)}) & {pack_horner_int(0xffffffff, fn_pack_int)}
        {v_k} = ({v_state} >> {pack_horner_int(16, fn_pack_int)}) & {pack_horner_int(0xff, fn_pack_int)}
        {v_val} = {v_byte} ^ {v_k} ^ {v_prev}
        {v_prev} = {v_byte}
        {v_decrypted}.append({v_val})
        
    {v_check_sha} = getattr({v_hash}({v_decrypted}), {make_s('hexdigest')})()
    if {v_check_sha} != {v_sha}:
        {v_die_ldr}()
        
    {v_src_text} = {v_decrypted}.decode({make_s('utf-8')})
    {v_code_obj} = {v_c}({v_src_text}, __file__, {make_s('exec')})
    
{mem_clean_impl}
    
    {v_g} = globals()
    for {v_attr} in [{', '.join(make_s(a) for a in ('__file__', '__name__', '__doc__', '__package__', '__spec__', '__loader__', '__annotations__', '__builtins__'))}]:
        if {v_attr} in globals():
            {v_g}[{v_attr}] = globals()[{v_attr}]
            
{hook_check_impl}

    {v_ex_stop} = getattr({v_b}, {make_s('StopIteration')})
    try:
        raise {v_ex_stop}({v_code_obj}, {v_g})
    except {v_ex_stop} as {v_xt}:
        {v_e}({v_xt}.args[0], {v_xt}.args[1])

{v_ex_sys} = getattr(__import__({make_s('builtins')}), {make_s('SystemError')})
try:
    raise {v_ex_sys}({v_loader})
except {v_ex_sys} as {v_run_init}:
    {v_run_init}.args[0]()
"""
    raw_template = stub.encode("utf-8")
    content_without_sig = raw_template.replace(PLACEHOLDER_SIG.encode("ascii"), b"")
    real_file_sig = hashlib.sha256(content_without_sig).hexdigest()
    final_stub = stub.replace(PLACEHOLDER_SIG, real_file_sig)
    return final_stub

def print_step(text: str, delay: float = 0.15):
    prefix = grad("  [⚡] ", "blue_to_cyan")
    styled_text = grad(text, "blue_to_cyan")
    sys.stdout.write(f"{prefix}{styled_text}")
    sys.stdout.flush()
    time.sleep(delay)
    done_prefix = f"  \033[92m[✔]\033[0m "
    sys.stdout.write(f"\r{done_prefix}{styled_text}\n")
    sys.stdout.flush()

def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def process_single_file(file_path: str, output_path: str = None, mode: int = 1) -> str:
    """Xử lý làm rối một file đơn lẻ.
    mode = 1: Thương Mại (Sạch Antivirus 100% + Khởi động siêu tốc <0.03s, ~40-60 KB)
    mode = 2: Ultra Paranoid (Full giáp C-API Hook Check, Anti-Frida, 750 KB)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            source_code = f.read()

    obfuscated_code = build_tdinh_apex_payload(source_code, mode=mode)
    
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        orig_filename = os.path.basename(file_path)
        name_without_ext, ext = os.path.splitext(orig_filename)
        output_path = os.path.join(output_dir, f"{name_without_ext}_obf{ext if ext else '.py'}")
    else:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(obfuscated_code.encode("utf-8"))

    return output_path

def process_folder(folder_path: str, mode: int = 1):
    """Xử lý làm rối toàn bộ dự án / thư mục đệ quy."""
    folder_name = os.path.basename(os.path.normpath(folder_path))
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_project_dir = os.path.join(base_dir, "output", f"{folder_name}_obf")
    
    py_files = []
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', '.venv', 'venv', 'build', 'dist', '.idea', '.vscode')]
        for f in files:
            if f.endswith('.py'):
                full_src = os.path.join(root, f)
                rel = os.path.relpath(full_src, folder_path)
                full_dest = os.path.join(output_project_dir, rel)
                py_files.append((full_src, full_dest, rel))

    if not py_files:
        print(f"\n  {CLR_RED}✖ Không tìm thấy file .py nào trong thư mục này!{CLR_RESET}\n")
        return

    if mode == 3:
        mode_label = "NEO-GHOST CHAOS (Flood Tàng Hình Ngang + Trộn Hàm)"
    elif mode == 2:
        mode_label = "ULTRA PARANOID (750KB)"
    else:
        mode_label = "THƯƠNG MẠI (Sạch AV + Siêu Tốc)"
    print(f"\n{grad('╭───[', 'purple_to_blue')} {grad(f'BẮT ĐẦU LÀM RỐI DỰ ÁN ({len(py_files)} FILES .PY) - CHẾ ĐỘ: {mode_label}', 'blue_to_cyan')} {grad(']───', 'purple_to_blue')}")
    print(f"{grad('│', 'purple_to_blue')}  {CLR_CYAN}📁 Thư mục gốc:{CLR_RESET} {folder_path}")
    print(f"{grad('│', 'purple_to_blue')}  {CLR_GREEN}📂 Thư mục xuất:{CLR_RESET} {output_project_dir}\n")

    start_time = time.time()
    for idx, (src, dest, rel) in enumerate(py_files, 1):
        step_str = f"[{idx}/{len(py_files)}] Đang xử lý: {rel}..."
        sys.stdout.write(f"  {grad(step_str, 'blue_to_cyan')}")
        sys.stdout.flush()
        process_single_file(src, dest, mode=mode)
        size_kb = os.path.getsize(dest) / 1024
        sys.stdout.write(f"\r  \033[92m[✔]\033[0m {grad(f'[{idx}/{len(py_files)}] {rel}', 'cyan_to_green')} -> {CLR_YELLOW}{size_kb:.1f} KB{CLR_RESET}\n")

    total_time = round(time.time() - start_time, 2)
    border = grad("═" * 74, "purple_to_blue")
    print(f"\n  {border}")
    print(f"  {grad(f'  🎉 HOÀN THÀNH LÀM RỐI DỰ ÁN THÀNH CÔNG! ({total_time}s)', 'cyan_to_green')}")
    print(f"  {border}")
    print(f"  {CLR_WHITE}• Thư mục kết quả:{CLR_RESET} {CLR_GREEN}{output_project_dir}{CLR_RESET}")
    print(f"  {CLR_WHITE}• Tổng số file .py:{CLR_RESET}{CLR_YELLOW} {len(py_files)} files{CLR_RESET}")
    print(f"  {CLR_WHITE}• Chế độ áp dụng:{CLR_RESET}  {CLR_CYAN}{mode_label}{CLR_RESET}")
    print(f"  {CLR_WHITE}• Chữ ký bản quyền:{CLR_RESET}{CLR_MAGENTA} tdinh | best obfuscator | ⋆౨ৎ˚⟡˖ ࣪tdinh⋆౨ৎ˚⟡˖ ࣪☠☠☠{CLR_RESET}")
    print(f"  {border}\n")

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print_banner()
        
        # Bước 1: Nhập file hoặc thư mục
        print(f"\n{grad('╭───[', 'purple_to_blue')} {grad('BƯỚC 1: CHỌN FILE .PY HOẶC THƯ MỤC DỰ ÁN CẦN LÀM RỐI', 'blue_to_cyan')} {grad(']──────────────────────────────', 'purple_to_blue')}")
        print(f"{grad('│', 'purple_to_blue')}  {grad('👉 KÉO THẢ 1 file .py LẺ HOẶC cả 1 thư mục dự án vào đây rồi nhấn Enter.', 'blue_to_cyan')}")
        print(f"{grad('│', 'purple_to_blue')}  \033[90m(Gõ 'q' hoặc 'exit' nếu muốn thoát)\033[0m")
        raw_path = input(f"{grad('╰─▶', 'purple_to_blue')} \033[92mBạn muốn obf file hoặc thư mục nào?: \033[0m")
        
        cleaned = clean_input_path(raw_path)
        if cleaned.lower() in ["q", "exit", "quit", "thoat"]:
            print(f"\n  {CLR_YELLOW}[!] Tạm biệt bạn! Hẹn gặp lại.{CLR_RESET}\n")
            break
            
        if not cleaned:
            continue
            
        if not os.path.exists(cleaned):
            print(f"\n  {CLR_RED}✖ Lỗi: Không tìm thấy đường dẫn này trên máy tính!{CLR_RESET}\n")
            input(f"  {CLR_DIM}Nhấn Enter để thử lại...{CLR_RESET}")
            continue

        # Bước 2: Chọn Chế độ bảo vệ
        print(f"\n{grad('╭───[', 'purple_to_blue')} {grad('BƯỚC 2: CHỌN CHẾ ĐỘ BẢO VỆ (SECURITY PROFILE)', 'blue_to_cyan')} {grad(']────────────────────────────────', 'purple_to_blue')}")
        print(f"{grad('│', 'purple_to_blue')}  \033[92m[1] THƯƠNG MẠI (Stealth / Fast & Clean) - \033[93m[MẶC ĐỊNH / KHUYÊN DÙNG]:\033[0m")
        print(f"{grad('│', 'purple_to_blue')}      ✔ \033[92m0% Báo đỏ Antivirus / Windows Defender\033[0m {grad('(Loại bỏ các API can thiệp nhạy cảm).', 'blue_to_cyan')}")
        print(f"{grad('│', 'purple_to_blue')}      ✔ \033[96mKhởi động SIÊU TỐC (< 0.03s - tức thì)\033[0m, {grad('file gọn nhẹ (~40-60 KB).', 'blue_to_cyan')}")
        print(f"{grad('│', 'purple_to_blue')}      ✔ {grad('Bảo mật: AST Pre-Obf (0% chuỗi thô), Khóa SHA-256 toàn file, Chữ ký tdinh.', 'blue_to_cyan')}")
        print(f"{grad('│', 'purple_to_blue')}")
        print(f"{grad('│', 'purple_to_blue')}  \033[95m[2] ULTRA PARANOID (Full giáp tối thượng - Dành cho Bot kín / Tool VIP):\033[0m")
        print(f"{grad('│', 'purple_to_blue')}      ✔ {grad('Tích hợp C-API Hook Check (Anti-Frida), Remote Debugger Check, Memory Crash.', 'blue_to_cyan')}")
        print(f"{grad('│', 'purple_to_blue')}      ✔ {grad('Ma trận 750 KB Decoy rác + Bẫy decompiler sâu.', 'blue_to_cyan')}")
        print(f"{grad('│', 'purple_to_blue')}")
        print(f"{grad('│', 'purple_to_blue')}  \033[93m[3] NEO-GHOST CHAOS (Flood Tàng Hình Ngang Cực Sâu + Trộn Hàm Hỗn Loạn):\033[0m")
        print(f"{grad('│', 'purple_to_blue')}      ✔ {grad('Flood 500+ KB khoảng trắng đẩy code tít sang phải (màn hình trái trống trơn).', 'blue_to_cyan')}")
        print(f"{grad('│', 'purple_to_blue')}      ✔ {grad('Trộn lẫn hàm: Xóa sổ loader ở đáy, phân tán toàn bộ logic vào giữa biển Emoji & Decoy.', 'blue_to_cyan')}")
        print(f"{grad('│', 'purple_to_blue')}      ✔ {grad('Động cơ Neo-Matrix: 4 tầng nén (bz2+lzma+zlib+b85), bom đa diện PyCDC, sys.monitoring.', 'blue_to_cyan')}")
        mode_choice = input(f"{grad('╰─▶', 'purple_to_blue')} \033[96mChọn chế độ [1, 2 hoặc 3] (Nhấn Enter = Mặc định 1): \033[0m").strip()
        if mode_choice == "3":
            mode = 3
            mode_name = "NEO-GHOST CHAOS (Flood Tàng Hình Ngang + Trộn Hàm)"
        elif mode_choice == "2":
            mode = 2
            mode_name = "ULTRA PARANOID (Giáp Nặng 750KB)"
        else:
            mode = 1
            mode_name = "THƯƠNG MẠI (Sạch AV + Siêu Tốc 45KB)"
        print(f"  \033[92m[✔]\033[0m {grad('Đã kích hoạt chế độ:', 'cyan_to_green')} {CLR_YELLOW}{mode_name}{CLR_RESET}\n")

        # NẾU LÀ THƯ MỤC DỰ ÁN
        if os.path.isdir(cleaned):
            process_folder(cleaned, mode=mode)
            next_action = input(f"  {grad('[?]', 'purple_to_blue')} \033[96mBạn có muốn obf thêm file/thư mục nào khác không? (y/n) [Mặc định: y]: \033[0m").strip().lower()
            if next_action in ["n", "no"]:
                print(f"\n  \033[92m[✓]\033[0m {grad('Đã hoàn thành mọi tác vụ. Cảm ơn bạn đã sử dụng!', 'cyan_to_green')}\n")
                break
            continue

        # NẾU LÀ 1 FILE LẺ
        original_size = os.path.getsize(cleaned)
        print(f"  \033[92m[✔]\033[0m {grad('Đã nhận diện file:', 'cyan_to_green')} {CLR_WHITE}{os.path.basename(cleaned)}{CLR_RESET} ({format_size(original_size)})")

        print(f"\n{grad('╭───[', 'purple_to_blue')} {grad('ĐANG TIẾN HÀNH BẢO VỆ MÃ NGUỒN (TDINH SPECIAL EDITION)', 'blue_to_cyan')} {grad(']──────────────────────', 'purple_to_blue')}")
        print_step("Tiền xử lý AST: Biến 100% chuỗi thành Lambda XOR, làm rối số nguyên, tiêm bẫy PyCDC...", 0.15)
        print_step("Khóa chặt chữ ký bản quyền: __owner__ = tdinh | __cmt__ = best obfuscator...", 0.15)
        print_step("Khởi tạo Bảng Ma Trận Ký Tự 2 Chiều & Mạng lưới hàm liên hoàn đa ngữ...", 0.15)
        print_step("Bơm ngập tràn Emojis & Ký tự đặc biệt (ᶻ 𝗓 𐰁, 𓃱, ִ 𖤐, 𖠋, ⋆౨ৎ˚⟡˖ ࣪tdinh⋆౨ৎ˚⟡˖ ࣪☠☠☠)...", 0.15)
        print_step("Mã hóa Rolling Stream Cipher đa hình khóa chặt theo chữ ký tdinh...", 0.15)
        if mode == 3:
            print_step("Bơm Flood Tàng Hình Ngang (Ghost Padding 500+ KB) đẩy mã sang góc phải...", 0.15)
            print_step("Xóa sổ khối Loader ở đáy, trà trộn & phân tán toàn bộ hàm vào biển Emoji & Decoy...", 0.15)
            print_step("Cài đặt Neo-Matrix Multi-Bomb Traps (1/0, IndexError, KeyError, TypeError, Open Bomb)...", 0.15)
            print_step("Nén siêu cấp 4 tầng: Zlib -> LZMA -> BZ2 -> Base85...", 0.15)
            print_step("Kích hoạt bảo vệ chuyên sâu: Quét sys.monitoring, Hook checks, Proxy MITM...", 0.15)
        elif mode == 2:
            print_step("Cài đặt C-API Hook Detection (Anti-Frida), Remote Debugger Check, Memory Shredding...", 0.2)
        else:
            print_step("Tối ưu hóa mã nguồn sạch, vượt kiểm duyệt Heuristics Antivirus & tăng tốc độ...", 0.15)
        print_step("Khóa cứng toàn vẹn mã băm SHA-256 toàn bộ file (Tamper-Lock)...", 0.15)
        
        try:
            output_file_path = process_single_file(cleaned, mode=mode)
        except Exception as err:
            print(f"\n  {CLR_RED}✖ Lỗi mã hóa: {err}{CLR_RESET}\n")
            input(f"  {CLR_DIM}Nhấn Enter để thử lại...{CLR_RESET}")
            continue

        obf_size = os.path.getsize(output_file_path)

        # Báo cáo kết quả
        border = grad("═" * 74, "purple_to_blue")
        print(f"\n  {border}")
        print(f"  {grad('  🎉 LÀM RỐI THÀNH CÔNG! TDINH SPECIAL EDITION ĐÃ SẴN SÀNG', 'cyan_to_green')}")
        print(f"  {border}")
        print(f"  {CLR_WHITE}• File gốc:{CLR_RESET}         {cleaned}")
        print(f"  {CLR_WHITE}• File kết quả:{CLR_RESET}     {CLR_GREEN}{output_file_path}{CLR_RESET}")
        print(f"  {CLR_WHITE}• Dung lượng file:{CLR_RESET}  {CLR_MAGENTA}{format_size(obf_size)}{CLR_RESET}")
        print(f"  {CLR_WHITE}• Chế độ áp dụng:{CLR_RESET}  {CLR_CYAN}{mode_name}{CLR_RESET}")
        print(f"  {CLR_WHITE}• Chữ ký khóa tử:{CLR_RESET}  {CLR_YELLOW}__owner__ = 'tdinh' | __cmt__ = 'best obfuscator'{CLR_RESET}")
        print(f"  {CLR_WHITE}• Trạng thái:{CLR_RESET}       {CLR_GREEN}Chạy độc lập 100% | Tự hủy ngay nếu bị xóa chữ ký/sửa file{CLR_RESET}")
        print(f"  {border}\n")

        # Hỏi chạy thử
        test_run = input(f"  {grad('[?]', 'purple_to_blue')} \033[93mBạn có muốn CHẠY THỬ file này ngay không? (y/n) [Mặc định: y]: \033[0m").strip().lower()
        if test_run in ["", "y", "yes"]:
            sep = grad("─" * 74, "blue_to_cyan")
            print(f"\n  {sep}")
            print(f"  {grad('▶ KẾT QUẢ CHẠY FILE ĐÃ LÀM RỐI:', 'blue_to_cyan')}")
            print(f"  {sep}\n")
            try:
                subprocess.run([sys.executable, output_file_path], check=False)
            except Exception as run_err:
                print(f"  {CLR_RED}Lỗi khi thực thi: {run_err}{CLR_RESET}")
            print(f"\n  {sep}\n")

        # Hỏi tiếp tục
        next_action = input(f"  {grad('[?]', 'purple_to_blue')} \033[96mBạn có muốn obf thêm file/thư mục nào khác không? (y/n) [Mặc định: y]: \033[0m").strip().lower()
        if next_action in ["n", "no"]:
            print(f"\n  \033[92m[✓]\033[0m {grad('Đã hoàn thành mọi tác vụ. Cảm ơn bạn đã sử dụng!', 'cyan_to_green')}\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{CLR_YELLOW}[!] Đã thoát chương trình. Tạm biệt!{CLR_RESET}\n")
        sys.exit(0)
