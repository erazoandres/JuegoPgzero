import pgzrun
import random
import os

WIDTH = 700
HEIGHT = 600

os.environ['SDL_VIDEO_CENTERED'] = '1'

enemigos = []
joyas = []
game_over = False
recolectar = 0
esquivados = 0
joyas_requeridas = 5

fondo = Actor("fondo")
personaje = Actor("personaje", (100,100))
silueta = Actor("silueta",((WIDTH//2) ,HEIGHT//2  + 150))
item = Actor("joya1_item")
boss = Actor("boss")
personaje2 = Actor("personaje2" , ((WIDTH//2) ,HEIGHT//2))
personaje3 = Actor("personaje3" , ((WIDTH//2) + 150 ,HEIGHT//2))

modo = "menu"


enemigo_asesino = ""
win = 0

def draw():
    fondo.draw()
    item.pos = ((WIDTH//2) -110 , HEIGHT//2 + 150)

    if modo == "juego":
    
        if game_over != True:
            personaje.draw()

            for enemigo in enemigos:
                enemigo.draw()

            for joya in joyas:
                joya.draw()

            screen.draw.text("JOYAS: " + str(recolectar) , (10,10) , fontsize = 30)
            screen.draw.text("Esquivados: " + str(esquivados) , (10,40) , fontsize = 30)

        elif win == 1:
            item.draw()
            screen.draw.text("GANASTE!" , ((WIDTH//2) -110 , HEIGHT//2) , fontsize = 52)
            screen.draw.text(str(recolectar) , ((WIDTH//2) -120 , HEIGHT//2 + 130) , fontsize = 52)


        else:
            item.draw()
            screen.draw.text("GAME OVER" , ((WIDTH//2) -110 , HEIGHT//2) , fontsize = 52)
            screen.draw.text("Te toco un personaje: " , ((WIDTH//2) -180 , (HEIGHT//2) + 30) , fontsize = 52)
            screen.draw.text(str(recolectar) , ((WIDTH//2) -120 , HEIGHT//2 + 130) , fontsize = 52)

            silueta.draw()
            enemigo_asesino.pos = ((WIDTH//2),HEIGHT//2  + 150)
            enemigo_asesino.draw()

    elif modo == "menu":
        personaje.pos = ((WIDTH//2 - 150) ,HEIGHT//2)
        personaje.draw()
        personaje2.draw()
        personaje3.draw()

def cargar_imagenes():
    global enemigos

    for i in range(1,43): #42 imagenes a cargar
        enemigo = Actor(str("enemigo"+ str(i)))
        enemigo.pos = (random.randint(900,12000) , random.randint(0,700))
        enemigo.speed = random.randint(5,10)
        enemigos.append(enemigo)


    for i in range(10): #5 imagenes a cargar
        joya = Actor("joya1", (random.randint(900,12000) , random.randint(0,700)))
        joya2 = Actor("joya2", (random.randint(900,12000) , random.randint(0,700)))
        joyas.append(joya)
        joyas.append(joya2)

def on_key_down():
    if keyboard.w or keyboard.up: 
        personaje.y -= 30
    if keyboard.s or keyboard.down: 
        personaje.y += 30

def colisiones():
    global game_over , recolectar , joyas , enemigo_asesino

    for i in range(len(enemigos)):
        if personaje.colliderect(enemigos[i]):
            enemigo_asesino = enemigos[i]
            game_over = True
            save(username,recolectar)
            break
        

    for i in range(len(joyas)):
        if personaje.colliderect(joyas[i]):
            recolectar += 1
            joyas.pop(i)
            break

def mover_enemigos():

    global joyas , esquivados , enemigos

    for j in range(len(enemigos)):
        if enemigos[j].x > -60:
            enemigos[j].x -= 5
        else:
            enemigos.pop(j)
            esquivados += 1
            break
            

    #movimiento de joyas

    for i in range(len( joyas)):
        if joyas[i].x > -60:
            joyas[i].x -= 5
        else: 
           joyas.pop(i)
           break
        
def verificacion_partida():
    global win , game_over
    if recolectar >= joyas_requeridas and esquivados >= 42:
        win = 1
        
        game_over = True

def update():

    verificacion_partida()
    if game_over != True:
        mover_enemigos()
        colisiones()
    
def save(username , recolectar):
    with open('saves.txt' , 'a+') as archivo:
        archivo.write(username+ " : " + str(recolectar) + "\n")

def on_mouse_down(button , pos):

    global modo
    if modo == "menu" and personaje.collidepoint(pos):
        modo = "juego"

    elif modo == "menu" and personaje2.collidepoint(pos):
        personaje.image = "personaje2"
        modo = "juego"

    elif modo == "menu" and personaje3.collidepoint(pos):
        personaje.image = "personaje3"
        modo = "juego"


#INICIO DE BLOQUE DE CODIGO
cargar_imagenes()

username = input("Ingrese un nombre de usuario para poder continuar: ")

pgzrun.go()