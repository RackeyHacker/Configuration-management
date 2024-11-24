import argparse1
import json

def assembler(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        code = [line.strip().split() for line in f.readlines()]
        code = [(op, *map(int, args)) for op, *args in code]

    bc = []
    log_entries = []
    for line_num, (op, *args) in enumerate(code, start=1):
        try:
            if op == 'load_const':
                if len(args) != 2:
                    raise ValueError(f"Line {line_num}: 'load_const' expects 2 arguments, got {len(args)}")
                b, c = args
                bc += serializer(10, ((b, 7), (c, 10)), 5)
                log_entries.append(f"load_const b={b} c={c}")
            elif op == 'read':
                if len(args) != 3:
                    raise ValueError(f"Line {line_num}: 'read' expects 3 arguments, got {len(args)}")
                b, c, d = args
                bc += serializer(54, ((b, 7), (c, 39), (d, 41)), 6)
                log_entries.append(f"read b={b} c={c} d={d}")
            elif op == 'write':
                if len(args) != 2:
                    raise ValueError(f"Line {line_num}: 'write' expects 2 arguments, got {len(args)}")
                b, c = args
                bc += serializer(39, ((b, 7), (c, 10)), 2)
                log_entries.append(f"write b={b} c={c}")
            elif op == 'popcnt':
                if len(args) != 2:
                    raise ValueError(f"Line {line_num}: 'popcnt' expects 2 arguments, got {len(args)}")
                b, c = args
                bc += serializer(18, ((b, 7), (c, 10)), 6)
                log_entries.append(f"popcnt b={b} c={c}")
            else:
                raise ValueError(f"Line {line_num}: Unknown operation '{op}'")
        except ValueError as e:
            print(f"Error in input file: {e}")
            return
    
    with open(output_file, 'wb') as f:
        f.write(bytearray(bc))
    
    with open(log_file, 'w') as f:
        json.dump(log_entries, f, indent=4)


def serializer(cmd, fields, size):
    bits = cmd
    for value, shift in fields:
        bits |= value << shift
    return bits.to_bytes(size, 'little')

def interpreter(input_file, output_file, memory_range):
    with open(input_file, 'rb') as f:
        bc = f.read()

    memory = [0] * 256
    commands = parse_binary_commands(bc)

    for op, *args in commands:
        if op == "load_const":
            memory[args[0]] = args[1]
        elif op == "read":
            memory[args[2]] = memory[args[0]]
        elif op == "write":
            memory[args[1]] = memory[args[0]]
        elif op == "popcnt":
            memory[args[0]] = bin(memory[args[1]]).count('1')

    result = {f"address_{i}": memory[i] for i in range(memory_range[0], memory_range[1])}
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=4)

def parse_binary_commands(bc):
    instructions = {
        10: ("load_const", 1, 4),
        54: ("read", 1, 4, 1),
        39: ("write", 1, 1),
        18: ("popcnt", 1, 4)
    }
    i, commands = 0, []
    while i < len(bc):
        cmd = bc[i]
        if cmd not in instructions:
            i += 1
            continue
        op, *sizes = instructions[cmd]
        args = [bc[i + 1 + j] for j in range(len(sizes))]
        i += 1 + sum(sizes)
        commands.append((op, *args))
    return commands

def main():
    parser = argparse.ArgumentParser(description='Assembler and Interpreter for a custom VM.')
    subparsers = parser.add_subparsers(dest='command')

    asm_parser = subparsers.add_parser('assemble', help='Assemble source code into binary')
    asm_parser.add_argument('input_file', help='Path to the input source file')
    asm_parser.add_argument('output_file', help='Path to the output binary file')
    asm_parser.add_argument('log_file', help='Path to the log JSON file')

    int_parser = subparsers.add_parser('interpret', help='Interpret binary file')
    int_parser.add_argument('input_file', help='Path to the input binary file')
    int_parser.add_argument('output_file', help='Path to the output JSON file')
    int_parser.add_argument('mem_range', type=int, nargs=2, help='Range of memory to output (start end)')

    args = parser.parse_args()
    if args.command == 'assemble':
        assembler(args.input_file, args.output_file, args.log_file)
    elif args.command == 'interpret':
        interpreter(args.input_file, args.output_file, args.mem_range)

if __name__ == "__main__":
    main()
