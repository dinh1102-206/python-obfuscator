"""Anti-analysis and runtime integrity verification."""

import textwrap
import random
import secrets


def _random_ident(prefix: str = "_0x") -> str:
    chars = "abcdef0123456789"
    return prefix + "".join(secrets.choice(chars) for _ in range(8))


def generate_anti_analysis_code() -> str:
    """Generates polymorphic anti-debugging, anti-tracing, and anti-hooking guard code."""
    guard_fn = _random_ident("_guard_")
    sys_alias = _random_ident("_s_")
    builtins_alias = _random_ident("_b_")

    code = f"""
def {guard_fn}():
    import sys as {sys_alias}
    import builtins as {builtins_alias}
    
    # Check for active debugger / tracer
    _tr = getattr({sys_alias}, 'gettrace', lambda: None)()
    if _tr is not None and getattr(_tr, '__name__', '') != '_silent_trace':
        {sys_alias}.exit(1)
        
    # Check if critical builtins have been monkey-patched / hooked
    _crit = ['exec', 'eval', 'compile', 'print']
    for _name in _crit:
        if hasattr({builtins_alias}, _name):
            _fn = getattr({builtins_alias}, _name)
            # Built-in functions in CPython are BuiltinFunctionType and do not have __code__
            if hasattr(_fn, '__code__') or type(_fn).__name__ != 'builtin_function_or_method':
                {sys_alias}.exit(1)
                
    # Neutralize tracing
    try:
        def _silent_trace(*_args):
            return None
        {sys_alias}.settrace(_silent_trace)
    except Exception:
        pass

{guard_fn}()
"""
    return textwrap.dedent(code).strip()
