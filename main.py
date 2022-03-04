import pygame, sys, random
import os

from pygame.constants import K_SPACE

#define function
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (600, random_pipe_pos))
    top_pipe =  pipe_surface.get_rect(midbottom = (600, random_pipe_pos - 130))
    return bottom_pipe, top_pipe

def move_pipe(pipes): 
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False     

    if bird_rect.top <= -5 or bird_rect.bottom >= 450:
        can_score = True
        return False

    return True    

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird            
        
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
       score_surface = game_font.render(str(int(score)), True, (255,255,255))
       score_rect = score_surface.get_rect(center = (144,100))
       screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,70))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High Score: {int(score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,415))
        screen.blit(high_score_surface, high_score_rect)

def pipe_score_check():
    global score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105:
                score += 0.5
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

pygame.init()

#screen
WIDTH, HEIGHT = 288, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',30)

#game variables
gravity = 0.5
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

#background image
bg_image = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Assets', 'background-day.png'))

#base image
floor_surface = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Assets', 'base.png'))
floor_x_pos = 0

bird_downflap = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Assets', 'yellowbird-downflap.png'))
bird_midflap = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Assets', 'yellowbird-midflap.png'))
bird_upflap = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Assets', 'yellowbird-upflap.png'))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#bird_surface = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Flappy Bird\Assets', 'yellowbird-midflap.png'))
#bird_rect = bird_surface.get_rect(center = (50, 256))

pipe_surface = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Assets', 'pipe-green.png'))
pipe_list = []
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)
pipe_height = [300,225,250]

game_over_surface = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Assets', 'message.png'))
game_over_rect = game_over_surface.get_rect(center = (144, 256))

message_surface = pygame.image.load(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Assets', 'gameover.png'))
message_rect = message_surface.get_rect(center = (144, 256))

flap_sound = pygame.mixer.Sound(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Sounds', 'sound_sfx_wing.wav'))
score_sound = pygame.mixer.Sound(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Sounds', 'sound_sfx_point.wav'))
death_sound = pygame.mixer.Sound(os.path.join('D:\Ahmad Syahmi\MyProgram\Python\Flappy Bird\Sounds', 'sound_sfx_hit.wav'))

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0       
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0                
                score = 0

        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())
            print("pipe_list")
        
        if event.type == BIRDFLAP:
            if bird_index < 2:
               bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()       

            
    screen.blit(bg_image, (0, 0))
    floor_x_pos -= 1

    if game_active: 

       #bird 
       bird_movement += gravity
       rotated_bird = rotate_bird(bird_surface)
       bird_rect.centery += bird_movement
       screen.blit(rotated_bird, bird_rect)
       game_active = check_collision(pipe_list)

       #pipes
       pipe_list = move_pipe(pipe_list)
       draw_pipes(pipe_list)
       
       #score
       pipe_score_check()
       score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        score_display('game_over')

    #floor
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
    


    pygame.display.update()
    clock.tick(60)