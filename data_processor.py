import re

def preprocess(text: str) -> str:
    """Metni temizler, gereksiz boşlukları ve özel karakterleri çıkarır."""
    if not text:
        return ""
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text)
    cleaned_text = text.strip()
    return cleaned_text
