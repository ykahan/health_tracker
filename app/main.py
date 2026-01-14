import argparse


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    hello_parser = subparsers.add_parser("hello")

    args = parser.parse_args()

    if args.command == "hello":
        print("Health tracker is alive.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
