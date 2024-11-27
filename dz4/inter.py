import json
import sys

MEMORY_SIZE = 1024
REG_COUNT = 1024

class BinaryBuffer:
    def __init__(self, binary_data: bytearray):
        self.binary_data: bytearray = binary_data
        self.bit_it = 0

    def read(self, bit_width):
        res = 0
        for i in range(bit_width):
            res ^= (((self.binary_data[self.bit_it // 8] >> (self.bit_it % 8)) & 1) << i)
            self.bit_it += 1
        return res

def interpret(binary_path, result_path, memory_range):
    memory = [0] * MEMORY_SIZE
    registers = [0] * REG_COUNT
    result = {}

    with open(binary_path, "rb") as f:
        binary_data = f.read()

    buffer = BinaryBuffer(binary_data)
    i = 0
    while i * 8 < len(binary_data):
        opcode = buffer.read(7)
        if opcode == 10:
            b = buffer.read(3)
            c = buffer.read(24)
            assert buffer.read(6) == 0
            registers[b] = c
            i += 5
        elif opcode == 54:
            b = buffer.read(32)
            c = buffer.read(3)
            assert buffer.read(6) == 0
            registers[c] = memory[b] 
            i += 6
        elif opcode == 39:
            b = buffer.read(3)
            c = buffer.read(3)
            assert buffer.read(3) == 0
            memory[b] = registers[c]  
            i += 2
        elif opcode == 18:
            b = buffer.read(3)
            c = buffer.read(32)
            assert buffer.read(6) == 0
            memory[registers[b]] = memory[c]
            i += 6
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
    
    result = {addr: memory[addr] for addr in range(*memory_range)}

    with open(result_path, "w") as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    memory_range = tuple(map(int, sys.argv[3:5]))
    interpret(binary_file, result_file, memory_range)
