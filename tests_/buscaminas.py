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

""" EJERCICIO 1 """
def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    nueva_matriz: list[list[int]] = []
    pos_ocupadas: list[tuple[int,int]] = posiciones_ocupadas(filas, columnas, minas)
    for f in range(filas):
        nueva_fila: list[int] = []
        for c in range(columnas):
            if (f,c) in pos_ocupadas:
                nueva_fila.append(-1)
            else:
                nueva_fila.append(0)
        nueva_matriz.append(nueva_fila)
    
    return nueva_matriz

#AUX: devuelve todas las posiciones aleatorias donde habría minas
def posiciones_ocupadas(filas:int, columnas: int, minas:int) -> list[tuple[int,int]]:
    i:int = 0
    pos_ocupadas: list[tuple[int,int]] = []
    #Aca se generan las posiciones aleatorias donde van a haber minas
    while i < minas:
        nueva_pos = (random.randint(0, filas-1), random.randint(0, columnas-1))
        if nueva_pos not in pos_ocupadas:
            pos_ocupadas.append(nueva_pos)
            i += 1
    return pos_ocupadas



""" EJERCICIO 2 """
def calcular_numeros(tablero: list[list[int]]) -> None:
    for f in range(len(tablero)):
        for c in range(len(tablero[f])):
            if tablero[f][c] != -1:
                tablero[f][c] = chequear_alrededor(tablero, f, c)
    return

#AUX: chequea alrededor de una pos distinta de bomba y devuelve cuantas bombas adyacentes tiene
def chequear_alrededor(tablero: list[list[int]], f: int, c: int) -> int:
    contador: int = 0
    for x in range(f-1, f+2):
        for y in range(c-1, c+2):
            if x > -1 and y > -1 and x < len(tablero) and y < len(tablero[0]):
                if tablero[x][y] == -1:
                    contador += 1                
    return contador



""" EJERCICIO 3 """
def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    r: EstadoJuego = {}
    r['filas'] = filas
    r['columnas'] = columnas
    r['minas'] = minas
    r['tablero_visible'] = crear_tablero_visible_VACIO(filas, columnas)
    r['juego_terminado'] = False

    y = colocar_minas(filas, columnas, minas)
    calcular_numeros(y)
    r['tablero'] = y
    return r

#AUX: dadas las filas y las columnas devuelve una matriz con todas las celdas en VACIO
def crear_tablero_visible_VACIO(filas: int, columnas:int) -> list[list[str]]:
    res: list[list[str]] = []
    for i in range(filas):
        fila: list[str] = []
        for j in range(columnas): 
            fila.append(VACIO)
        res.append(fila)
    return res

#!!!!!!! AUX: nose bien que funcion cumple en el punto 3 en PARTICULAR la usamos después
def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    res: bool = True
    for f in range(len(tablero)):
        for c in range(len(tablero[f])):
            if tablero[f][c] != -1 and str(tablero[f][c]) != tablero_visible[f][c]:
                res = False
    return res



""" EJERCICIO 4 """
def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    res = estado['tablero_visible']
    return res



""" EJERCICIO 5 """
def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if (not estado['juego_terminado']) and (estado['tablero_visible'][fila][columna] == BANDERA or estado['tablero_visible'][fila][columna] == VACIO):
        if estado['tablero_visible'][fila][columna] == BANDERA:
            estado['tablero_visible'][fila][columna] = VACIO
            ## como la primera condición pide que sea bandera o vacio, si no es bandera es vacio
        else: estado['tablero_visible'][fila][columna] = BANDERA


""" EJERCICIO 6 """
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if not estado['juego_terminado']:
        if estado['tablero'][fila][columna] == -1 and estado['tablero_visible'][fila][columna] != BANDERA:
            marcar_bombas(estado['tablero_visible'], estado['tablero'])
            estado['juego_terminado'] = True
        else:
            caminos_d: list[tuple[int,int]] = caminos_descubiertos(estado['tablero'], estado['tablero_visible'], fila, columna)
            for (f,c) in caminos_d:
                estado['tablero_visible'][f][c] = str(estado['tablero'][f][c])
            if todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']):
                estado['juego_terminado'] = True
    return

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int) -> list[list[(int, int)]]:
    camino: list[tuple[int,int]] = [] 
    return recursion_caminos_descubiertos(tablero, tablero_visible, f, c, camino)

#AUX: hace una recusion que recorre las celdas adyacentes en busqueda de celdas que, a su vez esten adyacentes a una bomba
def recursion_caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f: int, c: int, camino: list[list[(int, int)]]) -> list[list[(int, int)]]:
    if tablero_visible [f][c] != BANDERA :
        camino.append((f,c))
        if chequear_alrededor(tablero, f, c) == 0 : 
            for x in range(f-1, f+2):
                for y in range(c-1, c+2):
                    if x > -1 and y > -1 and x < len(tablero) and y < len(tablero[0]) and ((x,y) not in camino):
                        recursion_caminos_descubiertos(tablero, tablero_visible, x, y, camino)
    return camino

