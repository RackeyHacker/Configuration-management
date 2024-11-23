import json
import os

def assembler(input_file, output_file, log_file):
    # Примерная заглушка для работы ассемблера
    with open(input_file, 'r') as f:
        instructions = f.readlines()

    binary_code = []
    log_data = []

    for line in instructions:
        parts = line.strip().split()
        if parts[0] == "load_const":
            reg = int(parts[1])
            value = int(parts[2])
            # Генерация бинарных данных для load_const
            binary_code.append(0x0A)  # opcode for load_const
            binary_code.extend(value.to_bytes(2, 'little'))  # 16-bit value (little-endian)
            binary_code.append(0x00)  # padding byte
            binary_code.append(0x00)
            log_data.append({
                "instruction": {
                    "A": reg,
                    "B": value,
                    "C": 0  # Нет конкретного C
                }
            })
        elif parts[0] == "read_mem":
            reg = int(parts[1])
            mem_addr = int(parts[2])
            size = int(parts[3])
            # Генерация бинарных данных для read_mem
            binary_code.append(0x36)  # opcode for read_mem
            binary_code.append(0x48)  # additional byte for read_mem (example)
            binary_code.append(mem_addr)
            binary_code.append(size)
            log_data.append({
                "instruction": {
                    "A": reg,
                    "B": mem_addr,
                    "C": size
                }
            })
        elif parts[0] == "write_mem":
            reg = int(parts[1])
            mem_addr = int(parts[2])
            size = int(parts[3])
            # Генерация бинарных данных для write_mem
            binary_code.append(0xA7)  # opcode for write_mem
            binary_code.append(mem_addr)
            log_data.append({
                "instruction": {
                    "A": reg,
                    "B": mem_addr,
                    "C": size
                }
            })

    # Запись бинарных данных в выходной файл
    with open(output_file, 'wb') as f:
        f.write(bytes(binary_code))

    # Запись логов в файл
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=4)

def interpreter(bin_file, result_file, memory_range):
    # Примерная заглушка для работы интерпретатора
    with open(bin_file, 'rb') as f:
        binary_code = f.read()

    result = {
        "memory": {f"address_{i}": 0 for i in range(32)},  # Примерная карта памяти
        "registers": {f"reg_{i}": 0 for i in range(32)}   # Примерные регистры
    }

    # Обработка бинарного кода для load_const и других инструкций
    idx = 0
    while idx < len(binary_code):
        opcode = binary_code[idx]
        if opcode == 0x0A:  # load_const
            reg = binary_code[idx + 1]
            value = int.from_bytes(binary_code[idx + 2:idx + 4], 'little')
            result["registers"][f"reg_{reg}"] = value
            idx += 5
        elif opcode == 0x36:  # read_mem
            reg = binary_code[idx + 1]
            addr = binary_code[idx + 2]
            size = binary_code[idx + 3]
            result["memory"][f"address_{addr}"] = size  # Примерная логика
            idx += 4
        elif opcode == 0xA7:  # write_mem
            reg = binary_code[idx + 1]
            addr = binary_code[idx + 2]
            result["memory"][f"address_{addr}"] = result["registers"][f"reg_{reg}"]
            idx += 3
        else:
            idx += 1

    # Запись результата в файл
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=4)

def clean_up(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

# Тесты для проверки работы ассемблера и интерпретатора

def test_load_const_assembler():
    input_data = [
        "load_const 10 6 632"
    ]
    expected_binary = [0x0A, 0xE3, 0x09, 0x00, 0x00]

    with open('test.asm', 'w') as f:
        f.write("\n".join(input_data))

    assembler('test.asm', 'test.bin', 'test_log.json')

    with open('test.bin', 'rb') as f:
        binary_code = f.read()

    assert list(binary_code) == expected_binary, f"Expected: {expected_binary}, but got: {list(binary_code)}"
    print("Test passed: load_const (assembler)")

    clean_up(['test.asm', 'test.bin', 'test_log.json'])

def test_load_const_interpreter():
    input_data = [
        "load_const 10 6 632"
    ]
    expected_binary = [0x0A, 0xE3, 0x09, 0x00, 0x00]

    with open('test.asm', 'w') as f:
        f.write("\n".join(input_data))

    assembler('test.asm', 'test.bin', 'test_log.json')

    interpreter('test.bin', 'test_result.json', [0, 32])

    with open('test_result.json', 'r') as f:
        result = json.load(f)

    registers = result['registers']
    assert registers['reg_6'] == 632, f"Expected reg_6 to be 632, but got {registers['reg_6']}"
    print("Test passed: load_const (interpreter)")

    clean_up(['test.asm', 'test.bin', 'test_result.json', 'test_log.json'])

def test_read_mem_assembler():
    input_data = [
        "read_mem 54 328 3"
    ]
    expected_binary = [0x36, 0x48, 0x00, 0x00]

    with open('test.asm', 'w') as f:
        f.write("\n".join(input_data))

    assembler('test.asm', 'test.bin', 'test_log.json')

    with open('test.bin', 'rb') as f:
        binary_code = f.read()

    assert list(binary_code) == expected_binary, f"Expected: {expected_binary}, but got: {list(binary_code)}"
    print("Test passed: read_mem (assembler)")

    clean_up(['test.asm', 'test.bin', 'test_log.json'])

def test_read_mem_interpreter():
    input_data = [
        "load_const 10 328 100",
        "read_mem 54 328 3"
    ]

    with open('test.asm', 'w') as f:
        f.write("\n".join(input_data))

    assembler('test.asm', 'test.bin', 'test_log.json')

    interpreter('test.bin', 'test_result.json', [0, 32])

    with open('test_result.json', 'r') as f:
        result = json.load(f)

    registers = result['registers']
    assert registers['reg_3'] == 100, f"Expected reg_3 to be 100, but got {registers['reg_3']}"
    print("Test passed: read_mem (interpreter)")

    clean_up(['test.asm', 'test.bin', 'test_result.json', 'test_log.json'])

def test_write_mem_assembler():
    input_data = [
        "write_mem 39 1 5"
    ]
    expected_binary = [0xA7, 0x14]

    with open('test.asm', 'w') as f:
        f.write("\n".join(input_data))

    assembler('test.asm', 'test.bin', 'test_log.json')

    with open('test.bin', 'rb') as f:
        binary_code = f.read()

    assert list(binary_code) == expected_binary, f"Expected: {expected_binary}, but got: {list(binary_code)}"
    print("Test passed: write_mem (assembler)")

    clean_up(['test.asm', 'test.bin', 'test_log.json'])

def test_write_mem_interpreter():
    input_data = [
        "load_const 10 1 200",
        "write_mem 39 1 5"
    ]

    with open('test.asm', 'w') as f:
        f.write("\n".join(input_data))

    assembler('test.asm', 'test.bin', 'test_log.json')

    interpreter('test.bin', 'test_result.json', [0, 32])

    with open('test_result.json', 'r') as f:
        result = json.load(f)

    memory = result['memory']
    assert memory['address_5'] == 200, f"Expected address_5 to be 200, but got {memory['address_5']}"
    print("Test passed: write_mem (interpreter)")

    clean_up(['test.asm', 'test.bin', 'test_result.json', 'test_log.json'])

# Запуск тестов
test_load_const_assembler()
test_load_const_interpreter()
test_read_mem_assembler()
test_read_mem_interpreter()
test_write_mem_assembler()
test_write_mem_interpreter()
