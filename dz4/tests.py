import pytest
import json
from io import BytesIO
from tempfile import NamedTemporaryFile
from assem import assemble  
from inter import interpret, read_bin

@pytest.mark.parametrize("command, input_str, expected_binary_data, expected_log", [
    ("LOAD", "LOAD 10 15", 
     bytearray([0x0A, 0x00, 0x0A, 0x15, 0x00, 0x00]), 
     [{"command": "LOAD", "opcode": 10, "const": 15, "address": 10}]),

    ("READ", "READ 5 6 7", 
     bytearray([0x36, 0x05, 0x06, 0x07, 0x00, 0x00]), 
     [{"command": "READ", "opcode": 54, "addr1": 5, "addr2": 6}]),

    ("WRITE", "WRITE 1 2", 
     bytearray([0xA7, 0x01, 0x02, 0x00]), 
     [{"command": "WRITE", "opcode": 39, "addr1": 1, "addr2": 2}]),

    ("POP_CNT", "POP_CNT 5 6", 
     bytearray([0x12, 0x05, 0x06, 0x00, 0x00]), 
     [{"command": "POP_CNT", "opcode": 18, "addr1": 5, "addr2": 6}]),
])
def test_assembler_commands(command, input_str, expected_binary_data, expected_log):
    with NamedTemporaryFile(delete=False) as input_file:
        input_file.write(input_str.encode())
        input_file_name = input_file.name
    
    binary_file = f"{input_file_name}.bin"
    log_file = f"{input_file_name}.log"

    assemble(input_file_name, binary_file, log_file)

    with open(binary_file, 'rb') as f:
        binary_data = f.read()
        assert binary_data == expected_binary_data  

    with open(log_file, 'r') as f:
        log_entries = json.load(f)
        assert log_entries == expected_log 


@pytest.mark.parametrize("binary_data, expected_memory_result", [
    (bytearray([0x0A, 0x00, 0x0A, 0x15, 0x00, 0x00]), {0: 10, 1: 15}),
    (bytearray([0x36, 0x05, 0x06, 0x07, 0x00, 0x00]), {5: 6, 6: 7}),
    (bytearray([0xA7, 0x01, 0x02, 0x00]), {1: 2}),
    (bytearray([0x12, 0x05, 0x06, 0x00, 0x00]), {5: 6}),
])
def test_interpreter_commands(binary_data, expected_memory_result):

    with NamedTemporaryFile(delete=False) as input_file:
        input_file.write(binary_data)
        input_file_name = input_file.name

    result_file = f"{input_file_name}_result.json"
    interpret(binary_data, result_file, memory_range=(0, 10))

    with open(result_file, 'r') as f:
        result = json.load(f)
        assert result == expected_memory_result


def test_read_bin():

    binary_data = bytearray([0x0A, 0x00, 0x0A, 0x15, 0x00, 0x00])

    with NamedTemporaryFile(delete=False) as input_file:
        input_file.write(binary_data)
        input_file_name = input_file.name

    result = read_bin(input_file_name)

    assert result == binary_data
