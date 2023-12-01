"""Klasa, w ktorej mozna zrealizowac rozwiazanie Zadania 1"""

import uklad, wykresy
import iteracjaprosta, iteracjaseidela
import numpy as np

class Zadanie1:

    def __init__(self, sk = 1):
        """Konstruktor okreslajacy skale wektora poczatkowego"""
        self.skala = sk       # parametr skali
        self.n = 100          # wymiar macierzy
        self.norma = 0        # bede wykorzystywal norme kolumnowa
        self.k = 5            # liczba pomiarow dla jednej wartosci parametru
        
    def testy(self):
        """Testy wstepne"""
        # przeprowadzam dwa testowe eksperymenty dla wektorow o roznych normach
        # okreslam uklad rownan
        alfa1 = 0.1
        alfa2 = 2.7
        u1 = uklad.Uklad(wymiar = self.n)
        u2 = uklad.Uklad(wymiar = self.n)
        # losujemy uklad
        u1.losuj_uklad_symetryczny_dodatnio_okreslony(alfa1)
        u2.losuj_uklad_symetryczny_dodatnio_okreslony(alfa2)
        # rozwiazuje uklad z wykorzystaniem metody iteracji prostej
        test1 = iteracjaseidela.IteracjaSeidela(ukl = u1)
        test2 = iteracjaseidela.IteracjaSeidela(ukl = u2)
        # wyznaczam macierz D i wektor C
        test1.przygotuj()
        test2.przygotuj()
        # wyswietlam normy macierzy D
        u1.wypisz_normy_macierzy(macierz = test1.D)
        u2.wypisz_normy_macierzy(macierz = test2.D)

        # wykonuje iteracje do momentu, gdy norma roznicy kolejnych
        # przyblizen jest mniejsza niz eps = 0.0000001
        iter1 = test1.iteruj_twierdzenie(
            eps = 1e-10,
            norma = self.norma,
            wyswietlaj = 0)
        seria1 = test1.normy.copy()
        niedokl1 = test1.sprawdz_rozwiazanie(self.norma)
        iter2 = test2.iteruj_twierdzenie(
            eps = 1e-10,
            norma = self.norma,
            wyswietlaj = 0)
        seria2 = test2.normy.copy()
        niedokl2 = test2.sprawdz_rozwiazanie(self.norma)
        print(f"Liczba iteracji dla parametru alfa {alfa1}: {iter1}")
        print(f"Niedokladnosc rozwiazania: {niedokl1}")
        print(f"Liczba iteracji dla parametru alfa {alfa2}: {iter2}")
        print(f"Niedokladnosc rozwiazania: {niedokl2}")
        wykres_test = wykresy.Wykresy()
        wykres_test.badaj_zbieznosc(
            tytul = "Zbieznosc norm dlaparametrów afla o roznej skali",
            opis_OY = "Normy przyblizen",
            dane1 = seria1,
            opis1 = f"alfa = {alfa1}",
            dane2 = seria2,
            opis2 = f"alfa = {alfa2}"
        )
        
    def badaj_zbieznosc(self, epsilon = 1e-7):
        """Badam zbieznosc metody iteracji prostej"""
        # ustalam zbior parametrow
        # zmieniam je w skali logarytmicznej
        param = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
        # okreslam uklad rownan
        u1 = uklad.Uklad(wymiar = self.n)
        # dla kazdej wartosci parametru przeprowadzam po k testow
        # i wyswietlam wartosci wybranych charakterystyk eksperymentu
        sr_liczba_iteracji = []
        sr_norma_macierzy = []
        sr_alfa = []
        sr_niedokladnosc = []
        for sk in param:
            norma_macierzy = 0.0
            liczba_iteracji = 0.0
            niedokladnosc = 0.0
            alfa = 0
            iteracje = 0
            while iteracje < self.k:
                # losujemy uklad
                u1.losuj_uklad_symetryczny_dodatnio_okreslony(alfa=sk)
                # rozwiazuje uklad z wykorzystaniem metody iteracji prostej
                test1 = iteracjaseidela.IteracjaSeidela(ukl = u1)
                # wyznaczam macierz D i wektor C
                test1.przygotuj()
                # obliczam norma macierzy D
                norma_D = u1.norma_macierzy(
                        typ = self.norma,
                        macierz = test1.D
                    )
    
                # wykonuje iteracje do momentu, gdy norma roznicy kolejnych
                # przyblizen jest mniejsza niz zadany eps
                iter = test1.iteruj_twierdzenie(
                    eps = epsilon,
                    norma = self.norma,
                    wyswietlaj = 0)
                niedokl = test1.sprawdz_rozwiazanie(norma = self.norma)
                if iter == 0:
                    # jezeli nie mozna bylo wykonac iteracji
                    # nalezy powtorzyc pomiar
                    continue
                else:
                    # jezeli eksperyment udalo sie przeprowadzic
                    # agregujemy charakterystyki
                    norma_macierzy += norma_D
                    niedokladnosc += niedokl
                    liczba_iteracji += iter
                    alfa += sk
                    iteracje += 1
            # obliczam srednie wartosci charakterystyk
            sr_norma_macierzy.append(norma_macierzy/self.k)
            sr_liczba_iteracji.append(liczba_iteracji/self.k)
            sr_alfa.append(alfa/self.k)
            sr_niedokladnosc.append(niedokladnosc/self.k)
        # wypisujemy srednie charakterystyki
        print("alfa \t \t ||D|| \t     Iteracje   Niedkoladnosc")
        print("------"*9)
        for i in range(len(param)):
            wyniki = f"{sr_alfa[i]:.2e} \t"
            wyniki += f"{sr_norma_macierzy[i]:.6f} \t"
            wyniki += f"{sr_liczba_iteracji[i]:.2f} \t"
            wyniki += f"{sr_niedokladnosc[i]:.6e} \n"
            print(wyniki)
            