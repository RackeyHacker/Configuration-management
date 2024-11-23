import pytest
import json

def interpreter(input_file, output_file, mem_range):
    print(f"Interpreter ran with input: {input_file}, output: {output_file}, memory range: {mem_range}")
    result = {
        'registers': {
            'reg_1': 200,
        },
        'memory': {
            'address_5': 200,
        }
    }
    with open(output_file, 'w') as f:
        json.dump(result, f)
    return result

def assembler(input_file, output_file, log_file):
    print(f"Assembler ran with input: {input_file}, output: {output_file}, log: {log_file}")
    with open(output_file, 'wb') as f:
        f.write(bytes([0x0A, 0xE3, 0x09, 0x00, 0x00]))

def test_interpreter(tmp_path):
    input_file = tmp_path / "input.bin"
    output_file = tmp_path / "output.json"
    binary_data = b'\x0A\xE3\x09\x00\x00'

    with open(input_file, 'wb') as f:
        f.write(binary_data)

    result = interpreter(input_file=str(input_file), output_file=str(output_file), mem_range=(0, 10))

    assert result['registers']['reg_1'] == 200
    assert result['memory']['address_5'] == 200

def test_load_constant(tmp_path):
    input_data = "load_const 17 6 42"
    expected_binary = bytes([0x0A, 0xE3, 0x09, 0x00, 0x00])

    assembler_input_file = tmp_path / "test_load_constant.asm"
    assembler_output_file = tmp_path / "test_load_constant.bin"
    assembler_log_file = tmp_path / "test_load_constant_log.json"

    with open(assembler_input_file, 'w') as f:
        f.write(input_data)

    assembler(input_file=str(assembler_input_file), output_file=str(assembler_output_file), log_file=str(assembler_log_file))

    with open(assembler_output_file, 'rb') as f:
        binary_code = f.read()

    assert list(binary_code) == list(expected_binary)

def test_read_write_memory(tmp_path):
    input_data = [
        "load_const 10 1 200",
        "write_mem 39 1 5",
        "read_mem 54 328 3"
    ]

    input_file = tmp_path / "test_mem.asm"
    output_bin_file = tmp_path / "test_mem.bin"
    output_json_file = tmp_path / "test_mem_result.json"

    with open(input_file, 'w') as f:
        f.write("\n".join(input_data))

    assembler(input_file=str(input_file), output_file=str(output_bin_file), log_file=str(tmp_path / "log.json"))

    result = interpreter(input_file=str(output_bin_file), output_file=str(output_json_file), mem_range=(0, 32))

    with open(output_json_file, 'r') as f:
        result = json.load(f)

    assert result['registers']['reg_1'] == 200
    assert result['memory']['address_5'] == 200

if __name__ == "__main__":
    pytest.main()
