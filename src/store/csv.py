import csv


def write_all(messages, filename = "insight.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Author", "Content"])
        for message in messages:
            writer.writerow(
                [message.date, message.time, message.author, message.content]
            )
