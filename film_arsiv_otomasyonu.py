import json
import os

class IPuanlanabilir():     #abstract class

    def puan_ver(self, puan): pass

    def ortalama_puan_getir(self): pass

class Icerik(IPuanlanabilir):
    def __init__(self, id, baslik, yapim_yili, puanlar=None):    
        self._id = id
        self._baslik = baslik
        self._yapim_yili = yapim_yili
        self._puanlar = puanlar if puanlar is not None else []

    def puan_ver(self, puan):
        if 0 <= puan <= 10:
            self._puanlar.append(puan)
        else:
            print("(!) Puan 0-10 arasında olmalıdır.")

    def ortalama_puan_getir(self):
        if not self._puanlar: return 0.0
        return sum(self._puanlar) / len(self._puanlar)


    def bilgi_getir(self): pass

    def veri_hazirla(self):
        return {
            "type": self.__class__.__name__,
            "id": self._id,
            "baslik": self._baslik,
            "yapim_yili": self._yapim_yili,
            "puanlar": self._puanlar
        }

class Film(Icerik):
    def __init__(self, id, baslik, yapim_yili, sure, butce, puanlar=None):
        super().__init__(id, baslik, yapim_yili, puanlar)
        self._sure = sure
        self._butce = butce

    def bilgi_getir(self):
        return (f"[FILM] {self._baslik} ({self._yapim_yili}) | "
                f"IMDB: {self.ortalama_puan_getir():.1f} | {self._sure} dk")

    def veri_hazirla(self):
        data = super().veri_hazirla()
        data.update({"sure": self._sure, "butce": self._butce})
        return data

class Bolum:
    def __init__(self, bolum_adi, sure):
        self._bolum_adi = bolum_adi
        self._sure = sure
    def veri_hazirla(self):
        return {"bolum_adi": self._bolum_adi, "sure": self._sure}

class Sezon:
    def __init__(self, sezon_no, bolumler=None):
        self._sezon_no = sezon_no
        self._bolumler = bolumler if bolumler is not None else []
    def bolum_ekle(self, bolum): self._bolumler.append(bolum)
    def veri_hazirla(self):
        return {"sezon_no": self._sezon_no, "bolumler": [b.veri_hazirla() for b in self._bolumler]}

class Dizi(Icerik):
    def __init__(self, id, baslik, yapim_yili, devam_ediyor_mu, puanlar=None):
        super().__init__(id, baslik, yapim_yili, puanlar)
        self._devam_ediyor_mu = devam_ediyor_mu
        self._sezonlar = []

    def sezon_ekle(self, sezon): self._sezonlar.append(sezon)

    def bilgi_getir(self):
        durum = "Devam Ediyor" if self._devam_ediyor_mu else "Final"
        return (f"[DIZI] {self._baslik} ({self._yapim_yili}) | "
                f"IMDB: {self.ortalama_puan_getir():.1f} | {len(self._sezonlar)} Sezon | {durum}")

    def veri_hazirla(self):
        data = super().veri_hazirla()
        data.update({"devam_ediyor_mu": self._devam_ediyor_mu, "sezonlar": [s.veri_hazirla() for s in self._sezonlar]})
        return data

class VeriYoneticisi:
    def __init__(self, dosya_adi):
        self.__dosya_adi = dosya_adi

    def kaydet(self, liste):
        try:
            ham_veri = [nesne.veri_hazirla() for nesne in liste]
            with open(self.__dosya_adi, "w", encoding="utf-8") as f:
                json.dump(ham_veri, f, ensure_ascii=False, indent=4)
            print(f"✔ Kayıt Başarılı: {self.__dosya_adi}")
        except Exception as e:
            print(f"✖ Kayıt Hatası: {e}")

    def yukle(self):
        try:
            with open(self.__dosya_adi, "r", encoding="utf-8") as f:
                ham_veri = json.load(f)
            
            yuklenen_liste = []
            for item in ham_veri:
                if item["type"] == "Film":
                    yuklenen_liste.append(Film(item["id"], item["baslik"], item["yapim_yili"], item["sure"], item["butce"], item["puanlar"]))
                elif item["type"] == "Dizi":
                    dizi = Dizi(item["id"], item["baslik"], item["yapim_yili"], item["devam_ediyor_mu"], item["puanlar"])
                    for s_data in item["sezonlar"]:
                        sezon = Sezon(s_data["sezon_no"])
                        for b_data in s_data["bolumler"]:
                            sezon.bolum_ekle(Bolum(b_data["bolum_adi"], b_data["sure"]))
                        dizi.sezon_ekle(sezon)
                    yuklenen_liste.append(dizi)
            return yuklenen_liste
        except FileNotFoundError:
            return []

