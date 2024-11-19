import argparse
import json
import struct


def assembler(input_file, output_file, log_file):
    # Чтение исходного текстового файла
    with open(input_file, 'r') as f:
        code = [line.strip().split() for line in f.readlines()]

    binary_code = []
    log_entries = []

    for line_num, (op, *args) in enumerate(code, start=1):
        try:
            if op == 'load_const':  # Загрузка константы
                if len(args) != 3:
                    raise ValueError(f"Line {line_num}: Expected 3 arguments for 'load_const', got {len(args)}")
                a, b, c = map(int, args)
                binary_code.append(serialize(0x0A, b, c))  # Преобразование в байты
                log_entries.append({"A": a, "B": b, "C": c})

            elif op == 'read_mem':  # Чтение из памяти
                if len(args) != 3:
                    raise ValueError(f"Line {line_num}: Expected 3 arguments for 'read_mem', got {len(args)}")
                a, b, c = map(int, args)
                binary_code.append(serialize(0x36, b, c))
                log_entries.append({"A": a, "B": b, "C": c})

            elif op == 'write_mem':  # Запись в память
                if len(args) != 3:
                    raise ValueError(f"Line {line_num}: Expected 3 arguments for 'write_mem', got {len(args)}")
                a, b, c = map(int, args)
                binary_code.append(serialize(0xA7, b, c))
                log_entries.append({"A": a, "B": b, "C": c})

            elif op == 'popcnt':  # Унарная операция popcnt
                if len(args) != 2:
                    raise ValueError(f"Line {line_num}: Expected 2 arguments for 'popcnt', got {len(args)}")
                a, b = map(int, args)
                binary_code.append(serialize(0x12, a, b))
                log_entries.append({"A": a, "B": b})

            else:
                raise ValueError(f"Line {line_num}: Unknown operation '{op}'")
        except ValueError as e:
            print(f"Error in input file: {e}")
            return

    # Запись бинарного кода в файл
    with open(output_file, 'wb') as f:
        for bc in binary_code:
            f.write(bc)

    # Запись лога в формате JSON
    log_data = [{"instruction": entry} for entry in log_entries]
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=4)


def serialize(opcode, b, c):
    # Преобразует операнд в бинарное представление в зависимости от команды
    if opcode == 0xA7:  # write_mem (2 байта)
        return struct.pack('<BB', opcode, b)
    elif opcode == 0x12:  # popcnt (6 байт)
        return struct.pack('<BHH', opcode, b, c)
    else:  # load_const, read_mem (5 байт)
        return struct.pack('<BHH', opcode, b, c)


def interpreter(input_file, output_file, mem_range):
    # Чтение бинарного файла
    with open(input_file, 'rb') as f:
        binary_code = f.read()

    memory = [0] * 1024  # Инициализация памяти
    registers = [0] * 32  # Инициализация регистров

    i = 0
    while i < len(binary_code):
        opcode = binary_code[i]
        if opcode == 0xA7:  # Команда записи в память (2 байта)
            b, = struct.unpack('<B', binary_code[i + 1:i + 2])
            memory[b] = registers[b]  # Записать значение из регистра в память
            i += 2
        elif opcode == 0x12:  # Операция popcnt (6 байт)
            b, c = struct.unpack('<HH', binary_code[i + 1:i + 6])
            registers[b] = bin(registers[c]).count('1')  # Считаем количество единичных битов в регистре c
            i += 6
        elif opcode == 0x0A or opcode == 0x36:  # load_const или read_mem (5 байт)
            b, c = struct.unpack('<HH', binary_code[i + 1:i + 5])
            if opcode == 0x0A:
                registers[b] = c  # Загрузка константы в регистр
            elif opcode == 0x36:
                registers[c] = memory[b]  # Чтение из памяти в регистр
            i += 5
        else:
            print(f"Unknown opcode: {opcode}")
            break

    # Сохранение результатов в JSON
    result = {
        "memory": {f"address_{i}": memory[i] for i in range(mem_range[0], mem_range[1])},
        "registers": {f"reg_{i}": registers[i] for i in range(32)}
    }
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=4)


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
