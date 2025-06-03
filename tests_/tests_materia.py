import unittest
from buscaminas import (BOMBA, BANDERA, VACIO, EstadoJuego, 
                        colocar_minas, calcular_numeros, crear_juego, 
                        obtener_estado_tablero_visible,marcar_celda, descubrir_celda,
                        verificar_victoria,reiniciar_juego)


#reiniciar_juego,  , guardar_estado, cargar_estado, )


'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''
def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def cant_ceros_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de no minas en el tablero sea igual al número de espacios esperado"""
    contador_espacios:int = 0
    for fila in tablero:
        for celda in fila:
            if celda != -1:
                contador_espacios += 1
    return contador_espacios

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True



"""EJERCICIO 1"""
class colocar_minasTest(unittest.TestCase):
    def test_cuadrada_una_mina(self):
        filas = 2
        columnas = 2
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)


    def test_rectangular_mas_minas(self):
        filas = 5
        columnas = 9
        minas = 11
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)
    
    def test_(self):
        filas = 1
        columnas = 6
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        self.assertEqual(cant_ceros_en_tablero(tablero), filas*columnas-minas)

        
"""EJERCICIO 2"""
class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],
                                   [1, 1]])
    
    def test_matriz_mas_grande(self):
        # PRUEBO EJ 1 ADEMÁS
        filas = 9
        columnas = 15
        minas = 14
        # chequeo por cardinalidad como no puedo predecir el random 
        tablero = colocar_minas(filas, columnas, minas)

        calcular_numeros(tablero)
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
    

"""EJERCICIO 3"""
class crear_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
    

"""EJERCICIO 4"""
class obtener_estado_visible(unittest.TestCase):
    def test_(self): 
        filas = 3
        columnas = 11
        minas = 8
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        self.assertEqual(estado['tablero_visible'], obtener_estado_tablero_visible(estado))


""" EJERCICIO 5 """
class marcar_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_ejemplo_sacar_bandera(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_juego_terminado(self): 
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BOMBA, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': True
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BOMBA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertTrue(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_vacio_poner_bandera_en_matriz_con_bandera(self): 
        estado: EstadoJuego = {
                'filas': 3,
                'columnas': 3,
                'minas': 2,
                'tablero_visible': [[VACIO,BANDERA,VACIO],[VACIO,VACIO,VACIO],[VACIO,VACIO,VACIO]],
                'tablero': [[1, 2, -1], [1, -1, 2], [1, 1, 1]],
                'juego_terminado': False
            }
        marcar_celda(estado,1, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], 
             [[VACIO,BANDERA,VACIO],[BANDERA,VACIO,VACIO],[VACIO,VACIO,VACIO]]
        )
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], 
            [[1, 2, -1], [1, -1, 2], [1, 1, 1]],
        )
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya misma cant de minas en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']),2 )


""" EJERCICIO 6 """
class descubrir_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [VACIO, "3", "1"],
            [VACIO, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])

    def test_descubir_celda_con_BOMBA(self):
            estado: EstadoJuego = {
                'filas': 5,
                'columnas': 3,
                'minas': 6,
                'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
                'tablero': [[1, -1, 2], [2, 4, -1], [-1, 5, -1], [-1, 4, -1], [1, 2, 1]],
                'juego_terminado': False
            }
            descubrir_celda(estado, 0, 1)
            # Testeamos que la celda descubierta sea visible
            self.assertEqual(estado['tablero_visible'], [
                [VACIO, BOMBA, VACIO],
                [VACIO, VACIO, BOMBA],
                [BOMBA, VACIO, BOMBA],
                [BOMBA, VACIO, BOMBA],
                [VACIO, VACIO, VACIO]
            ])
            # Testeamos que el resto no se modificó
            self.assertEqual(estado['filas'], 5)
            self.assertEqual(estado['columnas'], 3)
            self.assertEqual(estado['minas'], 6)
            self.assertEqual(estado['tablero'], [
                [1, -1, 2], [2, 4, -1], [-1, 5, -1], [-1, 4, -1], [1, 2, 1]
            ])
            # Testeamos que haya una mina en el tablero
            self.assertEqual(cant_minas_en_tablero(estado['tablero']), 6)
            self.assertTrue(estado['juego_terminado'])

            ### MISMO código que no debería cambiar nada cuando ya se terminó el juego 
            descubrir_celda(estado, 6,9)
            self.assertEqual(estado['tablero_visible'], [
                [VACIO, BOMBA, VACIO],
                [VACIO, VACIO, BOMBA],
                [BOMBA, VACIO, BOMBA],
                [BOMBA, VACIO, BOMBA],
                [VACIO, VACIO, VACIO]
            ])
            # Testeamos que el resto no se modificó
            self.assertEqual(estado['filas'], 5)
            self.assertEqual(estado['columnas'], 3)
            self.assertEqual(estado['minas'], 6)
            self.assertEqual(estado['tablero'], [
                [1, -1, 2], [2, 4, -1], [-1, 5, -1], [-1, 4, -1], [1, 2, 1]
            ])
            # Testeamos que haya una mina en el tablero
            self.assertEqual(cant_minas_en_tablero(estado['tablero']), 6)
            self.assertTrue(estado['juego_terminado'])

    def todas_celdas_seguras(self):
        estado: EstadoJuego = {'filas': 3,
            'columnas': 3,
            'minas': 1,
            'tablero_visible': [['1', '🏳', VACIO], ['1', '1', '1'], ['0', '0', '0']],
            'tablero': [[1, -1, 1], [1, 1, 1], [0, 0, 0]],
            'juego_terminado': False}
        
        descubrir_celda(estado,0,2)
        #IGUAL
        descubrir_celda(estado,0,1)
        self.assertEqual(estado['tablero_visible'], [['1', '🏳', '1'], ['1', '1', '1'], ['0', '0', '0']])
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
                [[1, -1, 1], [1, 1, 1], [0, 0, 0]]
            ])
            # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertFalse(estado['juego_terminado'])
        self.assertTrue(estado['juego_terminado'])

    def recursion_al_lado_bandera(self):
        #Este caso no tiene sentido pero es suponiendo que una persona se haya equivocado 
        estado: EstadoJuego = {'filas': 3,
            'columnas': 3,
            'minas': 1,
            'tablero_visible': [[VACIO, BANDERA, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
            'tablero': [[1, -1, 1], [1, 1, 1], [0, 0, 0]],
            'juego_terminado': False}
        marcar_celda(estado, 1, 1)
        descubrir_celda(estado,2,1)

        self.assertEqual(estado['tablero_visible'], [
            [VACIO, '🏳', VACIO], ['1', '🏳', '1'], ['0', '0', '0']
        ])
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
                [[1, -1, 1], [1, 1, 1], [0, 0, 0]]
            ])
            # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertFalse(estado['juego_terminado'])

class verificar_victoriaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            ["1", "1"]
        ])
        self.assertFalse(estado['juego_terminado'])
        


class obtener_estado_tableroTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])


class reiniciar_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

# # Tarea: Pensar cómo testear  guardar_estado y cargar_estado

# class guardar_estadoTest(unittest.TestCase):
#     def test_ejemplo (self):
#         return

# class cargar_estadoTest(unittest.TestCase):
#     def test_ejemplo (self):
#         return


"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""

if __name__ == '__main__':
    unittest.main(verbosity=2)
