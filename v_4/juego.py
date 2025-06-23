#aca se importan las librerias
import pygame
import random
import sys
#esto es un modulo para interactuar con el sistema operativo (para obtener direcciones y no tener que escribir a mano)
import os

#directorio para cargar las imagenes
BASE_DIR = os.path.dirname(__file__)
#aca se inicializa pygame con la función init()
pygame.init()

# Aca se dibuja la ventana
#ancho y alto son los pixeles de cada dimensión
ANCHO, ALTO = 1200, 650
#pygame.display inicializa la función set_mode, a la cual se le pasan las dimensiones de la pantalla por parámetro
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
#esto es simplemente el titulo
pygame.display.set_caption("Dragon List")

#region carga de cartas

# Función para cargar las imágenes
# donde nombre es el nombre de la imagen
# hay que recordar poner bien el formato de la imagen (png, jpg, etc)
#ahora se cargan las imagenes de forma relativa, también se le pasa por parámetro el nombre
def cargar_img(nombre):
    #se pide la ruta relativa guardada en el sistema
    ruta_imagen = os.path.join(BASE_DIR, "imagenes", f"{nombre}.png")
    #aca queda igual que la anterior
    return pygame.transform.scale(pygame.image.load(ruta_imagen), (100, 140))

#nombres de las cartas, dentro de la carpeta imagenes
#ese nombre es el que se le pasa a la función como parametro para que las muestre
IMAGENES_CARTAS = {
    #va solo el nombre, la extensión se carga en la función cargar_img
    "eliminar_vida_del_rival": cargar_img("carta_extra"),
    "eliminar_carta_del_rival": cargar_img("carta_eliminar"),
    "robar_carta_extra_del_mazo": cargar_img("carta_extra"),
    "mostrar_carta_del_rival": cargar_img("carta_mostrar"),
    "saltar_turno_del_rival": cargar_img("carta_saltar"),
    "carta_de_relleno": cargar_img("carta_relleno")
}

#lo mismo que arriba pero con el jugador 2
def cargar_img_jug2(nombre):
    ruta_imagen = os.path.join(BASE_DIR, "imagenes_p_2", f"{nombre}.png")
    return pygame.transform.scale(pygame.image.load(ruta_imagen), (100, 140))

#se llama a las mismas funciones
#los nombres de las cartas son iguales
#no carga las mismas imagenes porque está en otra carpeta
IMAGENES_CARTAS_JUG2 = {
    "eliminar_vida_del_rival": cargar_img_jug2("carta_extra"),
    "eliminar_carta_del_rival": cargar_img_jug2("carta_eliminar"),
    "robar_carta_extra_del_mazo": cargar_img_jug2("carta_extra"),
    "mostrar_carta_del_rival": cargar_img_jug2("carta_mostrar"),
    "saltar_turno_del_rival": cargar_img_jug2("carta_saltar"),
    "carta_de_relleno": cargar_img_jug2("carta_relleno")
}

#endregion


#lo único que se cambió es agregar la dirección relativa del fondo. El ancho y el alto quedan iguales.
FONDO = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_DIR, "imagenes", "fondo.jpg")),
    (ANCHO, ALTO)
)

#igual que arriba pero con el mazo.
MAZO_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_DIR, "imagenes", "mazo.png")),
    (100, 140)
)


# Vidas del juego, en este caso son números para que sea mas facil hacer los calculos
# es importante separarlas para no agregar una capa de lógica extra
vidas_jug_1 = [1, 2, 3, 4, 5]
vidas_jug_2 = [1, 2, 3, 4, 5]

#region lógica del juego

#la función principal, que es la que determina quien gana
#se le tiene que pasar el jugador actual como parámetro
#este parametro es el que determina a quien se le quita la vida
def eliminar_vida_del_rival(jug_act):
    #validación para saber si el jugador actual es el 1 o no
    #además se verifica que la lista de vidas no este vacia
    if jug_act == 1 and vidas_jug_2:
        #aca se quita el primer elemento (posición 0 del índice) de la lista de vidas del jugador rival
        vidas_jug_2.pop(0)
    #aca se valida que el jugador sea el 2, no se maneja con else porque también hay que verificar que
    # el jugador 1 tenga vidas en la lista
    elif jug_act == 2 and vidas_jug_1:
        #aca se elimina
        vidas_jug_1.pop(0)

#aca se eliminan cartas del rival
#también se le pasa el jugador actual por parámetro
def eliminar_carta_del_rival(jug_act):
    #rival es el jugador opuesto al actual
    #esta validación significa:
    #la mano del rival es la del jugador 2 si el jugador actual es el 1
    #si la mano del rival no es del jugador 2, es del jugador 1
    rival = mano_p_2 if jug_act == 1 else mano_p_1
    #validación para eliminar bien las cartas
    if rival:
        #aca se borra la carta en la primera posición del índice
        rival.pop(0)
        #esta validación es importante
        #si el rival se fuera a quedar sin cartas, se le agrega 1 mas para que pueda robar las cartas del mazo
        if not rival:
            #aca se le da la carta para que pueda robar del mazo
            rival.append(random.choice(mazo))

