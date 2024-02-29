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

    parser.add_argument("--gui", action="store_true", help="Enable GUI mode")
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

    if not args.gui and not (args.config or args.chat_log or args.parser):
        parser.print_help()
        sys.exit()
    elif not args.chat_log and not args.gui:
        sys.exit(
            f"{_program_name}: error: specify a chat_log or run in gui mode. see {_program_name} -h"
        )

    if args.config:
        config_obj = config.config.parse(args.config)
        if args.parser:
            config_obj.parser = args.parser
        else:
            if not config_obj.parser:
                raise argparse.ArgumentTypeError(
                    f"Specify a valid parser for the chat log via a config file or with the --parser flag. see {_program_name} -h"
                )
    else:
        if args.parser:
            config_obj = config.config.new_config(args.parser)
        elif not args.gui:
            raise argparse.ArgumentTypeError(
                f"Specify a valid parser for the chat log via a config file or with the --parser flag. see {_program_name} -h"
            )
        else:
            config_obj = config.config.new_config()

    if args.gui:
        user_interface.gui.run(config_obj, args.chat_log)
    else:
        user_interface.cli.run(config_obj, args.chat_log)
