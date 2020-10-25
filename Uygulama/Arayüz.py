from tkinter import Button, Tk, Frame, Label, Text, W, N, S, E, WORD, END, HORIZONTAL
from tkinter.ttk import Progressbar, Style
from PIL import ImageTk

import tkinter.messagebox as msg
from eMagaza import VeriCek
import time as t
from LSTM import Model
 
class DuyguAnalizi:
    def __init__(self):
        self.pencere = Tk()
        
        self.pencere.iconbitmap('emotion.ico')
        self.pencere.title("Duygu Analizi")
        self.pencere.geometry('425x300')
        self.pencere.resizable(0, 0)
        
        photo = ImageTk.PhotoImage(file="rsz_amazon.jpg")
        label = Label(image=photo, borderwidth=0)
        label.image = photo
        label.pack(side = "top", pady = 0)
        
        self.cerceve = Frame(self.pencere)
        self.cerceve.pack(pady=10)

        self.cerceve.configure(background="#515C8B")
        self.pencere.configure(background="#515C8B")
                              
        s = Style()
        s.theme_use("default")
        s.configure("x.Horizontal.TProgressbar", thickness=5)
        
        Label(self.cerceve, text="Ürün Adresi: ", fg="white", bg="#535C8B").grid(row=1, column=0, sticky=W)
        self.progress = Progressbar(self.pencere, style="x.Horizontal.TProgressbar", orient = HORIZONTAL,length = 245, mode = 'determinate') 
        self.progress.pack()
        
        self.url = Text(self.cerceve, width=30, height=1, wrap=WORD, bd=1)
        self.url.grid(row=2, column=0, sticky = S + N + E + W)
        
        self.Analiz = Button(self.cerceve, width=7, height=1, text='Analiz', command= self.tahmin)
        self.Analiz.grid(row=3, column=0, padx=0, pady=8, sticky=E)

        self.pencere.mainloop()
    
    def progressbar(self): 
        self.progress['value'] = 0

        self.progress['value'] = 30
        self.pencere.update_idletasks() 
        t.sleep(1)
      
        self.progress['value'] = 60
        self.pencere.update_idletasks() 
        t.sleep(1)
      
        self.progress['value'] = 90
        self.pencere.update_idletasks() 
        t.sleep(1)
        
        self.progress['value'] = 100
        
    def tahmin(self):
        if self.url.get(1.0,END).strip() == "":
            msg.showwarning("Uyarı","Lütfen Gerekli Alanı Doldurun!")
        elif ".com" not in self.url.get(1.0,END):
            msg.showerror("Hata","Lütfen Uygun Bir Adres Girin!")
        else:
            try:
                gorusler = VeriCek.Veri(url = self.url.get(1.0,END))
                if len(gorusler) == 0:
                    msg.showerror("Hata","Girilen Adreste Veri Bulunamadı!")
                else:
                    self.progressbar()
                    sonuc = Model.Analiz(gorusler)        
                    msg.showinfo("Bilgi","Olumluluk: Yüzde %.2f" % (sonuc))
                    self.progress['value'] = 0
                
            except IOError:
                msg.showerror("Hata",'Lütfen Adresinizi "https://www..." Formunda Yazın.')

DuyguAnalizi()