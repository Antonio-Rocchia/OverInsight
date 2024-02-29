import tomllib


def parse(config_fname):
    with open(config_fname, "rb") as cf:
        config = tomllib.load(cf)
        return config
