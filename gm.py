import pygame
import random
import math
from pygame import mixer

#initialise pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((1000,700))

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',62)


#title
pygame.display.set_caption("Corona kill")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

#bckground sound 
mixer.music.load('GOwav.wav')
mixer.music.play(-1)


#player
medicine = pygame.image.load('player.png')
medicinex = 436
mediciney = 530 

medicinex_change = 0

#virus
virus_image = []
virusx = []
virusy = []
virusx_change = []
virusy_change = []
num_of_viruses = 6
for i in range (num_of_viruses):
	virus_image.append(pygame.image.load('virus.png'))
	virusx.append(random.randint(0,735))
	virusy.append( random.randint(50,150))
	virusx_change.append(2)
	virusy_change.append(40)

#pill
pill_image = pygame.image.load('pill.png')
pillx = 0
pilly = 530
pillx_change = 0
pilly_change = 3
pill_state = "ready"


def player(x,y):
	screen.blit(medicine,(x , y))


def virus(x,y,i):
	screen.blit(virus_image[i],(x , y))

def fire_pill(x,y):
	global pill_state
	pill_state = "fire"
	screen.blit(pill_image,(x + 64 ,y + 30))

def collision(virusx,virusy,pillx,pilly):
	dist = math.sqrt(math.pow((virusx - pillx),2) + math.pow((virusy - pilly),2))
	if dist <= 50:
		return True
	else :
		return False

def show_score(x,y):
	score = font.render("Score  :  "+str(score_value),True,(255,255,0))
	screen.blit(score,(x,y))

def game_over():
	over_text = over_font.render("GAME OVER",True,(0,255,0))
	screen.blit(over_text,(300,200))

running = True
while running:
	screen.fill((0,0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	

		#keystrokes
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				medicinex_change = -2
			if event.key == pygame.K_RIGHT:
				medicinex_change = 2
			if event.key == pygame.K_SPACE:
				if pill_state is "ready":
					pill_sound = mixer.Sound('shoot.wav')
					pill_sound.play()
					pillx = medicinex
					fire_pill(pillx,pilly)


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				medicinex_change = 0
	

	#boundary of player		
	medicinex += medicinex_change
	if medicinex <= 0:
		medicinex = 0
	elif medicinex >= 872:
		medicinex = 872

    #boundary of virus
	for i in range (num_of_viruses):
		#game over
		if virusy[i] >400:
			for j in range (num_of_viruses):
				virusy[j] = 2000
			game_over()
			break
		virusx[i] += virusx_change[i]
		if virusx[i] <= 0:
			virusx_change[i] = 2
		elif virusx[i] >= 872:
			virusx_change[i] = -2
		if virusx[i] <= 0 or virusx[i] >= 872:
			virusy_change[i] = 50
			virusy[i] += virusy_change[i]


		#colision
		is_collision = collision(virusx[i],virusy[i],pillx,pilly)
		if is_collision:
			pilly = 530
			pill_state ="ready" 
			score_value +=1
			virus_sound = mixer.Sound('effectwav.wav')
			virus_sound.play()
			virusx[i] = random.randint(0,735)
			virusy[i] = random.randint(0,150)

		virus(virusx[i],virusy[i],i)


	#PILL MOVEMENT
	if pilly <= 0:
		pilly = 530
		pill_state = "ready"
	if pill_state is "fire":
		fire_pill(pillx,pilly)
		pilly -= pilly_change 	


	player(medicinex,mediciney)
	show_score(textX,textY)
	pygame.display.update()
 