class Uygulama:
    def __init__(self):
        self.dosya_adi = "arsiv.json"
        self.yonetici = VeriYoneticisi(self.dosya_adi)
        self.arsiv = self.yonetici.yukle()
        print("Veriler yükleniyor...")

    def ekran_temizle(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_goster(self):
        self.ekran_temizle()
        print("="*40)
        print("   FİLM & DİZİ ARŞİV SİSTEMİ")
        print("="*40)
        print(f"Mevcut İçerik Sayısı: {len(self.arsiv)}")
        print("-" * 40)
        print("1. Tüm İçerikleri Listele")
        print("2. Yeni Film Ekle")
        print("3. Yeni Dizi Ekle")
        print("4. Bir İçeriğe Puan Ver")
        print("5. Kaydet ve Çık")
        print("="*40)

    def listele(self):
        self.ekran_temizle()
        print("--- ARŞİVDEKİ İÇERİKLER ---")
        if not self.arsiv:
            print("Arşiv henüz boş.")
        else:
            for icerik in self.arsiv:
                # Polimorfizm: Film ise film bilgisi, dizi ise dizi bilgisi gelir
                print(icerik.bilgi_getir())
        input("\nDevam etmek için Enter'a basınız...")

    def film_ekle(self):
        self.ekran_temizle()
        print("--- YENİ FİLM EKLE ---")
        try:
            baslik = input("Film Adı: ")
            yil = int(input("Yapım Yılı: "))
            sure = int(input("Süre (dk): "))
            butce = float(input("Bütçe ($): "))
            
            # ID'yi otomatik atayalım (Listenin boyutu + 1)
            yeni_id = len(self.arsiv) + 1
            
            yeni_film = Film(yeni_id, baslik, yil, sure, butce)
            self.arsiv.append(yeni_film)
            print("\n✔ Film başarıyla eklendi!")
        except ValueError:
            print("\n✖ HATA: Yıl, süre veya bütçe için sayı girmelisiniz!")
        
        time.sleep(1.5)

    def dizi_ekle(self):
        self.ekran_temizle()
        print("--- YENİ DİZİ EKLE ---")
        try:
            baslik = input("Dizi Adı: ")
            yil = int(input("Yapım Yılı: "))
            devam_input = input("Dizi devam ediyor mu? (E/H): ").lower()
            devam_ediyor = True if devam_input == 'e' else False
            
            yeni_id = len(self.arsiv) + 1
            yeni_dizi = Dizi(yeni_id, baslik, yil, devam_ediyor)
            
            # Basitlik olması için şimdilik boş dizi ekliyoruz
            self.arsiv.append(yeni_dizi)
            print("\n✔ Dizi başarıyla eklendi!")
        except ValueError:
            print("\n✖ HATA: Lütfen sayısal değerleri doğru giriniz.")

    def puan_ver(self):
        self.ekran_temizle()
        print("--- PUAN VERME EKRANI ---")
        if not self.arsiv:
            print("Puan verilecek içerik yok.")

            return

        # İçerikleri numaralı listele
        for i, icerik in enumerate(self.arsiv):
            print(f"{i+1}. {icerik.bilgi_getir()}")
        
        try:
            secim = int(input("\nHangi içeriğe puan vereceksiniz? (Sıra No): ")) - 1
            if 0 <= secim < len(self.arsiv):
                puan = int(input("Puanınız (0-10): "))
                self.arsiv[secim].puan_ver(puan)
                print("✔ Puan kaydedildi.")
            else:
                print("✖ Geçersiz seçim.")
        except ValueError:
            print("✖ Hatalı giriş.")

    def calistir(self):
        """Uygulamanın ana döngüsü"""
        while True:
            self.menu_goster()
            secim = input("Seçiminiz (1-5): ")

            if secim == '1':
                self.listele()
            elif secim == '2':
                self.film_ekle()
            elif secim == '3':
                self.dizi_ekle()
            elif secim == '4':
                self.puan_ver()
            elif secim == '5':
                self.yonetici.kaydet(self.arsiv)
                print("Çıkış yapılıyor... İyi günler!")
                break
            else:
                print("Lütfen geçerli bir seçim yapınız.")

# --- PROGRAMI BAŞLAT ---
if __name__ == "__main__":
    app = Uygulama()
    app.calistir()