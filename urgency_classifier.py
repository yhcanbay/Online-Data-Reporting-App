def classify_urgency(text: str) -> str:
    """Metin içindeki kelimelere bakarak aciliyet seviyesini sınıflandırır."""
    high_keywords = ["acil", "kritik", "önemli", "çok önemli", "hemen", "ölümcül", "tehlike", "kriz", "çöktü", "çalışmıyor", "hata"]
    medium_keywords = ["ortalama", "zaman alabilir", "gecikme", "yavaş", "iyileştirme", "can sıkıcı", "rahatsız", "sorun"]
    
    text_lower = text.lower()
    
    if any(kelime in text_lower for kelime in high_keywords):
        return "Yüksek"
    if any(kelime in text_lower for kelime in medium_keywords):
        return "Orta"
        
    return "Düşük"
