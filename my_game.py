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
sky_img = pygame.image.load('game_images/sky.gif').convert_alpha()
text_surface = font.render('My Game', False, (250, 250, 250))

#playerA (64 x 64)
PlayerA_img = None
playerA_rect = pygame.Rect(50,100,64,64)
playerA_health = 10
playerA_speed = 10
playerA_gravity = 0
playerA_jump = 20
playerA_attack = False
facing_rightA = True


#playerB
playerB_img = None
playerB_rect = pygame.Rect(WIDTH - 100,100,64,64)
playerB_health = 10
playerB_speed = 10
playerB_gravity = 0
playerB_jump = 20
playerB_attack = False
facing_rightB = True

# weapons
weaponA_timer = 20
current_framesA = 0
weaponB_timer = 20
current_framesB = 0


#ground
ground_img = pygame.image.load('game_images/ground.gif').convert_alpha()
ground_rect = ground_img.get_rect(topleft = (0,HEIGHT*3/4))

float_ground1_img = pygame.image.load('game_images/float_ground1.gif').convert_alpha()
float_ground1_rect = float_ground1_img.get_rect(topleft = (WIDTH/10,HEIGHT*3/4-150))

float_ground2_img = pygame.image.load('game_images/float_ground2.gif').convert_alpha()
float_ground2_rect = float_ground2_img.get_rect(topleft = (WIDTH*1/3,HEIGHT*2/6))

float_ground3_rect = float_ground1_img.get_rect(topleft = (900,HEIGHT*3/4-150))


#game functions
def game_restart():
    playerA_rect.x, playerA_rect.y = 100, 100
    global playerA_health; playerA_health = 10
    playerB_rect.x, playerB_rect.y = WIDTH - 100, 100
    global playerB_health; playerB_health  = 10
    

def play_again(player, player1_name, player2_name):
    if player == 1: winner = player1_name + " WON"; winner_color = (0,79,152)
    else: winner = player2_name + " WON"; winner_color = 'pink'
    winner_text = font.render(winner, 1*len(winner), (255,255,255))
    play_again = font.render('Play again?', 13, (255,255,255))
    play_againx = WIDTH / 2 - max(play_again.get_width() / 2 , winner_text.get_width() / 2)
    play_againy = HEIGHT / 2 - (play_again.get_height() / 2 + winner_text.get_height() / 2)
    play_againx_size = max(play_again.get_width(),winner_text.get_width())
    play_againy_size = (play_again.get_height() + winner_text.get_height()+ 20)
    padding = 2*len(winner)
    pygame.draw.rect(screen, winner_color, ((play_againx - padding, play_againy - padding),
                                               (play_againx_size + padding*3.5, play_againy_size + padding)))
    screen.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2,
                       HEIGHT / 2 -30 - winner_text.get_height() / 2))
    screen.blit(play_again, (WIDTH / 2 -play_again.get_width() / 2,
                       HEIGHT / 2 + 30 - play_again.get_height() / 2 ))

    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:
        clock.tick(60)
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

