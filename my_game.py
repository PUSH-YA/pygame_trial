import pygame
from sys import exit

#init & global var
pygame.init()
gravity = 1

#create window
WIDTH = 1600
HEIGHT = WIDTH * 9//16
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#game elements
pygame.display.set_caption('game from scratch')
clock = pygame.time.Clock()
font = pygame.font.Font('game_fonts/slkscr.ttf', 50)

#sky
sky_img = pygame.Surface((WIDTH,HEIGHT*3/4))
sky_img.fill((90,150,180))
text_surface = font.render('My Game', False, (250, 250, 250))

#playerA (64 x 64)
playerA_img = pygame.image.load('game_images/player/player.png').convert_alpha() #TODO: FORALL imported imgs 
playerA_rect = playerA_img.get_rect(topleft = (10,HEIGHT/2))
playerA_health = 10
playerA_speed = 10
playerA_gravity = 0
playerA_jump = 20
playerA_attack = False
global facing_rightA 
facing_rightA = True

#weapon
weaponA_img = pygame.Surface((64,32))
weaponA_img.fill('Pink')
weaponA_timer = 20


#playerB
playerB_img = pygame.image.load('game_images/player/player2.png').convert_alpha() #TODO: FORALL imported imgs 
playerB_rect = playerB_img.get_rect(topleft = (1000,HEIGHT/2))
playerB_health = 10
playerB_speed = 10
playerB_gravity = 0
playerB_jump = 20
playerB_attack = False
global facing_rightB 
facing_rightB = True

#weaponB
weaponB_img = pygame.Surface((64,32))
weaponB_img.fill('Pink')
weaponB_timer = 20



#ground
ground_img = pygame.Surface((WIDTH, HEIGHT*1/4))
ground_img.fill((90,90,90))
ground_rect = ground_img.get_rect(topleft = (0,HEIGHT*3/4))

float_ground1_img = pygame.Surface((WIDTH/4, HEIGHT*1/10))
float_ground1_img.fill((90,90,90))
float_ground1_rect = float_ground1_img.get_rect(topleft = (WIDTH/10,HEIGHT*3/4-150))

float_ground2_img = pygame.Surface((WIDTH/4, HEIGHT*1/10))
float_ground2_img.fill((90,90,90))
float_ground2_rect = float_ground2_img.get_rect(topleft = (WIDTH*1/3,HEIGHT*2/6))

float_ground3_img = pygame.Surface((WIDTH/4, HEIGHT*1/10))
float_ground3_img.fill((90,90,90))
float_ground3_rect = float_ground3_img.get_rect(topleft = (900,HEIGHT*3/4-150))


#game functions
def game_restart():
    playerA_rect.x, playerA_rect.y = 10, HEIGHT/2
    global playerA_health; playerA_health = 10
    playerB_rect.x, playerB_rect.y = 1000, HEIGHT/2
    global playerB_health; playerB_health  = 10

def play_again(player):
    if player == 1: winner = "player A WON"; winner_color = (0,79,152)
    else: winner = "player B WON"; winner_color = 'pink'
    winner_text = font.render(winner, 13, (255,255,255))
    play_again = font.render('Play again?', 13, (255,255,255))
    play_againx = WIDTH / 2 - min(play_again.get_width() / 2 , winner_text.get_width() / 2)
    play_againy = HEIGHT / 2 - (play_again.get_height() / 2 + winner_text.get_height() / 2)
    play_againx_size = max(play_again.get_width(),winner_text.get_width())
    play_againy_size = (play_again.get_height() + winner_text.get_height()+ 20)
    print(play_againx_size, play_againy_size)
    pygame.draw.rect(screen, winner_color, ((play_againx - 20, play_againy - 20),
                                               (play_againx_size + 10, play_againy_size +
                                                10)))
    screen.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2,
                       HEIGHT / 2 -30 - winner_text.get_height() / 2))
    screen.blit(play_again, (WIDTH / 2 -play_again.get_width() / 2,
                       HEIGHT / 2 + 30 - play_again.get_height() / 2 ))

    clock = pygame.time.Clock()
    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= play_againx - 5 and x <= play_againx + play_againx_size + 5:
                    if y >= play_againy - 5 and y <= play_againy + play_againy_size + 5:
                        in_main_menu = False
                        print("play again")
                        game_restart()

def playerA_move(keys):
        global facing_rightA
        if keys[pygame.K_d]: playerA_rect.x += playerA_speed; facing_rightA = True
        if keys[pygame.K_a]: playerA_rect.x -= playerA_speed; facing_rightA = False

def playerB_move(keys):
        global facing_rightB
        if keys[pygame.K_RIGHT]: playerB_rect.x += playerB_speed; facing_rightB = True
        if keys[pygame.K_LEFT]: playerB_rect.x -= playerB_speed; facing_rightB = False


