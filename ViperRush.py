import pygame
import random
import os

pygame.init()
pygame.mixer.init()

eat_sound = pygame.mixer.Sound('eat.mp3')


#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (147,242,137)
blue = (23 , 100,212)
snake_col = (133, 29, 224)

screen_width = 900
screen_height = 600
hiscore = 0
hiscoreData =[0,0,0]
 
level = "Medium"
snake_speed = {"Easy":7 , "Medium":10,"Hard":20}

gameWindow = pygame.display.set_mode((screen_width , screen_height))
pygame.display.set_caption("Viper Rush")
pygame.display.update()

#images
bgimg = pygame.image.load('grass.jpg')
bgimg = pygame.transform.scale(bgimg , (screen_width,screen_height)).convert_alpha()

game_over_img = pygame.image.load('end.jpg')
game_over_img = pygame.transform.scale(game_over_img , (screen_width,screen_height)).convert_alpha()

homeimg = pygame.image.load('home.jpg')
homeimg = pygame.transform.scale(homeimg , (screen_width,screen_height)).convert_alpha()

settingsimg = pygame.image.load('settings.jpg')
settingsimg = pygame.transform.scale(settingsimg , (100,100)).convert_alpha()

font = pygame.font.SysFont(None , 50)
smallFont = pygame.font.SysFont(None , 40)
clock = pygame.time.Clock()

def text_screen(text , color , x, y,bgcol = None,small = False):
    if(small):
        screen_text = smallFont.render(text , True,color , bgcol)
    else:
        screen_text = font.render(text , True,color , bgcol)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow , color , snake_list , snake_size):
    n = len(snake_list)
    for x,y in snake_list[:-1]:
        pygame.draw.rect(gameWindow,color,[x , y , snake_size , snake_size],border_radius=8)
    pygame.draw.rect(gameWindow,black,[snake_list[n-1][0] , snake_list[n-1][1] , snake_size , snake_size],border_radius=8)

def plot_levels():
    pygame.draw.rect(gameWindow,red,[250,200,400,75],border_radius=50)
    pygame.draw.rect(gameWindow,red,[250,300,400,75],border_radius=50)
    pygame.draw.rect(gameWindow,red,[250,400,400,75],border_radius=50)
    text_screen("Select Game Level",white,300,120)
    text_screen(f"Easy\tHiscore:{hiscoreData[0]}",white,300,220)
    text_screen(f"Medium\tHiscore:{hiscoreData[1]}",white,290,320)
    text_screen(f"Hard\tHiscore:{hiscoreData[2]}",white,300,420)
    text_screen("Press (1) for easy, (2) for medium and (3) for hard",white,150,520,small=True)

def levels():
    global level
    level_select = True

    while level_select:
        gameWindow.fill(green)
        plot_levels()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = "Easy"
                    level_select = False
                if event.key == pygame.K_2:
                    level = "Medium"
                    level_select = False
                if event.key == pygame.K_3:
                    level = "Hard"
                    level_select = False


        pygame.display.update()
        clock.tick(30) 


def welcome():
    exit_game = False
    global hiscore
    global hiscoreData
    if not os.path.exists('hiscore.txt'):
        with open('hiscore.txt','w') as f:
            f.write('0 0 0')
    with open('hiscore.txt') as f:
        hiscoreData = f.read().split()
        hiscore = hiscoreData[0] if level == "Easy" else hiscoreData[1] if level == "Medium"  else hiscoreData[2]


    while not exit_game:
        gameWindow.fill(green)
        gameWindow.blit(homeimg , (0,0))
        gameWindow.blit(settingsimg , (775,40))
        text_screen("(Press Space to play)" , white , 270,550)
        text_screen("Level :"+level , white , 700,180,small=1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()
            elif event.type == pygame.MOUSEMOTION:
                if event.pos[0] >= 775 and event.pos[0] <=875 and event.pos[1]>=40 and event.pos[1]<=140:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 775 and event.pos[0] <=875 and event.pos[1]>=40 and event.pos[1]<=140:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    levels()
                    if not os.path.exists('hiscore.txt'):
                        with open('hiscore.txt','w') as f:
                            f.write('0 0 0')
                    with open('hiscore.txt') as f:
                        hiscoreData = f.read().split()
                        hiscore = hiscoreData[0] if level == "Easy" else hiscoreData[1] if level == "Medium"  else hiscoreData[2]
                    

        pygame.display.update()
        clock.tick(30) 
    
    pygame.quit()
    quit()
        
def gameloop():
    #game vars
    exit_game = False
    game_over = False
    score =0
    snake_x = 45
    snake_y = 55
    snake_size = 20
    fps = 30
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20,screen_width-20)
    food_y = random.randint(20,screen_height-20)
    snake_length = 1
    snake_list = []
    global hiscore
    global hiscoreData


    while not exit_game:
        if game_over:
            gameWindow.fill(green)
            gameWindow.blit(game_over_img , (0,0))

            if score > int(hiscore):
                text_screen("New Hiscore : "+str(score) , blue , 300,300)
                with open('hiscore.txt' , 'w') as f:
                    if level == "Easy":
                        f.write(str(score)+' '+hiscoreData[1]+' '+hiscoreData[2])
                    elif level == "Medium":
                        f.write(hiscoreData[0]+' '+str(score)+' '+hiscoreData[2])
                    else:
                        f.write(hiscoreData[0]+' '+hiscoreData[1]+' '+str(score))
            else:
                text_screen("Score : "+str(score) , blue , 350,300)

            text_screen("Press Space to Continue" , blue , 270,350)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT and velocity_x >=0:
                        velocity_x = snake_speed[level]
                        velocity_y = 0
                    if event.key == pygame.K_LEFT and velocity_x <=0:
                        velocity_x = -snake_speed[level]
                        velocity_y = 0
                    if event.key == pygame.K_UP and velocity_y <=0:
                        velocity_y = -snake_speed[level]
                        velocity_x =0
                    if event.key == pygame.K_DOWN and velocity_y >=0:
                        velocity_y = snake_speed[level]
                        velocity_x =0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x) < 16 and abs(snake_y-food_y) < 16:
                score += 10
                food_x = random.randint(20,screen_width-20)
                food_y = random.randint(20,screen_height-20)
                snake_length += 5
                eat_sound.play()


            gameWindow.fill(green)
            gameWindow.blit(bgimg , (0,0))
            text_screen("Score : "+str(score)+" Hiscore : "+hiscore , red,5 ,5,(51,255,255))
            pygame.draw.rect(gameWindow , red , [food_x , food_y , snake_size , snake_size],border_radius=10)


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if(len(snake_list) > snake_length):
                del snake_list[0]

            if head in snake_list[:-1]:
                pygame.mixer.music.load('over.wav')
                pygame.mixer.music.play()
                game_over = True
            
            if snake_x<0 or snake_y<0 or snake_x > screen_width or snake_y>screen_height:
                pygame.mixer.music.load('over.wav')
                pygame.mixer.music.play()
                game_over = True
            
            plot_snake(gameWindow , snake_col , snake_list , snake_size)
        
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()