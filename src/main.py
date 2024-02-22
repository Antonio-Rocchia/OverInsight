#!/usr/bin/env python3
import argparse
import json
import os.path

import parse
import store


def _is_valid_file(fname):
    try:
        if not os.path.isfile(fname):
            raise argparse.ArgumentTypeError(f"{fname} is not a file")
        with open(fname, "r", encoding="utf-8") as _:
            pass  # Make sure you can open file
        return fname
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f"The file {fname} can't be opened")


def read_content_filter(fname):
    with open(fname, "r") as f:
        config = json.load(f)
    return config["valid_content"]


def main(parser):
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    messagge_app = args.message_app
    filer_file = args.content_filter

    content_filter = read_content_filter(filer_file)

    # Write all messages to CSV
    message_parser = None
    match messagge_app:
        case "whatsapp":
            message_parser = parse.whatsapp.yield_message

    store.csv.write_all(
        message_parser(input_file, content_filter),  # pyright: ignore
        output_file,
    )

    # Count occurrences of valid content for each author
    count = {}
    for message in message_parser(input_file, content_filter):  # pyright: ignore
        if message.author not in count:
            count[message.author] = {}
            for f in content_filter:
                count[message.author][f] = 0

        if message.content in content_filter:
            count[message.author][message.content] += 1

    print(count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="OverInsight: A Python tool for analyzing chat logs from popular messaging apps.",
        epilog="For more information, visit: https://github.com/Antonio-Rocchia/OverInsight",
    )
    parser.add_argument(
        "input_file",
        help="Path to the input file containing the exported chat logs.",
        metavar="INPUT_FILE",
        type=_is_valid_file,
    )
    parser.add_argument(
        "message_app",
        help="Messaging app that generated the log. This will be used to correctly parse the chat.",
        choices=["whatsapp"],
    )
    parser.add_argument(
        "content_filter",
        help="Path to JSON file containing the content filter",
        metavar="CONTENT_FILTER",
        type=_is_valid_file,
    )
    parser.add_argument(
        "-o",
        "--output_file",
        help="File name for the output file. Default is 'insight.csv'.",
        default="insight.csv",
    )

    main(parser)
