import random
#para hacer pausas y que no sea mostrado tan rapido el códgigo
#se importa la función sleep de la librería time
from time import sleep

vidas_jug_1 = [1, 2, 3, 4, 5]
vidas_jug_2 = [1, 2, 3, 4, 5]

def EliminarVidaDelRival(jug_act):
    global vidas_jug_1, vidas_jug_2
    if jug_act == 1:
        if len(vidas_jug_2) > 0:
            vidas_jug_2.pop(0)
    else:
        if len(vidas_jug_1)>0:
            vidas_jug_1.pop(0)

def EliminarCartaDelRival(jug_act):
    global mano_p_1, mano_p_2

    #quedó aca redundante, se comentó para eliminar porque lo estaba preguntando dos veces
    #print("ingresar la posición de la carta que se quiere borrar, recordar que empieza desde el 0")
    #pos = int(input())

    if jug_act == 1:
        rival_mano = mano_p_2
    else:
        rival_mano = mano_p_1

    print("ingresar posición de la carta del rival a borrar (desde 0):")
    pos = int(input())

    if 0 <= pos < len(rival_mano):
        carta_eliminada = rival_mano.pop(pos)
        print("carta eliminada")
        
        #nuevo if porque está eliminando cartas que no se robaron todavía
        #se chequea si el rival tiene cartas
        if len(rival_mano) == 0:
            #para que no se elimine, agregué una carta mas
            rival_mano.append(random.choice(mazo))
    else:
        print("fuera de rango")

def RobarCartaExtraDelMazo(jug_act):
    actual = mano_p_1 if jug_act == 1 else mano_p_2
    actual.append(random.choice(mazo))

def MostrarCartaDelRival(jug_act):
    rival = mano_p_2 if jug_act == 1 else mano_p_1

    elem_azar = random.choice(rival)
    #se cambió para mostrar el nombre de la función y no el objeto
    print(f"Carta del rival: {elem_azar.__name__}")

def SaltarTurnoDelRival(turn_act):
    return turn_act + 2

#cartas de relleno para que no sea tan rapido el juego
def CartaDeRelleno(jug_act):
    #este pass es para que avance el búcle
    pass

#lista con "cartas"
#"CartaDeRelleno" se repite para aumentar la probabilidad de que salga
mazo = [EliminarVidaDelRival, CartaDeRelleno, EliminarCartaDelRival, CartaDeRelleno, RobarCartaExtraDelMazo, CartaDeRelleno, MostrarCartaDelRival, CartaDeRelleno, SaltarTurnoDelRival]

turno = 0

mano_p_1 = random.sample(mazo, 3)
mano_p_2 = random.sample(mazo, 3)

while True:
    jug_act = 1 if turno % 2 == 0 else 2

    #se cambió de lugar y se agregó saber quien es el rival para mostrar la cantidad de cartas
    if jug_act == 1:
        mano = mano_p_1
        rival = mano_p_2
    else:
        mano = mano_p_2
        rival = mano_p_1
    
    print (f"\n turno del jugador {jug_act}")

    print(f"vidas jugador 1: {len(vidas_jug_1)}")
    print(f"vidas jugador 2: {len(vidas_jug_2)}")

    #se muestra la cantidad de cartas del rival
    print(f"cantidad de cartas del rival: {len(rival)}")
    
    #se espera 3 segundos antes de continuar
    sleep(1.5)

    print(f"cartas jugador {jug_act}:")

    for idx, carta in enumerate(mano, start=1):
        print(f"{idx}: {carta.__name__}")

    print("se seleccionan las cartas con 1, 2, 3, etc.")
    carta_elegida = input()
    
    if carta_elegida.lower() == "salir":
        print(f"jugador {jug_act} se rindió")
        break

    #se cambió para poder contemplar mas de 3 cartas
    #isdigit() devuelve los caracteres a dígtos numéricos
    if carta_elegida.isdigit():
        carta_elegida = int(carta_elegida) - 1
        if 0 <= carta_elegida < len(mano):
            carta_a_usar = mano[carta_elegida]

            print(f"carta elegida: {carta_a_usar.__name__}")
        else:
            print("error 404, seleccione una carta dentro del rango")
            continue
    else:
        print("error 404, seleccione una carta dentro del rango")
        continue
    
    #la cambie de lugar porque estaba eliminando cartas que no debía
    #aca se usa pop() para eliminar la carta usada
    #se le pasa por parámetro la carta seleccionada, en lugar del jugador actual
    mano.pop(carta_elegida)

    #se cambió de lugar porque el código seguía ejecutandose despues que un jugador ganó
    if not vidas_jug_1:
        print("ganador: jugador 2")
        break
    elif not vidas_jug_2:
        print("ganador: jugador 1")
        break
    
    #cambio para detectar si se usa la carta de saltar turno, porque esa fucnión necesita saber el turno, no el jugador
    if carta_a_usar.__name__ == "SaltarTurnoDelRival":
        #se le pasa el turno a la función para que funcione correctamente
        turno = carta_a_usar(turno)
    #si no se usa la carta de saltar turno, se le pasa el jugador actual a las demás
    else:
        carta_a_usar(jug_act)
        #se cambió de lugar para que al usar los saltar turno no funcionaban bien
        #se estaban agregando 3 turnos cuando se usaba, 2 de la función y 1 al final del búcle, lo cual hacia
        #que en vez de saltar el turno del rival, se pasara de turno
        #esperar 3 segundos para terminar el turno
        sleep(1.5)
        turno += 1

    #validación para comprobar si el jugador tiene cartas en la mano, sino roba 3 del mazo
    #originalmente era una(1) carta sola
    if len(mano) == 0:
        #se agrega a la mano una carta random del mazo al jugador 1
        if jug_act == 1:
            mano_p_1.extend(random.sample(mazo, 3))
        else:
            # se le dan 3 cartas al jugador 2
            mano_p_2.extend(random.sample(mazo, 3))
        print("como no tenías carta robaste tres del mazo")
