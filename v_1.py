import random

#las "vidas" de los jugadores para testear
lis_jug_1 = [1, 2, 3, 4, 5]
lis_jug_2 = [1, 2, 3, 4, 5]

#función para eliminar "vidas" del rival en la posición 0
def baja_0(jug_act):
    #si es el jugador 1
    if jug_act == 1:
        #elimina de la lista del jugador 2
        lis_jug_2.pop(0)
    #cuando sea turno del jugador 2
    else:
        #elimina de la lista del jugador 1
        lis_jug_1.pop(0)

#función para eliminar "vidas" del rival con inputs
def baja_index(jug_act):
    #se pide la posición
    print("ingresar la posición que se quiere borrar, recordar que empieza desde el 0")
    #se pide la posición a borrar
    pos = int(input())

    #si es el jugador 1
    if jug_act == 1:
        #elimina de la lista del jugador 2, con la posición que se le pasa por parámetro
        lis_jug_2.pop(pos)
    #cuando sea turno del jugador 2
    else:
        #elimina de la lista del jugador 1, con la posición que se le pasa por parámetro
        lis_jug_1.pop(pos)

#función para agregar elementos al rival
#ahora mismo solo agrega "vidas", pero despues tendria que agregarse algún efecto negativo
def alta_rival(jug_act):
    #aca se cheque a si es el turno del otro jugador
    #la variable tiene el valor de la lista del jugador 2 si el jugador actual es el 1
    #si es el jugador 2 tiene el valor del jugador 1
    rival = lis_jug_2 if jug_act == 1 else lis_jug_1

    #para buscar el maximo número
    max_num = 0
    #búcle para recorrer la lista del rival
    for i in rival:
        if i >= max_num:
            max_num = i + 1
    
    nuevo_elemento = max_num
    #se agrega una vida por ahora, despues tienen que ser cartas
    rival.append(nuevo_elemento)

#función para agregar elementos al jugador
#ahora mismo solo agrega "vidas", pero despues tendria que robar una "carta"
def alta_cur(jug_act):
    #aca se cheque a que sea el jugador actual
    #si el jugador es el 1, se trabaja sobre el mismo
    #si el jugador activo no es el 1, se trabaja sobre el 2
    actual = lis_jug_1 if jug_act == 1 else lis_jug_2

    #para buscar el maximo número
    max_num = 0
    #búcle para recorrer la lista del jugador actual
    for i in actual:
        if i >= max_num:
            max_num = i + 1
    
    nueva_vida = max_num
    #se agrega una nueva vida
    #después tienen que ser cartas
    actual.append(nueva_vida)


#función para listar una carta al azar del rival
def listar_index_rival(jug_act):
    #aca se cheque a si es el turno del otro jugador
    #la variable tiene el valor de la lista del jugador 2 si el jugador actual es el 1
    #si es el jugador 2 tiene el valor del jugador 1
    rival = lis_jug_2 if jug_act == 1 else lis_jug_1

    #elección random con choice() de la lista del rival
    elem_azar = random.choice(rival)
    #se muestra el elemnto en concreto
    #ahora son vidas, pero despues tendrian que ser sobre las cartas del rival
    print(f"Vida del rival: {elem_azar}")

#función para saltar el turno del oponente
#no le veo mucho uso, siendo que te estas drenando de recursos, ver que hacer con esto
def saltar_rival(turn_act):
    #como los turnos son en base a si el número es par o no
    #al agregar +2 a los turnos, se asegura que siga el mismo jugador
    #si es el "turno" 1 (jugador 1), pasa a ser el turno 3 (otra vez el jugador 1)
    return turn_act +2



#mazo de "cartas" con las funciones para actuar sobre las "vidas" del rival, arreglar despues
mazo = [baja_0, baja_index, alta_rival, alta_cur, listar_index_rival, saltar_rival]


#para calcular el turno de cada jugador
#basico por ahora
turno = 0

#bucle para "jugar"
while True:
    #aca se cheque si es el turno del jugador 1 o 2
    #si la iteración del bucle es par, es el turno del jugador 1
    #si la iteración es impar es turno del jugador 2
    jug_act = 1 if turno % 2 == 0 else 2
    #se muestra de quien es el turno
    print (f"\n turno del jugador {jug_act}")

    #se muestran las vidas
    print(f"Vidas Jugador 1: {lis_jug_1}")
    print(f"Vidas Jugador 2: {lis_jug_2}")

    #para manejar el "juego"
    accion = int(input())

    #aca se llaman a las funciones
    #a la mayoria se les pasa el jugador actual por parámetro porque es lo que se define en las funciones
    if accion == 1:
        baja_0(jug_act)
    elif accion == 2:
        baja_index(jug_act)
    elif accion == 3:
        alta_rival(jug_act)
    elif accion == 4:
        alta_rival(jug_act)
    elif accion == 5:
        #aca se le pasa el turno porque es lo que se definió en la función para saltar turno del rival
        saltar_rival(turno)
    elif accion == 6:
        listar_index_rival(jug_act)
    elif accion == 0:
        break
    else:
        print("ingresar un número valido")

    #las listas vacias y llenas tienen valores booleanos por defecto
    #las listas llenas tienen un valor true
    #mientras que las vacias tienen un valor false
    if not lis_jug_1:
        print("ganador: jugador 2")
        #sale del juego
        break
    #aca no se puede usar un else porque se está verificando una condición especifica
    elif not lis_jug_2:
        print("ganador: jugador 1")
        break

    turno += 1
