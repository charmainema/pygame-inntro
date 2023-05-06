# import modules
import pygame
import os
from PIL import Image
import sys

# initialize game
pygame.init()
pygame.mixer.init()

# change directory to assets folder
os.chdir(os.path.join("assets")) 

# set window
window_width = 1350
window_height = 700
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("The Attack of the New York Rat")

# set background
background_alley_origin = (0, -120)
background_water_origin = (0, 120)
border_color = pygame.Color(153, 170, 196)

# set characters
player1_origin_x, player1_origin_y = 850, 500
player2_origin_x, player2_origin_y = 300, 100
player_width, player_height = 125, 100
player_size = (player_width, player_height)
x_velocity = 60
y_velocity = 60
# hitbox
player1_hitbox = pygame.Rect(player1_origin_x, player1_origin_y, player_width, player_height)
player2_hitbox = pygame.Rect(player2_origin_x, player2_origin_y, player_width, player_height)
# player health
player_health = 100
healthbar_width, healthbar_height = 404, 24
player1_healthbar = pygame.Rect(28, 28, healthbar_width, healthbar_height)
player1_healthbar_outline = pygame.Rect(25, 25, 410, 30)
player2_healthbar = pygame.Rect(918, 648, healthbar_width, healthbar_height)
player2_healthbar_outline = pygame.Rect(915, 645, 410, 30)

# assign fonts
sigmar_regular = os.path.join("fonts", "Sigmar-Regular", "Sigmar-Regular.ttf")
roboto_condensed = os.path.join("fonts", "Roboto-Condensed", "RobotoCondensed-Bold.ttf")

# set game mechanics
# pizzashot
pizzashot_dmg = 5
pizza_velocity = 180
pizza_bullet = []
#snickershot
snickershot_dmg = 5
snicker_velocity = -180
snicker_bullet = []
# player hit
player1_hit = pygame.USEREVENT + 1
player2_hit = pygame.USEREVENT + 2
player1_target_hit = pygame.USEREVENT + 3
player2_target_hit = pygame.USEREVENT + 4
# bullets
bullet_width, bullet_height = 100, 100
max_bullets = 2

# set sounds
# intro sound
intro_sound = pygame.mixer.Sound(os.path.join("sfx", "intro-sound.mp3"))
# bgm
game_bgm = pygame.mixer.Sound(os.path.join("sfx", "hipjazz.mp3"))
instructions_bgm = pygame.mixer.Sound(os.path.join("sfx", "jazzyfrenchy.mp3"))
# bullet sounds
bullet_sound = pygame.mixer.Sound(os.path.join("sfx", "bullet.mp3"))
pizza_bullet_hit = pygame.mixer.Sound(os.path.join("sfx", "pizza-bullet-hit.mp3"))
snicker_bullet_hit =pygame.mixer.Sound(os.path.join("sfx", "snicker-bullet-hit.mp3"))
# win sounds
player1_win_sound = pygame.mixer.Sound(os.path.join("sfx", "duck-win.mp3"))
player2_win_sound = pygame.mixer.Sound(os.path.join("sfx", "rat-win.mp3"))

# set game
framerate = 60
clock = pygame.time.Clock()