def game_loop(playerA_img, playerB_img, mode, player1_name, player2_name):
    #setup player A for game
    global playerA_health; global playerA_speed; global playerA_gravity; global playerA_jump; global playerA_attack; global facing_rightA
    global weaponA_timer; global current_framesB

    #setup player B for game
    global playerB_health; global playerB_speed; global playerB_gravity; global playerB_jump; global playerB_attack; global facing_rightB
    global weaponB_timer; global current_framesA

    #load weapon animation
    frames = []
    if mode == 1:
        img_path = 'game_images/player/lightening/'
        frames_num = 15
        img_hurt_path = 'game_images/player/player'
    else: 
        img_path = 'game_images/player/special_attack/'
        frames_num = 7
        img_hurt_path = 'game_images/player/special'
    for i in range(frames_num):
        frames.append(pygame.image.load(img_path + "sprite_"+str(i)+".png").convert_alpha())

    #prevent list out of index if previous had a different mode
    current_framesA, current_framesB = (current_framesA)%frames_num, (current_framesB)%frames_num

    #main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()              
                exit()                      # quit system after pygame
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w and (ground_contact(playerA_rect)> 0)): 
                        playerA_gravity = -playerA_jump
                if (event.key == pygame.K_LSHIFT or event.key == pygame.K_e):
                    playerA_attack = True
                if (event.key == pygame.K_UP and (ground_contact(playerB_rect)> 0)): 
                    playerB_gravity = -playerB_jump
                if (event.key == pygame.K_PAGEDOWN or event.key == pygame.K_PAGEUP):
                    playerB_attack = True
                if (event.key == pygame.K_r):
                    choose_option(player1_name, player2_name)
        
        #draw surfaces
        screen.blit(sky_img,(0,0))
        screen.blit(ground_img,ground_rect)
        screen.blit(float_ground1_img, float_ground1_rect)
        screen.blit(float_ground2_img, float_ground2_rect)
        screen.blit(float_ground1_img, float_ground3_rect)
        screen.blit(text_surface, (WIDTH/2-100, 30))
        screen.blit(playerA_img, playerA_rect)
        screen.blit(playerB_img, playerB_rect)

        #player health
        playerA_health_str =player1_name + " health: " + str(int(playerA_health))
        playerA_health_text = font.render(playerA_health_str, False, (0,79,152))
        screen.blit(playerA_health_text, (50, 30))
        playerB_health_str = player2_name+ " health: " + str(int(playerB_health))
        playerB_health_text = font.render(playerB_health_str, False, 'pink')
        screen.blit(playerB_health_text, (WIDTH-max(70*len(player2_name),600), 30))

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
            playerA_img_jump = pygame.transform.scale(playerA_img, (64,64-min(playerA_gravity*2,0)))
            screen.blit(playerA_img_jump, playerA_rect)



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

        #player A attacks
        if playerA_attack:
            if facing_rightA: 
                weaponA_rect = pygame.Rect(playerA_rect.right, playerA_rect.top+15, 64,32)
                screen.blit(frames[current_framesA], weaponA_rect)
            else: 
                weaponA_rect = pygame.Rect(playerA_rect.left-50, playerA_rect.top+15, 64,32)
                screen.blit(pygame.transform.flip(frames[current_framesA], True, False), weaponA_rect)
            pygame.display.flip()
            current_framesA = (current_framesA + 1) % frames_num
            weaponA_timer -= 1
            playerB_hurt_img = pygame.image.load(img_hurt_path+"B_hurt.gif").convert_alpha()
            if weaponA_rect.colliderect(playerB_rect): playerB_health -= 0.1; screen.blit(playerB_hurt_img,playerB_rect)
            if weaponA_timer <= 0: playerA_attack = False; weaponA_timer = 20

        # player B attack
        if playerB_attack:
            if facing_rightB: 
                weaponB_rect = pygame.Rect(playerB_rect.right, playerB_rect.top+15, 64,32)
                screen.blit(frames[current_framesB], weaponB_rect)
            else: 
                weaponB_rect = pygame.Rect(playerB_rect.left-50, playerB_rect.top+15, 64,32)
                screen.blit(pygame.transform.flip(frames[current_framesB], True, False), weaponB_rect)
                
            current_framesB = (current_framesB + 1) % frames_num
            weaponB_timer -= 1
            playerA_hurt_img = pygame.image.load(img_hurt_path+"A_hurt.gif").convert_alpha()
            if weaponB_rect.colliderect(playerA_rect): playerA_health -= 0.1;screen.blit(playerA_hurt_img,playerA_rect)
            if weaponB_timer <= 0: playerB_attack = False; weaponB_timer = 20 

        if playerB_health < 0:
            play_again(1, player1_name, player2_name)
        elif playerA_health < 0:
            play_again(2, player1_name, player2_name)

        pygame.display.update() 
        clock.tick(60)                      # max 60fps         

def how_to_play(player1_name, player2_name):
    play = pygame.Surface((WIDTH,HEIGHT))
    play.fill('Red')
    screen.blit(play, (0,0))

    back_text = font.render('Back', 13, (255,255,255))
    back_textx = 100
    back_texty = HEIGHT  / 5 
    pygame.draw.rect(screen, 'black', ((back_textx - 20, back_texty - 20),
                                            (back_text.get_width() + 30, back_text.get_height() + 30)))
    screen.blit(back_text, (back_textx, back_texty))
        
    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                    choose_option(player1_name, player2_name)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= back_textx - 5 and x <= back_textx + back_text.get_width() + 5:
                    if y >= back_texty - 5 and y <= back_texty + back_text.get_height() + 5:
                        in_main_menu = False
                        choose_option(player1_name, player2_name)
        pygame.display.update()
        clock.tick(60)


