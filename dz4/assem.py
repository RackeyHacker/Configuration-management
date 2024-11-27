
import struct
import json
import sys
from dataclasses import dataclass

COMMANDS = {
    "LOAD": 10,
    "READ": 54,
    "WRITE": 39,
    "POPCNT": 18,
}

@dataclass
class BinaryBuffer:
    binary_data = bytearray()
    bit_size = 0
    
    def write(self, x, bit_width):
        for i in range(bit_width):
            if (self.bit_size + 1) * 8 > len(self.binary_data):
                self.binary_data.append(0)
            self.binary_data[self.bit_size // 8] ^= (((x >> i) & 1) << (self.bit_size % 8))
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

        buffer.write(opcode, 7)
        if command == "LOAD":
            addr, const = map(int, parts[1:])
            buffer.write(addr, 3)
            buffer.write(const, 24)
            buffer.write(0, 6)
            log.append({"command": command, "opcode": opcode, "address": addr, "const": const}) 
        elif command == "READ":
            addr1, addr2 = map(int, parts[1:])
            buffer.write(addr1, 32)
            buffer.write(addr2, 3)
            buffer.write(0, 6)
            log.append({"command": command, "opcode": opcode, "addr1": addr1, "addr2": addr2})
        elif command == "WRITE":    
            addr1, addr2 = map(int, parts[1:])
            buffer.write(addr1, 3)
            buffer.write(addr2, 3)
            buffer.write(0, 3)
            log.append({"command": command, "opcode": opcode, "addr1": addr1, "addr2": addr2})
        elif command == "POPCNT":
            addr1, addr2 = map(int, parts[1:])
            buffer.write(addr1, 3)
            buffer.write(addr2, 32)
            buffer.write(0, 6)
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