#aca, el juagador actual roba una carta extra del mazo
#se le tiene que pasar el jugador actuar como parámetro
def robar_carta_extra_del_mazo(jug_act):
    #se guarda la mano del jugador actual
    #es decir, la mano actual es la del jugador 1 si el jugador actual es el 1
    #sino la mano actual es la del jugador 2
    actual = mano_p_1 if jug_act == 1 else mano_p_2
    #aca se agrega la carta con append
    #choice() es una función de la librería random
    #esta selecciona un elemento al azar del mazo
    actual.append(random.choice(mazo))

#region cambiar

#aca se muestra una carta del rival
def mostrar_carta_del_rival(jug_act):
    #variable global para guardar la carta mostrada
    global carta_mostrada, carta_mostrada_timer
    #se verifica quien es el rival
    rival = mano_p_2 if jug_act == 1 else mano_p_1
    #se muestra la carta del rival
    if rival:
        #carta mostrada es el nombre de la carta
        carta_mostrada = rival[0].__name__.replace("_", " ").capitalize()
        #el timer es el frame en que se va a mostrar
        carta_mostrada_timer = pygame.time.get_ticks()


#endregion

#aca se pasa el turno, simplemente se agregan dos iteraciones al búcle principal
#por lo mismo se le tiene que pasar el turno como parámetro
def saltar_turno_del_rival(turno):
    return turno + 2

#carta de relleno, solo pasa un turno
#si bien en la función no se le pasan parámetros
#se le pasa para que no de error
def carta_de_relleno(jug_act):
    pass

#endregion

# "Mazo de cartas" es una lista con las funciones
# carta de relleno se repite para aumentar la probabilidad de que salga, pero siempre es la misma función 
mazo = [
    eliminar_vida_del_rival,
    carta_de_relleno,
    eliminar_carta_del_rival,
    carta_de_relleno,
    robar_carta_extra_del_mazo,
    carta_de_relleno,
    mostrar_carta_del_rival,
    carta_de_relleno,
    saltar_turno_del_rival
]

# Aca se crean las manos de los jugadores
# sample() funciona igual que choice, pero devuelve varios elementos
# 3 en este caso
mano_p_1 = random.sample(mazo, 3)
mano_p_2 = random.sample(mazo, 3)
#se incializan los turnos en 0 para manejar la lógica del pasar turno
turno = 0
#aca se usa una fuente (de letras) de pygame para mostrar por pantalla
fuente = pygame.font.SysFont(None, 24)
#inicializar un timer para que el juego no vaya tan rapido
clock = pygame.time.Clock()
FPS = 30

# Para mostrar temporalmente una carta del rival
carta_mostrada = None
carta_mostrada_timer = 0

#función para mostrar imagenes
#se le pasa la función para cargar imagenes y el jjugador actual
def obtener_imagen(funcion, jugador):
    #se guarda el nombre de la lista de "cartas" (son funciones)
    nombre = funcion.__name__
    #validación para saber quien es el jugador
    if jugador == 1:
        #se cargan las imagenes usando la función 
        return IMAGENES_CARTAS.get(nombre, IMAGENES_CARTAS["carta_de_relleno"])
    #lo mismo pero con el jugador 2
    else:
        return IMAGENES_CARTAS_JUG2.get(nombre, IMAGENES_CARTAS_JUG2["carta_de_relleno"])

#region dibujar tablero

