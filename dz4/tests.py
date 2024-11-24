import pytest1
import os
import json
from io import BytesIO
from assem import assembler, interpreter, serializer, parse_binary_commands

def test_load_const(tmp_path):
    input_file = tmp_path / "input.bin"
    output_file = tmp_path / "output.json"

    with open(input_file, 'wb') as f:
        f.write(bytes([10, 6, 0, 0, 0]))

    try:
        interpreter(str(input_file), str(output_file), (0, 10))
    except Exception as e:
        pytest.fail(f"Error during interpretation: {e}")

    with open(output_file, 'r') as f:
        result = json.load(f)
        address_6_value = result.get("address_6", None)
        assert address_6_value == 632, f"Expected 632 at address_6, but got {address_6_value}"

def test_read(tmp_path):
    input_file = tmp_path / "input.bin"
    output_file = tmp_path / "output.json"

    with open(input_file, 'wb') as f:
        f.write(bytes([10, 6, 0, 0, 0]))
        f.write(bytes([54, 0xA4, 0x00, 0x00, 0x80, 0x01]))

    try:
        interpreter(str(input_file), str(output_file), (0, 10))
    except Exception as e:
        pytest.fail(f"Error during interpretation: {e}")

    with open(output_file, 'r') as f:
        result = json.load(f)
        address_4_value = result.get("address_4", None)
        assert address_4_value == 0, f"Expected 0 at address_4, but got {address_4_value}"

def test_write(tmp_path):
    input_file = tmp_path / "input.bin"
    output_file = tmp_path / "output.json"

    with open(input_file, 'wb') as f:
        f.write(bytes([10, 6, 0, 0, 0]))
        f.write(bytes([39, 6, 7]))

    try:
        interpreter(str(input_file), str(output_file), (0, 10))
    except Exception as e:
        pytest.fail(f"Error during interpretation: {e}")

    with open(output_file, 'r') as f:
        result = json.load(f)
        address_7_value = result.get("address_7", None)
        address_6_value = result.get("address_6", None)
        assert address_7_value == address_6_value, f"Expected address_7 to be {address_6_value}, but got {address_7_value}"

def test_popcnt(tmp_path):
    input_file = tmp_path / "input.bin"
    output_file = tmp_path / "output.json"

    with open(input_file, 'wb') as f:
        f.write(bytes([10, 6, 0, 0, 0]))
        f.write(0b11110000.to_bytes(1, byteorder='little'))

    try:
        interpreter(str(input_file), str(output_file), (0, 10))
    except Exception as e:
        pytest.fail(f"Error during interpretation: {e}")

    with open(output_file, 'r') as f:
        result = json.load(f)
        address_6_value = result.get("address_6", None)
        assert address_6_value == 4, f"Expected 4 at address_6 (popcnt result), but got {address_6_value}"
