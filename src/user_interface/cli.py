import parse.parse
import store.csv


def _default_output(messages):
    for m in messages:
        print(m)


def run(config, chat_log_fname):
    if not config.output:
        _default_output(
            parse.parse.yield_message(chat_log_fname, config.parser, config.filter)
        )
    else:
        for o in config.output:
            match o:
                case "stdout":
                    _default_output(
                        parse.parse.yield_message(
                            chat_log_fname, config.parser, config.filter
                        )
                    )
                case "csv":
                    store.csv.write_all(
                        parse.parse.yield_message(
                            chat_log_fname, config.parser, config.filter
                        )
                    )
