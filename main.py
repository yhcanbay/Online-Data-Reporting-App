import json
import sys
import os
import time
from scrapers import get_all_data
from idea_generator import generate_idea, load_config

def generate_report(keywords: list = None):
    """İnternetten veri çekip Gemini AI ile analiz eder ve dosyaya yazar."""
    print("Veriler toplanıyor (bu işlem yaklaşık 1 dakika sürebilir)...")
    posts = get_all_data(keywords=keywords)
    
    if not posts:
        print("Uygun veri bulunamadı. Lütfen farklı anahtar kelimeler deneyin.")
        return
        
    rapor_listesi = []
    
    print(f"Toplam {len(posts)} adet içerik analiz ediliyor...")
    
    for i, post in enumerate(posts):
        print(f"[{i+1}/{len(posts)}] Kayıt ediliyor: {post['kaynak']}")
        
        # AI Analizi geçici olarak devre dışı (Kullanıcı manuel yapacak)
        # raw_analysis = generate_idea(post['icerik'])
        analiz_sonucu = {
            "Sorun_Tanimi": "Beklemede (Manuel Analiz)",
            "Firsat_Fikri": "Beklemede (Manuel Analiz)",
            "Hedef_Kitle": "Beklemede (Manuel Analiz)"
        }
        
        # Sonucu formatla
        rapor_elemani = {
            "Kaynak": post["kaynak"],
            "URL": post["url"],
            "Orijinal_Mesaj": post['icerik'],
            "AI_Analizi": analiz_sonucu
        }
        rapor_listesi.append(rapor_elemani)
    
    # JSON Dosyasına Yaz
    with open("analiz_raporu.json", "w", encoding="utf-8") as f:
        json.dump(rapor_listesi, f, ensure_ascii=False, indent=4)
        
    # Okunabilir Markdown Raporu Yaz
    with open("analiz_raporu.md", "w", encoding="utf-8") as f:
        f.write("# Otomatik Pazar ve Fırsat Analiz Raporu\n")
        f.write(f"*Üretim Zamanı: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n")
        if keywords:
            f.write(f"**Arama Terimleri:** {', '.join(keywords)}\n\n")
        else:
            f.write("**Arama Terimleri:** Genel Arama (Standart Kalıplar)\n\n")
            
        for r in rapor_listesi:
            f.write(f"## Kaynak: {r['Kaynak']}\n")
            f.write(f"**URL:** [Link]({r['URL']})\n\n")
            
            ai = r.get("AI_Analizi", {})
            f.write("### Gemini AI Analizi\n")
            f.write(f"**1. Sorun Tanımı:**\n> {ai.get('Sorun_Tanimi', 'Tespit edilemedi.')}\n\n")
            f.write(f"**2. Fırsat Fikri (Çözüm Önerisi):**\n> {ai.get('Firsat_Fikri', 'Fikir üretilemedi.')}\n\n")
            f.write(f"**3. Hedef Kitle:**\n> {ai.get('Hedef_Kitle', 'Belirlenemedi.')}\n\n")
            f.write("---\n\n")

    print(f"\nAnaliz tamamlandı! '{len(rapor_listesi)}' adet içerik işlendi.")
    print("Sonuçlar 'analiz_raporu.json' ve 'analiz_raporu.md' dosyalarına kaydedildi.")

if __name__ == "__main__":
    # Komut satırından anahtar kelime alma
    # Örn: python main.py dental insurance
    keywords = sys.argv[1:] if len(sys.argv) > 1 else None
    
    # API Kontrolü
    if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") or load_config()):
        print("UYARI: GOOGLE_API_KEY bulunamadı. AI analizi çalışmayacaktır (config.env dosyasını kontrol edin).")
        
    generate_report(keywords=keywords)
