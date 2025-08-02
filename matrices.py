from __future__ import annotations

from pydantic import BaseModel, field_validator
from typing import List, Tuple, Callable


class Matrix(BaseModel):
    raw_data: List[List[float]]

    # === validators ===
    @classmethod
    @field_validator('raw_data')
    def validate_val(cls, m: List[List[float]]) -> List[List[float]]:
        if (not m) or (not m[0]):
            raise ValueError('The matrix cannot be empty')

        num_cols = len(m[0])
        for row in m:
            if len(row) != num_cols:
                raise ValueError('Irregular matrices are not accepted - All rows must have the same number of elements')

        return m

    # === factory methods ===
    @classmethod
    def of(cls, data: List[List[float]]) -> Matrix:
        return Matrix(raw_data=data)

    @classmethod
    def null(cls, rows: int, columns: int) -> Matrix:
        raw = Matrix.__empty_structure(rows, columns)
        return Matrix(raw_data=raw)

    @classmethod
    def identity(cls, order: int) -> Matrix:
        raw = Matrix.__empty_structure(order, order)

        for i in range(order):
            for j in range(order):
                if i == j:
                    raw[i][j] = 1

        return Matrix(raw_data=raw)

    # === element manipulation ===
    def get(self, row: int, col: int) -> float:
        return self.raw_data[row][col]

    def set(self, row: int, col: int, val: float) -> None:
        self.raw_data[row][col] = val

    # === properties getters ===
    def order(self) -> Tuple[int, int]:
        x: int = len(self.raw_data)
        y: int = len(self.raw_data[0])
        return x, y

    def is_square(self) -> bool:
        x, y = self.order()
        return x == y

    def is_identity(self) -> bool:
        if not self.is_square(): return False

        x, y = self.order()

        for i in range(x):
            for j in range(y):
                if i == j and self.raw_data[i][j] != 1:
                    return False

        return True


    # === auxiliary functions ===
    def __basic_operation(self, other: Matrix, operator: Callable[[float, float], float]) -> Matrix:
        if operator not in (float.__sub__, float.__add__):
            raise ValueError('The operator must either be float.__add__ or float.__sub__')


        if self.order() != other.order():
            raise ValueError('Both matrices should be of the same order')

        x, y = self.order()
        new: List[List[float]] = Matrix.__empty_structure(x, y)

        for i in range(x):
            for j in range(y):
                new[i][j] = operator(self.get(i, j), other.get(i, j))

        return Matrix(raw_data=new)

    @staticmethod
    def __empty_structure(rows, columns) -> List[List[float]]:
        return [[0] * columns for _ in range(rows)]

    def __simple_multiplication(self, n: float) -> Matrix:
        x, y = self.order()
        new = Matrix.__empty_structure(x, y)

        for i in range(x):
            for j in range(y):
                new[i][j] = self.get(i, j) * n

        return Matrix(raw_data=new)

    def __complex_multiplication(self, other: Matrix) -> Matrix:
        if self.order()[1] != other.order()[0]:
            raise ValueError("The order of those matrices doesn't allow multiplication")

        x, y = self.order()[0], other.order()[1]
        new: List[List[float]] = Matrix.__empty_structure(x, y)

        for i in range(x):
            for j in range(y):
                local_sum: float = 0

                for k in range(other.order()[0]):
                    local_sum += self.get(i, k) * other.get(k, j)

                new[i][j] = local_sum

        return Matrix(raw_data=new)

    # === native operators ===
    def __str__(self) -> str:
        max_width: int = max(len(f'{x:.2f}') for row in self.raw_data for x in row)

        lines: List[str] = []
        for row in self.raw_data:
            formatted: List[str] = [f'{x:>{max_width}.2f}' for x in row]    
            lines.append(f'| {' '.join(formatted)} |')

        return '\n' + '\n'.join(lines)

    def __add__(self, other: Matrix) -> Matrix:
        return self.__basic_operation(other, float.__add__)

    def __sub__(self, other: Matrix) -> Matrix:
        return self.__basic_operation(other, float.__sub__)

    def __truediv__(self, other: float | int) -> Matrix:
        if other == 0:
            raise ZeroDivisionError('Cannot divide by zero')

        x, y = self.order()
        new: List[List[float]] = Matrix.__empty_structure(x, y)

        for i in range(x):
            for j in range(y):
                new[i][j] = self.get(i, j) / other

        return Matrix(raw_data=new)

    def __mul__(self, other: Matrix | float | int) -> Matrix:
        if type(other) in (float, int):
            return self.__simple_multiplication(other)
        else:
            return self.__complex_multiplication(other)

    def __pow__(self, power: int, modulo=None) -> Matrix:
        if power < 1:
            raise ValueError('Cannot raise matrices to powers less than 1')

        x, y = self.order()
        new = Matrix.of(self.raw_data)

        for _ in range(power - 1):
            new *= self

        return new

    def __eq__(self, other: Matrix) -> bool:
        return self.raw_data == other.raw_data
