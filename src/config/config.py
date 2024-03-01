import datetime
import os
import sys
from pathlib import Path

import config.toml as _toml

_program_name = os.path.basename(sys.argv[0])

allowed_config_extensions = (".toml",)
allowed_parser_opts = ("whatsapp",)
allowed_ouput_opts = ("csv", "stdout")


class ConfigExeption(Exception):
    pass

def new_config(parser = ""):
    filter = Filter([],None,None,None,None)
    return Config(filter, parser, [])

def parse(config_fname):
    file_extension = Path(config_fname).suffix.lower()
    match file_extension:
        case ".toml":
            config = _toml.parse(config_fname)
        case _:
            raise ConfigExeption(
                f"{_program_name}: error: config format({file_extension}) not supported. try {_program_name} --help"
            )

    if "parser" in config:
        if isinstance(config["parser"], str):
            if not config["parser"] in allowed_parser_opts:
                raise ConfigExeption(
                    f"{_program_name}: error: the specified parser({config.get("parser")}) in not currently supported. try {allowed_parser_opts}"
                )
        else:
            raise ConfigExeption(
                f"{_program_name}: error: the specified parser preference is not correctly formatted. try {_program_name} --help"
            )
    else:
        config["parser"] = ""


    if "output" in config:
        if isinstance(config["output"], list):
            for o in config["output"]:
                if o not in allowed_ouput_opts:
                    raise ConfigExeption(
                        f"{_program_name}: error: the specified output preference ({o}) in not currently supported. try {allowed_parser_opts}"
                    )
        else:
            raise ConfigExeption(
                f"{_program_name}: error: the specified output preferences are not correctly formatted. try {_program_name} --help"
            )
    else:
        config["output"] = []


    if "filter" in config:
        if isinstance(config["filter"], dict):
            if "allowed_content" in config["filter"]:
                if isinstance(config["filter"]["allowed_content"], list):
                    for c in config["filter"]["allowed_content"]:
                        if not isinstance(c, str):
                            raise ConfigExeption(
                                f"{_program_name}: error: the specified content is not correctly formatted. (expected string).  try {_program_name} --help"
                            )
                else:
                    raise ConfigExeption(
                        f"{_program_name}: error: the specified filter preferences for allowed_content are not correctly formatted. try {_program_name} --help"
                    )
            else:
                config["filter"]["allowed_content"] = []
            if "start_date" in config["filter"] and not isinstance(config["filter"]["start_date"], datetime.date):
                raise ConfigExeption(
                    f"{_program_name}: error: the specified filter preferences for start_date are not correctly formatted. (expected date). try {_program_name} --help"
                )
            if "end_date" in config["filter"] and not isinstance(config["filter"]["end_date"], datetime.date):
                raise ConfigExeption(
                    f"{_program_name}: error: the specified filter preferences for end_date are not correctly formatted. (expected date). try {_program_name} --help"
                )
            if "start_time" in config["filter"] and not isinstance(config["filter"]["start_time"], datetime.time):
                raise ConfigExeption(
                    f"{_program_name}: error: the specified filter preferences for start_time are not correctly formatted. (expected date). try {_program_name} --help"
                )
            if "end_time" in config["filter"] and not isinstance(config["filter"]["end_time"], datetime.time):
                raise ConfigExeption(
                    f"{_program_name}: error: the specified filter preferences for end_time are not correctly formatted. (expected date). try {_program_name} --help"
                )
        else:
            raise ConfigExeption(
                f"{_program_name}: error: the specified filter preferences are not correctly formatted. try {_program_name} --help"
            )
    else:
        config["filter"] = {
            "allowed_content": []
        }

    parsed_filter = config["filter"]
    filter = Filter(parsed_filter.get("allowed_content"),
                    parsed_filter.get("start_date"),parsed_filter.get("start_time"),parsed_filter.get("end_date"),parsed_filter.get("end_time"))

    return Config(filter, config.get("parser"), config.get("output"))

class Filter():

    def __init__(self, allowed_content, start_date, start_time, end_date, end_time):
        self.allowed_content = allowed_content
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time

    def is_valid_content(self, content):
        if self.allowed_content:
            if content in self.allowed_content:
                return True
            else:
                return False
        else:
            return True

    def is_valid_date(self, date):
        if not (self.start_date or self.end_date):
            return True
        if self.start_date and self.end_date:
            if self.start_date <= date <= self.end_date:
                return True
        elif self.start_date and not self.end_date:
            if self.start_date <= date:
                return True
        elif self.end_date and not self.start_date:
            if date <= self.end_date:
                return True
        return False

    def is_valid_time(self, time):
        if not (self.start_time and self.end_time):
            return True
        if self.start_time and self.end_time:
            if self.start_time <= time <= self.end_time:
                return True
        elif self.start_time and not self.end_time:
            if self.start_time <= time:
                return True
        elif self.end_time and not self.start_time:
            if time <= self.end_time:
                return True
        return False


class Config():

    def __init__(self, filter, parser, output_opts):
        self.filter = filter
        self.parser = parser
        self.output = output_opts