class create:
    class file:
        # check for existence and create folder
        def file(filename):
            if os.path.exists(os.path.join(filename)) == False:
                os.mkdir(os.path.join(filename))        
    class image:
        # create resized image
        def resize(image, filename, size):
            image_name = image.split("\\")[-1]
            create.file.file(filename)
            Image.open(image).resize(size).save(os.path.join(filename, image_name))
        
        # loop through folder to create all resized images
        def resizeImages(original_filename, filename, size):
            for i in os.listdir(os.path.join(original_filename)):
                create.image.resize(os.path.join(original_filename, i), filename, size)

        def list_images(filename):
            all_backgrounds = []
            for i in os.listdir(os.path.join(filename)):
                all_backgrounds.append(os.path.join(filename, i))
            return all_backgrounds 
        
    class player:
        def __init__(self, name, graphic, right_graphic, left_graphic, x_velocity, \
        y_velocity, character_size, left_key, right_key, up_key, down_key, top_limit, \
        bottom_limit, left_limit, right_limit, hitbox, health, healthbar, \
        healthbar_outline, healthbar_color, healthtext_color, name_pos, attack_key, attack, \
        player_hit, target_hit, num_targets, num_targets_pos):
            self.name = name
            self.graphic = graphic
            self.right_graphic = right_graphic
            self.left_graphic = left_graphic
            self.x_velocity = x_velocity
            self.y_velocity = y_velocity
            self.character_size = character_size
            self.right_key = right_key
            self.left_key = left_key
            self.up_key = up_key
            self.down_key = down_key
            self.top_limit = top_limit
            self.bottom_limit = bottom_limit
            self.left_limit = left_limit
            self.right_limit = right_limit
            self.hitbox = hitbox
            self.health = health
            self.healthbar = healthbar
            self.healthbar_outline = healthbar_outline
            self.healthbar_color = healthbar_color
            self.name_pos = name_pos
            self.healthtext_color = healthtext_color
            self.attack_key = attack_key
            self.attack = attack
            self.player_hit = player_hit
            self.target_hit = target_hit
            self.num_targets = num_targets
            self.num_targets_pos = num_targets_pos

    class target:
        def __init__(self, sprite, velocity):
            self.sprite = sprite
            self.velocity = velocity

    class mechanics:
        class attack:
            def __init__(self, bullet_sprite, dmg, bullet_velocity, bullets):
                self.bullet_sprite = bullet_sprite
                self.dmg = dmg
                self.bullet_velocity = bullet_velocity
                self.bullets = bullets

# create resized backgrounds
create.image.resizeImages("backgrounds", "backgrounds-resized", window_size)

# check whether backgrounds were converted
try:
    background_water = os.path.join("backgrounds-resized", "water.png")
    background_alley = os.path.join("backgrounds-resized", "alley.png")
    background_intro = os.path.join("backgrounds-resized", "intro-img.png")
except:
    print("Error: image not converted")

# create resized player images
create.image.resizeImages(os.path.join("character-assets", "original"), \
    os.path.join("character-assets", "characters-resized"), player_size)

# character images
images = {
    "player1-right": os.path.join("character-assets", "characters-resized", "rubber-duck.png"),
    "player1-left": os.path.join("character-assets", "characters-resized-mirrored", "rubber-duck-left.png"),
    "player2": os.path.join("character-assets", "characters-resized", "new-york-rat.png"),
    "player2-left": os.path.join("character-assets", "characters-resized-mirrored", "new-york-rat-left.png"),
    "pizzashot": os.path.join("player-attacks", "pizzashot.png"),
    "snickershot": os.path.join("player-attacks", "snickershot.png")
}

# create attacks
pizzashot_attack = create.mechanics.attack(
    images["pizzashot"],
    pizzashot_dmg,
    pizza_velocity,
    pizza_bullet
) 

snickershot_attack = create.mechanics.attack(
    images["snickershot"],
    snickershot_dmg,
    snicker_velocity,
    snicker_bullet
) 

# assign players
player1 = create.player(
    "Player 1",
    images["player1-right"],
    images["player1-right"], 
    images["player1-left"],
    x_velocity,
    y_velocity,
    player_size, 
    pygame.K_j, 
    pygame.K_l, 
    pygame.K_i, 
    pygame.K_k,
    window_height // 2 + player1_hitbox.height // 2,                # top limit
    window_height - Image.open(images["player1-right"]).height,     # bottom limit
    0,                                                              # left limit
    window_width - Image.open(images["player1-right"]).width,       # right limit
    player1_hitbox,
    player_health,
    player1_healthbar,
    player1_healthbar_outline,
    pygame.Color(255, 122, 142),
    "black",
    (918, 615),
    pygame.K_7, 
    snickershot_attack,
    player1_hit,
    player1_target_hit,
    0,
    (window_width - 380, window_height - 70))

