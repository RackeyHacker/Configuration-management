Задание №3 - 5 ВАРИАНТ

Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на языке yaml принимается из стандартного ввода. Выходной
текст на учебном конфигурационном языке попадает в файл, путь к которому
задан ключом командной строки.

Однострочные комментарии:

; Это однострочный комментарий

Массивы:

array( значение, значение, значение, ... )

Имена:

[_a-zA-Z]+

Значения:
• Числа.
• Массивы.

Объявление константы на этапе трансляции:

значение -> имя

Вычисление константного выражения на этапе трансляции (постфиксная
форма), пример:

.{имя 1 +}.

Результатом вычисления константного выражения является значение.
Для константных вычислений определены операции и функции:
1. Сложение.
2. Вычитание.
3. Умножение.
4. pow().

Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.

Для запуска кода нужно прописать данную команду (находясь в директории с программой):

![{5D013DF0-56A4-45DD-8943-5EEEBD174DD3}](https://github.com/user-attachments/assets/3e75d94f-11d2-445e-914a-958db8a3c6aa)

Здесь в качестве аргументов поступают: исполняемый код, файл из которого берутся данные, а также файл, в который будет записываться информация

Пример входного файла:

![{4B70293B-027C-475C-B2B8-1947CC55F85E}](https://github.com/user-attachments/assets/a2be8725-645f-4d28-97c4-7676894478d9)

Пример выходного файла:

![{CC97A32B-3380-45DE-A338-35EED50B1BC9}](https://github.com/user-attachments/assets/d56d741d-c0fb-4281-9d5f-b700143c9c2b)

3 примера описания конфигураций из разных предметных областей:

Пример 1: Конфигурация для математических вычислений (арифметика)

пример входного файла:

![{26B2AB4A-F24B-451C-91D1-B961E348BC6F}](https://github.com/user-attachments/assets/f70482a1-210a-4779-ad90-c261d1601cab)


пример выходного файла:

![{93ED3CDA-4B30-4973-A3D2-1CB0101A7957}](https://github.com/user-attachments/assets/3d1e6f6a-a1a1-4927-aae3-be089d585434)

Пример 2: Конфигурация для работы с массивами данных (обработка списков)

пример входного файла:

![{64701008-95E5-4718-9A62-6E795117AE4A}](https://github.com/user-attachments/assets/26d56394-3e17-46ae-bd80-8bfaf2ad99ec)

пример выходного файла:

![{9879C39A-B791-440C-8568-2634EAE5C4BA}](https://github.com/user-attachments/assets/a93e61a7-174d-4131-a953-481f007e512e)

Пример 3: Конфигурация для логических значений и условий

пример входного файла:

![{C2D0261F-7E94-41E5-9470-5EA60E81128E}](https://github.com/user-attachments/assets/f9234e4b-d0db-4039-9ca8-42e9f61a4c27)


пример выходного файла:

![{BA3CAACD-513F-403D-A5F7-39E32A15DB29}](https://github.com/user-attachments/assets/d1f5dbe2-f95c-4405-a2bc-6971dce40342)


Также по заданию требовалось провести тесты. Результат запуска файла с тестами:

![{17DA22F5-5860-4FE0-AE3F-CB2D97C8AC10}](https://github.com/user-attachments/assets/f24c3ec4-76ec-4d22-a688-5e6e96e09237)






