"""
DrawStackTables.py 
Author: snowcra5h@icloud.com

This code takes in three inputs: 
    1. a list of integers called `stack_data`, 
    2. a list of strings called `labels`, 
    3. a list of integers called `sizes`.
It then draws a visual representation of a stack data structure, with each section of the stack 
labeled with the corresponding element from `labels` and the corresponding size from `sizes`. 

Usage example:

stack_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
labels = ["Section 1", "Section 2"]
sizes = [8, 7]

draw_stack(stack_data, labels, sizes)

This would output the following table:
+----------+-------+-------+------------------------+
|   Label  |  Pos  | Size  |      Stack Data        |
+----------+-------+-------+------------------------+
| Section 1|   +0  |   8   | 01 02 03 04 05 06 07 08|
| Section 2|   +8  |   7   | 09 0A 0B 0C 0D 0E 0F 00|
+----------+-------+-------+------------------------+

Work in progress; currently only supports 4-byte and 8-byte stack data structures. 
in the future DrawStackTables will parse code to get stack data, labels, and sizes.
"""

import colorama
import re
from tabulate import tabulate
import ast

class StackDrawer:
    # Constants for colorama
    LIGHTBLACK_EX = colorama.Back.LIGHTBLACK_EX
    LIGHTRED_EX = colorama.Back.LIGHTRED_EX
    LIGHTBLUE_EX = colorama.Back.LIGHTBLUE_EX
    LIGHTMAGENTA_EX = colorama.Back.LIGHTMAGENTA_EX
    LIGHTCYAN_EX = colorama.Back.LIGHTCYAN_EX
    WHITE = colorama.Fore.WHITE
    BRIGHT = colorama.Style.BRIGHT
    RESET_ALL = colorama.Style.RESET_ALL

    # List of colors to use
    __colors = [LIGHTBLACK_EX, LIGHTRED_EX, LIGHTBLUE_EX,
                LIGHTMAGENTA_EX, LIGHTCYAN_EX]

    def __init__(self, stack_data, labels, sizes, width) -> None:
        self.stack_data = stack_data
        self.labels = labels
        self.sizes = sizes
        self.width = width

    def draw_stack(self) -> None:
        table_data = []
        pos = 0

        for label, size in zip(self.get_labels(), self.get_sizes()):
            color = self.__colors[len(table_data) % len(self.__colors)]
            section_rows = self.__get_section_rows(size, self.get_width())

            for i in range(section_rows):
                row_data = self.get_stack_data()[pos:pos+self.get_width()]
                row_data += [0] * (self.get_width() - len(row_data))
                hex_values = self.__get_hex_values(row_data)
                stack_data_string = self.__get_stack_data_string(
                    hex_values, color)
                table_data.append(self.__get_table_row(
                    label, pos, size, stack_data_string))
                pos += self.get_width()

        print(tabulate(table_data, headers=[
              "Label", "Pos", "Size", "Stack Data"]))

    def get_stack_data(self) -> list:
        return self.stack_data

    def get_labels(self) -> list:
        return self.labels

    def get_sizes(self) -> list:
        return self.sizes

    def get_width(self) -> int:
        return self.width

    def __get_section_rows(self, size, width) -> int:
        return size // width + (size % width != 0)

    def __get_hex_values(self, row_data) -> list:
        return ["0" + hex(x)[2:] if len(hex(x)[2:]) < 2 else hex(x)[2:] for x in row_data]

    def __get_stack_data_string(self, hex_values, color) -> str:
        return f"{color}{self.BRIGHT}{self.WHITE}{' '.join(hex_values)}{self.RESET_ALL}"

    def __get_table_row(self, label, pos, size, stack_data_string) -> list:
        if label:
            return [label, "+0x" + hex(pos)[2:], size, stack_data_string]
        else:
            return ["", "", "", stack_data_string]


