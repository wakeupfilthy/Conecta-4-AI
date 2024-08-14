import numpy as np
import random
import math
FILAS = 6
COLUMNAS = 7
JUGADOR = 1
BOT = 2
EMPTY = 0
#Se crea el tablero con ceros de 6x7
def crear_tablero():
    tablero = np.zeros((FILAS, COLUMNAS))
    return tablero
#Se coloca la ficha en la fila y columna indicada
def colocar_ficha(tablero, fila, columna, jugador):
    tablero[fila][columna] = jugador
#Se imprime el tablero
def print_tablero(tablero):
    tablero_invertido = np.flip(tablero.astype(int), 0)
    print("1234567\n-------")
    for fila in tablero_invertido:
        for celda in fila:
            if celda == JUGADOR:
                print("\033[92m{}\033[0m".format(celda), end="")  # Jugador 1 en verde
            elif celda == BOT:
                print("\033[91m{}\033[0m".format(celda), end="")  # Jugador 2 en rojo
            else:
                print(celda, end="")
        print()
#Se verifica si hay un ganador
def check_win(tablero, turno):
	# Horizontal, se recorre el tablero de izquierda a derecha y se verifica si hay 4 fichas iguales
	for c in range(COLUMNAS-3):
		for f in range(FILAS):
			if tablero[f][c] == turno and tablero[f][c+1] == turno and tablero[f][c+2] == turno and tablero[f][c+3] == turno:
				return True

	# Vertical, se recorre el tablero de arriba a abajo y se verifica si hay 4 fichas iguales
	for c in range(COLUMNAS):
		for f in range(FILAS-3):
			if tablero[f][c] == turno and tablero[f+1][c] == turno and tablero[f+2][c] == turno and tablero[f+3][c] == turno:
				return True

	# Diagonal positiva, se recorre el tablero de izquierda a derecha y de arriba a abajo y se verifica si hay 4 fichas iguales
	for c in range(COLUMNAS-3):
		for f in range(FILAS-3):
			if tablero[f][c] == turno and tablero[f+1][c+1] == turno and tablero[f+2][c+2] == turno and tablero[f+3][c+3] == turno:
				return True

	# Diagonal negativa, se recorre el tablero de izquierda a derecha y de abajo a arriba y se verifica si hay 4 fichas iguales
	for c in range(COLUMNAS-3):
		for f in range(3, FILAS):
			if tablero[f][c] == turno and tablero[f-1][c+1] == turno and tablero[f-2][c+2] == turno and tablero[f-3][c+3] == turno:
				return True
#Se verifica si la posicion es valida
def posicion_valida(tablero, col):
	return tablero[FILAS-1][col] == 0
#Se obtiene la fila en la que se colocara la ficha
def obtener_fila(tablero, col):
	for f in range(FILAS):
		if tablero[f][col] == 0:
			return f
#Se evalua la ventana de 4 fichas para determinar el puntaje (score) de la posicion
def evaluar_ventana(ventana, turno):
	score = 0
	turno_oponente = JUGADOR
	if turno == JUGADOR:
		turno_oponente = BOT
    #Si hay 4 fichas iguales en la ventana, se suma 100 al score para forzar la jugada ganadora
	if ventana.count(turno) == 4:
		score += 100
    #Si hay 3 fichas iguales y una casilla vacia en la ventana, se suma 5 al score
	elif ventana.count(turno) == 3 and ventana.count(EMPTY) == 1:
		score += 5
    #Si hay 2 fichas iguales y dos casillas vacias en la ventana, se suma 2 al score
	elif ventana.count(turno) == 2 and ventana.count(EMPTY) == 2:
		score += 2
    #Si hay 3 fichas del oponente y una casilla vacia en la ventana, se resta 4 al score
	if ventana.count(turno_oponente) == 3 and ventana.count(EMPTY) == 1:
		score -= 4

	return score
