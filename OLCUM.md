# Tokenizer v1 — tokenizer

Ayarlar: kök_min=100, ek_min=100, bütün=0. Yeni token: **32,202** ({'ingilizce korunan': 27867, 'yedek kök': 17454, 'yedek zincir': 4778, 'kök': 18655, 'ek': 5404, 'kesme işaretli ek': 127, 'bütün bırakılan sık kelime': 0}); gömme tablosuna +31,959 satır (+65 milyon parametre; ilk 243 token Qwen'in boş satırlarına oturdu).

Bölünme kaynağı: {'altın (UD train)': 22831, 'Zemberek tanımıyor': 186723, 'kök sıklığı önceliği': 229288, 'bağlam (derlem)': 84393}

| | BOUN kök bütün | BOUN sınır tam | IMST kök bütün | IMST sınır tam | parça/kelime |
|---|---|---|---|---|---|
| Qwen3.5 (olduğu gibi) | %56.3 | %44.4 | %56.0 | %43.7 | 2.08 |
| **v1 (işaretli)** | %91.7 | %90.2 | %92.3 | %90.8 | 1.62 |
| v1: kök bütün **veya** yalnız geçerli ek sınırından bölünmüş (temiz·lik) | %96.3 | – | %96.5 | – | – |

UD test kelimelerinin tabloda bulunma oranı: BOUN %96.7, IMST %96.7

Tatoeba TR/EN token oranı: Qwen 1.28× → v1 **1.07×**

Geri dönüş (decode(encode(metin)) == metin): %100.0

İngilizce cümle Qwen ile birebir aynı: işaretlemeden %99.6, işaretleyici açıkken %99.5

İngilizce kod (transformers/trainer.py) birebir aynı: işaretlemeden False, işaretleyici açıkken False

### v1'de kökü hâlâ bölünen örnekler

soya (kök: soy) → so·ya; çıkarmış (kök: çıkar) → çık·armış; bağlı (kök: bağlı) → bağ·lı; yürüyor (kök: yürü) → yür·üyor; küldür (kök: küldür) → kü·ld·ür; uçarlar (kök: uçar) → uç·arlar; Postmodernleşen (kök: postmodernleş) → Post·modern·leşen; dönüştü (kök: dönüş) → dön·üştü; hoşça (kök: hoşça) → hoş·ça; Sonradan (kök: sonradan) → Sonra·dan; gerilimler (kök: gerilim) → geri·limler; Firkateyni (kök: firkateyn) → F·irk·ate·yn·i; Duş (kök: duş) → Du·ş; parfümsüz (kök: parfümsüz) → parfüm·süz; temizlik (kök: temizlik) → temiz·lik; klitoris (kök: klitoris) → kl·itoris; anüse (kök: anüs) → an·üs·e; dışkılık (kök: dışkılık) → dışkı·lık; patlatılmaz (kök: patla) → pat·lat·ılmaz; Adjani (kök: Adjani) → Adj·ani; Parasız (kök: parasız) → Para·sız; pulsuzduk (kök: pulsuz) → puls·uz·duk; adlı (kök: adlı) → ad·lı; girebilirdik (kök: gir) → g·ire·bil·irdik; Nazik (kök: nazik) → Naz·ik; rahatsız (kök: rahatsız) → rahat·sız; uygulamayı (kök: uygulama) → uygula·mayı; kurallaştırmamıştır (kök: kurallaş) → kur·alla·şt·ı·rm·am·ıştır; görevlileriyle (kök: görevli) → görev·lileriyle; Değerlendirme (kök: değerlen) → Değer·lendirme
