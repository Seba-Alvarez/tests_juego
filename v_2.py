import random

vidas_jug_1 = [1, 2, 3, 4, 5]
vidas_jug_2 = [1, 2, 3, 4, 5]

def baja_0(jug_act):
    #para asegurarse que se están modificando bien las listas
    global vidas_jug_1, vidas_jug_2
    if jug_act == 1:
        #validación porque no estaba quitando nada
        if len(vidas_jug_2) > 0:
            vidas_jug_2.pop(0)
    else:
        #lo mismo que arriba
        if len(vidas_jug_1)>0:
            vidas_jug_1.pop(0)

def baja_index(jug_act):
    global mano_p_1, mano_p_2 
    print("ingresar la posición que se quiere borrar, recordar que empieza desde el 0")
    pos = int(input())

    if jug_act == 1:
        rival_mano = mano_p_2
    else:
        rival_mano = mano_p_1

    print("ingresar posición de la carta del rival a borrar (desde 0):")
    pos = int(input())

    if 0 <= pos < len(rival_mano):
        carta_eliminada = rival_mano.pop(pos)
        print("carta eliminada")
    else:
        print("fuera de rango")

def alta_cur(jug_act):
    actual = vidas_jug_1 if jug_act == 1 else vidas_jug_2
    actual.append(random.choice(mazo))


def listar_index_rival(jug_act):
    rival = mano_p_2 if jug_act == 1 else mano_p_1

    elem_azar = random.choice(rival)
    print(f"Vida del rival: {elem_azar}")


def saltar_rival(turn_act):
    return turn_act +2

mazo = [baja_0, baja_index, alta_cur, listar_index_rival, saltar_rival]

turno = 0

#con sample de la biblioteca random se forman las "manos" de los "jugadores"
#a sample se le pasa el lugar donde está almacenada la información y el rango
mano_p_1 = random.sample(mazo, 3)
mano_p_2 = random.sample(mazo, 3)

#apra depurar, porque son las manos siempre iguales
print("Mano jugador 1 inicial:", [c.__name__ for c in mano_p_1])
print("Mano jugador 2 inicial:", [c.__name__ for c in mano_p_2])

while True:
    jug_act = 1 if turno % 2 == 0 else 2
    print (f"\n turno del jugador {jug_act}")

    print(f"Vidas Jugador 1: {len(vidas_jug_1)}")
    print(f"Vidas Jugador 2: {len(vidas_jug_2)}")


    #se verifica de quien es la mano
    #se guarda en una variable para mostrarla después
    if jug_act == 1:
        mano = mano_p_1
    else:
        mano = mano_p_2


    #se recorren las "manos" de los jugadores para poder mostrarlas
    print(f"cartas jugador {jug_act}:")
    #aca se usa idx como una convención, en nombre puede ser cualquiera
    #es lo mismo que las constantes en mayuscula e iniciar las clases con el método self
    #enumerate convierte los datos de la lista en un objeto enumerate
    #estos objetos son un par (indice, valor), es decir:
    #la posción y lo que está en la misma
    #se le pasa la variable con las manos de los jugadores
    #el start es para que arranque desde el 1 en lugar del 0, para que al jugar no se tenga que usar 0,1 y 2. En su lugar
    #se juega con 1,2 y 3
    for idx, carta in enumerate(mano, start=1):
        #el idx es para mostrar el número de la carta
        #__name__ es para mostrar el nombre de la función
        #es carta.__name__ porque se están mostrando solo los de las cartas que tiene el jugador en la "mano"
        print(f"{idx}: {carta.__name__}")


    #aca se manejan los inputs del usuario:
    #se aclara que va del 1 al 3 y no del 0 al 2
    print("se seleccionan las cartas con 1, 2 y 3")
    #se pide el input
    carta_elegida = input()
    
    #condición para terminar el juego antes
    #si el input es "salir" (no importan las mayusculas por el .lower)
    if carta_elegida.lower() == "salir":
        #se muestra quien se rindió
        print(f"jugador {jug_act} se rindió")
        #importante poner este break dentro del if porque sino va a cortar todo el búcle acá
        break

    #se pone el rango del input para despues pasarlo a la posición del índice
    if carta_elegida in ["1", "2", "3"]:
        #se toma el input y se le resta 1 para que ejecute bien la posición y si se selecciona la 3er carta no de fuera de rango
        carta_elegida = int(carta_elegida) - 1
        #este manejo de excepciones se lo pedí a chatgpt
        #esto es un manejo de excepciones
        #aca se asegura que la elección de cartas no puede ser mayor a la cantidad que se tiene
        #no se puede poner un 4, si solo hay 3 cartas
        if 0 <= carta_elegida < len(mano):
            #aca se asigna la carta seleccionada en una variable para incializar la función
            carta_a_usar = mano[carta_elegida]

            #se muestra el nombre de la carta que se va a usar
            print(f"carta elegida: {carta_a_usar.__name__}")
        else:
            #el continue es para que el programa no se caiga y siga
            print("error 404, seleccione una carta dentro del rango")
            continue
    else:
        print("error 404, seleccione una carta dentro del rango")
        continue
    
    #se inicializa la función pasandole el jugador actual como parámetro
    carta_a_usar(jug_act)

    if not vidas_jug_1:
        print("ganador: jugador 2")
        break
    elif not vidas_jug_2:
        print("ganador: jugador 1")
        break

    turno += 1

