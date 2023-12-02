"""Klasa, w ktorej mozna zrealizowac rozwiazanie Zadania 2"""

import uklad, wykresy
import iteracjaprosta, iteracjaseidela, pagerank, potegowa
import numpy as np

class Zadanie2:

    def __init__(self):
        """Konstruktor"""
        self.k = 5            # liczba pomiarow dla jednej wartosci parametru
        self.norma = 1
        self.n = 30
        self.eps = 1e-2

    def testy(self):
        """Testy wstepne"""
        rank = pagerank.PageRank(self.n)
        rank.losuj(0.4)
        print(f"Srednia liczba linkow: {rank.srednia_liczba_linkow()}")
        rank.przygotuj_do_iteracji()
        test1 = iteracjaprosta.IteracjaProsta(rank.v)
        test1.przygotuj()
        iter1 = test1.iteruj_roznica(eps=self.eps, norma=self.norma)
        test1.wypisz_rozwiazanie(iter)
        niedokladnosc1 = test1.sprawdz_rozwiazanie(norma=self.norma)
        print("\nIteracja Prosta")
        rank.ranking_po_iteracji(test1.X)
        print("Liczba iteracji: ", iter1)
        print("Niedokladnosc: ", niedokladnosc1)

        print("\nMetoda Potegowa")
        test2 = potegowa.Potegowa(rank.u)
        iter2 = test2.iteruj_roznica(eps=self.eps)
        test2.wypisz_rozwiazanie(iter2)
        niedokladnosc2 = test2.sprawdz_rozwiazanie(norma=self.norma)
        rank.ranking(test2.y)
        print("Liczba iteracji: ", iter2)
        print("Niedokladnosc: ", niedokladnosc2)

        return 0
        
    def badaj_zbieznosc(self):
        """Badam zbieznosc metody iteracji seidela"""
        # ustalam zbior parametrow
        param = [1e-13,1e-12, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2,1e-1]
        sr_liczba_iteracji1 = []
        sr_liczba_iteracji2 = []
        sr_niedokladnosc1 = []
        sr_niedokladnosc2 = []
        for cur_eps in param:
            niedokladnosc1 = 0.0
            niedokladnosc2 = 0.0
            iteracje1 = 0
            iteracje2 = 0
            iteracje = 0
            while iteracje < self.k:
                rank = pagerank.PageRank(self.n)
                rank.losuj(0.4)
                rank.przygotuj_do_iteracji()
                test1 = iteracjaprosta.IteracjaProsta(rank.v)
                test1.przygotuj()
                iter1 = test1.iteruj_roznica(eps=cur_eps, norma=self.norma)

                niedokl1 = test1.sprawdz_rozwiazanie(norma=self.norma)
                rank.ranking_po_iteracji(test1.X)

                test2 = potegowa.Potegowa(rank.u)
                iter2 = test2.iteruj_roznica(eps=cur_eps)
                niedokl2 = test2.sprawdz_rozwiazanie(norma=self.norma)
                rank.ranking(test2.y)
                
                niedokladnosc1 += niedokl1
                niedokladnosc2 += niedokl2
                
                iteracje += 1
                iteracje1 += iter1
                iteracje2 += iter2
            sr_liczba_iteracji1.append(iteracje1/self.k)
            sr_liczba_iteracji2.append(iteracje2/self.k)
            sr_niedokladnosc1.append(niedokladnosc1/self.k)
            sr_niedokladnosc2.append(niedokladnosc2/self.k)
        print("Epsilon  Iteracje  Niedkoladnosc")
        print("------"*9)
        for i in range(len(param)):
            wyniki1 = f"{param[i]} \t"
            wyniki1 += f"{sr_liczba_iteracji1[i]} \t"
            wyniki1 += f"{sr_niedokladnosc1[i]:.6e} \n"
            print(wyniki1)

        print("Epsilon  Iteracje  Niedkoladnosc")
        print("------"*9)
        for i in range(len(param)):
            wyniki2 = f"{param[i]} \t"
            wyniki2 += f"{sr_liczba_iteracji2[i]} \t"
            wyniki2 += f"{sr_niedokladnosc2[i]:.6e} \n"
            print(wyniki2)

        return 0