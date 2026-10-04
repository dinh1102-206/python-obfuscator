"""AST Transformer for code obfuscation:
- Number obfuscation (bitwise & arithmetic splitting)
- String encryption via StringEncryptor
- Name mangling for variables and private functions
- Dead code & opaque predicate injection
- Control flow flattening
"""

import ast
import random
import secrets
from typing import Dict, Set, Optional, List
from .string_encryptor import StringEncryptor, _random_ident

PYTHON_BUILTINS = set(dir(__builtins__)) | {
    "__name__", "__doc__", "__package__", "__loader__", "__spec__",
    "__annotations__", "__builtins__", "__file__", "__cached__",
    "self", "cls", "args", "kwargs"
}


def _obfuscate_int(val: int) -> ast.AST:
    """Transforms an integer into an equivalent bitwise/arithmetic expression."""
    if abs(val) > 1000000:
        return ast.Constant(value=val)
    
    choice = random.randint(0, 2)
    if choice == 0:
        # val == (val ^ r) ^ r
        r = random.randint(10, 500)
        masked = val ^ r
        return ast.BinOp(
            left=ast.BinOp(
                left=ast.Constant(value=masked),
                op=ast.BitXor(),
                right=ast.Constant(value=r),
            ),
            op=ast.BitXor(),
            right=ast.Constant(value=r ^ r),  # equals (val ^ r) ^ 0 => wait, (masked ^ r) is val
        )
    elif choice == 1:
        # val == (val + delta) - delta
        delta = random.randint(100, 1000)
        return ast.BinOp(
            left=ast.Constant(value=val + delta),
            op=ast.Sub(),
            right=ast.Constant(value=delta),
        )
    else:
        # val == (val * 1)
        r = random.randint(1, 255)
        masked = val ^ r
        return ast.BinOp(
            left=ast.Constant(value=masked),
            op=ast.BitXor(),
            right=ast.Constant(value=r),
        )


