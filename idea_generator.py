import os
import json
import urllib.request
import urllib.error

def load_config():
    """config.env dosyasından API anahtarını okur."""
    config_path = os.path.join(os.path.dirname(__file__), "config.env")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            for line in f:
                if line.startswith("GOOGLE_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return None

def generate_idea(text: str) -> str:
    """Verilen soruna Google Gemini Pro API kullanarak yazılımla çözülebilecek bir fikir üretir."""
    # Öncelik: Ortam değişkeni -> config.env
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") or load_config()
    
    if not api_key:
        return "HATA: Gemini API anahtarı (GOOGLE_API_KEY) bulunamadı. Lütfen config.env dosyasına ekleyin."

    try:
        # Gemini 2.5 Flash API URL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        prompt = f"""Bir pazar araştırmacısısın. Aşağıdaki kullanıcı mesajını analiz et ve:
1. Sorunu tanımla.
2. Bu sorunu çözecek yaratıcı ve gerçekçi bir yazılım/SaaS fikir öner.
3. Hedef kitleyi belirle.

Mesaj: {text}

Lütfen yanıtı şu JSON formatında ver (sadece JSON):
{{
  "Sorun_Tanimi": "...",
  "Firsat_Fikri": "...",
  "Hedef_Kitle": "..."
}}"""
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if "candidates" in result and len(result["candidates"]) > 0:
                raw_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                return raw_text
            return f"Gemini'den geçerli bir yanıt alınamadı: {json.dumps(result)}"
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Gemini API HTTP Hatası ({e.code}): {error_body}")
        return f"API Hatası ({e.code}): {error_body}"
    except Exception as e:
        print(f"Gemini API Hatası: {e}")
        return f"Analiz hatası: {str(e)}"

if __name__ == "__main__":
    print(generate_idea("I hate manually tracking my taxes as a freelancer."))
