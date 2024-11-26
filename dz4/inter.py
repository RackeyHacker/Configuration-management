import json

MEMORY_SIZE = 1024  # Размер памяти
REG_COUNT = 8  # Количество регистров

# Чтение бинарных данных
def read_bin(binary_path):
    try:
        with open(binary_path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading binary file {binary_path}: {e}")
        return None

# Функция для интерпретации команд
def interpret(binary_data, result_path, memory_range):
    memory = [0] * MEMORY_SIZE
    registers = [0] * REG_COUNT
    i = 0  # Индекс команды

    # Открываем файл debug_log.txt для записи
    try:
        with open("debug_log.txt", "w") as log_file:
            log_file.write("Starting interpretation...\n")

            while i < len(binary_data):
                opcode = binary_data[i]
                i += 1

                # Выводим только нужные байты в соответствии с вашими требованиями
                if opcode == 0x0A:  # Если байт 0x0A, это LOAD
                    b = binary_data[i:i+4]
                    c = binary_data[i+4:i+8]
                    i += 8
                    # Выводим биты в нужном формате с пустой строкой после каждого блока
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in b])}\n")
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in c])}\n\n")

                elif opcode == 0x36:  # Если байт 0x36, это READ
                    b = binary_data[i:i+4]
                    c = binary_data[i+4:i+8]
                    d = binary_data[i+8:i+12]
                    i += 12
                    # Выводим биты в нужном формате с пустой строкой после каждого блока
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in b])}\n")
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in c])}\n")
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in d])}\n\n")

                elif opcode == 0xA7:  # Если байт 0xA7, это WRITE
                    b = binary_data[i:i+4]
                    c = binary_data[i+4:i+7]
                    i += 7
                    # Выводим биты в нужном формате с пустой строкой после каждого блока
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in b])}\n")
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in c])}\n\n")

                elif opcode == 0x12:  # Если байт 0x12, это POPCNT
                    b = binary_data[i:i+4]
                    c = binary_data[i+4:i+7]
                    i += 7
                    # Выводим биты в нужном формате с пустой строкой после каждого блока
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in b])}\n")
                    log_file.write(f"{', '.join([f'0x{byte:02X}' for byte in c])}\n\n")

                else:
                    # Пропуск всех неизвестных опкодов
                    pass

            # Запись результата в JSON
            result = {addr: memory[addr] for addr in range(memory_range[0], memory_range[1])}
            try:
                with open(result_path, "w") as f:
                    json.dump(result, f, indent=4)
            except Exception as e:
                pass

            log_file.write("Interpretation completed.\n")
    
    except Exception as e:
        print(f"Error during interpretation or logging: {e}")
        return


if __name__ == "__main__":
    binary_data = read_bin("output.bin")
    if binary_data:
        interpret(binary_data, "result.json", (0, 100))
