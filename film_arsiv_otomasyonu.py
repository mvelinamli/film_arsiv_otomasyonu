class Icerik:
    def __init__(self, id, baslik, yapim_yili, puanlar):    
        self._id = id
        self._baslik = baslik
        self._yapim_yili = yapim_yili
        self._puanlar = puanlar

    def bilgi_getir(self):
        pass

class VeriYoneticisi:
    def __init__(self, dosya_adi):
        self.__dosya_adi = dosya_adi

    def kaydet(self, liste):    # içerik listesi
        pass

    def yukle(self, liste):
        pass

class Film(Icerik):
    def __init__(self, sure, butce):
        super().__init__(id, baslik, yapim_yili, puanlar)
        self._sure = sure
        self._butce = butce

    def bilgi_getir(self):
        pass

class Dizi(Icerik):
    def __init__(self, sezon_sayisi, devam_ediyor_mu, sezonlar):
        super().__init__(id, baslik, yapim_yili, puanlar)
        self.__sezon_sayisi = sezon_sayisi
        self.__devam_ediyor_mu = devam_ediyor_mu
        self.__sezonlar = sezonlar

    def sezon_ekle(self):
        pass

class Sezon:
    def __init__(self, sezon_no, bolumler):
        self.__sezon_no = sezon_no
        self.__bolumler = bolumler
        
class Bolum:
    def __init__(self, bolum_adi, sure):
        self.__bolum_adi = bolum_adi
        self.__sure = sure

class IPuanlanabilir:
    def __init__(self):
        pass
    
    def puan_ver(self, puan):
        pass

    def ortalama_puan_getir():
        pass