def choose_option(player1_name, player2_name):
    screen.blit(sky_img,(0,0))
    screen.blit(ground_img,ground_rect)

    normal_text = font.render('Normal', 13, (255,255,255))
    normal_textx = WIDTH / 3 - normal_text.get_width()
    normal_texty = HEIGHT / 4 
    pygame.draw.rect(screen, (0,79,152), ((normal_textx - 20, normal_texty - 20),
                                               (normal_text.get_width() + 30, normal_text.get_height() + 30)))
    screen.blit(normal_text, (normal_textx,normal_texty))

    special_text = font.render('Special', 13, (255,255,255))
    special_textx = WIDTH *3 / 4 - special_text.get_width()
    special_texty = HEIGHT / 4 
    pygame.draw.rect(screen, 'violet', ((special_textx - 20, special_texty - 20),
                                               (special_text.get_width() + 30, special_text.get_height() + 30)))
    screen.blit(special_text, (special_textx,special_texty))

    instruction_text = font.render('How to play', 13, (255,255,255))
    instruction_textx = (normal_textx + normal_text.get_width() + special_textx) /2 - instruction_text.get_width()/2
    instruction_texty = HEIGHT *3/5 
    pygame.draw.rect(screen, (150,150,150), ((instruction_textx - 20, instruction_texty - 20),
                                               (instruction_text.get_width() + 30,instruction_text.get_height() + 30)))
    screen.blit(instruction_text, (instruction_textx,instruction_texty))

    in_main_menu = True
    while in_main_menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= normal_textx - 5 and x <= normal_textx + normal_text.get_width() + 5:
                    if y >= normal_texty - 5 and y <= normal_texty + normal_text.get_height() + 5:
                        in_main_menu = False
                        playerA_img = pygame.image.load('game_images/player/playerA.gif').convert_alpha() 
                        playerB_img = pygame.image.load('game_images/player/playerB.gif').convert_alpha()
                        game_restart() 
                        game_loop(playerA_img, playerB_img, 1, player1_name, player2_name)
                elif x >= special_textx - 5 and x <= special_textx + special_text.get_width() + 5:
                    if y >= special_texty - 5 and y <= special_texty + special_text.get_height() + 5:
                        in_main_menu = False
                        playerA_img = pygame.image.load('game_images/player/specialA.gif').convert_alpha()
                        playerB_img = pygame.image.load('game_images/player/specialB.gif').convert_alpha()
                        game_restart()        
                        game_loop(playerA_img, playerB_img, 2, player1_name, player2_name)
                elif x >= instruction_textx - 5 and x <= instruction_textx + instruction_text.get_width() + 5:
                    if y >= instruction_texty - 5 and y <= instruction_texty + instruction_text.get_height() + 5:
                        in_main_menu = False
                        how_to_play(player1_name, player2_name)
        pygame.display.update()
        clock.tick(60)
    

# Function to switch active player for name input
def switch_active_player():
    global player1_active, player2_active
    player1_active = not player1_active
    player2_active = not player2_active


def enter_name():

    pygame.init()

    global player1_active
    global player2_active

    # Font settings
    font = pygame.font.Font(None, 40)
    text_color = pygame.Color("White")

    # Input box1 settings
    input_box1_width = 300
    input_box1_height = 50
    input_box1_x = WIDTH // 2 - input_box1_width // 2
    input_box1_y = HEIGHT // 2 - input_box1_height
    input_box1_rect = pygame.Rect(input_box1_x, input_box1_y, input_box1_width, input_box1_height)

    # Input box2 settings
    input_box2_width = 300
    input_box2_height = 50
    input_box2_x = WIDTH // 2 - input_box2_width // 2
    input_box2_y = HEIGHT // 2 + input_box2_height + 30
    input_box2_rect = pygame.Rect(input_box2_x, input_box2_y, input_box2_width, input_box2_height)

    # Player 1 input
    player1_text = ""
    player1_active = True

    # Player 2 input
    player2_text = ""
    player2_active = False

    # Enter name
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player1_active:
                        player1_name = player1_text
                        switch_active_player()
                        player1_text = ""
                    elif player2_active:
                        player2_name = player2_text
                        #duct tape fix bc limited window and dont wanna do dynamic typo
                        choose_option(player1_name[:8], player2_name[:8])
                        pygame.quit()
                        quit()
                elif event.key == pygame.K_BACKSPACE:
                    if player1_active:
                        player1_text = player1_text[:-1]
                    elif player2_active:
                        player2_text = player2_text[:-1]
                else:
                    if player1_active:
                        player1_text += event.unicode
                    elif player2_active:
                        player2_text += event.unicode

        screen.fill(pygame.Color(60,60,60))

        # Render text
        player1_text_surface = font.render("Enter Player 1's name:", True, text_color)
        player2_text_surface = font.render("Enter Player 2's name:", True, text_color)
        screen.blit(player1_text_surface, (input_box1_x, input_box1_y - 50))
        screen.blit(player2_text_surface, (input_box2_x, input_box2_y - 50))

        # Render input boxes
        pygame.draw.rect(screen, pygame.Color((0,79,152)), input_box1_rect)
        pygame.draw.rect(screen, pygame.Color("white"), input_box1_rect, 2)
        pygame.draw.rect(screen, pygame.Color('violet'), input_box2_rect)
        pygame.draw.rect(screen, pygame.Color("white"), input_box2_rect, 2)

        # Render player 1 input text
        player1_input_surface = font.render(player1_text, True, text_color)
        screen.blit(player1_input_surface, (input_box1_x + 5, input_box1_y + 5))

        # Render player 2 input text
        player2_input_surface = font.render(player2_text, True, text_color)
        screen.blit(player2_input_surface, (input_box2_x + 5, input_box2_y + 5))

        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
        
enter_name()

# GAME START



    