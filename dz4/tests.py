from dataclasses import dataclass
import pytest
import pathlib
import subprocess
import json

project_dir = pathlib.Path(__file__).parent

@dataclass1
class BasicOpsCase:
    name: str
    input: str
    expected_output: bytes

BASIC_OPS_CASES = [
    BasicOpsCase("load",
                 "LOAD 6 632\n",
                 bytes([0x0a, 0xe3, 0x09, 0x00, 0x00])
    ),
    BasicOpsCase("read",
                 "READ 328 3\n",
                 bytes([0x36, 0xa4, 0x00, 0x00, 0x80, 0x01])
    ),
    BasicOpsCase("write",
                 "WRITE 1 5",
                 bytes([0xa7, 0x14])
    ),
    BasicOpsCase("popcnt",
                 "POPCNT 6 310\n",
                 bytes([0x12, 0xdb, 0x04, 0x00, 0x00, 0x00])
    )
]

def run_assembler(input_file, output_file, log_file):
    return subprocess.run(["python3", "assem.py", str(input_file), str(output_file), str(log_file)], capture_output=True)

def run_interpreter(assembler_file, interpreter_file, start, end):
    return subprocess.run(["python3", "inter.py", str(assembler_file), str(interpreter_file), str(start), str(end)], capture_output=True)

@pytest.mark.parametrize("op", BASIC_OPS_CASES)
def test_basic_operations(tmp_path, op):
    input_file = tmp_path / f"input_{op.name}.asm"
    log_file = tmp_path / f"log_{op.name}.json"
    output_file = tmp_path / f"output_{op.name}.bin"
    
    input_file.write_text(op.input)
    res = run_assembler(input_file, output_file, log_file)
    assert res.returncode == 0, f"Assembler failed for case {op.name}"
    
    got = output_file.read_bytes()[:len(op.expected_output)]
    assert got == op.expected_output, f"Test {op.name} failed: expected {op.expected_output}, got {got}"

def test_full_program(tmp_path):
    input_file = tmp_path / "input.asm"
    log_file = tmp_path / "log_file.json"
    assembler_file = tmp_path / "assembler.bin"
    interpreter_file = tmp_path / "result.json"

    input_file.write_text(
        """LOAD 1 1
WRITE 1 1

LOAD 2 2
WRITE 2 2

LOAD 3 3
WRITE 3 3

LOAD 4 4
WRITE 4 4

LOAD 5 5
WRITE 5 5

LOAD 6 6
WRITE 6 6

LOAD 7 7
WRITE 7 7

LOAD 8 8
WRITE 8 8

LOAD 9 9
LOAD 10 10
LOAD 11 11
LOAD 12 12
LOAD 13 13
LOAD 14 14
LOAD 15 15
LOAD 16 16

POPCNT 9 1
POPCNT 10 2
POPCNT 11 3
POPCNT 12 4
POPCNT 13 5
POPCNT 14 6
POPCNT 15 7
POPCNT 16 8
""")
    
    assembler_res = run_assembler(input_file, assembler_file, log_file)
    assert assembler_res.returncode == 0, "Assembler failed for the full program"

    interpreter_res = run_interpreter(assembler_file, interpreter_file, 0, 20)
    assert interpreter_res.returncode == 0, "Interpreter failed for the full program"

    got = json.loads(interpreter_file.read_text())
    expected = {
        "0": 8,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 0,
        "9": 1,
        "10": 2,
        "11": 3,
        "12": 4,
        "13": 5,
        "14": 6,
        "15": 7,
        "16": 0,
        "17": 0,
        "18": 0,
        "19": 0
    }
    assert got == expected, f"Interpreter output mismatch: expected {expected}, got {got}"

def test_invalid_command(tmp_path):
    input_file = tmp_path / "invalid_input.asm"
    log_file = tmp_path / "invalid_log.json"
    output_file = tmp_path / "invalid_output.bin"

    input_file.write_text("INVALID 1 2 3\n")
    res = run_assembler(input_file, output_file, log_file)
    assert res.returncode != 0, "Assembler should fail for invalid command"
    assert "TypeError" in res.stderr.decode(), "Assembler should provide a meaningful error message for unknown commands"

def test_memory_range(tmp_path):
    input_file = tmp_path / "input_memory.asm"
    log_file = tmp_path / "log_memory.json"
    assembler_file = tmp_path / "assembler_memory.bin"
    interpreter_file = tmp_path / "result_memory.json"

    input_file.write_text(
        """LOAD 1 42
WRITE 1 0
""")
    
    assembler_res = run_assembler(input_file, assembler_file, log_file)
    assert assembler_res.returncode == 0, "Assembler failed for memory test"

    interpreter_res = run_interpreter(assembler_file, interpreter_file, 0, 2)
    assert interpreter_res.returncode == 0, "Interpreter failed for memory test"

    got = json.loads(interpreter_file.read_text())
    expected = {
        "0": 0,
        "1": 0
    }
    assert got == expected, f"Interpreter output mismatch for memory range: expected {expected}, got {got}"
