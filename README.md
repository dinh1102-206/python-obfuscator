# 🐾 WHISCAT OBFUSCATOR v9.0 🐾

Một công cụ làm mờ (Obfuscator) và bảo vệ mã nguồn Python toàn diện, hội tụ các kỹ thuật hàng đầu từ Shadow, Tsunami, Pymeomeo với giao diện **Gradient Menu** tương tác đẹp mắt.

---

## 🚀 Tính năng chính (Key Features)

1. **🎨 Interactive Gradient Menu**:
   - Giao diện console tương tác mượt mà với dải màu chuyển động ANSI TrueColor/pystyle.
   - Hỗ trợ cả 2 cách dùng: Chạy tương tác (Interactive menu) hoặc dòng lệnh (CLI).

2. **⚡ AST Transformation & Decompiler Bomb**:
   - **Anti-PyCDC Decompiler Bomb**: Chèn bẫy làm sập trực tiếp engine dịch ngược C++ của `pycdc` (`1/int(0)`).
   - **Dynamic String Encryption**: Mã hóa chuỗi ký tự bằng thuật toán mã hóa động đa khóa (Rolling XOR + Salt + Shifting), tự động sinh decryptor tại runtime. Hỗ trợ chuẩn xác cả f-strings (`JoinedStr`).
   - **Number & Constant Splitting**: Tách số và hằng số thành các biểu thức bitwise và số học phức tạp.
   - **Control Flow Flattening (CFF)**: Chuyển các khối lệnh tuần tự thành các máy trạng thái (State Machine Dispatcher) với thứ tự nhánh bị xáo trộn ngẫu nhiên.
   - **Variable Name Mangling**: Đổi tên biến sang mã Hex hoặc chữ tượng hình CJK Unicode (`0x4E00` - `0x9FA5`), bảo toàn 100% logic của built-in, method và import.

3. **🔒 Memory & Debugger Guard (CPython Level)**:
   - **CPython Memory Hook Detection**: Kiểm tra trực tiếp trong RAM thông qua `ctypes.pythonapi` 8 bytes prologue của hàm `PyEval_EvalCode` để phát hiện breakpoint phần cứng/phần mềm (`0xCC` INT 3).
   - **Builtin Integrity Guard**: Kiểm tra xem các hàm nhạy cảm `exec`, `eval`, `compile` có bị hook hoặc monkey-patch không.
   - **Anti-Tracing & Anti-Debugger**: Phát hiện `gettrace`, chặn `settrace`, vô hiệu hóa debugger Windows API (`IsDebuggerPresent`, `CheckRemoteDebuggerPresent`).
   - Tự động dọn dẹp frame và loader trong bộ nhớ ngay sau khi thực thi.

4. **🎨 TDIH ASCII Art Mode (Độc quyền)**:
   - Toàn bộ file output được tạo hình bằng **ASCII Art Banner TDIH**.
   - Mọi biến, hàm, và toàn bộ dữ liệu payload được mã hóa hoàn toàn bằng 4 chữ cái `t`, `d`, `i`, `h`.
   - Vừa bảo mật cao vừa mang dấu ấn thương hiệu `tdih`.

5. **🚀 4-Tier Polymorphic Packing**:
   - Nén bytecode qua 4 tầng: `BZ2` + `LZMA` + `ZLIB` + `Base85`.
   - Mã hóa luồng Rolling Stream Cipher với seed, key và salt ngẫu nhiên mỗi lần obf.
   - Đóng gói trong loader tự giải mã đa hình (Polymorphic Self-Executing Loader).

6. **📂 Batch Folder Obfuscation**:
   - Hỗ trợ kéo thả hoặc nhập đường dẫn nguyên cả thư mục dự án -> Tự động xử lý và bảo vệ toàn bộ cây thư mục.

---

## 💻 Cách sử dụng (Usage)

### 1. Chạy Menu tương tác (Khuyên dùng)

Chỉ cần gõ:
```bash
python main.py
```
Menu tương tác với dải màu Gradient sẽ xuất hiện:
```text
    [1] ⚡ Commercial Clean Shield (Nhanh, Sạch Antivirus, Khởi động tức thì)
    [2] 🥷 Ultra Paranoid Shield (Chống Debugger, RAM Hook, 4-Tier Packing)
    [3] 🐾 WHISCAT NEO-GHOST CHAOS (TỐI THƯỢNG: 40k+ Spaces Flood, Matrix Chunks, SHA-256 Lock)
    [4] 🎨 TDIH ASCII ART OBF (Full Code Chữ TDIH / TDINH + ASCII Art)
    [5] 📂 Batch Obfuscate Project (Bảo vệ toàn bộ Folder / Dự án)
    [6] 🧪 Self-Diagnostic Test (Chạy kiểm tra tự động)
    [0] 🚪 Thoát
```

### 2. Sử dụng qua dòng lệnh (CLI)

```bash
# Obfuscate theo chế độ TDIH ASCII Art
python main.py -i input.py -o output.py -m 4

# Obfuscate theo chế độ Neo-Ghost Chaos (Tối thượng)
python main.py -i input.py -o output.py -m 3

# Obfuscate với biến đổi tên sang ký tự CJK Unicode
python main.py -i input.py -o output.py --cjk

# Obfuscate nguyên một folder dự án
python main.py -i my_project/ -o my_project_whiscat/
```

### 3. Chạy file đã bảo vệ

File kết quả chạy trực tiếp và hoàn toàn độc lập (Zero-Dependency):
```bash
python output.py
```