player2 = create.player(
    "Player 2",
    images["player2"],
    images["player2"],
    images["player2-left"], 
    x_velocity,
    y_velocity, 
    player_size,
    pygame.K_d, 
    pygame.K_g, 
    pygame.K_r, 
    pygame.K_f,
    0,                                                              # top limit
    window_height // 2 - player2_hitbox.height,                     # bottom limit
    0,                                                              # left limit
    window_width - Image.open(images["player2"]).width,             # right limit
    player2_hitbox,
    player_health,
    player2_healthbar,
    player2_healthbar_outline,
    pygame.Color(136, 255, 117),
    "white",
    (30, 60),
    pygame.K_SPACE,
    pizzashot_attack,
    player2_hit,
    player2_target_hit,
    0,
    (50, window_height - 70))

# render graphics
class render:
    class graphics:
        def background_img(background_img, coordinate):
            pygame.Surface.blit(
                screen, 
                pygame.image.load(background_img), 
                coordinate)

        def border(color):
            # define border
            border = pygame.Rect(
                0, 
                window_height / 2 + 15, 
                window_width, 
                10)
            # draw border
            pygame.Surface.fill(screen, color, border)
    
        def player_sprite(player_graphic, coordinate):
            player_graphic = pygame.image.load(player_graphic)
            pygame.Surface.blit(screen, player_graphic, coordinate)
        
        def health_text(player, string, position):
            font = pygame.font.Font(roboto_condensed, 20)
            text = pygame.font.Font.render(font, string, False, player.healthtext_color)
            pygame.Surface.blit(screen, text, position)

        def health(player):
            # render healthbar
            pygame.draw.rect(screen, "black", player.healthbar_outline)
            pygame.draw.rect(screen, player.healthbar_color, player.healthbar)
            # render text
            render.graphics.health_text(player, f"{str(player.health)}%", \
                (player.healthbar_outline.left + 10, player.healthbar_outline.top + 2))
            render.graphics.health_text(player, player.name, player.name_pos)
        
        def bullets(player):
            for bullet in player.attack.bullets:
                pygame.Surface.blit(screen, pygame.transform.scale(pygame.image.load(player.attack.bullet_sprite), (bullet_width, bullet_height)), bullet)

        # render all graphics
        def all_graphics():
            render.graphics.background_img(background_alley, background_alley_origin)
            render.graphics.background_img(background_water, background_water_origin)
            render.graphics.health(player1)
            render.graphics.health(player2)
            render.graphics.player_sprite(player2.graphic, (player2.hitbox.x, player2.hitbox.y))
            render.graphics.player_sprite(player1.graphic, (player1.hitbox.x, player1.hitbox.y))
            render.graphics.bullets(player1)
            render.graphics.bullets(player2)
            pygame.display.update()

    class mechanics:
        class movement:
            def player(player):
                keys_pressed = pygame.key.get_pressed()
                # handle input (move player and player's hitbox)
                if keys_pressed[player.left_key] and player.hitbox.x >= player.left_limit:
                    player.hitbox.left -= player.x_velocity
                    player.graphic = player.left_graphic
                if keys_pressed[player.right_key] and player.hitbox.x <= player.right_limit:
                    player.hitbox.left += player.x_velocity
                    player.graphic = player.right_graphic
                if keys_pressed[player.up_key] and player.hitbox.y >= player.top_limit:
                    player.hitbox.top -= player.x_velocity
                if keys_pressed[player.down_key] and player.hitbox.y <= player.bottom_limit:
                    player.hitbox.top += player.x_velocity
  
        class attack:
            class player:
                def bullet_control(player, enemy):
                    for bullet in player.attack.bullets:
                        bullet.y += player.attack.bullet_velocity
                        if enemy.hitbox.colliderect(bullet):
                            pygame.event.post(pygame.event.Event(player.player_hit))
                            player.attack.bullets.remove(bullet)
                        elif bullet.y > window_height or bullet.y < 0:
                            player.attack.bullets.remove(bullet)

                def Attack(player, event):
                    # handle input
                    if event.key == player.attack_key and len(player.attack.bullets) < max_bullets:
                        bullet = pygame.Rect(player.hitbox.x, player.hitbox.y, bullet_width, bullet_height)
                        player.attack.bullets.append(bullet)
                        bullet_sound.play()
                      
