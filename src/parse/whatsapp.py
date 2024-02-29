import datetime
import re
import unicodedata

from domain import message

_date_pattern = (
    r"((?:(?:[0-2][0-9])|(?:3[0-1]))\/(?:(?:0[1-9])|(?:1[0-2]))\/(?:[0-9]{2}))"
)
_time_pattern = r"([0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,3})?)"
_sender_pattern = r"(.+?(?=: ))"
_msg_pattern = r"(.+)"
_begin_chat_msg_pattern = re.compile(
    r"^\[" + _date_pattern + r", " + _time_pattern + r"\] " + _sender_pattern,
    re.IGNORECASE,
)
_msg_parse_pattern = re.compile(
    r"^\["
    + _date_pattern
    + r", "
    + _time_pattern
    + r"\] "
    + _sender_pattern
    + r": "
    + _msg_pattern,
    re.IGNORECASE,
)


def _yield_entry(chat_fname):
    buffer = ""
    current_entry = ""
    with open(chat_fname, "r", encoding="utf-8") as chat:
        for line in chat:
            sanitized_line = "".join(
                ch for ch in line if unicodedata.category(ch)[0] != "C"
            )
            if _begin_chat_msg_pattern.search(sanitized_line):
                if not buffer:
                    buffer += f"{sanitized_line}"
                else:
                    current_entry = buffer
                    buffer = sanitized_line
                    yield current_entry
            else:
                if buffer:
                    buffer += f"\n{sanitized_line}"
        if buffer:
            yield buffer


def yield_message(chat_fname):
    for entry in _yield_entry(chat_fname):
        parsed_msg = _msg_parse_pattern.match(entry)
        if parsed_msg:
            date = datetime.datetime.strptime(parsed_msg.group(1), "%d/%m/%y").date()
            time = datetime.time.fromisoformat(parsed_msg.group(2))
            author = parsed_msg.group(3)
            content = parsed_msg.group(4)

            yield message.Message(date, time, author, content)
