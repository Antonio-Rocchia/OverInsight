import datetime
import re
import unicodedata
from typing import List

from . import message


def yield_message(chat_fname: str, content_filter: List[str] = []):
    date_pattern = (
        r"((?:(?:[0-2][0-9])|(?:3[0-1]))\/(?:(?:0[1-9])|(?:1[0-2]))\/(?:[0-9]{2}))"
    )
    time_pattern = r"([0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,3})?)"
    sender_pattern = r"(.+?(?=: ))"
    msg_pattern = r"(.+)"
    with open(chat_fname, "r", encoding="utf-8") as chat:
        begin_chat_msg_pattern = re.compile(
            r"^\[" + date_pattern + r", " + time_pattern + r"\] " + sender_pattern,
            re.IGNORECASE,
        )
        msg_parse_pattern = re.compile(
            r"^\["
            + date_pattern
            + r", "
            + time_pattern
            + r"\] "
            + sender_pattern
            + r": "
            + msg_pattern,
            re.IGNORECASE,
        )
        while line := chat.readline():
            sanitized_line = "".join(
                ch for ch in line if unicodedata.category(ch)[0] != "C"
            )
            if begin_chat_msg_pattern.search(sanitized_line):
                current_entry_fptr = chat.tell()
                # Handle multiple line entries
                while next_line := chat.readline():
                    sanitized_next_line = "".join(
                        ch for ch in next_line if unicodedata.category(ch)[0] != "C"
                    )
                    if begin_chat_msg_pattern.search(sanitized_next_line):
                        # Put file one line back
                        chat.seek(current_entry_fptr)
                        break
                    else:
                        sanitized_line += f"\n{sanitized_next_line}"
            else:
                continue  # skip bad entries
            parsed_msg = msg_parse_pattern.match(sanitized_line)
            if parsed_msg:
                date = datetime.datetime.strptime(
                    parsed_msg.group(1), "%d/%m/%y"
                ).date()
                time = datetime.time.fromisoformat(parsed_msg.group(2))
                author = parsed_msg.group(3)
                content = parsed_msg.group(4)

                # Apply content filter
                if content in content_filter:
                    yield message.Message(date, time, author, content)
                else:
                    continue  # Skip unwanted messages
            else:
                continue  # skip bad entries
