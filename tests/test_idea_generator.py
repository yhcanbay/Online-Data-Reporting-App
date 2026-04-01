import unittest
from unittest.mock import patch, MagicMock
from idea_generator import generate_idea

class TestIdeaGenerator(unittest.TestCase):
    @patch("idea_generator.os.environ.get")
    def test_generate_idea_no_api_key(self, mock_env_get):
        mock_env_get.return_value = None
        text = "Uygulama çok yavaş çalışıyor."
        result = generate_idea(text)
        self.assertTrue("taslak çözüm" in result.lower())
        self.assertTrue(text[:50] in result)

    @patch("idea_generator.urllib.request.urlopen")
    @patch("idea_generator.os.environ.get")
    def test_generate_idea_with_api_key(self, mock_env_get, mock_urlopen):
        mock_env_get.return_value = "test_key"
        
        # Mocking the context manager for urlopen
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"choices": [{"message": {"content": "\\u00d6nbellekleme sistemi eklenebilir."}}]}'
        
        mock_context_manager = MagicMock()
        mock_context_manager.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_context_manager
        
        result = generate_idea("Sistem yavaş.")
        self.assertEqual(result, "Önbellekleme sistemi eklenebilir.")
        mock_urlopen.assert_called_once()

if __name__ == '__main__':
    unittest.main()
