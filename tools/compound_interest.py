import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate compound interest.")
    parser.add_argument("principal", type=float, help="Initial amount of money")
    parser.add_argument("annual_rate", type=float, help="Annual interest rate in percent")
    parser.add_argument("compounds_per_year", type=int, help="Number of compound periods per year")
    parser.add_argument("years", type=float, help="Total number of years")
    return parser.parse_args()


def main():
    args = parse_args()
    principal = args.principal
    rate = args.annual_rate / 100
    n = args.compounds_per_year
    t = args.years

    amount = principal * (1 + rate / n) ** (n * t)
    interest = amount - principal

    print(f"Final amount: ${amount:,.2f}")
    print(f"Interest earned: ${interest:,.2f}")


if __name__ == "__main__":
    main()
