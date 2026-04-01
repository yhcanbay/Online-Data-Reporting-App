import unittest
from audience_finder import find_audience

class TestAudienceFinder(unittest.TestCase):
    def test_find_audience_students(self):
        self.assertEqual(find_audience("Bu okul öğrencileri için bir sorun."), "Öğrenciler")
        self.assertEqual(find_audience("Üniversite sınavı stresi çok yüksek"), "Öğrenciler")

    def test_find_audience_customers(self):
        self.assertEqual(find_audience("Bankacılıkta müşteri memnuniyetsizliği"), "Müşteriler")
        self.assertEqual(find_audience("Kredi kartı limiti yetersiz"), "Müşteriler")

    def test_find_audience_workers(self):
        self.assertEqual(find_audience("Maaşlar yatmadı, şirket zor durumda"), "Çalışanlar")

    def test_find_audience_general(self):
        self.assertEqual(find_audience("Uygulama arayüzü çok karmaşık"), "Genel Kullanıcılar")

if __name__ == '__main__':
    unittest.main()
