import csv
import json
from pathlib import Path


def csv_to_json(input_path, output_path=None, encoding="utf-8", indent=2):
    """Read a CSV file and convert it to JSON.

    Args:
        input_path (str | Path): Path to the input CSV file.
        output_path (str | Path, optional): Path to write JSON output. If None,
            returns the JSON string.
        encoding (str): File encoding to use when reading/writing.
        indent (int): Number of spaces to use for pretty-printing JSON.

    Returns:
        str: JSON content if output_path is None, otherwise the written file path.
    """
    input_path = Path(input_path)

    with input_path.open("r", encoding=encoding, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    if output_path is None:
        return json.dumps(rows, indent=indent)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding=encoding) as json_file:
        json.dump(rows, json_file, indent=indent)

    return str(output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert a CSV file to JSON."
    )
    parser.add_argument("input_csv", help="Input CSV file path")
    parser.add_argument(
        "output_json",
        nargs="?",
        default=None,
        help="Optional output JSON file path. If omitted, prints JSON to stdout.",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Number of spaces to indent the output JSON.",
    )
    args = parser.parse_args()

    json_content = csv_to_json(args.input_csv, args.output_json, indent=args.indent)
    if args.output_json is None:
        print(json_content)
