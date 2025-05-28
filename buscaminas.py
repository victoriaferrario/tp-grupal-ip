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
    r['juego_terminado'] = False
    
    return r

def crear_tablero_visible_VACIO(filas: int, columnas:int) -> list[list[str]]:
    res: list[list[str]] = []
    fila: list[str] = []
    for j in range(columnas): 
        fila.append(VACIO)
    for i in range(filas) :
        res.append(fila)
    
    return res

# <-----
# def estado_valido(estado: EstadoJuego) -> bool:
#     return False
#
# def estructura_y_tipos_validos(estado: EstadoJuego) -> Bool:
#     ret = True
#     if estado['filas'] < 1 or estado['columnas'] < 1 or estado['minas'] < 1 or estado['minas'] < estado['filas']*estado['columnas']:
#         ret = False
#     return ret
# -----> Estas funciones solo sirven si fuesemos muy boludos y la cagaramos en otra funcion, se pueden implementar despues, son una paja (_)_)========D

def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    res: bool = True
    for f in range(tablero):
        for c in range(tablero[f]):
            if tablero[f][c] == -1:
                if tablero_visible[f][c] != VACIO and tablero_visible[f][c] != BANDERA:
                    res = False
            elif tablero[f][c] != tablero_visible[f][c]:
                res = False
    return res

def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    res = estado['tablero_visible']
    return res


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if (not estado['juego_terminado']) and (estado['tablero_visible'][fila][columna] == BANDERA or estado['tablero_visible'][fila][columna] == VACIO):
        if estado['tablero_visible'][fila][columna] == BANDERA:
            estado['tablero_visible'][fila][columna] = VACIO
        elif estado['tablero_visible'][fila][columna] == VACIO:
            estado['tablero_visible'][fila][columna] = BANDERA
    return


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if not estado['juego_terminado']:
        if estado['tablero'][fila][columna] == -1:
            estado['juego_terminado'] = True
            marcar_bombas(estado['tablero_visible'], estado['tablero'])
        else:
            if todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']):
                estado['juego_terminado'] = True
            #Falta implementar caminos_descubiertos() en el else!!!!! <---- IMPORTANTE
    return

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int) -> list[list[(int, int)]]:
    # la definicion de esta funcion es medio confusa, pero lo que tiene que hacer es devolver todas las posiciones que rodeen una posicion
    # que tenga valor 0hasta que llegue a una que tenga valor >0, es para que funcione como en el bucaminas que cuando tocas una celda
    # se rompen muchas porque no hay ninguna bomba alrededor, la peor explicacion del mundo, cualquier cosa pregunta !
    return [[]]


def marcar_bombas(tablero_visible: list[list[str]], tablero: list[list[str]]) -> None:
    for f in tablero_visible:
        for c in tablero_visible:
            if tablero[f][c] == -1:
                tablero_visible[f][c] = BOMBA
    return 


def verificar_victoria(estado: EstadoJuego) -> bool:
    return True


def reiniciar_juego(estado: EstadoJuego) -> None:
    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False
