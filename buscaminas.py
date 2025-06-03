#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 13:41:39 2025

@author: Estudiante
"""

import random
from typing import Any
from typing import TextIO
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
    for f in range(filas):
        nueva_fila: list[int] = []
        for c in range(columnas):
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
            if x > -1 and y > -1 and x < len(tablero) and y < len(tablero[0]):
                if tablero[x][y] == -1:
                    contador += 1                
    return contador

def calcular_numeros(tablero: list[list[int]]) -> None:
    for f in range(len(tablero)):
        for c in range(len(tablero[f])):
            if tablero[f][c] != -1:
                tablero[f][c] = chequear_alrededor(tablero, f, c)
    return


def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    r: EstadoJuego = {}
    r['filas'] = filas
    r['columnas'] = columnas
    r['minas'] = minas
    r['tablero_visible'] = crear_tablero_visible_VACIO(filas, columnas)
    
    y = colocar_minas(filas, columnas, minas)
    calcular_numeros(y)
    r['tablero'] = y
    r['juego_terminado'] = False

    return r


def crear_tablero_visible_VACIO(filas: int, columnas:int) -> list[list[str]]:
    res: list[list[str]] = []
    for i in range(filas):
        fila: list[str] = []
        for j in range(columnas): 
            fila.append(VACIO)
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
    for f in range(len(tablero)):
        for c in range(len(tablero[f])):
            if tablero[f][c] == -1:
                if tablero_visible[f][c] != VACIO and tablero_visible[f][c] != BANDERA:
                    res = False
            elif str(tablero[f][c]) != tablero_visible[f][c]:
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


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if not estado['juego_terminado']:
        if estado['tablero'][fila][columna] == -1 and estado['tablero_visible'][fila][columna] != BANDERA:
            marcar_bombas(estado['tablero_visible'], estado['tablero'])
            estado['juego_terminado'] = True
        else:
            aux: list[tuple[int,int]] = caminos_descubiertos(estado['tablero'], estado['tablero_visible'], fila, columna)
            # print(aux)
            for (f,c) in aux:
                estado['tablero_visible'][f][c] = str(estado['tablero'][f][c])
            if todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']):
                estado['juego_terminado'] = True
    return

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int) -> list[list[(int, int)]]:
    camino: list[tuple[int,int]] = [] 
    return recursion_caminos_descubiertos(tablero, tablero_visible, f, c, camino)

def recursion_caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int, camino: list[list[(int, int)]]) -> list[list[(int, int)]]:
    if tablero_visible [f][c] != BANDERA :
        camino.append((f,c))
        if chequear_alrededor(tablero, f, c) == 0 : 
            for x in range(f-1, f+2):
                for y in range(c-1, c+2):
                    if x > -1 and y > -1 and x < len(tablero) and y < len(tablero[0]) and ((x,y) not in camino):
                        recursion_caminos_descubiertos(tablero, tablero_visible, x, y, camino)
    return camino

def marcar_bombas(tablero_visible: list[list[str]], tablero: list[list[str]]) -> None:
    for f in range (len(tablero_visible)):
        for c in range (len(tablero_visible[f])):
            if tablero[f][c] == -1:
                tablero_visible[f][c] = BOMBA
    return 

def verificar_victoria(estado: EstadoJuego) -> bool:
    return todas_celdas_seguras_descubiertas(estado['tablero'],estado['tablero_visible'])

def reiniciar_juego(estado: EstadoJuego) -> None:
    estado = crear_juego(estado['filas'], estado['columnas'], estado['minas'])
    # filas = estado['filas'] 
    # columnas = estado['columnas'] 
    # minas = estado['minas']
    # estado['tablero_visible'] = crear_tablero_visible_VACIO(filas, columnas)
    # y = colocar_minas(filas, columnas, minas)
    # calcular_numeros(colocar_minas(filas, columnas, minas))
    # estado['tablero'] = calcular_numeros(colocar_minas(filas, columnas, minas))

    # estado['juego_terminado'] = False

    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    archivo_tablero: TextIO = open(generar_ruta(ruta_directorio, 'tablero.txt'), 'w')
    archivo_tablero_visible: TextIO  = open(generar_ruta(ruta_directorio, 'tablero_visible.txt'),'w')
    
    archivo_tablero.write(tableros_a_strings(estado, estado['tablero']))
    archivo_tablero_visible.write(tableros_a_strings(estado, estado['tablero_visible']))
    
    archivo_tablero.close()
    archivo_tablero_visible.close()
    return

def tableros_a_strings(estado: EstadoJuego, tablero:list[list[any]]) -> str: 
    res: str = str()
    for f in range (len(tablero)):
        for c in range(len(tablero[0])):
            if tablero == estado['tablero_visible']:
                if tablero[f][c] == BANDERA: 
                    res += '*'
                else: 
                    if tablero[f][c] == VACIO: 
                        res += '?'
                    else:  res += tablero[f][c]
            else: 
                res += str(tablero[f][c])
                
            if c == len(tablero[0])-1: #último elemento de la fila 
                res += '\n'
            else: res += ','
    return res 

def generar_ruta(ruta_directorio:str, nombre_archivo:str):
    return os.path.join(ruta_directorio,nombre_archivo)

def string_a_matriz(archivo: TextIO) -> list[list[int]]:
    texto: list[str] = archivo.readlines()
    m: list[list[int]] = []
    for l in texto:
        char: str = ''
        linea: list = []
        for c in range(len(l)):
            if l[c] == ',' or c == len(l)-1 :
                if c == len(l)-1:
                    char += l[c]
                linea.append(char)
                char = ''
            else:
                char += l[c]
        m.append(linea)
    return m

def tablero_valido(archivo: TextIO) -> bool:
    res: bool = True
    hayBomba: bool = False
    tablero = string_a_matriz(archivo)
    for f in range(len(tablero)):
        if '-1' in tablero[f]:
            hayBomba = True
        for i in range(len(tablero[f])):
            if tablero[f][i] != '-1':
                if tablero[f][i] != str(chequear_alrededor(tablero, f, i)):
                    res = False
    return (res and hayBomba)

def tablero_visible_valido(archivo_tablero_visible: TextIO, archivo_tablero: TextIO) -> bool:
    res: bool = True
    tablero_visible = string_a_matriz(archivo_tablero_visible)
    tablero = string_a_matriz(archivo_tablero)
    for f in range(len(tablero_visible)):
        for c in range(len(tablero_visible[f])):
            if tablero_visible[f][c] != '*' and tablero_visible[f][c] != '?' and tablero_visible[f][c] != tablero[f][c]:
                res = False
    
    return res


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    res: bool = True
    
    if os.path.exists(generar_ruta(ruta_directorio, 'tablero.txt')) and os.path.exists(generar_ruta(ruta_directorio, 'tablero_visible.txt')):
        archivo_tablero: TextIO = open(generar_ruta(ruta_directorio, 'tablero.txt'), 'r')
        archivo_tablero_visible: TextIO  = open(generar_ruta(ruta_directorio, 'tablero_visible.txt'),'r')

        res = dimensiones_validas(estado, archivo_tablero) and dimensiones_validas(estado, archivo_tablero_visible) and tablero_valido(archivo_tablero) and tablero_visible_valido(archivo_tablero_visible, archivo_tablero)
        
        archivo_tablero.close()
        archivo_tablero_visible.close()
    else: 
        res = False 
    return res

def quitar_lineas_vacias(texto: list[str]) -> list[str]:
    res: list[str] = []
    for l in texto:
        if len(l) > 0:
            res.append(l)
    return res

# AUX Ejercicio 10 
def dimensiones_validas(estado: EstadoJuego, archivo: TextIO) -> bool: 
    res: bool = True 
    contenido = quitar_lineas_vacias(archivo.readlines())
    for l in contenido:
        if contar_apariciones(l, ',') != (estado['columnas'] - 1) or len(contenido) != estado['filas']:
            res = False
    return res
    
# def leer_archivo(ruta_directorio: str, nombre_archivo): 
#     archivo: TextIO = open(generar_ruta(ruta_directorio, nombre_archivo), 'r')
#     texto = archivo.read()
#     archivo.close()
#     return texto 

# AUX Ejercicio 10 -> quiero contar las comas y los \n (apariciones de dos chars)
# itero por s y por x a la vez si encuentro una coincidencia

def contar_apariciones(s:str, x:str):
    cont: int = 0
    i = 0
    while i < len(s):
        j = 0
        if s[i] != x[j]: i += 1
        else:   
            while j < len(x) and s[i] == x[j]:
                j += 1
                i += 1
            if j == len(x): cont +=1
    return cont



# la ponen como recomendación
def existe_archivo(ruta_directorio:str, nombre_archivo:str) -> bool: 
    return True
