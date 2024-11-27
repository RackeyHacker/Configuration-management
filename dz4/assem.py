import json
import sys

COMMANDS = {
    "LOAD": 10,
    "READ": 54,
    "WRITE": 39,
    "POP_CNT": 18,
}

# Функция для записи в бинарный файл
def write_binary(buffer, value, bit_width):
    # Вычисляем количество байтов, необходимых для записи
    byte_value = value.to_bytes((bit_width + 7) // 8, byteorder='big')  # Big-endian byte order
    buffer.extend(byte_value)

    # Отладочный вывод, чтобы видеть, что пишется
    print(f"Writing value {value} (bit width {bit_width}) as bytes: {byte_value.hex()}")

def assemble(input_path, binary_path, log_path):
    log = []
    binary_data = bytearray()

    with open(input_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            continue
        
        parts = line.strip().split()
        command = parts[0].upper()
        opcode = COMMANDS.get(command)

        if opcode is None:
            raise ValueError(f"Unknown command: {command}")

        # Запись опкода (7 бит)
        write_binary(binary_data, opcode, 7)

        if command == "LOAD":
            addr, const = map(int, parts[1:])
            # Адрес (3 бита) - записываем 3 бита
            write_binary(binary_data, addr, 3)
            # Константа (24 бита) - записываем 24 бита
            write_binary(binary_data, const, 24)
            log.append({"command": command, "opcode": opcode, "const": const, "address": addr})

        elif command == "READ":
            addr1, addr2 = map(int, parts[1:])
            # Адрес1 (32 бита) - записываем 32 бита
            write_binary(binary_data, addr1, 32)
            # Адрес2 (3 бита) - записываем 3 бита
            write_binary(binary_data, addr2, 3)
            log.append({"command": command, "opcode": opcode, "addr1": addr1, "addr2": addr2})

        elif command == "WRITE":
            addr1, addr2 = map(int, parts[1:])
            # Адрес1 (6 бит) - записываем 6 бит
            write_binary(binary_data, addr1, 6)
            # Адрес2 (6 бит) - записываем 6 бит
            write_binary(binary_data, addr2, 6)
            log.append({"command": command, "opcode": opcode, "addr1": addr1, "addr2": addr2})

        elif command == "POP_CNT":
            addr1, addr2 = map(int, parts[1:])
            # Адрес1 (3 бита) - записываем 3 бита
            write_binary(binary_data, addr1, 3)
            # Адрес2 (32 бита) - записываем 32 бита
            write_binary(binary_data, addr2, 32)
            log.append({"command": command, "opcode": opcode, "addr1": addr1, "addr2": addr2})

        else:
            raise ValueError(f"Unknown command: {command}")

    # Запись в бинарный файл
    with open(binary_path, "wb") as f:
        f.write(binary_data)

    # Логирование команд в формате JSON
    with open(log_path, "w") as f:
        json.dump(log, f, indent=4)

    # Бинарный вывод (в hex-формате)
    print("Binary File Content:")
    print(" ".join(f"{byte:02x}" for byte in binary_data))

if __name__ == "__main__":
    input_file = sys.argv[1]
    binary_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, binary_file, log_file)
