import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate total test coverage.")
    parser.add_argument("generated", type=float, help="Number of test cases generated")
    parser.add_argument("written", type=float, help="Number of unit test cases written")
    return parser.parse_args()


def main():
    args = parse_args()
    generated = args.generated
    written = args.written

    if written == 0:
        print("Error: written unit test cases must be greater than zero.")
        return

    coverage = generated / written
    print(f"Test coverage: {coverage:.2f}")


if __name__ == "__main__":
    main()
