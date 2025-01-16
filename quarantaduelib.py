#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:37:11 2021

@author: robins
"""
import numpy as np
import random as rn
#import sys
from termcolor import cprint

colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

PIU = 1
MENO = 2
PER = 3
DIVISO = 4

debug = False

def unisciSezioni(s0, s1):
    L = checkMonoAdiacenza(s0, s1)[1]
    return Sezione(s0.partenza, s0.lati + [L] + s1.lati, s0.valore)


def biseziona(s,l):
    partenza1 = l[0]; partenza2 = l[1];
    s.lati.remove(l)
    lati1 = []; lati2 = [];
    passeggia({partenza1}, s.lati, lati1)
    passeggia({partenza2}, s.lati, lati2)
    return partenza1, partenza2, lati1, lati2
     
def passeggia(celle, latiUsufruibili, latiUsati):
    for l in latiUsufruibili:
        for cella in celle:
            if l[0] in celle or l[1] in celle:
                latiUsufruibili.remove(l)
                latiUsati.append(l)
                celle.add(l[1]) if l[0] in celle else celle.add(l[0])
                passeggia(celle, latiUsufruibili, latiUsati)
                break

def dividiSezioni(sezione, lato, operazione):
    valore = sezione.valore
    # Calcola Struttura
    partenza1, partenza2, lati1, lati2 = biseziona(sezione, lato)
    # Calcola Valori
    mossa = str(lato[0])
    if operazione == PIU:
        mossa += '+'
        valore1 = rn.randint(0, valore)
        valore2 = valore - valore1 # Così che valore1 + valore2 = valore
    elif operazione == MENO:
        mossa += '-'
        valore2 = rn.randint(0, valore)
        valore1 = valore + valore2 # Così che valore1 - valore2 = valore
    elif operazione == PER:
        mossa += '*'
        if valore == 0:
            if rn.randint(0,1):
                valore1 = 0; valore2 = rn.randint(1,42);
            else:
                valore2 = 0; valore1 = rn.randint(1,42);
        else:
            divisori = []
            for i in range(1, valore + 1):
                if valore % i == 0:
                    divisori += [i]
            valore2 = divisori[rn.randint(0, len(divisori) - 1)]
            valore1 = valore // valore2 # Così che valore1 * valore2 = valore
    elif operazione == DIVISO:
        mossa += ':'
        valore2 = 1
        if valore != 0:
            if int(1000 / valore) > 0:
                valore2 = rn.randint(1, int(1000 / valore))
            valore1 = valore * valore2 # Così che valore1 / valore2 = valore
        else:
            valore1 = 0;
            valore2 = rn.randint(1, 42)
    mossa += str(lato[1])
    return Sezione(partenza1, list(lati1), valore1), Sezione(partenza2, list(lati2), valore2), mossa    

def checkMonoAdiacenza(s1, s2):
    adiacenti = 0; L = None;
    celle1 = s1.getCelle(); celle2 = s2.getCelle();
    if celle1 == celle2:
        return False, None
    for c1 in celle1:
        for c2 in celle2:
            x = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
            if x == 1:
                adiacenti += 1
                L = (c1, c2)
    return (True, L) if adiacenti == 1 else (False, None)

def costruzioneRic(sezioni, mosse):
    for i in range(len(sezioni)):
        N = len(sezioni[i].lati)
        s = sezioni[i]
        if N < 1: # Se s è solo una cella
            pass
        else:
            sezioni.remove(s)
            # Scegli un lato
            j = rn.randint(0, N - 1)
            L = s.lati[j]
            # Scegli un'operazione
            O = rn.randint(1,4)
            # Dividi
            s1, s2, mossa = dividiSezioni(s, L, O)
            mosse.insert(0, mossa)
            sezioni.append(s1); sezioni.append(s2);
            costruzioneRic(sezioni, mosse)
            
def cercaSoprasezione(sezioni, sezione):
    celle = sezione.getCelle()
    for sez in sezioni:
        sopraCelle = sez.getCelle()
        for sopraCella in sopraCelle:
            for cella in celle:
                if cella == sopraCella:
                    return sez
    return None

class Operazione:
    def __init__(self, op, s0, s1):
        self.operazione = op
        self.verso = [s0, s1] # s0, s1 sezioni, op in [1,2,3,4,0]

class Sezione:
    def __init__(self, partenza = (0,0), lati = [], valore = 42):
        self.partenza = partenza # cella
        self.lati = lati # coppie di celle, del tipo ((i, j), (l, k))
        self.valore = valore
        
    def getCelle(self):
        celle = {self.partenza}
        for l in self.lati:
            celle.add(l[0])
            celle.add(l[1])
        return celle
    
    def contieneCella(self, i, j):
        celle = self.getCelle()
        for cella in celle:
            if cella == (i, j):
                return True
        return False
    
    def __str__(self):
        txt = 'Valore = ' + str(self.valore) + '.\nCelle:\n'
        celle = self.getCelle()
        for cella in celle:
            txt += str(cella) + '\n'
        return txt
    
class Schema:
    def __init__(self, m = 2, n = 4):
        self.size = (m, n)
        self.sezioni = []
        for i in range(m):
            for j in range(n):
                self.sezioni += [Sezione((i,j))]
        #self.operazioni = []
        self.creaSezioni((n * m) // 4) #Scelta arbitraria
        self.numeroSezioniGarantite = len(self.sezioni)
        self.unaSoluzione = []
        #self.stampa() #Debug
        self.costruzione()
        self.pilaMosse = []
    
    def creaSezioni(self, k):
        N = len(self.sezioni)
        itMax = 100 # Vedi se puoi dare un numero più sensato
        while N > k and itMax:
            itMax -= 1
            #Scelgo sezione
            i = rn.randint(0,N-1);
            s1 = self.sezioni.pop(i); N -= 1;
            #Scelgo adiacente
            adiacenti = []
            for j in range(N):
                s2 = self.sezioni[j]
                if checkMonoAdiacenza(s1, s2)[0]:
                    adiacenti += [j]
            M = len(adiacenti)
            if M >= 1:
                k = rn.randint(0, M - 1)
                s2 = self.sezioni.pop(adiacenti[k]); N -= 1;
                s = unisciSezioni(s1, s2)
                self.sezioni += [s]; N += 1;
            else:
                self.sezioni += [s1]; N += 1;
                
    def costruzione(self):
        costruzioneRic(self.sezioni, self.unaSoluzione)

    def stampa(self):
        caratteri = 5
        M = np.zeros((self.size), dtype = 'int')
        for s in self.sezioni:
            valore = s.valore
            celle = s.getCelle()
            for cella in celle:
                M[cella] = valore
        N = len(self.sezioni)
        for i in range(self.size[0]):
            print('\n')
            for j in range(self.size[1]):
                el = str(M[i, j])
                m = caratteri - len(el)
                el += ' ' * m
                colorBack = 'on_grey'
                color = 'grey'
                for l in range(min(8, N)):
                    if self.sezioni[l].contieneCella(i, j):
                        color = colors[(l + 5) % 8]
                        colorBack = 'on_' + colors[l]
                        break
                cprint(el, color, colorBack, end = '')
        #print('\nUna soluzione con ' + str(self.numeroSezioniGarantite) + ' sezioni è data da:\n')
        #for mossa in self.unaSoluzione:
        #    print('\n' + mossa)
            
    def muovi(self, s1, s2, op):
        muovi, L = checkMonoAdiacenza(s1, s2)
        if not muovi:
            return
        v1 = s1.valore; v2 = s2.valore;
        if op == PIU:
            v = v1 + v2
        elif op == MENO:
            v = v1 - v2
        elif op == PER:
            v = v1 * v2
        elif op == DIVISO:
            if v2 == 0 or v1 % v2:
                return
            v = v1 // v2
        s = Sezione(s1.partenza, s1.lati + [L] + s2.lati, v)
        self.pilaMosse += [{'a':s1, 'b':s2, 'aOPb': s, 'operazione':op}]
        self.sezioni.remove(s1); self.sezioni.remove(s2);
        self.sezioni.append(s);
        if debug:
            print('Ho mosso')
            for mossa in self.pilaMosse:
                print('a:'); print(mossa['a']);
                print('b:'); print(mossa['b']);
                print('opertazione:', end = ' ')
                if mossa['operazione'] == PIU:
                    print('+')
                elif mossa['operazione'] == PER:
                    print('*')
                elif mossa['operazione'] == MENO:
                    print('-')
                elif mossa['operazione'] == DIVISO:
                    print(':')
        
    def indietro(self):
        if self.pilaMosse == []:
            pass
        else:
            mossa = self.pilaMosse.pop()
            self.sezioni.remove(mossa['aOPb'])
            self.sezioni.append(mossa['a'])
            self.sezioni.append(mossa['b'])
#            s1 = mossa['a']; val1 = s1.valore;
#            s2 = mossa['b']; val2 = s2.valore;
#            app, lato = checkMonoAdiacenza(s1, s2)
#            sezione = cercaSoprasezione(self.sezioni, s1)
#            operazione = mossa['operazione']
#            s1, s2, app = dividiSezioni(sezione, lato, operazione)
#            s1.valore = val1; s2.valore = val2;
#            self.sezioni += [s1, s2]
            if debug:
                print('Sono tornato indietro')
                for mossa in self.pilaMosse:
                    print('a:'); print(mossa['a']);
                    print('b:'); print(mossa['b']);
                    print('opertazione:', end = ' ')
                    if mossa['operazione'] == PIU:
                        print('+')
                    elif mossa['operazione'] == PER:
                        print('*')
                    elif mossa['operazione'] == MENO:
                        print('-')
                    elif mossa['operazione'] == DIVISO:
                        print(':')   
                        
    def scopriSoluzione(self):
        for mossa in self.unaSoluzione:
            c1 = (int(mossa[1]),int(mossa[4]))
            c2 = (int(mossa[8]),int(mossa[11]))
            op = mossa[6]
            if op == '+':
                op = PIU
            elif op == '-':
                op = MENO
            elif op == '*':
                op = PER
            elif op == ':':
                op = DIVISO
            s1 = None; s2 = None;
            for sezione in self.sezioni:
                if sezione.contieneCella(c1[0], c1[1]):
                    s1 = sezione
                elif sezione.contieneCella(c2[0], c2[1]):
                    s2 = sezione
            input('Premi invio per fare una mossa:')
            self.muovi(s1, s2, op)
            self.stampa()
            
    def checkWin(self):
        for sez in self.sezioni:
            if sez.valore != 42:
                return False
        return True
        
#schema = Schema(4,4)
#schema.stampa()
#schema.scopriSoluzione()
#schema.indietro()


