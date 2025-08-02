import utils
from matrices import Matrix


def main() -> None:
    a: Matrix = Matrix.null(1, 2)

    print(a)


if __name__ == '__main__':
    utils.clear_terminal()
    main()