class NameCollector(ast.NodeVisitor):
    """Collects names defined locally that are safe to rename."""

    def __init__(self):
        self.local_vars: Set[str] = set()
        self.reserved_names: Set[str] = set(PYTHON_BUILTINS)
        self.in_class: bool = False

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            name = alias.asname or alias.name.split(".")[0]
            self.reserved_names.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            name = alias.asname or alias.name
            self.reserved_names.add(name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.reserved_names.add(node.name)
        # Record all method and attribute names in class body
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.reserved_names.add(item.name)
        old_in_class = self.in_class
        self.in_class = True
        self.generic_visit(node)
        self.in_class = old_in_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.in_class:
            self.reserved_names.add(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if self.in_class:
            self.reserved_names.add(node.name)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Store):
            if not self.in_class and not node.id.startswith("__"):
                self.local_vars.add(node.id)
        self.generic_visit(node)


class ASTObfuscator(ast.NodeTransformer):
    """AST Transformer executing multi-level transformations."""

    def __init__(
        self,
        string_encryptor: Optional[StringEncryptor] = None,
        obfuscate_numbers: bool = True,
        obfuscate_strings: bool = True,
        mangle_names: bool = True,
        flatten_control_flow: bool = True,
        inject_opaque_predicates: bool = True,
    ):
        super().__init__()
        self.string_encryptor = string_encryptor or StringEncryptor()
        self.obfuscate_numbers = obfuscate_numbers
        self.obfuscate_strings = obfuscate_strings
        self.mangle_names = mangle_names
        self.flatten_control_flow = flatten_control_flow
        self.inject_opaque_predicates = inject_opaque_predicates
        self.name_map: Dict[str, str] = {}
        self.reserved_names: Set[str] = set(PYTHON_BUILTINS)

    def prepare_name_mappings(self, root: ast.AST):
        if not self.mangle_names:
            return
        collector = NameCollector()
        collector.visit(root)
        self.reserved_names.update(collector.reserved_names)
        for name in collector.local_vars:
            if name not in self.reserved_names:
                self.name_map[name] = _random_ident("_var_")

    def visit_JoinedStr(self, node: ast.JoinedStr) -> ast.AST:
        new_values = []
        for val in node.values:
            if isinstance(val, ast.Constant) and isinstance(val.value, str):
                if len(val.value) > 0 and self.obfuscate_strings:
                    encrypted = self.string_encryptor.encrypt_string(val.value)
                    call_node = self.string_encryptor.create_call_ast(encrypted)
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
        # String constant obfuscation
        if self.obfuscate_strings and isinstance(node.value, str):
            if len(node.value) > 0 and node.value not in {"__main__", "utf-8"}:
                encrypted = self.string_encryptor.encrypt_string(node.value)
                return self.string_encryptor.create_call_ast(encrypted)

        # Integer constant obfuscation
        if self.obfuscate_numbers and isinstance(node.value, int) and not isinstance(node.value, bool):
            return _obfuscate_int(node.value)

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

        # Strip docstring
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        # Control flow flattening for function body
        if self.flatten_control_flow and len(node.body) > 2:
            node.body = self._flatten_statements(node.body)

        self.generic_visit(node)
        return node

    def _create_opaque_predicate(self) -> ast.If:
        """Creates an opaque predicate: condition is always false, containing dead code."""
        # Condition: (0x55 & 0xAA) != 0 -> always False (0 != 0)
        condition = ast.Compare(
            left=ast.BinOp(
                left=ast.Constant(value=0x55),
                op=ast.BitAnd(),
                right=ast.Constant(value=0xAA),
            ),
            ops=[ast.NotEq()],
            comparators=[ast.Constant(value=0)],
        )
        # Dead code
        dead_stmt = ast.Assign(
            targets=[ast.Name(id=_random_ident("_dead_"), ctx=ast.Store())],
            value=ast.Constant(value=random.randint(1000, 9999)),
        )
        return ast.If(test=condition, body=[dead_stmt], orelse=[])

    def _flatten_statements(self, stmts: List[ast.stmt]) -> List[ast.stmt]:
        """Flattens a list of linear statements into an obfuscated state-machine dispatcher."""
        # If any statement contains return, yield, break, continue, function definitions, keep structure safe
        for stmt in stmts:
            if isinstance(stmt, (ast.Return, ast.Yield, ast.YieldFrom, ast.Break, ast.Continue, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                return stmts

        state_var = _random_ident("_st_")
        n = len(stmts)
        state_ids = list(range(1, n + 1))
        # Random mapping of order
        shuffled_indices = list(range(n))
        random.shuffle(shuffled_indices)

        # Map each block step to a state id
        state_mapping = {i: state_ids[i] for i in range(n)}
        
        # Build if-elif branches for each state
        branches: List[ast.If] = []
        
        # We need a while loop:
        # state = state_mapping[0]
        # while state != 0:
        #    if state == state_mapping[0]:
        #        stmt_0
        #        state = state_mapping[1]
        #    elif state == state_mapping[1]:
        #    ...
        
        # Create dispatcher cases
        cases = []
        for i in range(n):
            current_state = state_mapping[i]
            next_state = state_mapping[i + 1] if i + 1 < n else 0
            
            body = [stmts[i]]
            # assign next state
            body.append(
                ast.Assign(
                    targets=[ast.Name(id=state_var, ctx=ast.Store())],
                    value=ast.Constant(value=next_state)
                )
            )
            cases.append((current_state, body))
        
        # Shuffle cases to break linear static flow
        random.shuffle(cases)
        
        # Assemble nested if-elif chain
        root_if = None
        current_if = None
        for state_val, body in cases:
            cond = ast.Compare(
                left=ast.Name(id=state_var, ctx=ast.Load()),
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

        # Init state
        init_state = ast.Assign(
            targets=[ast.Name(id=state_var, ctx=ast.Store())],
            value=ast.Constant(value=state_mapping[0])
        )

        # While loop
        while_loop = ast.While(
            test=ast.Compare(
                left=ast.Name(id=state_var, ctx=ast.Load()),
                ops=[ast.NotEq()],
                comparators=[ast.Constant(value=0)]
            ),
            body=[root_if],
            orelse=[]
        )

        result: List[ast.stmt] = [init_state, while_loop]
        if self.inject_opaque_predicates:
            result.insert(0, self._create_opaque_predicate())
        return result
