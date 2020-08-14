# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 23:25:39 2019

@author: Jiddy
"""

import numpy as np
import math
import time
import numpy as np
import math

class GA:

    def __init__(self,jumlahPopulasi, persenPopTerbaik, batasan, fungsi):
        self.fungsi = fungsi
        self.batasan = batasan
        self.jumlahPopulasi = jumlahPopulasi
        self.persenPopTerbaik = persenPopTerbaik
        self.probabilitas = 0.000001
        self.populasiX1 = []
        self.populasiX2 = []

    def populasiBaru(self):
        minimum = self.batasan[0]
        maximum = self.batasan[1]
        koefisien = np.random.random(self.jumlahPopulasi)
        populasi = minimum + (koefisien * (maximum - minimum))
        return populasi

    def inisiasiPopulasi(self):
        self.populasiX1 = self.populasiBaru()
        self.populasiX2 = self.populasiBaru()

    def populasiTerbaik(self):
        nilaiFungsi = self.fungsi(self.populasiX1, self.populasiX2)
        sortIndex = nilaiFungsi.argsort()
        jumlahPopTerbaik = int(len(nilaiFungsi) * self.persenPopTerbaik)
        bestX1 = self.populasiX1[sortIndex[:jumlahPopTerbaik]]
        bestX2 = self.populasiX2[sortIndex[:jumlahPopTerbaik]]
        return [bestX1, bestX2]
    
    def crossover(self):
        panjangPopX1 = len(self.populasiX1)
        panjangPopX2 = len(self.populasiX2)
        populasiX1Baru = np.zeros(self.jumlahPopulasi)
        populasiX2Baru = np.zeros(self.jumlahPopulasi)
        for i in range(panjangPopX1):
            populasiX1Baru[i] = self.populasiX1[i]
            populasiX2Baru[i] = self.populasiX2[i]
        i = panjangPopX1
        while i < self.jumlahPopulasi:
            randomPertamaX1 = self.populasiX1[np.random.randint(0 , panjangPopX1 - 1)]
            randomKeduaX1 = self.populasiX1[np.random.randint(0 , panjangPopX1 - 1)]
            avgX1 = (randomPertamaX1 + randomKeduaX1) / 2.0
            populasiX1Baru[i] = avgX1

            randomPertamaX2 = self.populasiX2[np.random.randint(0 , panjangPopX2 - 1)]
            randomKeduaX2 = self.populasiX2[np.random.randint(0 , panjangPopX2 - 1)]
            avgX2 = (randomPertamaX2 + randomKeduaX2) / 2.0
            populasiX2Baru[i] = avgX2

            i += 1
        self.populasiX1 = populasiX1Baru
        self.populasiX2 = populasiX2Baru
    
    def mutasi(self):
        minimalPopX1 = np.min(self.populasiX1)
        minimalPopX2 = np.min(self.populasiX2)
        self.populasiX1 += minimalPopX1 * (self.probabilitas * np.random.normal(0, 0.0001, len(self.populasiX1)))
        self.populasiX2 += minimalPopX2 * (self.probabilitas * np.random.normal(0, 0.0001, len(self.populasiX2)))
    
    def getIndexNilaiMinimal(self):
        nilai = self.fungsi(self.populasiX1, self.populasiX2)
        sortIndexNilai = nilai.argsort()
        indexNilaiMinimum = sortIndexNilai[0]
        return indexNilaiMinimum

    def minimum(self, iterasi):
        self.inisiasiPopulasi()
        bagianIterasi = 0.3
        i = 0
        while i < iterasi:
            tempPopulasi = self.populasiTerbaik()
            self.populasiX1 = tempPopulasi[0]
            self.populasiX2 = tempPopulasi[1]
            self.crossover()
            self.mutasi()
            i += 1
            if i > bagianIterasi*iterasi:
                self.probabilitas = 0.00000001
        indexNilaiMinimum = self.getIndexNilaiMinimal()
        return self.fungsi(self.populasiX1[indexNilaiMinimum], self.populasiX2[indexNilaiMinimum])

    def getTitikMinimum(self):
        indexNilaiMinimum = self.getIndexNilaiMinimal()
        minX1 = self.populasiX1[indexNilaiMinimum]
        minX2 = self.populasiX2[indexNilaiMinimum]
        return [minX1, minX2]
    
    def fitness(self, x1, x2):
        return math.pow(2,self.fungsi(x1,x2))

def fungsi1(x,y):
    sum1 = 0
    sum2 = 0
    for i in range(5):
        i += 1
        sum1 += i*np.cos((i+1)*x + 1)
        sum2 += i*np.cos((i+1)*y + 1)
    return -sum1*sum2


def fungsi2(x,y):
    return -(np.cos(x)*np.cos(y)*np.exp(-(x-math.pi)*(x-math.pi) - (y-math.pi)*(y-math.pi)))

jumlahPopulasi = 500
persenPopTerbaik = 0.8
batasan = [-100, 100]
iterasi = 100

hasil1 = GA(jumlahPopulasi, persenPopTerbaik, batasan, fungsi1)
hasil2 = GA(jumlahPopulasi, persenPopTerbaik, batasan, fungsi2)

print("Mencari nilai minimum...")
for i in range(20):
    print("Fungsi 1\n")
    nilaiMinimum = hasil1.minimum(iterasi)
    titikMinimum = hasil1.getTitikMinimum()
    fitness = hasil1.fitness(titikMinimum[0], titikMinimum[1])
    print("Nilai Minimum : ", nilaiMinimum, " pada titik", titikMinimum, ", Fitness = \n", fitness)
    print("\nFungsi 2\n")
    nilaiMinimum = hasil2.minimum(iterasi)
    titikMinimum = hasil2.getTitikMinimum()
    fitness = hasil2.fitness(titikMinimum[0], titikMinimum[1])
    print("Nilai Minimum : ", nilaiMinimum, " pada titik", titikMinimum, ", Fitness = \n", fitness)