import parse.whatsapp


def yield_message(chat_fname, parser, filter):
    match parser:
        case "whatsapp":
            messages = parse.whatsapp.yield_message(chat_fname)
            # filter
            for m in messages:

                if (
                    filter.is_valid_content(m.content)
                    and filter.is_valid_date(m.date)
                    and filter.is_valid_time(m.time)
                ):
                    yield m
        case _:
            raise Exception("error: unkown parser")
