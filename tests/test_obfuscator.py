import subprocess
import sys
import tempfile
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core import Obfuscator, ObfuscationConfig


SAMPLE_SCRIPT = """
class Calculator:
    def __init__(self, factor=2):
        self.factor = factor
        self._cache = {}

    def compute(self, items):
        total = 0
        for x in items:
            val = (x * self.factor) + 5
            total += val
        return total

def run_tests():
    calc = Calculator(3)
    nums = [1, 2, 3, 4]
    res = calc.compute(nums)
    print("Computed total:", res)
    d = {"status": "success", "code": 200}
    print("Dict status:", d["status"])
    try:
        raise ValueError("custom error")
    except ValueError as e:
        print("Caught exception:", str(e))

run_tests()
"""


def test_obfuscator_execution():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        input_file = tmp_path / "sample.py"
        input_file.write_text(SAMPLE_SCRIPT.strip(), encoding="utf-8")

        # Get original output
        orig_run = subprocess.run(
            [sys.executable, str(input_file)],
            capture_output=True,
            text=True,
            check=True,
        )
        orig_stdout = orig_run.stdout

        for level, config in [
            ("low", ObfuscationConfig.preset_low()),
            ("medium", ObfuscationConfig.preset_medium()),
            ("high", ObfuscationConfig.preset_high()),
            ("extreme", ObfuscationConfig.preset_extreme()),
        ]:
            out_file = tmp_path / f"sample_{level}.py"
            obf = Obfuscator(config)
            obf.obfuscate_file(str(input_file), str(out_file))

            # Run obfuscated file
            obf_run = subprocess.run(
                [sys.executable, str(out_file)],
                capture_output=True,
                text=True,
            )
            assert obf_run.returncode == 0, f"Failed at level {level}: {obf_run.stderr}"
            assert obf_run.stdout == orig_stdout, (
                f"Output mismatch at level {level}!\nExpected:\n{orig_stdout}\nGot:\n{obf_run.stdout}"
            )
            print(f"[PASS] Level {level} executed perfectly and matched original output!")


if __name__ == "__main__":
    test_obfuscator_execution()
    print("All tests passed successfully!")
