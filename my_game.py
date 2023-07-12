import pygame
from sys import exit

#init & global var
pygame.init()
gravity = 3

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

#ground
ground_img = pygame.Surface((WIDTH, HEIGHT*1/4))
ground_img.fill((90,90,90))
ground_rect = ground_img.get_rect(topleft = (0,HEIGHT*3/4))

#player (64 x 64)
player_img = pygame.image.load('game_images/player/player.png').convert_alpha() #TODO: FORALL imported imgs 
player_rect = player_img.get_rect(topleft = (10,HEIGHT/2))
player_speed = 10
player_gravity = 0

#game functions
def game_restart():
    player_rect.x, player_rect.y = 10, HEIGHT/2

def play_again():
    play_again = font.render('Play again?', 13, (255,255,255))
    play_againx = WIDTH / 2 - play_again.get_width() / 2
    play_againy = HEIGHT / 2 - play_again.get_height() / 2
    play_againx_size = play_again.get_width()
    play_againy_size = play_again.get_height()
    pygame.draw.rect(screen, (10, 10, 10), ((play_againx - 5, play_againy - 5),
                                               (play_againx_size + 10, play_againy_size +
                                                10)))

    screen.blit(play_again, (WIDTH / 2 -play_again.get_width() / 2,
                       HEIGHT / 2 - play_again.get_height() / 2))

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

def player_move(keys):
        if keys[pygame.K_d]: player_rect.x += player_speed
        if keys[pygame.K_a]: player_rect.x -= player_speed

def ground_contact(obj_rect):
    return obj_rect.bottom >= HEIGHT*3/4  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()              
            exit()                      # quit system after pygame
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w and ground_contact(player_rect)): 
                    player_gravity = -20
    
    #draw surfaces
    screen.blit(sky_img,(0,0))
    screen.blit(ground_img,ground_rect)
    screen.blit(text_surface, (WIDTH/2-100, 30))

    #player
    # if player_rect.colliderect(): #TODO
        # play_again()
    player_move(pygame.key.get_pressed())
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.right < 0: player_rect.left = WIDTH
    if player_rect.left > WIDTH: player_rect.right = 0
    ##bouncy effect
    if ground_contact(player_rect): 
        player_rect.bottom = HEIGHT*3/4
        screen.blit(player_img, player_rect)
    else: 
        player_img_jump = pygame.transform.scale(player_img, (64,64-min(player_gravity*2,0)))
        screen.blit(player_img_jump, player_rect)
        

    pygame.display.update() 
    clock.tick(60)                      # max 60fps         


    