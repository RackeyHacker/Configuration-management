import pytest
import os
import json
from io import BytesIO
from tempfile import NamedTemporaryFile
from assem import assembler, interpreter, serializer, parse_binary_commands

def test_serializer():
    result = serializer(17, ((3, 5), (7, 15)), 3)
    assert result == (17 | (3 << 5) | (7 << 15)).to_bytes(3, 'little')

    result = serializer(1, ((4, 5), (8, 12), (15, 19)), 5)
    assert result == (1 | (4 << 5) | (8 << 12) | (15 << 19)).to_bytes(5, 'little')
    
def test_assembler(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.bin"
    log_file = tmp_path / "log.json"

    input_file.write_text("load_const 1 3\nread 2 3 4\n")

    assembler(str(input_file), str(output_file), str(log_file))

    with open(output_file, 'rb') as f:
        binary_data = f.read()
        assert len(binary_data) > 0

    with open(log_file, 'r') as f:
        log_entries = json.load(f)
        assert len(log_entries) == 2
        assert log_entries[0] == "load_const b=1 c=3"
        assert log_entries[1] == "read b=2 c=3 d=4"


def test_interpreter(tmp_path):
    input_file = tmp_path / "input.bin"
    output_file = tmp_path / "output.json"

    with open(input_file, 'wb') as f:
        f.write(serializer(17, ((0, 5), (10, 15)), 3))
        f.write(serializer(54, ((2, 7), (3, 39), (4, 41)), 6))

    interpreter(str(input_file), str(output_file), memory_range=(0, 10))

    with open(output_file, 'r') as f:
        result = json.load(f)
        assert len(result) == 10
        assert result.get("address_0") == 0
        assert result.get("address_2") == 10

def test_parse_binary_commands():
    bc = b''
    result = parse_binary_commands(bc)
    assert result == []

def test_load_constant():
    result = serializer(17, ((62, 5), (3, 15)), 3)
    assert result == bytes([0xD1, 0x87, 0x01])

def test_write_memory():
    result = serializer(1, ((61, 5), (52, 12), (812, 19)), 5)
    assert result == bytes([0xA1, 0x47, 0x63, 0x19, 0x00])

def test_bitwise_rotate_right():
    result = serializer(20, ((852, 5), (103, 34)), 6)
    assert result == bytes([0x94, 0x6A, 0x00, 0x00, 0x9C, 0x01])

def test_read_memory():
    result = serializer(3, ((103, 5), (101, 12), (76, 26)), 5)
    assert result == bytes([0xE3, 0x5C, 0x06, 0x30, 0x01])

def test_program_execution(tmp_path):
    input_file = tmp_path / "input.bin"
    output_file = tmp_path / "output.json"

    with open(input_file, 'wb') as f:
        for i in range(7):
            f.write(serializer(20, ((i, 5), (i + 1, 34)), 6))

    interpreter(str(input_file), str(output_file), memory_range=(0, 7))

    with open(output_file, 'r') as f:
        result = json.load(f)
        assert len(result) == 7


if __name__ == "__main__":
    pytest.main()