#AUX: muestra las bombas en el tablero visible 
def marcar_bombas(tablero_visible: list[list[str]], tablero: list[list[str]]) -> None:
    for f in range (len(tablero_visible)):
        for c in range (len(tablero_visible[f])):
            if tablero[f][c] == -1:
                tablero_visible[f][c] = BOMBA
    return 


""" EJERCICIO 7 """
def verificar_victoria(estado: EstadoJuego) -> bool:
    return todas_celdas_seguras_descubiertas(estado['tablero'],estado['tablero_visible'])


""" EJERCICIO 8 """
def reiniciar_juego(estado: EstadoJuego) -> None:
    filas = estado['filas'] 
    columnas = estado['columnas'] 
    minas = estado['minas']
    estado['tablero_visible'] = crear_tablero_visible_VACIO(filas, columnas)

    estado_tablero_anterior = estado['tablero']

    nuevo_tablero: list[list[int]]
    while estado_tablero_anterior == nuevo_tablero:
        nuevo_tablero = colocar_minas(filas, columnas, minas)
        calcular_numeros(nuevo_tablero)
    estado['tablero'] = nuevo_tablero

    estado['juego_terminado'] = False
    return

estado: EstadoJuego = {'filas': 3,
            'columnas': 3,
            'minas': 1,
            'tablero_visible': [['1', '🏳', VACIO], ['1', '1', '1'], ['0', '0', '0']],
            'tablero': [[1, -1, 1], [1, 1, 1], [0, 0, 0]],
            'juego_terminado': False}
descubrir_celda(estado,0,2 )

# def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
#     archivo_tablero: TextIO = open(generar_ruta(ruta_directorio, 'tablero.txt'), 'w')
#     archivo_tablero_visible: TextIO  = open(generar_ruta(ruta_directorio, 'tablero_visible.txt'),'w')
    
#     archivo_tablero.write(tableros_a_strings(estado, estado['tablero']))
#     archivo_tablero_visible.write(tableros_a_strings(estado, estado['tablero_visible']))
    
#     archivo_tablero.close()
#     archivo_tablero_visible.close()
#     return

# def tableros_a_strings(estado: EstadoJuego, tablero:list[list[any]]) -> str: 
#     res: str = str()
#     for f in range (len(tablero)):
#         for c in range(len(tablero[0])):
#             if tablero == estado['tablero_visible']:
#                 if tablero[f][c] == BANDERA: 
#                     res += '*'
#                 else: 
#                     if tablero[f][c] == VACIO: 
#                         res += '?'
#                     else:  res += tablero[f][c]
#             else: 
#                 res += str(tablero[f][c])
                
#             if c == len(tablero[0])-1: #último elemento de la fila 
#                 res += '\n'
#             else: res += ','
#     return res 

# def generar_ruta(ruta_directorio:str, nombre_archivo:str):
#     return os.path.join(ruta_directorio,nombre_archivo)


# ----------------------------------------> ESTA vVenia con el template solo que estaba arriba de todo 
# def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
#     """Chequea si existe el archivo en la ruta dada"""
#     return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))


# def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
#     res: bool = True
    
#     if os.path.exists(generar_ruta(ruta_directorio, 'tablero.txt')) and os.path.exists(generar_ruta(ruta_directorio, 'tablero_visible.txt')):
#         archivo_tablero: TextIO = open(generar_ruta(ruta_directorio, 'tablero.txt'), 'r')
#         archivo_tablero_visible: TextIO  = open(generar_ruta(ruta_directorio, 'tablero_visible.txt'),'r')
#         if not dimensiones_validas(estado, archivo_tablero) or not dimensiones_validas(estado, archivo_tablero_visible):
#             res = False
        
        
#     else: 
#         res = False 
#     return False

# def quitar_lineas_vacias(texto: list[str]) -> list[str]:
#     res: list[str] = []
#     for l in texto:
#         if len(l) > 0:
#             res.append(l)
#     return res

# # AUX Ejercicio 10 
# def dimensiones_validas(estado: EstadoJuego, archivo: TextIO) -> bool: 
#     res: bool = True 
#     contenido = quitar_lineas_vacias(archivo.readlines())
#     for l in contenido:
#         if contar_apariciones(l, ',') != (estado['columnas'] - 1) or len(contenido) != estado['filas']:
#             res = False
#     return res
    
# # def leer_archivo(ruta_directorio: str, nombre_archivo): 
# #     archivo: TextIO = open(generar_ruta(ruta_directorio, nombre_archivo), 'r')
# #     texto = archivo.read()
# #     archivo.close()
# #     return texto 

# # AUX Ejercicio 10 -> quiero contar las comas y los \n (apariciones de dos chars)
# # itero por s y por x a la vez si encuentro una coincidencia

# def contar_apariciones(s:str, x:str):
#     cont: int = 0
#     i = 0
#     while i < len(s):
#         j = 0
#         if s[i] != x[j]: i += 1
#         else:   
#             while j < len(x) and s[i] == x[j]:
#                 j += 1
#                 i += 1
#             if j == len(x): cont +=1
#     return cont



# # la ponen como recomendación
# def existe_archivo(ruta_directorio:str, nombre_archivo:str) -> bool: 
#     return True
