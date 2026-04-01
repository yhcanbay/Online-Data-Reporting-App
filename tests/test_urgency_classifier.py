import unittest
from urgency_classifier import classify_urgency

class TestUrgencyClassifier(unittest.TestCase):
    def test_classify_urgency_high(self):
        self.assertEqual(classify_urgency("Bu acil bir durum."), "Yüksek")
        self.assertEqual(classify_urgency("Sistem çöktü, müdahale kritik!"), "Yüksek")

    def test_classify_urgency_medium(self):
        self.assertEqual(classify_urgency("Biraz zamanımız var ama sorun can sıkıcı."), "Orta")
        self.assertEqual(classify_urgency("Arayüzde iyileştirme yapılabilir."), "Orta")

    def test_classify_urgency_low(self):
        self.assertEqual(classify_urgency("Mümkünse renkleri değiştirelim."), "Düşük")
        self.assertEqual(classify_urgency("Herhangi bir sıkıntı yok, sadece ufak bir şey."), "Düşük")

if __name__ == '__main__':
    unittest.main()