#aca se "dibuja" el tablero
#se le tiene que pasar el jugador actual como parámetro para que pueda mostrar los datos de forma correcta
def dibujar_tablero(jug_act):
    #esto dibuja la ventana
    VENTANA.blit(FONDO, (0, 0))
    #esto limita el tamaño de la imagen del mazo
    VENTANA.blit(MAZO_IMG, (ANCHO - 120, ALTO // 2 - 70))

    #esto muestra las vidas, es simplemente un texto mostrando la cantidad de vidas con len()
    vidas = fuente.render(f"Vidas Jugador 1: {len(vidas_jug_1)} | Vidas Jugador 2: {len(vidas_jug_2)}", True, (255, 255, 255))
    #blit() es lo que le dice a pygame que dibujar
    #(20,20) es el tamaño
    VENTANA.blit(vidas, (20, 20))

    #validación para establecer quien es el rival
    rival = mano_p_2 if jug_act == 1 else mano_p_1
    #esto muestra la cantidad de cartas del rival, pero no lo muestra para simular un "juego"
    cant_cartas_rival = fuente.render(f"Cartas del rival: {len(rival)}", True, (255, 255, 255))
    #aca se dibujan, también se especifica el tamaño
    VENTANA.blit(cant_cartas_rival, (20, 50))

    #guarda en una variable un f-string con quien es el jugador actual, además de los colores (255,255,255 son los valores rgb)
    turno_texto = fuente.render(f"Turno del Jugador {jug_act}", True, (255, 255, 255))
    #se dibuja quien es el jugador actual con blit()
    VENTANA.blit(turno_texto, (ANCHO // 2 - 80, ALTO - 40))

    #se guarda la mano del jugador actual
    #la mano actual, es la del jugador 1, si es su turno, sino es la del 2
    mano = mano_p_1 if jug_act == 1 else mano_p_2
    #se recorren las cartas y se enumeran
    for i, carta in enumerate(mano):
        #se llama a la función para cargar las imagenes
        img = obtener_imagen(carta, jug_act)
        #se muestra la carta por pantalla y se determina las dimensiones
        VENTANA.blit(img, (150 + i * 120, ALTO - 160))


    #esto es para mostrar el nombre de la carta del rival
    #se muestra por dos segundos
    if carta_mostrada and pygame.time.get_ticks() - carta_mostrada_timer < 2000:
        #se muestra el nombre de la carta
        mostrar_texto = fuente.render(f"Carta del rival: {carta_mostrada}", True, (255, 255, 0))
        #se dibuja el texto en pantalla
        VENTANA.blit(mostrar_texto, (ANCHO // 2 - 100, ALTO - 200))

    #se inicializa el juego
    pygame.display.flip()
    #se muestra la mano actual
    return mano

#endregion

#region aca se juega

#Búcle while para jugar
jugando = True
while jugando:
    #el jugador actual es el 1, si el número es par, sino es el 2
    jug_act = 1 if turno % 2 == 0 else 2
    #se muestra la mano del jugador actual
    mano = dibujar_tablero(jug_act)

    #condición de victoria
    #cuando algún jugador se queda sin vidas
    if not vidas_jug_1:
        print("Ganador: Jugador 2")
        #para salir del búcle
        break
    if not vidas_jug_2:
        print("Ganador: Jugador 1")
        break

    #aca se comprueba si algún jugador se quedó sin cartas
    if len(mano) == 0:
        #si no tiene cartas, "roba" 3 del mazo con sample (son randoms)
        nuevas = random.sample(mazo, 3)
        #validación para actualizar la pantalla
        if jug_act == 1:
            #se agregan las cartas a la mano
            mano_p_1.extend(nuevas)
        #lo mismo pero con el jugador 2
        else:
            mano_p_2.extend(nuevas)
        #continua el búcle
        continue

    #region clicks

    #se inicializa una variable como true
    esperando = True
    #se anida un while mientras que la variable sea true
    while esperando:
        #captura los eventos dentro de la pantalla de pygame (los clicks en este caso)
        for evento in pygame.event.get():
            #si se cierra la ventana, se sale de este y el búcle superior (se sale del juego)
            if evento.type == pygame.QUIT:
                jugando = False
                esperando = False
            #si se hace click en algún lugar, se guarda la posición del click
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                #se obtienen las coordenadas del click en la pantalla
                x, y = pygame.mouse.get_pos()
                #se recorre la mano del jugador
                for i, carta in enumerate(mano):
                    #por cada carta, se crea una "zona" clickeable
                    rect = pygame.Rect(150 + i * 120, ALTO - 160, 100, 140)
                    #si se clickea dentro de esa zona
                    if rect.collidepoint(x, y):
                        #se llama a la "carta", que en realidad es una función
                        funcion = carta
                        #se quita la carta de la mano, porque ya se uso
                        mano.pop(i)
                        #validación para ejecutar la lógica de la función (de la carta)
                        if funcion.__name__ == "saltar_turno_del_rival":
                            #esto es porque saltar_turno requiere que se le pase el turno, no el jugador actual
                            turno = funcion(turno)
                        else:
                            #si no se clickea saltar_turno
                            #se le pasa el jugador actual a la función (a la carta) seleccionada
                            funcion(jug_act)
                            #se suma el turno para que sea un "contador"
                            turno += 1

                        #650 milisegundos de espera para que el juego no sea tan "brusco"
                        pygame.time.wait(650)
                        #una vez que se clickeo la carta se sale del búcle anidado
                        esperando = False
                        break
    #esto también evita que el juego corra muy rapido, limitando los frames (en este caso a 60)
    clock.tick(FPS)

    #endregion

#se sale del juego
#esta cierra los módulos abiertos que corren el juego
pygame.quit()
#frena el script de python
sys.exit()

#endregion
