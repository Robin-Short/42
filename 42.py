#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:03:37 2021

@author: robins
"""

import pyglet
import quarantaduelib as ql

window = pyglet.window.Window(1280, 720)#(fullscreen = True)
WIDTH, HEIGHT = window.get_size()

SCEGLI_A = 1
SCEGLI_B = 2
SCEGLI_OP = 3

I = 100 # Dimensione lineare di un quadratino

from pyglet.window import mouse
from pyglet.window import key
from pyglet import image
from pyglet import shapes

inGame = True
schema = ql.Schema(4,2)

quadrati = [image.load('q1.png'),  image.load('q2.png'),  image.load('q3.png'),  image.load('q4.png'),
            image.load('q5.png'),  image.load('q6.png'),  image.load('q7.png'),  image.load('q8.png'),
            image.load('q9.png'),  image.load('q10.png'), image.load('q11.png'), image.load('q12.png'),
            image.load('q13.png'), image.load('q14.png'), image.load('q15.png'), image.load('q16.png')]

quadratiCliccati = [image.load('qq1.png'),  image.load('qq2.png'),  image.load('qq3.png'),  image.load('qq4.png'),
                    image.load('qq5.png'),  image.load('qq6.png'),  image.load('qq7.png'),  image.load('qq8.png'),
                    image.load('qq9.png'),  image.load('qq10.png'), image.load('qq11.png'), image.load('qq12.png'),
                    image.load('qq13.png'), image.load('qq14.png'), image.load('qq15.png'), image.load('qq16.png')]


scegliOp = image.load('operazioni.png')

indietro = image.load('back.png')

win = image.load('win.png')

def ind2pos(i, j):
    x = j * I + I
    y = i * I + I
    return x, y

def pos2ind(x, y):
    x -= I; y -= I;
    i = y // I
    j = x // I
    if (i < 0) or (j < 0) or (i >= schema.size[0]) or (j >= schema.size[1]):
        return None, None
    return i, j

sezioneA = None; sezioneB = None;
storicoMosse = []

fase = SCEGLI_A

@window.event
def on_draw():
    window.clear()
    global inGame
    if inGame:
        # Stampa valori
        for k in range(len(schema.sezioni)):
            sez = schema.sezioni[k]
            celle = sez.getCelle()
            for cella in celle:
                i, j = cella
                x, y = ind2pos(i, j)
                if sezioneA == sez or sezioneB == sez:
                    quadratiCliccati[k].blit(x, y)
                else:
                    quadrati[k].blit(x, y)
                x += I / 2; y += I / 2;
                val = pyglet.text.Label(str(sez.valore),font_name='Times New Roman',font_size=42,
                                        x = x, y = y, anchor_x='center', anchor_y='center')
                val.color = (0,0,0,128)
                val.draw()
        # Stampa operazioni
        if fase == SCEGLI_OP:
            scegliOp.blit((2 + schema.size[1]) * I, I)
        # Stampa back
        if schema.pilaMosse != [] or fase == SCEGLI_OP:
            indietro.blit(I, 6 * I)
        # Stampa Vittoria
        if schema.checkWin():
            win.blit((2 + schema.size[1]) * I, I)
    else:
        pass
@window.event
def on_mouse_press(x, y, button, modifiers):
    global fase, sezioneA, sezioneB
    if fase == SCEGLI_A:
        i, j = pos2ind(x, y)
        if i != None:
            fase = SCEGLI_B
            for sez in schema.sezioni:
                celle = sez.getCelle()
                for cella in celle:
                    if cella == (i, j):
                        sezioneA = sez
                        break
                if sezioneA != None:
                    break
        if I <= x <= 2 * I and 6 * I <= y <= 7 * I and schema.pilaMosse != []:
            schema.indietro()
    elif fase == SCEGLI_B:
        if sezioneA != None:
            i, j = pos2ind(x, y)
            if i != None:
                for sez in schema.sezioni:
                    celle = sez.getCelle()
                    for cella in celle:
                        if cella == (i, j):
                            sezioneB = sez
                            break
                    if sezioneB != None:
                        break
        if sezioneB == None:
            sezioneA = None
            fase = SCEGLI_A
        else:
            if ql.checkMonoAdiacenza(sezioneA, sezioneB)[0]:
                fase = SCEGLI_OP
            else:
                sezioneA = None
                sezioneB = None
                fase = SCEGLI_A
    elif fase == SCEGLI_OP:
        op = None
        m, n = schema.size
        if x >= (2 + n) * I and x <= (3 + n) * I:
            if y >= I and y <= 2 * I:
                op = ql.PER
            elif y > 2 * I and y <= 3 * I:
                op = ql.PIU
        elif x > (3 + n) * I and x <= (4 + n) * I:
            if y >= I and y <= 2 * I:
                op = ql.MENO
            elif y > 2 * I and y <= 3 * I:
                op = ql.DIVISO
        if op != None:
            schema.muovi(sezioneA, sezioneB, op)
            sezioneA = None
            sezioneB = None
            fase = SCEGLI_A
        if I <= x <= 2 * I and 6 * I <= y <= 7 * I and schema.pilaMosse != []:
            fase = SCEGLI_A
            sezioneA = None; sezioneB = None
            schema.indietro()
    
@window.event
def on_mouse_release(x, y, button, modifiers):
    pass
    
pyglet.app.run()
