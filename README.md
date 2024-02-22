# OverInsight

OverInsight: A Python tool for analyzing chat logs from popular messaging apps, tracking specified messages. 

## Description

OverInsight is a Python tool designed to analyze chat logs from various messaging apps, including WhatsApp, Telegram, and others*. It meticulously identifies specified valid messages, whether they're emojis, words, or sentences, and tallies their occurrences. Each message must precisely match a valid message to be counted. Users have the option to save parsed messages in CSV format, allowing for further analysis with other tools. Additionally, OverInsight provides insights into message frequency per user.

*Please note that, at present, OverInsight exclusively supports parsing WhatsApp logs.

## Getting Started

### Dependencies

* python 3.6

### Installing

```sh
git clone https://github.com/Antonio-Rocchia/OverInsight.git
```

### Executing program

### Usage

```sh
usage: OverInsight.py [-h] [-o OUTPUT_FILE] INPUT_FILE {whatsapp} CONTENT_FILTER

OverInsight: A Python tool for analyzing chat logs from popular messaging apps.

positional arguments:
  INPUT_FILE            Path to the input file containing the exported chat logs.
  {whatsapp}            Messaging app that generated the log. This will be used to correctly parse the chat.
  CONTENT_FILTER        Path to JSON file containing the content filter

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File name for the output file. Default is 'insight.csv'.

For more information, visit: https://github.com/Antonio-Rocchia/OverInsight
```

#### Content filter
```json
{
  "valid_content": [
    "😀",
    "😂",
    "Hello",
    "Hello world",
  ]
}
```

### Exporting: Whatsapp guide

#### Android:

* Open a chat/group chat
* Tap on three dots on the top right
* Tap "More"
* Choose "Export chat"
* Choose "Without Media"

#### iOS

* Open a chat/group chat
* Tap on contact name/group name on the top to see the details
* Scroll down to find "Export Chat" menu
* Choose "Without Media"

## Authors

[Antonio Rocchia](https://github.com/Antonio-Rocchia)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

* [PetengDedet/WhatsApp-Analyzer](https://github.com/PetengDedet/WhatsApp-Analyzer)
