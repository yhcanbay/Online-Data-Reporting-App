def find_audience(text: str) -> str:
    """Metindeki anahtar kelimelere göre hedef kitleyi belirler."""
    text_lower = text.lower()
    
    # Basit anahtar kelime kuralları
    if any(word in text_lower for word in ["öğrenci", "okul", "ders", "sınav", "üniversite", "lise"]):
        return "Öğrenciler"
    elif any(word in text_lower for word in ["müşteri", "banka", "kart", "hesap", "alışveriş", "satın"]):
        return "Müşteriler"
    elif any(word in text_lower for word in ["çalışan", "mesai", "ofis", "maaş", "şirket", "patron"]):
        return "Çalışanlar"
    elif any(word in text_lower for word in ["hasta", "hastane", "doktor", "randevu", "ilaç", "sağlık"]):
        return "Hastalar"
    elif any(word in text_lower for word in ["çocuk", "ebeveyn", "anne", "baba", "oyuncak", "bebek"]):
        return "Ebeveynler"
    elif any(word in text_lower for word in ["öğretmen", "eğitimci"]):
        return "Öğretmenler"
    
    return "Genel Kullanıcılar"
