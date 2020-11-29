import pygame
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

#functions
def playermove():
    player.y += p_speed
    if player.top <=0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT
    if opp.top <=0:
        opp.top = 0
    if opp.bottom >= HEIGHT:
        opp.bottom = HEIGHT

def opp_ai():
    global opp_speed
    if ball.x > WIDTH/1.8 and ball_speed_x >= -1:        
        if opp.top + 70 >= ball.top:
            opp.top -= opp_speed
        if opp.top + 70 < ball.top:
            opp.top += opp_speed

def ballmove():
    global ball_speed_x, ball_speed_y, player_score, opp_score
    ball.y += ball_speed_y
    ball.x += ball_speed_x
    
    if ball.y <= 0 or ball.y >= HEIGHT - ball_speed_y - 27:
        pygame.mixer.Sound.play(wall_sound)
        ball_speed_y *= -1

    if ball.x <= -40:
        opp_score +=1
        pygame.mixer.Sound.play(score_sound)
        ball_speed_x *= -1
        ball_reset()
    
    if ball.x >= WIDTH + 10:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_speed_x *= -1
        ball_reset()

    if ball.colliderect(player) and ball_speed_x < 0:
        if abs(ball.left - player.right) < 10:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_x *= -1
        elif abs(ball.top - player.bottom) < 0 and abs(ball.bottom - player.top) < 0 :
            ball_speed_y *= -1

    if ball.colliderect(opp) and ball_speed_x > 0:
        if abs(ball.right - opp.left) < 10:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_x *= -1
        elif abs(ball.top - player.bottom) < 0 and abs(ball.bottom - player.top) < 0 :
            ball_speed_y *= -1
def ball_reset():
    global ball_speed_x, ball_speed_y, reset, score_time
    ball.center = (WIDTH/2, HEIGHT/2) 
    ball_speed_x *= random.choice((-1,1))
    ball_speed_y *= random.choice((-1,1))
    pygame.time.delay(200)
    reset = 1
    

#setup
clock = pygame.time.Clock()
FPS = 100
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')
run = True

#colors
BG_GREY = (30,30,40)
WHITE = (220,220,220)

#fonts
mainfont = pygame.font.Font("freesansbold.ttf", 40)

#gameobjects
ball = pygame.Rect(WIDTH//2 - 15, HEIGHT//2 - 15, 30, 30)
player = pygame.Rect(20, HEIGHT//2 - 70, 10, 140)
opp = pygame.Rect(WIDTH - 30, HEIGHT//2 - 70, 10, 140)

#gamevariables
xrand = random.random()
yrand = random.random()
speed = 10
ball_speed_x = (7 + xrand) * random.choice((-1,1))
ball_speed_y = (8 + yrand) * random.choice((-1,1))
player_score = 0
opp_score = 0
press = 0
xdir = 1
ydir = 1
pdir = 0
p_speed = 0
opp_speed = 6
reset = 0

#sound
pong_sound = pygame.mixer.Sound("pong.ogg")
wall_sound = pygame.mixer.Sound("wall.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

#pygame.mixer.music.load("SynthwaveJam.mp3")
#pygame.mixer.music.play(2,0.0)
#gameloop
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                p_speed += speed

            if event.key == pygame.K_UP:
                p_speed -= speed   
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                p_speed -= speed

            if event.key == pygame.K_UP:
                p_speed += speed   
    
    #gamelogic
    ballmove()
    playermove()
    opp_ai()

    #redraw
    screen.fill(BG_GREY)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opp)
    pygame.draw.aaline(screen, WHITE, (WIDTH/2,0), (WIDTH/2,HEIGHT))
    if player_score <= 9: player_scr = "0" + str(player_score)
    else:  player_scr = str(player_score)
    if opp_score <= 9: opp_scr = "0" + str(opp_score)
    else :  opp_scr = str(opp_score)     
           
    player_text = mainfont.render(player_scr, 1, WHITE)
    screen.blit(player_text, (WIDTH//2 - 80, 20))
    opp_text = mainfont.render(opp_scr, 1, WHITE)
    screen.blit(opp_text, (WIDTH//2 + 35, 20))
    pygame.display.update()

    if reset == 1:
        pygame.time.delay(400)
        reset = 0
        
    
pygame.quit()