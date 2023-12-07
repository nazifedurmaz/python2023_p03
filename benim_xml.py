import os
import xml.etree.ElementTree as ET
from tkinter import Tk, Button, Label, Toplevel, Text, Scrollbar, END
from PIL import Image, ImageTk

class ResimGosterici:
    def __init__(self, ana_pencere, xml_dosya_yolu):
        self.ana_pencere = ana_pencere
        self.ana_pencere.title("Kütüphanem")

        self.xml_dosya_yolu = xml_dosya_yolu
        self.kitap_listesi = self._kitaplari_oku()

        self.suanki_kitap_indeks = 0
        self.resim = None
        self.photo_image = None

        self._arayuz_olustur()
        self._resmi_goster()

    def _kitaplari_oku(self):
        kitap_listesi = []
        tree = ET.parse(self.xml_dosya_yolu)
        root = tree.getroot()

        for kitap_elem in root.findall('.//eser'):
            kitap = {}
            kitap['dcTitle'] = kitap_elem.find('dcTitle').text
            kitap['dcSubject'] = kitap_elem.find('dcSubject').text
            kitap['dcContributor'] = kitap_elem.find('dcContributor').text
            kitap['dcDescributor'] = kitap_elem.find('dcDescributor').text
            kitap['dcLanguage'] = kitap_elem.find('dcLanguage').text
            kitap['dcIdentifier'] = kitap_elem.find('dcIdentifier').text
            kitap['dcImage'] = kitap_elem.find('dcImage').text

            kitap_listesi.append(kitap)

        return kitap_listesi

    def _resmi_goster(self):
        resim_yolu = os.path.join(os.path.dirname(self.xml_dosya_yolu), self.kitap_listesi[self.suanki_kitap_indeks]['dcImage'])
        img = Image.open(resim_yolu)
        img = img.resize((350, 350))
        self.photo_image = ImageTk.PhotoImage(img)

        self.resim_label.config(image=self.photo_image)
        self.resim_label.photo = self.photo_image

        # Kitap bilgilerini doğrula ve güncelle
        bilgi_text = (f"Başlık: {self.kitap_listesi[self.suanki_kitap_indeks]['dcTitle']}\n"
                      f"Konu: {self.kitap_listesi[self.suanki_kitap_indeks]['dcSubject']}\n"
                      f"Yazar: {self.kitap_listesi[self.suanki_kitap_indeks]['dcContributor']}\n"
                      f"Açıklama:\n{self._alt_satira_indir(self.kitap_listesi[self.suanki_kitap_indeks]['dcDescributor'])}\n"
                      f"Dil: {self.kitap_listesi[self.suanki_kitap_indeks]['dcLanguage']}\n"
                      f"Kimlik: {self.kitap_listesi[self.suanki_kitap_indeks]['dcIdentifier']}")
        self.bilgi_text.delete(1.0, END)
        self.bilgi_text.insert(END, bilgi_text)

    def _alt_satira_indir(self, metin, karakter_sayisi=50):
        if len(metin) > karakter_sayisi:
            # Belirli bir karakter sayısında ise bir alt satıra geç
            return '\n'.join([metin[i:i+karakter_sayisi] for i in range(0, len(metin), karakter_sayisi)])
        else:
            return metin

    def _sonraki_kitabi_goster(self):
        self.suanki_kitap_indeks = (self.suanki_kitap_indeks + 1) % len(self.kitap_listesi)
        self._resmi_goster()

    def _onceki_kitabi_goster(self):
        self.suanki_kitap_indeks = (self.suanki_kitap_indeks - 1) % len(self.kitap_listesi)
        self._resmi_goster()

    def _listele_penceresi(self):
        listele_pencere = Toplevel(self.ana_pencere)
        listele_pencere.title("Kitap Listesi")

        text_widget = Text(listele_pencere, wrap='none', width=80, height=20, font=('Times New Roman', 14))
        text_widget.pack(side='left', fill='both', expand=True)

        scrollbar = Scrollbar(listele_pencere, command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.config(yscrollcommand=scrollbar.set)

        for kitap in self.kitap_listesi:
            text_widget.insert(END, f"\n\nBaşlık: {kitap['dcTitle']}\n"
                                     f"Konu: {kitap['dcSubject']}\n"
                                     f"Yazar: {kitap['dcContributor']}\n"
                                     f"Açıklama:\n{self._alt_satira_indir(kitap['dcDescributor'])}\n"
                                     f"Dil: {kitap['dcLanguage']}\n"
                                     f"Kimlik: {kitap['dcIdentifier']}")

    def _arayuz_olustur(self):
        self.resim_label = Label(self.ana_pencere)
        self.resim_label.pack()

        self.bilgi_text = Text(self.ana_pencere, wrap='none', width=50, height=10, font=('Times New Roman', 12))
        self.bilgi_text.pack()

        onceki_button = Button(self.ana_pencere, text="Geri", command=self._onceki_kitabi_goster)
        onceki_button.pack(side="left")

        sonraki_button = Button(self.ana_pencere, text="İleri", command=self._sonraki_kitabi_goster)
        sonraki_button.pack(side="right")

        listele_button = Button(self.ana_pencere, text="Listele", command=self._listele_penceresi)
        listele_button.pack(side="bottom")


if __name__ == "__main__":
    xml_dosya_yolu = "proje_files/kitap.xml"
    root = Tk()
    fotograf = ResimGosterici(root, xml_dosya_yolu)
    root.mainloop()


