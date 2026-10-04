"""Core pipeline for Python Obfuscator."""

import ast
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from .string_encryptor import StringEncryptor
from .ast_transformer import ASTObfuscator
from .packer import pack_code_to_standalone_script


@dataclass
class ObfuscationConfig:
    """Configuration options for obfuscation."""
    obfuscate_strings: bool = True
    obfuscate_numbers: bool = True
    mangle_names: bool = True
    flatten_control_flow: bool = True
    inject_opaque_predicates: bool = True
    enable_anti_analysis: bool = True
    pack_bytecode: bool = True
    rounds: int = 1

    @classmethod
    def preset_low(cls) -> "ObfuscationConfig":
        return cls(
            obfuscate_strings=True,
            obfuscate_numbers=False,
            mangle_names=False,
            flatten_control_flow=False,
            inject_opaque_predicates=False,
            enable_anti_analysis=False,
            pack_bytecode=True,
            rounds=1,
        )

    @classmethod
    def preset_medium(cls) -> "ObfuscationConfig":
        return cls(
            obfuscate_strings=True,
            obfuscate_numbers=True,
            mangle_names=True,
            flatten_control_flow=False,
            inject_opaque_predicates=True,
            enable_anti_analysis=True,
            pack_bytecode=True,
            rounds=1,
        )

    @classmethod
    def preset_high(cls) -> "ObfuscationConfig":
        return cls(
            obfuscate_strings=True,
            obfuscate_numbers=True,
            mangle_names=True,
            flatten_control_flow=True,
            inject_opaque_predicates=True,
            enable_anti_analysis=True,
            pack_bytecode=True,
            rounds=1,
        )

    @classmethod
    def preset_extreme(cls) -> "ObfuscationConfig":
        return cls(
            obfuscate_strings=True,
            obfuscate_numbers=True,
            mangle_names=True,
            flatten_control_flow=True,
            inject_opaque_predicates=True,
            enable_anti_analysis=True,
            pack_bytecode=True,
            rounds=2,
        )


class Obfuscator:
    """High-level orchestrator for transforming and packing Python code."""

    def __init__(self, config: Optional[ObfuscationConfig] = None):
        self.config = config or ObfuscationConfig()

    def obfuscate_code(self, source_code: str) -> str:
        current_code = source_code

        for _ in range(max(1, self.config.rounds)):
            # 1. Parse AST
            tree = ast.parse(current_code)
            string_encryptor = StringEncryptor()

            # 2. Transform AST
            transformer = ASTObfuscator(
                string_encryptor=string_encryptor,
                obfuscate_numbers=self.config.obfuscate_numbers,
                obfuscate_strings=self.config.obfuscate_strings,
                mangle_names=self.config.mangle_names,
                flatten_control_flow=self.config.flatten_control_flow,
                inject_opaque_predicates=self.config.inject_opaque_predicates,
            )
            transformer.prepare_name_mappings(tree)
            transformed_tree = transformer.visit(tree)
            ast.fix_missing_locations(transformed_tree)

            # Insert string decryptor if strings were encrypted
            if self.config.obfuscate_strings and string_encryptor.cache:
                decryptor_node = string_encryptor.generate_decryptor_ast()
                transformed_tree.body.insert(0, decryptor_node)
                ast.fix_missing_locations(transformed_tree)

            # Unparse back to code
            current_code = ast.unparse(transformed_tree)

        # 3. Polymorphic bytecode packer
        if self.config.pack_bytecode:
            current_code = pack_code_to_standalone_script(
                current_code,
                enable_anti_analysis=self.config.enable_anti_analysis,
            )

        return current_code

    def obfuscate_file(self, input_file: str, output_file: str) -> None:
        in_path = Path(input_file)
        out_path = Path(output_file)

        if not in_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        source_code = in_path.read_text(encoding="utf-8")
        obfuscated_code = self.obfuscate_code(source_code)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(obfuscated_code, encoding="utf-8")
