from .operations import add, subtract


def main():
    x, y = 10, 4
    print("add:", add(x, y))
    print("subtract:", subtract(x, y))


if __name__ == "__main__":
    main()
