import requests
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords

class VeriCek:    
    def Veri(url):
        url_yeni = ""
        sayac = 0
        for i in url:
            url_yeni += i
            if i == "/":
                sayac += 1
            if sayac == 6:
                break
        url_yeni = url_yeni.replace("dp/","product-reviews/")
        url = url_yeni + "ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        liste = []
        sayfa = 1
        sonraki_sayfa = ""
        while True:
            sonraki_sayfa = url + str(sayfa)
            req = requests.get(sonraki_sayfa, headers=headers)
            soup = BeautifulSoup(req.content,"html.parser")
            durak = "mevcut seçimleriniz ile eşleşen yorum bulunamadı"
            durak_kontrol = soup.find_all("span", attrs={"class" : "a-size-medium"})
            if str(durak) not in str(durak_kontrol):
                texts = soup.find_all("span",attrs={"data-hook" : "review-body"})
                for i in range(len(texts)):
                    liste.append([texts[i].find('span').text.strip()])
                sayfa += 1
            else:
                break

        yorumlar_temiz = []
        etkisizler = list(stopwords.words('Turkish'))
        for text in liste:
            x = str(text)
            #x = text.lower()
            #x = re.sub(r'\W', ' ', str(x))
            x = re.sub(r'\<a href', ' ', x)
            x = re.sub(r'&amp;', '', x)
            x = re.sub(r'<br />', ' ', x)
            """x = re.sub(r"^\s+|\s+$", "", x)
            x = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', x)
            x = re.sub(r'\'', ' ', x)
            x = re.sub('\s{2,}', ' ', x)
            x = re.sub(r'\s+[a-zA-Z]\s+', ' ', x)
            x = re.sub(r'\^[a-zA-Z]\s+', ' ', x)
            x = re.sub(r'\s+', ' ', x, flags=re.I)
            x = re.sub(r'^b\s+', '', x)"""
            x = x.split()
            x = [word for word in x if word not in etkisizler]
            x = ' '.join(x)
            yorumlar_temiz.append(x)
        
        #print(len(yorumlar_temiz))
        return yorumlar_temiz