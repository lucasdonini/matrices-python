import utils
from matrices import Matrix


def main() -> None:
    a: Matrix = Matrix.of([
        [1, 2],
        [2, 1]
    ])
    
    b: Matrix = Matrix.of([
        [1, 0],
        [0, 1]
    ])

    print(a * b)


if __name__ == '__main__':
    utils.clear_terminal()
    main()
