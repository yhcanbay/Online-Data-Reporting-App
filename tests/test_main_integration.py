import json
import unittest
from main import process_text_to_dict

class TestMainIntegration(unittest.TestCase):
    def test_process_text_to_dict(self):
        text = "Okul internet sistemi çöktü, öğrenciler ders çalışamıyor. Çok kritik!"
        data = process_text_to_dict(text)
        
        self.assertIn("Sorun_Tanimi", data)
        self.assertIn("Hedef_Kitle", data)
        self.assertIn("Firsat_Fikri", data)
        self.assertIn("Aciliyet_Seviyesi", data)
        
        self.assertEqual(data["Hedef_Kitle"], "Öğrenciler")
        self.assertEqual(data["Aciliyet_Seviyesi"], "Yüksek")

    def test_process_text_empty_input(self):
        result = process_text_to_dict("   ")
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
