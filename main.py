#!/usr/bin/env python3
"""CLI Entry point for Python Obfuscator."""

import argparse
import sys
import time
from pathlib import Path

# Ensure utf-8 encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.core import Obfuscator, ObfuscationConfig


def parse_args():
    parser = argparse.ArgumentParser(
        description="Advanced Multi-layer Python Code Obfuscator & Protector",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to source Python file (.py) to obfuscate",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Path to save obfuscated output file (default: <input>_obf.py)",
    )
    parser.add_argument(
        "-l", "--level",
        choices=["low", "medium", "high", "extreme"],
        default="high",
        help="Obfuscation preset level",
    )
    parser.add_argument(
        "--no-strings",
        action="store_true",
        help="Disable string encryption",
    )
    parser.add_argument(
        "--no-numbers",
        action="store_true",
        help="Disable number obfuscation",
    )
    parser.add_argument(
        "--no-mangling",
        action="store_true",
        help="Disable variable/function name mangling",
    )
    parser.add_argument(
        "--no-flatten",
        action="store_true",
        help="Disable control flow flattening",
    )
    parser.add_argument(
        "--no-anti-debug",
        action="store_true",
        help="Disable anti-debugging and anti-analysis guards",
    )
    parser.add_argument(
        "--no-pack",
        action="store_true",
        help="Disable bytecode serialization and polymorphic packaging",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"[!] Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_name(f"{input_path.stem}_obf.py")

    # Select preset
    preset_map = {
        "low": ObfuscationConfig.preset_low,
        "medium": ObfuscationConfig.preset_medium,
        "high": ObfuscationConfig.preset_high,
        "extreme": ObfuscationConfig.preset_extreme,
    }
    config = preset_map[args.level]()

    # Apply manual flags overrides
    if args.no_strings:
        config.obfuscate_strings = False
    if args.no_numbers:
        config.obfuscate_numbers = False
    if args.no_mangling:
        config.mangle_names = False
    if args.no_flatten:
        config.flatten_control_flow = False
    if args.no_anti_debug:
        config.enable_anti_analysis = False
    if args.no_pack:
        config.pack_bytecode = False

    print(f"[*] Obfuscating '{input_path.name}' -> '{output_path.name}' (Level: {args.level.upper()})...")
    start_time = time.time()

    obfuscator = Obfuscator(config)
    try:
        obfuscator.obfuscate_file(str(input_path), str(output_path))
    except Exception as e:
        print(f"[!] Obfuscation failed: {e}", file=sys.stderr)
        sys.exit(1)

    elapsed = (time.time() - start_time) * 1000
    print(f"[+] Done in {elapsed:.2f}ms!")
    print(f"[+] Output generated at: {output_path.resolve()}")
    print(f"[+] You can run it simply with: python \"{output_path}\"")


if __name__ == "__main__":
    main()
