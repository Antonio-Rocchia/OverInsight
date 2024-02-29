import datetime


class Message:

    def __init__(
        self,
        date: datetime.date,
        time: datetime.time,
        author: str,
        message: str,
    ) -> None:
        self.date = date
        self.time = time
        self.author = author
        self.content = message

    def __repr__(self) -> str:
        return f"Message(date={self.date}, time={self.time}, sender='{self.author}', message='{self.content}')"
