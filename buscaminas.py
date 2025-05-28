#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 13:41:39 2025

@author: Estudiante
"""

import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    i:int = 0
    pos_ocupadas = []
    #Aca se generan las posiciones aleatorias donde van a haber minas
    while i < minas:
        nueva_pos = (random.randint(0, filas-1), random.randint(0, columnas-1))
        if nueva_pos not in pos_ocupadas:
            pos_ocupadas.append(nueva_pos)
            i += 1
    
    #Aca se genera la matriz considerando las posiciones anteriormente generadas!
    nueva_matriz:list[list[int]]  = []
    for c in range(columnas):
        nueva_fila: list[int] = []
        for f in range(filas):
            if (f,c) in pos_ocupadas:
                nueva_fila.append(-1)
            else:
                nueva_fila.append(0)
        nueva_matriz.append(nueva_fila)
    
    return nueva_matriz

#PREGUNTAR SI ES NECESARIO USARLA EN colocar_minas()
def es_matriz(m:list[list[int]]) -> bool:
    r:bool = True
    i:int = 0
    while i < (len(m)-1) and r:
        if len(m[i]) != len(m[i+1]):
            r = False
        i += 1
    return r

def chequear_alrededor(tablero: list[list[int]], f: int, c: int) -> int:
    contador: int = 0
    for x in range(f-1, f+2):
        for y in range(c-1, c+2):
            if x > -1 and y > -1 and x < len(tablero[0]) and y < len(tablero):
                if tablero[x][y] == -1:
                    contador += 1                
    return contador
        

def calcular_numeros(tablero: list[list[int]]) -> None:
    for c in range(len(tablero)):
        for f in range(len(tablero[c])):
            if tablero[f][c] != -1:
                tablero[f][c] = chequear_alrededor(tablero, f, c)
    return


def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    r: EstadoJuego = {}
    r['filas'] = filas
    r['columnas'] = columnas
    r['minas'] = minas
    r['tablero_visible'] = crear_tablero_visible_VACIO(filas, columnas)
    
    return {}

def crear_tablero_visible_VACIO(filas: int, columnas:int) -> list[list[str]]:
    res: list[list[str]] = []
    fila: list[str] = []
    for j in range(columnas): 
        fila.append(VACIO)
    for i in range(filas) :
        res.append(fila)
    
    return res 
        


def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    return [[]]


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def verificar_victoria(estado: EstadoJuego) -> bool:
    return True


def reiniciar_juego(estado: EstadoJuego) -> None:
    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False