class StackInputSource:
    def __init__(self) -> None:
        self.__data = {
            4: ([0x90]*8 + [0x41] * 16 + [0x12, 0x34, 0x56, 0x78] + [0x66]*4,
                ["nop sled", "buffer", "Old RBP", "ret ADDR"],
                [8, 16, 4, 4], 4),
            8: ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], ["Section 1", "Section 2"], [8, 7], 8)
        }

    def get_test_input(self, width: int) -> tuple:
        return self.__data.get(width)


    def expand_multiplier(self, input_string):
        match = re.fullmatch(r"(.+)\*(\d+)", input_string)
        if match is None:
            return [input_string]

        element = match.group(1)
        multiplier = int(match.group(2))

        return [element] * multiplier

    def flatten_list(self, input_list):
        return [item for sublist in input_list for item in sublist]

    def convert_hex_strings(self, input_list):
        return [hex(ord(s[1])) if len(s) == 3 else s for s in input_list]

    def parse_stack_data(self, input_list):
        input_list = input_list[1:-1].split(", ")

        if len(input_list) == 1 and input_list[0] == "":
            return []

        input_list = [s[1:] if s[0] in "+-" else s for s in input_list]
        expanded_input_list = [self.expand_multiplier(s) for s in input_list]
        flattened_input_list = self.flatten_list(expanded_input_list)
        hex_string_list = self.convert_hex_strings(flattened_input_list)

        hex_digits = []
        for input_string in hex_string_list:
            try:
                hex_value = hex(int(input_string, 16))
                if len(hex_value) == 3:
                    hex_value = "0x0" + hex_value[2]
                if len(hex_value) > 4:
                    raise ValueError(
                        f"{hex_value} is more than one byte. Hex values must be one byte (two hexadecimal digits).")
                hex_digits.append(int(hex_value, 16))
            except ValueError as e:
                raise ValueError(
                    "Invalid input: the stack data must be a list of hexadecimal integers. for example [0xA*4, 0xB*2, 0xC*8, 0xD, ...]") from e
        return hex_digits

    def str_to_list(self, s):
      try:
        label_list = ast.literal_eval(s)
      except ValueError:
        print("Error: Invalid input")
      except SyntaxError:
        print("Error: Invalid list format")
      else:
        return label_list

    def get_width(self) -> int:
        while True:
            size = input("Enter the size you want to use (4 or 8): ")      
            if size != "4" and size != "8":
                print("Error: Invalid size. Please enter either 4 or 8.")
            else:
                width = int(size)
                break
        return width
    
    def get_stack_data(self) -> list:
        stack_data = input(
            "Enter the stack data as a list of hexadecimal integers, in the format [0xA*4, 0xB*2, 0xC*8, 0xD, \"A\"*10...]: ")
        stack_data = self.parse_stack_data(stack_data)
        return stack_data
    
    def get_labels(self) -> list:
        labels = input("Enter the labels as a list of strings: ")
        labels = self.str_to_list(labels)
        return labels
    
    def get_sizes(self) -> list:
        sizes = input("Enter the sizes as a list of integers: ")
        sizes = [int(s) for s in sizes[1:-1].split(", ")]
        return sizes
    
    def get_manual_input(self) -> tuple:
        stack_data = self.get_stack_data()
        labels = self.get_labels()
        sizes = self.get_sizes()
        width = self.get_width()

        return stack_data, labels, sizes, width

    def get_input(self, automate: bool, width: int = 8) -> tuple:
        if automate:
            return self.get_test_input(width)
        else:
            return self.get_manual_input()

if __name__ == "__main__":
    
    ui = StackInputSource()

    while True:
        print("Menu:")
        print("1. Automate with test data (width = 4)")
        print("2. Automate with test data (width = 8)")
        print("3. Manually input stack data, labels, and sizes")
        print("4. Quit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            stack_data, labels, sizes, width = ui.get_input(
                automate=True, width=4)
            stack_drawer = StackDrawer(stack_data, labels, sizes, width)
            stack_drawer.draw_stack()
        elif choice == "2":
            stack_data, labels, sizes, width = ui.get_input(
                automate=True, width=8)
            stack_drawer = StackDrawer(stack_data, labels, sizes, width)
            stack_drawer.draw_stack()
        elif choice == "3":
            stack_data, labels, sizes, width = ui.get_input(automate=False)
            stack_drawer = StackDrawer(stack_data, labels, sizes, width)
            stack_drawer.draw_stack()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")