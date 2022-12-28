# DrawStack
```bash
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
```

![image](https://user-images.githubusercontent.com/90065760/209877014-cdbf8df7-60a4-4047-be6c-d47b026519c6.png)