def ground_contact(obj_rect):
    if obj_rect.bottom >= ground_rect.top and obj_rect.right >= ground_rect.left and obj_rect.left <= ground_rect.right: return 1
    elif (obj_rect.bottom >= float_ground1_rect.top) and (obj_rect.right >= float_ground1_rect.left) and (obj_rect.left <= float_ground1_rect.right) and (obj_rect.top <= float_ground1_rect.top): return 2
    elif (obj_rect.bottom >= float_ground2_rect.top) and (obj_rect.right >= float_ground2_rect.left) and (obj_rect.left <= float_ground2_rect.right) and (obj_rect.top <= float_ground2_rect.top): return 3
    elif (obj_rect.bottom >= float_ground3_rect.top) and (obj_rect.right >= float_ground3_rect.left) and (obj_rect.left <= float_ground3_rect.right) and (obj_rect.top <= float_ground3_rect.top): return 4
    else: return -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()              
            exit()                      # quit system after pygame
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w and (ground_contact(playerA_rect)> 0)): 
                    playerA_gravity = -playerA_jump
            if (event.key == pygame.K_LSHIFT):
                playerA_attack = True
            if (event.key == pygame.K_UP and (ground_contact(playerB_rect)> 0)): 
                playerB_gravity = -playerB_jump
            if (event.key == pygame.K_PAGEDOWN or event.key == pygame.K_PAGEUP):
                playerB_attack = True
    
    #draw surfaces
    screen.blit(sky_img,(0,0))
    screen.blit(ground_img,ground_rect)
    screen.blit(float_ground1_img, float_ground1_rect)
    screen.blit(float_ground2_img, float_ground2_rect)
    screen.blit(float_ground3_img, float_ground3_rect)
    screen.blit(text_surface, (WIDTH/2-100, 30))
    screen.blit(playerA_img, playerA_rect)
    screen.blit(playerB_img, playerB_rect)

    #player health
    playerA_health_str ="A health: " + str(int(playerA_health))
    playerA_health_text = font.render(playerA_health_str, False, (0,79,152))
    screen.blit(playerA_health_text, (50, 30))
    playerB_health_str = "B health: " + str(int(playerB_health))
    playerB_health_text = font.render(playerB_health_str, False, 'pink')
    screen.blit(playerB_health_text, (WIDTH-450, 30))

    #playerA
    playerA_move(pygame.key.get_pressed())
    playerA_gravity += gravity
    playerA_rect.y += playerA_gravity
    if playerA_rect.right < 0: playerA_rect.left = WIDTH
    if playerA_rect.left > WIDTH: playerA_rect.right = 0
    
    ##bouncy effect
    ground_num = ground_contact(playerA_rect)
    if ground_num > 0: playerA_gravity -= gravity; playerA_rect.y -= playerA_gravity # normal force

    # 1 is ground; 2 is float_grnd1; 3 is float_grnd2; 4 is float_grnd3
    if ground_num == 1:
        playerA_rect.bottom = ground_rect.top
    elif ground_num == 2:
        playerA_rect.bottom = float_ground1_rect.top
    elif ground_num == 3:
        playerA_rect.bottom = float_ground2_rect.top
    elif ground_num == 4:
        playerA_rect.bottom = float_ground3_rect.top
    else: 
        playerA_img_jump = pygame.transform.scale(playerA_img, (64,64-min(playerA_gravity*1.75,0)))
        screen.blit(playerA_img_jump, playerA_rect)

    if playerA_attack:
        if facing_rightA: weaponA_rect = weaponA_img.get_rect(topleft=(playerA_rect.right, playerA_rect.top+15))
        else: weaponA_rect = weaponA_img.get_rect(topright=(playerA_rect.left, playerA_rect.top+15))
        screen.blit(weaponA_img, weaponA_rect)
        weaponA_timer -= 1
        if weaponA_rect.colliderect(playerB_rect): playerB_health -= 0.1
        if weaponA_timer <= 0: playerA_attack = False; weaponA_timer = 20

    #playerB
    playerB_move(pygame.key.get_pressed())
    playerB_gravity += gravity
    playerB_rect.y += playerB_gravity
    if playerB_rect.right < 0: playerB_rect.left = WIDTH
    if playerB_rect.left > WIDTH: playerB_rect.right = 0
    
    ##bouncy effect
    ground_num = ground_contact(playerB_rect)
    if ground_num > 0: playerB_gravity -= gravity; playerB_rect.y -= playerB_gravity # normal force

    # 1 is ground; 2 is float_grnd1; 3 is float_grnd2; 4 is float_grnd3
    if ground_num == 1:
        playerB_rect.bottom = ground_rect.top
    elif ground_num == 2:
        playerB_rect.bottom = float_ground1_rect.top
    elif ground_num == 3:
        playerB_rect.bottom = float_ground2_rect.top
    elif ground_num == 4:
        playerB_rect.bottom = float_ground3_rect.top
    else: 
        playerB_img_jump = pygame.transform.scale(playerB_img, (64,64-min(playerB_gravity*1.75,0)))
        screen.blit(playerB_img_jump, playerB_rect)


    if playerB_attack:
        if facing_rightB: weaponB_rect = weaponB_img.get_rect(topleft=(playerB_rect.right, playerB_rect.top+15))
        else: weaponB_rect = weaponB_img.get_rect(topright=(playerB_rect.left, playerB_rect.top+15))
        screen.blit(weaponB_img, weaponB_rect)
        weaponB_timer -= 1
        if weaponB_rect.colliderect(playerA_rect): playerA_health -= 0.1
        if weaponB_timer <= 0: playerB_attack = False; weaponB_timer = 20

    if playerB_health <= 0:
        play_again(1)
    elif playerA_health <= 0:
        play_again(2)
        

    pygame.display.update() 
    clock.tick(60)                      # max 60fps         


    