#Se obtienen los valores del score de acuerdo a la posicion de las fichas
def score_posicion(tablero, turno):
	score = 0

	# Score de la columna central, lo que se busca es que el bot juegue en el centro
	centro = [int(i) for i in list(tablero[:, COLUMNAS//2])]
	centro_count = centro.count(turno)
	score += centro_count * 3

	# Score Horizontal, se recorre el tablero de izquierda a derecha y se evalua la ventana de 4 fichas
	for f in range(FILAS):
		fila = [int(i) for i in list(tablero[f,:])]
		for c in range(COLUMNAS-3):
			ventana = fila[c:c+4]
			score += evaluar_ventana(ventana, turno)

	# Score Vertical, se recorre el tablero de arriba a abajo y se evalua la ventana de 4 fichas
	for c in range(COLUMNAS):
		columna = [int(i) for i in list(tablero[:,c])]
		for f in range(FILAS-3):
			ventana = columna[f:f+4]
			score += evaluar_ventana(ventana, turno)

	# Score Diagonal positiva, se recorre el tablero de izquierda a derecha y de arriba a abajo y se evalua la ventana de 4 fichas
	for f in range(FILAS-3):
		for c in range(COLUMNAS-3):
			ventana = [tablero[f+i][c+i] for i in range(4)]
			score += evaluar_ventana(ventana, turno)
    # Score Diagonal negativa, se recorre el tablero de izquierda a derecha y de abajo a arriba y se evalua la ventana de 4 fichas
	for f in range(FILAS-3):
		for c in range(COLUMNAS-3):
			ventana = [tablero[f+3-i][c+i] for i in range(4)]
			score += evaluar_ventana(ventana, turno)
	return score
#Se verifica si el nodo es terminal, es decir, si hay un ganador o si no hay mas movimientos validos
def es_nodo_terminal(tablero):
	return check_win(tablero, JUGADOR) or check_win(tablero, BOT) or len(get_posiciones_validas(tablero)) == 0
#Se implementa el algoritmo minimax para determinar el mejor movimiento
def minimax(tablero, profundidad, maximizando):
	#Se obtienen las posiciones validas
	posiciones_validas = get_posiciones_validas(tablero)
	#Se verifica si el nodo es terminal
	es_terminal = es_nodo_terminal(tablero)
	#Si la profundidad es 0 o el nodo es terminal, se retorna el score de la posicion
	if profundidad == 0 or es_terminal:
		if es_terminal:
			if check_win(tablero, BOT):
				return (None, 100000000000000)
			elif check_win(tablero, JUGADOR):
				return (None, -10000000000000)
			else: # No hay mas movimientos validos
				return (None, 0)
		else: # Profundidad 0
			return (None, score_posicion(tablero, BOT))
	if maximizando:
		valor = -math.inf
		#Se elige una columna aleatoria
		columna = random.choice(posiciones_validas)
		#Se recorren las posiciones validas
		for col in posiciones_validas:
			fila = obtener_fila(tablero, col)
			#Se hace una copia del tablero para simular el movimiento
			tablero_copia = tablero.copy()
			colocar_ficha(tablero_copia, fila, col, BOT)
			#Se obtiene el score de la posicion y se compara con el valor actual, después va a minimizar
			new_score = minimax(tablero_copia, profundidad-1, False)[1]
			#Si el score es mayor que el valor actual, se actualiza el valor y la columna
			if new_score > valor:
				valor = new_score
				columna = col
		#Al final se retorna la mejor columna y el mejor valor
		return columna, valor

	else: # Si se esta minimizando (turno del jugador)
		valor = math.inf
		columna = random.choice(posiciones_validas)
		#Se recorren las posiciones validas
		for col in posiciones_validas:
			fila = obtener_fila(tablero, col)
			#Se hace una copia del tablero para simular el movimiento
			tablero_copia = tablero.copy()
			colocar_ficha(tablero_copia, fila, col, JUGADOR)
			#Se obtiene el score de la posicion y se compara con el valor actual,después va a maximizar
			new_score = minimax(tablero_copia, profundidad-1, True)[1]
			#Si el score es menor que el valor actual, se actualiza el valor y la columna
			if new_score < valor:
				valor = new_score
				columna = col
		return columna, valor
#Se obtienen las posiciones validas
def get_posiciones_validas(tablero):
	posiciones_validas = []
	#Se recorren las columnas y se verifica si la posicion es valida
	for col in range(COLUMNAS):
		if posicion_valida(tablero, col):
			posiciones_validas.append(col)
	return posiciones_validas
#Se inicia el juego
def iniciar_juego(tablero):
	#Se elige un turno aleatorio
    #turno = random.choice([JUGADOR, BOT])
    #turno = JUGADOR
    turno = BOT
    while True:
		#Si el turno es del jugador
        if turno == JUGADOR:
            print("Jugador 1")
			#Se obtiene la columna del jugador 1-7 y se coloca la ficha
            columna = int(input("Jugador 1, elige una columna (1-7):")) - 1
            if posicion_valida(tablero, columna):
                fila = obtener_fila(tablero, columna)
                colocar_ficha(tablero, fila, columna, JUGADOR)
				#Se verifica si el jugador gana
                if check_win(tablero, JUGADOR):
                    print("Jugador 1 gana!")
                    print_tablero(tablero)
                    break
                #Se cambia el turno
                turno = BOT
        else: # Si el turno es del bot
            print("bot")
			#Se obtiene la mejor columna para el bot con el algoritmo minimax, recomendado profundidad 3
            columna, minimax_score = minimax(tablero, 4, True)
            print("columna:",columna+1)
            if posicion_valida(tablero, columna):
                fila = obtener_fila(tablero, columna)
				#Se coloca la ficha en la columna obtenida
                colocar_ficha(tablero, fila, columna, BOT)
				#Se verifica si el bot gana
                if check_win(tablero, BOT):
                    print("Jugador 2 gana!")
                    print_tablero(tablero)
                    break
                turno = JUGADOR
        print_tablero(tablero)
#Inicio del juego
tablero = crear_tablero()
print_tablero(tablero)
iniciar_juego(tablero)