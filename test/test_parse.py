import unittest
from unittest.mock import mock_open, patch

from src.domain.message import Message
from src.parse import _whatsapp


class Test_Filter(unittest.TestCase):
    def test_read_filter(self):
        pass

    def test_is_allowed_date(self):
        pass

    def test_is_allowed_content(self):
        pass

    def test_is_allowed_sender(self):
        pass


class Test_Whatsapp(unittest.TestCase):
    def test_yield_entry_single_line(self):
        chat_log = [
            "[01/01/24, 06:31:29] Mario Ollare: 🧹",
            "[01/01/24, 11:49:02] Lorenzo Leppy: 🧹",
        ]

        mock_chat_log = "\n".join(chat_log)
        with patch("builtins.open", mock_open(read_data=mock_chat_log)):
            result = list(_whatsapp._yield_entry("file"))

        expected = [
            "[01/01/24, 06:31:29] Mario Ollare: 🧹",
            "[01/01/24, 11:49:02] Lorenzo Leppy: 🧹",
        ]
        self.assertEqual(result, expected)

    def test_yield_entry_empty_file(self):
        mock_chat_log = ""

        with patch("builtins.open", mock_open(read_data=mock_chat_log)):
            result = list(_whatsapp._yield_entry("file"))

        expected = []
        self.assertEqual(result, expected)

    def test_yield_entry_multi_line(self):
        chat_log = [
            "[01/01/22, 18:16:02] Agormitino: Ago",
            "Marco",
            "Leo",
            "Frapp",
            "[01/01/22, 18:16:12] Merk🥵: Invito Filippo",
            "[01/01/22, 18:20:00] Agormitino: Raga",
            "Marco",
            "",
            "Opzione:",
            "Frapp",
        ]

        mock_chat_log = "\n".join(chat_log)
        with patch("builtins.open", mock_open(read_data=mock_chat_log)):
            result = list(_whatsapp._yield_entry("file"))

        expected = [
            "[01/01/22, 18:16:02] Agormitino: Ago\nMarco\nLeo\nFrapp",
            "[01/01/22, 18:16:12] Merk🥵: Invito Filippo",
            "[01/01/22, 18:20:00] Agormitino: Raga\nMarco\n\nOpzione:\nFrapp",
        ]
        self.assertEqual(result, expected)

    def test_yield_message(self):
        pass
