import struct
import json
import sys
from dataclasses import dataclass

COMMANDS = {
    "LOAD": 10,
    "READ": 54,
    "WRITE": 39,
    "POP_CNT": 18,
}

class BinaryBuffer:
    def __init__(self):
        self.binary_data = bytearray()
        self.bit_size = 0

    def write(self, x, bit_width):
        while self.bit_size % 8 != 0:
            self.bit_size += 1  # Padding to next byte
        
        for i in range(bit_width):
            byte_index = self.bit_size // 8
            bit_index = self.bit_size % 8
            
            if byte_index >= len(self.binary_data):
                self.binary_data.append(0)
            
            # Set the bit at position 'bit_index' in byte at 'byte_index'
            self.binary_data[byte_index] |= (((x >> i) & 1) << bit_index)
            
            self.bit_size += 1


def assemble(input_path, binary_path, log_path):
    log = []
    buffer = BinaryBuffer()

    with open(input_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            continue
        
        parts = line.strip().split()
        command = parts[0].upper()
        opcode = COMMANDS.get(command)

        buffer.write(opcode, 7)  # Для команды всегда записываем 7 бит

        if command == "LOAD":
            const, addr = map(int, parts[1:])
            buffer.write(addr, 4)
            buffer.write(const, 27)
            log.append({"command": command, "opcode": opcode, "const": const, "address": addr})
        elif command == "READ":
            addr1, addr2 = map(int, parts[1:])
            buffer.write(addr1, 6)
            buffer.write(addr2, 39)
            log.append({"command": command, "opcode": opcode, "addr1": addr1, "addr2": addr2})
        elif command == "WRITE":
            addr1, addr2 = map(int, parts[1:])
            buffer.write(addr1, 6)
            buffer.write(addr2, 12)  # Заменить на 12 бит для корректной записи в память
            log.append({"command": command, "opcode": opcode, "addr1": addr1, "addr2": addr2})
        elif command == "POP_CNT":
            addr1, addr2 = map(int, parts[1:])
            buffer.write(addr1, 6)
            buffer.write(addr2, 41)
            log.append({"command": command, "opcode": opcode, "addr1": addr1, "addr2": addr2})
        else:
            raise ValueError(f"Unknown command: {command}")

    with open(binary_path, "wb") as f:
        f.write(buffer.binary_data)

    with open(log_path, "w") as f:
        json.dump(log, f, indent=4)

if __name__ == "__main__":
    input_file = sys.argv[1]
    binary_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, binary_file, log_file)