# animate scenes
class animate:
    def intro():
        # stop previous sounds
        player1_win_sound.stop()
        player2_win_sound.stop()
        # play intro sound
        intro_sound.play()
        clock.tick(framerate)
        # animate text movement
        x = 1
        text_y = 300
        text_x = 400
        size = 20
        for i in range(10):
            # scale size at x^2
            size = int(x) ^ 2
            title_font = pygame.font.Font(sigmar_regular, size)
            text = pygame.font.Font.render(title_font, "The Attack of the New York Rat", False, "black")
            # draw text
            render.graphics.background_img(background_intro, (0, 0))
            pygame.Surface.blit(screen, text, (text_x, text_y))
            pygame.display.flip()
            pygame.time.delay(80)
            x += 5
            # reposition text to center of screen
            text_x -= size // 2 

        pygame.time.delay(500)
        # break intro animation
        proceed = True
        while proceed:
            # render text
            font2 = pygame.font.Font(sigmar_regular, 20)
            text2 = pygame.font.Font.render(font2, "(Press ESCAPE to continue)", False, "black")
            pygame.Surface.blit(screen, text2, (520, 400))
            pygame.display.flip()

            # terminate program if window is closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    proceed = False
        
        # game instruction screen
        instructions_bgm.play()
        proceed = True
        while proceed:
            font2 = pygame.font.Font(sigmar_regular, 50)
            font3 = pygame.font.Font(sigmar_regular, 30)
            text3 = pygame.font.Font.render(font2, "INSTRUCTIONS:", False, "white")
            text4 = pygame.font.Font.render(font3, "Player 1: Use keys 'RDFG' to move", False, "white")
            text5 = pygame.font.Font.render(font3, "Use '7' to fire.", False, "white")
            text6 = pygame.font.Font.render(font3, "Player 2: Use keys 'IJKL' to move.", False, "white")
            text7 = pygame.font.Font.render(font3, "Use 'SPACE' to fire.", False, "white")
            text8 = pygame.font.Font.render(font3, "(Press ESCAPE to continue)", False, "white")
            
            # draw screen
            pygame.Surface.fill(screen, "blue")
            pygame.Surface.blit(screen, text3, (window_width // 2 - text3.get_width() // 2, 100))
            pygame.Surface.blit(screen, text4, (window_width // 2 - text4.get_width() // 2, 230))
            pygame.Surface.blit(screen, text5, (window_width // 2 - text5.get_width() // 2, 260))
            pygame.Surface.blit(screen, text6, (window_width // 2 - text6.get_width() // 2, 350))
            pygame.Surface.blit(screen, text7, (window_width // 2 - text7.get_width() // 2, 380))
            pygame.Surface.blit(screen, text8, (window_width // 2 - text8.get_width() // 2, 460))
            pygame.display.flip()

            # terminate program if window is closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    proceed = False
                    instructions_bgm.stop()
        
    def win_loss(player1_win, player2_win):
        # play sound
        if player1_win == 1:
            player1_win_sound.play()
        elif player2_win == 1:
            player2_win_sound.play()

        # draw winner screen
        proceed = True
        while proceed:
            text_font = pygame.font.Font(sigmar_regular, 50)
            quote_font = pygame.font.Font(sigmar_regular, 30)
            continue_text = pygame.font.Font.render(quote_font, "(Press ESCAPE to continue)", False, "white")
            # blit win screen based on winner
            if player1_win == 1:           
                # draw background
                pygame.Surface.blit(screen, pygame.image.load(os.path.join("win-loss-screen", "rat-lose.png")), (0, 0))
                # draw text
                text = "Player 1 wins!"
                quote = "\"You're not you when you're hungry.\" -rubber duck"
                render_text = pygame.font.Font.render(text_font, text, False, "white")
                render_quote = pygame.font.Font.render(quote_font, quote, False, "white")
                pygame.Surface.blit(screen, render_text, (window_width / 2 - render_text.get_width() / 2 - 200, 100))
                pygame.Surface.blit(screen, render_quote, (window_width / 2 - render_quote.get_width() / 2 - 200, 170))  
                pygame.Surface.blit(screen, continue_text, (window_width / 2 - continue_text.get_width() / 2 - 200, 240))
                pygame.display.flip()
            elif player2_win == 1:
                # draw background
                pygame.Surface.blit(screen, pygame.image.load(os.path.join("win-loss-screen", "duck-lose.png")), (0, 0))
                # draw text
                text = "Player 2 wins!"
                quote = "\"NEW YORK PIZZA\" -new york rat"
                render_text = pygame.font.Font.render(text_font, text, False, "white")
                render_quote = pygame.font.Font.render(quote_font, quote, False, "white")
                pygame.Surface.blit(screen, render_text, (window_width / 2, 200))
                pygame.Surface.blit(screen, render_quote, (window_width / 2, 270))
                pygame.Surface.blit(screen, continue_text, (window_width / 2, 340))
                pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    proceed = False

class target_practice:
    target = create.target(os.path.join("target.png"), 20)
    targets = [pygame.Rect(window_width / 2, window_height / 4, 50, 50)]
    def target_movement(target, targets):
        for object in targets:
            object.x += target.velocity
            pygame.Surface.blit(screen, pygame.image.load(target.sprite), object)
            if object.x >= window_width - 100:
                target.velocity = target.velocity * -1
            elif object.x <= 0:
                target.velocity = target.velocity * -1
            pygame.display.flip()
    
    def target_hit(player, target, targets):
        for bullet in player.attack.bullets:
            bullet.y += player.attack.bullet_velocity
            if targets[0].colliderect(bullet):
                pygame.event.post(pygame.event.Event(player.target_hit))
                player.attack.bullets.remove(bullet)
            elif bullet.y > window_height or bullet.y < 0:
                player.attack.bullets.remove(bullet)
    
    def draw_text(player):
        font = pygame.font.Font(roboto_condensed, 30)
        text = f"{player.name} targets hit: {player.num_targets}"
        render_text = font.render(text, False, "black")
        pygame.Surface.blit(screen, render_text, player.num_targets_pos)

    def draw_exit_text():
        font = pygame.font.Font(roboto_condensed, 30)
        text = "(Press ESCAPE to exit)"
        render_text = font.render(text, False, "black")
        pygame.Surface.blit(screen, render_text, (window_width / 2 - render_text.get_width() / 2, window_height - 70))

    def all_graphics():
        render.graphics.background_img(background_alley, background_alley_origin)
        render.graphics.border(border_color)
        render.graphics.background_img(background_water, background_water_origin)
        target_practice.draw_text(player1)
        target_practice.draw_text(player2)
        target_practice.draw_exit_text()
        render.graphics.player_sprite(player2.graphic, (player2.hitbox.x, player2.hitbox.y))
        render.graphics.player_sprite(player1.graphic, (player1.hitbox.x, player1.hitbox.y))
        target_practice.target_movement(target_practice.target, target_practice.targets)
        render.graphics.bullets(player1)
        render.graphics.bullets(player2)
        pygame.display.update()

    def play():
        intro_sound.stop()
        # set variables
        # player 1
        player1.num_targets = 0
        # player 2
        player2.num_targets = 0
        player2.bottom_limit = player1.bottom_limit
        player2.top_limit = player1.top_limit
        player2.attack.bullet_velocity = player1.attack.bullet_velocity
        player2.hitbox.y = player1.hitbox.y
        player2.attack.bullet_sprite = os.path.join("player-attacks", "pizzashot-rotated.png")
        # run game
        run = True
        game_bgm.play(-1)
        proceed = True
        while proceed:
            clock.tick(framerate)
            # exit game if window is closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        proceed = False
                    # handle player attack
                    render.mechanics.attack.player.Attack(player1, event)
                    render.mechanics.attack.player.Attack(player2, event)
                if event.type == player1.target_hit:
                    # play sound
                    snicker_bullet_hit.play()
                    # set num targets hit
                    player1.num_targets += 1
                if event.type == player2.target_hit:
                    # play sound
                    pizza_bullet_hit.play()
                    # set num targets hit
                    player2.num_targets += 1
                
            # handle player movement
            render.mechanics.movement.player(player1)
            render.mechanics.movement.player(player2)
            
            target_practice.target_hit(player1, target_practice.target, target_practice.targets)
            target_practice.target_hit(player2, target_practice.target, target_practice.targets)
            target_practice.all_graphics()
            
# play game
def main():
    while True:
        player1_win_sound.stop()
        player2_win_sound.stop()

        # play intro
        animate.intro()

        # choose game mode
        proceed = True
        while proceed:
            # define text
            text = "Choose a game mode:"
            text1 = "Press '1' to play pvp."
            text2 = "Press '2' to play target practice."
            text3 = "Press ESCAPE to exit."
            font2 = pygame.font.Font(sigmar_regular, 50)
            font3 = pygame.font.Font(sigmar_regular, 30)
            render_text = font2.render(text, False, "white")
            render_text1 = font3.render(text1, False, "white")
            render_text2 = font3.render(text2, False, "white")
            render_text3 = font3.render(text3, False, "white")
            # draw screen
            pygame.Surface.fill(screen, "blue")
            pygame.Surface.blit(screen, render_text, (window_width / 2 - render_text.get_width() / 2, 200))
            pygame.Surface.blit(screen, render_text1, (window_width / 2 - render_text1.get_width() / 2, 280))
            pygame.Surface.blit(screen, render_text2, (window_width / 2 - render_text2.get_width() / 2, 340))
            pygame.Surface.blit(screen, render_text3, (window_width / 2 - render_text3.get_width() / 2, 400))
            pygame.display.flip()

            # handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    instructions_bgm.stop()
                    proceed = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    instructions_bgm.stop()
                    target_practice.play()
                    game_bgm.stop()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit()

        # initialize variables
        # player 1
        player1_win = 0
        player1.health = 100
        player1.healthbar.width = healthbar_width
        player1.hitbox.x = player1_origin_x
        player1.hitbox.y = player1_origin_y
        player1.attack.bullets = []
        # player 2
        player2_win = 0
        player2.health = 100
        player2.healthbar.width = healthbar_width
        player2.hitbox.x = player2_origin_x
        player2.hitbox.y = player2_origin_y
        player2.attack.bullets = []
        player2.bottom_limit = window_height // 2 - player2_hitbox.height
        player2.top_limit = 0
        player2.attack.bullet_velocity = pizza_velocity
        player2.hitbox.y = player2_origin_y
        player2.attack.bullet_sprite = os.path.join("player-attacks", "pizzashot.png")

        # run game
        run = True
        game_bgm.play(-1)
        while run:
            clock.tick(framerate)
            # exit game if window is closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # handle player attack
                    render.mechanics.attack.player.Attack(player1, event)
                    render.mechanics.attack.player.Attack(player2, event)
                if event.type == player1.player_hit:
                    # subtract health from player 1 if hit with bullet
                    player1.health -= player2.attack.dmg
                    healthbar_percentage = player1.health / 100
                    # draw player 1 healthbar as percentage of health
                    player1.healthbar.width = healthbar_width * healthbar_percentage
                    # play sound
                    snicker_bullet_hit.play()
                if event.type == player2.player_hit:
                    # subtract health from player 2 if hit with bullet
                    player2.health -= player1.attack.dmg
                    healthbar_percentage = player2.health / 100
                    # draw player 2 healthbar as percentage of health
                    player2.healthbar.width = healthbar_width * healthbar_percentage
                    # play sound
                    pizza_bullet_hit.play()

            # check for winner
            if player1.health <= 0:
                player1_win = 1
                break
            elif player2.health <= 0:
                player2_win = 1
                break
                
            # handle player movement
            render.mechanics.movement.player(player1)
            render.mechanics.movement.player(player2)
            render.mechanics.attack.player.bullet_control(player1, player2)
            render.mechanics.attack.player.bullet_control(player2, player1)
            
            # render graphics
            render.graphics.all_graphics()
        
        # render win-loss screen
        game_bgm.stop()
        animate.win_loss(player1_win, player2_win)
             
main()
