# Python Obfuscator & Protector

Một công cụ làm mờ (Obfuscator) và bảo vệ mã nguồn Python đa tầng mạnh mẽ, giúp chống dịch ngược (decompile), chống dịch ngược tĩnh và động, chống hooking và dump bộ nhớ cơ bản.

---

## 🚀 Tính năng nổi bật (Features)

1. **AST Transformation (Biến đổi cây cú pháp)**:
   - **Dynamic String Encryption**: Mã hóa toàn bộ chuỗi ký tự bằng thuật toán mã hóa động đa khóa (Rolling XOR + Salt + Shifting). Tạo decryptor ngẫu nhiên tại runtime.
   - **Number & Constant Obfuscation**: Tách các giá trị số và hằng số thành các biểu thức số học và bitwise phức tạp (`^`, `&`, `|`, `+`, `-`).
   - **Name Mangling**: Đổi tên các biến nội bộ thành chuỗi hex/nhận dạng ngẫu nhiên (`_var_0x...`), đồng thời giữ an toàn tuyệt đối cho methods, imports và builtins.
   - **Control Flow Flattening (Làm phẳng luồng điều khiển)**: Biến đổi các khối lệnh tuần tự thành các máy trạng thái (State Machine Dispatcher) với thứ tự nhánh bị xáo trộn ngẫu nhiên.
   - **Opaque Predicates & Dead Code**: Chèn các khối rẽ nhánh giả với điều kiện luôn sai nhưng tĩnh học không thể đoán được.

2. **Polymorphic Bytecode Packing**:
   - Biên dịch AST sang mã bytecode (`marshal`).
   - Nén luồng dữ liệu ở mức tối đa (`zlib level 9`).
   - Mã hóa bytecode bằng khóa ngẫu nhiên sinh mới ở mỗi lần chạy.
   - Đóng gói trong một Loader tự giải mã đa hình (Polymorphic Self-Executing Loader).

3. **Anti-Analysis & Anti-Hooking Guard**:
   - Phát hiện và vô hiệu hóa Tracing (`sys.settrace`, `sys.gettrace`).
   - Phát hiện Monkey-Patching / Hooking trên các hàm built-in nhạy cảm (`exec`, `eval`, `compile`, `print`).
   - Tự động dọn dẹp frame và loader trong bộ nhớ ngay sau khi thực thi (`frame cleanup`).

---

## 🛠️ Hướng dẫn sử dụng (Usage)

### 1. Sử dụng qua dòng lệnh (CLI)

Cực kỳ đơn giản, chỉ cần chỉ định file `.py` cần làm mờ:

```bash
# Obfuscate với mức độ mặc định (HIGH)
python main.py -i your_script.py -o your_script_obf.py

# Obfuscate với mức độ tối đa (EXTREME)
python main.py -i your_script.py -o your_script_obf.py -l extreme
```

#### Các mức độ (Presets):
* `low`: Mã hóa chuỗi + Đóng gói Bytecode đa hình.
* `medium`: Mã hóa chuỗi + Biến đổi số + Đổi tên biến + Anti-Analysis + Đóng gói Bytecode.
* `high` *(mặc định)*: Toàn bộ tính năng Medium + Control Flow Flattening (Làm phẳng luồng thực thi).
* `extreme`: Toàn bộ tính năng High + Nhiều vòng (multi-round) biến đổi AST.

#### Các cờ tùy chỉnh khác:
* `--no-strings`: Tắt mã hóa chuỗi.
* `--no-numbers`: Tắt làm mờ số học.
* `--no-mangling`: Tắt đổi tên biến.
* `--no-flatten`: Tắt làm phẳng luồng điều khiển.
* `--no-anti-debug`: Tắt bảo vệ chống debugger/tracing.
* `--no-pack`: Chỉ xuất mã nguồn AST đã làm mờ, không đóng gói bytecode.

---

### 2. Chạy file đã Obfuscate

Người dùng cuối chỉ cần chạy file kết quả bằng Python như bình thường:

```bash
python your_script_obf.py
```

Không yêu cầu cài thêm bất kỳ thư viện ngoài nào (100% Zero Dependency).

---

### 3. Sử dụng dưới dạng Python Library

```python
from src.core import Obfuscator, ObfuscationConfig

# Sử dụng cấu hình preset
config = ObfuscationConfig.preset_extreme()
obfuscator = Obfuscator(config)

# Làm mờ file
obfuscator.obfuscate_file("input.py", "output.py")

# Hoặc làm mờ trực tiếp chuỗi code
protected_code = obfuscator.obfuscate_code("print('Hello World')")
```

---

## 🧪 Kiểm thử (Testing)

Chạy bộ test tự động để xác minh tính toàn vẹn và độ chính xác của output qua tất cả các cấp độ:

```bash
python tests/test_obfuscator.py
```
