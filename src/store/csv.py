import csv

from parse.message import Message


def write_all(messages: Message, filename):
    """Writes a list of messages

    Args:
        messages ([TODO:parameter]): [TODO:description]
        filename ([TODO:parameter]): [TODO:description]
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Author", "Content"])
        for message in messages:
            writer.writerow(
                [message.date, message.time, message.author, message.content]
            )
