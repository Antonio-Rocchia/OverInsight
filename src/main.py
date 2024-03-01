#!/usr/bin/env python3
import argparse
import os.path
import sys

import config.config
import user_interface.cli
import user_interface.gui

_program_name = os.path.basename(sys.argv[0])


def _is_readable_file(fname):
    try:
        if not os.path.isfile(fname):
            raise argparse.ArgumentTypeError(f"{fname} is not a file")
        with open(fname, "r", encoding="utf-8") as _:
            pass  # Make sure you can open file
        return fname
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f"The file {fname} can't be opened")


def _is_readable_config(fname):
    _is_readable_file(fname)
    # Additional configuration format can be added
    if fname.endswith(config.config.allowed_config_extensions):
        return fname
    else:
        raise argparse.ArgumentTypeError(
            f"Incorrect file extension for config file. Currently supported expections are {config.config.allowed_config_extensions}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="OverInsight: A Python tool for analyzing chat logs from popular messaging apps.",
        epilog="For more information, visit: https://github.com/Antonio-Rocchia/OverInsight",
    )

    parser.add_argument(
        "--config",
        metavar="CONFIG_FILE",
        type=_is_readable_config,
        help="The path to the config file",
    )
    parser.add_argument(
        "chat_log",
        metavar="CHAT_LOG",
        nargs="?",
        type=_is_readable_file,
        help="The path to the chat log",
    )
    parser.add_argument(
        "--parser",
        metavar="MESSAGING_APP",
        choices=config.config.allowed_parser_opts,
        help="The name of the messaging app that generated the logs. Will override 'parser' if specified in the config file",
    )

    args = parser.parse_args()

    if args.chat_log:  # cli mode
        if not args.parser and not args.config:
            sys.exit(
                f"{_program_name}: error: A parser is needed to run the program. see {_program_name} -h"
            )

        if args.config:
            try:
                config_obj = config.config.parse(args.config)
            except config.config.ConfigExeption as e:
                sys.exit(str(e))

            if not args.parser and not config_obj.parser:
                sys.exit(
                    f"{_program_name}: error: A parser is needed to run the program. see {_program_name} -h"
                )
            elif args.parser:
                config_obj.parser = args.parser
        else:
            config_obj = config.config.new_config(args.parser)

        user_interface.cli.run(config_obj, args.chat_log)
    else:
        user_interface.gui.run(config.config.new_config())
