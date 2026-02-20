# A simple, playable Mama-mia Bros. game using the Pygame library.

import pygame
import sys
import random

# --- Pygame Setup ---
# Initialize Pygame and set up the window.
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Mario Bros.")
clock = pygame.time.Clock()

# --- Game Variables and Constants ---
# Colors
bg_color = (135, 206, 235)  # Sky blue
mario_color = (255, 0, 0)   # Default to red
luigi_color = (0, 128, 0)   # Green
floor_color = (139, 69, 19) # Brown
goomba_color = (139, 69, 19)  
koopa_color = (0, 150, 0) 
platform_color = (139, 69, 19) # Brown for platforms
question_block_color = (255, 200, 0) # Gold for question blocks
used_block_color = (169, 169, 169) # Gray for used blocks
fireball_powerup_color = (255, 105, 180) # Pink for the fireball power-up
superstar_color = (255, 255, 20) # Pale yellow for the star
button_color = (100, 100, 100) # Gray for buttons
castle_wall_color = (150, 150, 150) # Gray for castle walls
bowser_body_color = (160, 129, 94) # Brownish-yellow for 's body
bowser_shell_color = (0, 128, 0) # Green for B's shell
moon_color = (255, 255, 200) # Pale yellow for the moon
flagpole_color = (200, 200, 200) # Gray for the flagpole
flag_color = (255, 0, 0) # Red for the flag

# properties
mario_width = 40
mario_height = 60
mario_speed = 5
gravity = 0.5
jump_strength = -12
mario_velocity_y = 0
# New game states: 'menu', 'character_select', 'tutorial', 'playing', 'level_complete', 'game_over', 'win_screen', 'note_screen', 'the_end'
game_state = 'menu'
on_ground = True
victory_walk_speed = 3 # A slower speed for Mario's victory walk
# Power-up variables
mario_powerup = None  # Can be None, 'fireball', or 'star'
is_invincible = False
star_timer = 0
star_duration = 8000 # 8 seconds of invincibility
star_flash_interval = 150 # Flash every 150 milliseconds
last_flash_time = 0
is_flashing = False

# Enemy properties
goomba_width = 40
goomba_height = 40
goomba_speed = 2
koopa_width = 40
koopa_height = 60
koopa_speed = 3
goomba_list = []
koopa_list = []

# properties
bowser_width = 80
bowser_height = 100
bowser_health = 5 # Increased health from 3 to 5
bowser_rect = None
bowser_defeated = False

# Platforms and Question Blocks 
platforms = []
question_blocks = []
used_blocks = [] # New list for used blocks
item_list = [] # New list for items
end_point = None # The final point of the level, now a physical flagpole
moon_rect = None

# Camera properties for scrolling level
camera_offset_x = 0
level_width = 0 # The total width of the current level
current_level = 0 # Track which level we are on

# rectangle (will be created after screen size is chosen)
mario_rect = None
player_character = "Mario" # Default player

# Game state flags, score, and text
score = 0
font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 24)
restart_font = pygame.font.Font(None, 28)
tutorial_font = pygame.font.Font(None, 28)
note_font = pygame.font.Font(None, 24)
end_screen_font = pygame.font.Font(None, 40)

# Time tracking for the victory screen delay
win_time = 0
win_delay = 3000 # 3 seconds

# The personalized notes have been shortened
peach_note = "Thank you, MARiO! The cake is waiting at the castle. - Princess Peach"
daisy_note = "That was amazing, LUIgI! The cake is waiting at my castle. - Princess Daisy"
current_note = ""

# --- Functions ---

def setup_game_screen(width, height):
    """Sets up the screen and the floor based on the selected size."""
    global screen, screen_width, screen_height, game_state
    screen_width, screen_height = width, height
    screen = pygame.display.set_mode((screen_width, screen_height))
    # Move to the character select screen after screen size is chosen
    game_state = 'character_select'

def setup_level_1():
    """Sets up the platforms, blocks, and goombas for the first level."""
    global game_state, goomba_list, koopa_list, mario_rect, mario_velocity_y, score, on_ground, platforms, question_blocks, used_blocks, item_list, camera_offset_x, end_point, level_width, current_level, mario_powerup, is_invincible
    game_state = 'playing'
    current_level = 1
    level_width = 1500
    goomba_list.clear()
    koopa_list.clear()
    item_list.clear()
    used_blocks.clear()
    platforms.clear()
    question_blocks.clear()
    camera_offset_x = 0
    mario_powerup = None
    is_invincible = False
    
    platforms = [
        pygame.Rect(0, screen_height - 50, level_width, 50),
        pygame.Rect(400, screen_height - 150, 100, 20),
        pygame.Rect(600, screen_height - 250, 40, 40),
        pygame.Rect(640, screen_height - 250, 40, 40),
        pygame.Rect(680, screen_height - 250, 40, 40)
    ]
    
    question_blocks = [
        pygame.Rect(420, screen_height - 200, 40, 40),
        pygame.Rect(660, screen_height - 300, 40, 40),
        pygame.Rect(800, screen_height - 150, 40, 40), # Added new block
        pygame.Rect(1000, screen_height - 250, 40, 40) # Added new block
    ]
    
    goomba_list = [
        pygame.Rect(500, screen_height - 50 - goomba_height, goomba_width, goomba_height),
        pygame.Rect(850, screen_height - 50 - goomba_height, goomba_width, goomba_height),
        pygame.Rect(1100, screen_height - 50 - goomba_height, goomba_width, goomba_height)
    ]
    
    # Set the end point for level 1 (now a visible flagpole)
    end_point = pygame.Rect(1300, screen_height - 200, 10, 150)
    
    mario_rect.x = 50
    mario_rect.y = screen_height - 50 - mario_height
    mario_velocity_y = 0
    on_ground = True
    
def setup_level_2():
    """Sets up the platforms, blocks, and goombas for the second level."""
    global game_state, goomba_list, koopa_list, mario_rect, mario_velocity_y, score, on_ground, platforms, question_blocks, used_blocks, item_list, camera_offset_x, end_point, level_width, current_level, mario_powerup, is_invincible
    game_state = 'playing'
    current_level = 2
    level_width = 2500
    goomba_list.clear()
    koopa_list.clear()
    item_list.clear()
    used_blocks.clear()
    platforms.clear()
    question_blocks.clear()
    camera_offset_x = 0
    mario_powerup = None
    is_invincible = False
    
    # Redefine the level layout to be a larger, scrolling level
    platforms = [
        pygame.Rect(0, screen_height - 50, level_width, 50),
        pygame.Rect(400, screen_height - 150, 100, 20),
        pygame.Rect(600, screen_height - 250, 40, 40),
        pygame.Rect(640, screen_height - 250, 40, 40),
        pygame.Rect(680, screen_height - 250, 40, 40),
        pygame.Rect(900, screen_height - 150, 100, 20),
        pygame.Rect(1100, screen_height - 150, 100, 20),
        pygame.Rect(2000, screen_height - 100, 40, 40),
        pygame.Rect(2000, screen_height - 140, 40, 40),
        pygame.Rect(2000, screen_height - 180, 40, 40),
        pygame.Rect(1500, screen_height - 200, 100, 20), # New platform
        pygame.Rect(1700, screen_height - 250, 40, 40) # New block location
    ]
    
    question_blocks = [
        pygame.Rect(420, screen_height - 200, 40, 40),
        pygame.Rect(660, screen_height - 300, 40, 40),
        pygame.Rect(800, screen_height - 200, 40, 40),
        pygame.Rect(1520, screen_height - 250, 40, 40), # New block
        pygame.Rect(1720, screen_height - 300, 40, 40)  # New block
    ]
    
    goomba_list = [
        pygame.Rect(500, screen_height - 50 - goomba_height, goomba_width, goomba_height),
        pygame.Rect(950, screen_height - 50 - goomba_height, goomba_width, goomba_height)
    ]
    
    koopa_list = [
        pygame.Rect(1150, screen_height - 50 - koopa_height, koopa_width, koopa_height),
        pygame.Rect(1600, screen_height - 50 - koopa_height, koopa_width, koopa_height) # New koopa
    ]
    
    # Set the end point for level 2
    end_point = pygame.Rect(2300, screen_height - 200, 10, 150)
    
    mario_rect.x = 50
    mario_rect.y = screen_height - 50 - mario_height
    mario_velocity_y = 0
    on_ground = True

def setup_level_3():
    """Sets up the castle level with Bowser."""
    global game_state, goomba_list, koopa_list, mario_rect, mario_velocity_y, score, on_ground, platforms, question_blocks, used_blocks, item_list, camera_offset_x, end_point, level_width, current_level, bowser_rect, bowser_health, bowser_defeated, moon_rect, mario_powerup, is_invincible
    game_state = 'playing'
    current_level = 3
    level_width = 3000
    goomba_list.clear()
    koopa_list.clear()
    item_list.clear()
    used_blocks.clear()
    platforms.clear()
    question_blocks.clear()
    camera_offset_x = 0
    bowser_health = 5 # Increased health
    bowser_defeated = False
    moon_rect = None
    mario_powerup = None
    is_invincible = False
    
    platforms = [
        pygame.Rect(0, screen_height - 50, level_width, 50),
        pygame.Rect(400, screen_height - 150, 200, 20),
        pygame.Rect(800, screen_height - 250, 100, 20),
        pygame.Rect(1200, screen_height - 150, 100, 20),
        pygame.Rect(1600, screen_height - 150, 100, 20),
        pygame.Rect(2000, screen_height - 150, 100, 20), # Bowser's arena floor
    ]
    
    question_blocks = [
        pygame.Rect(500, screen_height - 200, 40, 40), # Added new block
        pygame.Rect(900, screen_height - 300, 40, 40), # Added new block
        pygame.Rect(1300, screen_height - 200, 40, 40), # Added new block
    ]
    
    goomba_list = [
        pygame.Rect(500, screen_height - 50 - goomba_height, goomba_width, goomba_height),
        pygame.Rect(900, screen_height - 50 - goomba_height, goomba_width, goomba_height)
    ]
    
    koopa_list = [
        pygame.Rect(900, screen_height - 50 - koopa_height, koopa_width, koopa_height),
        pygame.Rect(1400, screen_height - 50 - koopa_height, koopa_width, koopa_height)
    ]
    
    # Bowser's position
    bowser_rect = pygame.Rect(2500, screen_height - 50 - bowser_height, bowser_width, bowser_height)
    end_point = None # The end is handled by defeating Bowser
    
    mario_rect.x = 50
    mario_rect.y = screen_height - 50 - mario_height
    mario_velocity_y = 0
    on_ground = True


def start_tutorial():
    """Sets up a clean state for the tutorial level."""
    global platforms, question_blocks, used_blocks, item_list, game_state, mario_rect, on_ground, camera_offset_x, level_width, goomba_list, koopa_list
    
    # Clear all game objects to ensure a fresh start
    platforms.clear()
    question_blocks.clear()
    used_blocks.clear()
    item_list.clear()
    goomba_list.clear()
    koopa_list.clear()

    # Set the game state and level properties
    game_state = 'tutorial'
    level_width = screen_width
    
    # Create the player's character with the current screen dimensions
    mario_rect = pygame.Rect(50, screen_height - 50 - mario_height, mario_width, mario_height)
    on_ground = True
    camera_offset_x = 0
    
    # Dynamically create tutorial platforms based on the current screen size
    tutorial_platform = pygame.Rect(screen_width / 2 - 50, screen_height - 150, 100, 20)
    question_block1 = pygame.Rect(screen_width / 4, screen_height - 200, 40, 40)
    question_block2 = pygame.Rect(screen_width / 4 + 60, screen_height - 200, 40, 40)
    question_block3 = pygame.Rect(screen_width / 4 + 120, screen_height - 200, 40, 40) # Added new block

    platforms = [
        pygame.Rect(0, screen_height - 50, screen_width, 50),
        tutorial_platform,
        question_block1,
        question_block2,
        question_block3
    ]
    question_blocks = [question_block1, question_block2, question_block3]
    

def handle_input():
    global mario_velocity_y, on_ground, game_state, mario_rect, camera_offset_x
    
    if mario_rect is None:
        return
    
    keys = pygame.key.get_pressed()
    
    if game_state == 'playing' or game_state == 'tutorial':
        # Move left and right
        if keys[pygame.K_LEFT]:
            mario_rect.x -= mario_speed
            # Prevent Mario from moving left past the start of the level
            if mario_rect.left < 0:
                mario_rect.left = 0
        if keys[pygame.K_RIGHT]:
            mario_rect.x += mario_speed
            
        # Update camera offset to follow Mario, but only during the main game
        if game_state == 'playing':
            camera_offset_x = mario_rect.x - screen_width / 3
            # Keep the camera from scrolling past the beginning of the level
            if camera_offset_x < 0:
                camera_offset_x = 0
            # Keep the camera from scrolling past the end of the level
            max_camera_offset = level_width - screen_width
            if camera_offset_x > max_camera_offset:
                camera_offset_x = max_camera_offset
            
        # Jump - now checks the on_ground flag
        if keys[pygame.K_UP] and on_ground:
            mario_velocity_y = jump_strength
            on_ground = False # Mario is no longer on the ground after jumping

def apply_gravity():
    global mario_velocity_y, on_ground, platforms, question_blocks, used_blocks, item_list
    
    if mario_rect is None:
        return
    
    # Apply gravity to the vertical velocity
    mario_velocity_y += gravity
    mario_rect.y += mario_velocity_y
    
    on_ground = False
    # Check for collision with all platforms
    for platform in platforms[:]: # Iterate over a copy to safely remove items
        if mario_rect.colliderect(platform):
            # Collision from above
            if mario_velocity_y > 0 and mario_rect.bottom >= platform.top and mario_rect.bottom <= platform.top + 20:
                mario_rect.bottom = platform.top
                mario_velocity_y = 0
                on_ground = True
            # Collision from below
            elif mario_velocity_y < 0 and mario_rect.top <= platform.bottom and mario_rect.top >= platform.bottom - 20:
                mario_rect.top = platform.bottom
                mario_velocity_y = 0
                
                # Check if the block is a question block
                if platform in question_blocks:
                    # Remove the question block and add a used block
                    question_blocks.remove(platform)
                    platforms.remove(platform)
                    used_blocks.append(platform)
                    
                    # Randomly spawn one of the new items
                    item_type = random.choice(['fireball', 'superstar'])
                    if item_type == 'fireball':
                         item_rect = pygame.Rect(platform.x, platform.y - 40, 40, 40)
                    else: # superstar
                         item_rect = pygame.Rect(platform.x, platform.y - 40, 40, 40)
                    item_list.append((item_rect, item_type))

def check_enemy_collision():
    global game_state, goomba_list, koopa_list, mario_velocity_y, score, bowser_health, bowser_rect, bowser_defeated, moon_rect, mario_powerup, is_invincible
    if mario_rect is None:
        return
    
    # Check Goomba collision
    goombas_to_remove = []
    for goomba in goomba_list:
        if mario_rect.colliderect(goomba):
            # If Mario is invincible, the enemy dies
            if is_invincible:
                goombas_to_remove.append(goomba)
                score += 10 # Bonus score for superstar kills
            # If Mario has the fireball power-up, he loses the power-up
            elif mario_powerup == 'fireball':
                mario_powerup = None
            # Standard stomp
            elif mario_velocity_y > 0 and mario_rect.bottom <= goomba.top + 10:
                goombas_to_remove.append(goomba)
                mario_velocity_y = jump_strength / 2
                score += 1
            # Standard death
            else:
                game_state = 'game_over'

    for goomba in goombas_to_remove:
        goomba_list.remove(goomba)
        
    # Check Koopa collision
    koopas_to_remove = []
    for koopa in koopa_list:
        if mario_rect.colliderect(koopa):
            # If Mario is invincible, the enemy dies
            if is_invincible:
                koopas_to_remove.append(koopa)
                score += 10
            # If Mario has the fireball power-up, he loses the power-up
            elif mario_powerup == 'fireball':
                mario_powerup = None
            # Standard stomp
            elif mario_velocity_y > 0 and mario_rect.bottom <= koopa.top + 10:
                koopas_to_remove.append(koopa)
                mario_velocity_y = jump_strength / 2
                score += 1
            # Standard death
            else:
                game_state = 'game_over'

    for koopa in koopas_to_remove:
        koopa_list.remove(koopa)

    # Check collision
    if current_level == 3 and not bowser_defeated and mario_rect.colliderect(bowser_rect):
        # Superstar does NOT work on
        if is_invincible:
            pass # Mario just bounces off
        # If Mario has fireball, he loses it
        elif mario_powerup == 'fireball':
             mario_powerup = None
        elif mario_velocity_y > 0 and mario_rect.bottom <= bowser_rect.top + 20:
            bowser_health -= 1
            mario_velocity_y = jump_strength / 2
            if bowser_health <= 0:
                bowser_defeated = True
                moon_rect = pygame.Rect(bowser_rect.x, bowser_rect.y - 50, 40, 40)
        else:
            game_state = 'game_over'


def check_item_collision():
    global score, item_list, game_state, moon_rect, mario_powerup, is_invincible, star_timer
    if mario_rect is None:
        return
    
    items_to_remove = []
    for item_tuple in item_list[:]:
        item, item_type = item_tuple
        if mario_rect.colliderect(item):
            items_to_remove.append(item_tuple)
            if item_type == 'fireball':
                mario_powerup = 'fireball'
            elif item_type == 'superstar':
                mario_powerup = 'star'
                is_invincible = True
                star_timer = pygame.time.get_ticks()
            score += 5 # Add a bonus for collecting the item

    for item in items_to_remove:
        item_list.remove(item)

    # Check moon collision
    if moon_rect and mario_rect.colliderect(moon_rect):
        game_state = 'the_end'

def draw_game():
    """Draws all elements based on the current game state."""
    global is_flashing, last_flash_time, star_flash_interval
    screen.fill(bg_color)

    if game_state == 'menu':
        title_text = font.render("Simple Mario Bros.", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width/2, screen_height/4))
        screen.blit(title_text, title_rect)
        menu_buttons = {
            "Small": pygame.Rect(screen_width/2 - 100, screen_height/2, 200, 50),
            "Medium": pygame.Rect(screen_width/2 - 100, screen_height/2 + 70, 200, 50),
            "Large": pygame.Rect(screen_width/2 - 100, screen_height/2 + 140, 200, 50),
            "Quit": pygame.Rect(screen_width/2 - 100, screen_height/2 + 210, 200, 50)
        }
        for button_text, button_rect in menu_buttons.items():
            pygame.draw.rect(screen, button_color, button_rect)
            text_surface = restart_font.render(button_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)
    
    elif game_state == 'character_select':
        title_text = font.render("Choose your character!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width/2, screen_height/4))
        screen.blit(title_text, title_rect)
        
        mario_button = pygame.Rect(screen_width/2 - 150, screen_height/2, 100, 50)
        luigi_button = pygame.Rect(screen_width/2 + 50, screen_height/2, 100, 50)
        
        pygame.draw.rect(screen, (255, 0, 0), mario_button)
        pygame.draw.rect(screen, (0, 128, 0), luigi_button)
        
        mario_text = restart_font.render("Mario", True, (255, 255, 255))
        luigi_text = restart_font.render("Luigi", True, (255, 255, 255))
        
        screen.blit(mario_text, mario_text.get_rect(center=mario_button.center))
        screen.blit(luigi_text, luigi_text.get_rect(center=luigi_button.center))
    
    elif game_state == 'note_screen':
        note_text = note_font.render(current_note, True, (255, 255, 255))
        note_rect = note_text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(note_text, note_rect)
        
        continue_text = restart_font.render("Press SPACE to continue.", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(screen_width/2, screen_height/2 + 100))
        screen.blit(continue_text, continue_rect)
    
    elif game_state == 'game_over':
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
        screen.blit(game_over_text, text_rect)
        
        restart_text = restart_font.render("Press SPACE to go to Menu", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.blit(restart_text, restart_rect)

    elif game_state == 'win_screen':
        win_text = font.render("You Win!", True, (255, 255, 255))
        win_rect = win_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
        screen.blit(win_text, win_rect)

        restart_text = restart_font.render("Press SPACE to go to Menu", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.blit(restart_text, restart_rect)
    
    elif game_state == 'the_end':
        if player_character == "Mario":
            # Green fields of Mushroom Kingdom
            screen.fill((144, 238, 144))
            # Draw Peach
            pygame.draw.rect(screen, (255, 182, 193), pygame.Rect(screen_width/2 - 100, screen_height - 150, 40, 60))
            pygame.draw.rect(screen, mario_color, pygame.Rect(screen_width/2 - 150, screen_height - 110, 40, 60))
        else: # Luigi
            # Deserts
            screen.fill((244, 164, 96))
            # Draw Daisy
            pygame.draw.rect(screen, (255, 204, 0), pygame.Rect(screen_width/2 - 100, screen_height - 150, 40, 60))
            pygame.draw.rect(screen, luigi_color, pygame.Rect(screen_width/2 - 150, screen_height - 110, 40, 60))

        end_text = end_screen_font.render("The End", True, (255, 255, 255))
        end_rect = end_text.get_rect(center=(screen_width/2, screen_height/4))
        screen.blit(end_text, end_rect)
        
        restart_text = restart_font.render("Press SPACE to go to Menu", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.blit(restart_text, restart_rect)
        
    elif game_state == 'playing' or game_state == 'tutorial' or game_state == 'level_complete':
        # Draw platforms with the camera offset
        for platform in platforms:
            if platform in question_blocks:
                pygame.draw.rect(screen, question_block_color, platform.move(-camera_offset_x, 0))
            else:
                if current_level == 3:
                    pygame.draw.rect(screen, castle_wall_color, platform.move(-camera_offset_x, 0))
                else:
                    pygame.draw.rect(screen, platform_color, platform.move(-camera_offset_x, 0))

        # Draw used blocks with the camera offset
        for block in used_blocks:
            pygame.draw.rect(screen, used_block_color, block.move(-camera_offset_x, 0))
        
        # Draw, with a flashing effect if he has the star power-up
        if mario_rect:
            current_mario_color = mario_color
            if is_invincible and pygame.time.get_ticks() - last_flash_time > star_flash_interval:
                is_flashing = not is_flashing
                last_flash_time = pygame.time.get_ticks()
            
            if is_invincible and is_flashing:
                current_mario_color = (255, 255, 255) # White flash
            
            pygame.draw.rect(screen, current_mario_color, mario_rect.move(-camera_offset_x, 0))

        # Draw items with the camera offset
        for item_tuple in item_list:
            item, item_type = item_tuple
            item_rect = item.move(-camera_offset_x, 0)
            if item_type == 'fireball':
                pygame.draw.rect(screen, fireball_powerup_color, item_rect)
            elif item_type == 'superstar':
                 pygame.draw.rect(screen, superstar_color, item_rect)
        
        # Draw goombas and koopas with the camera offset
        if game_state == 'playing':
            for goomba in goomba_list:
                goomba_rect = goomba.move(-camera_offset_x, 0)
                pygame.draw.rect(screen, goomba_color, goomba_rect)
            for koopa in koopa_list:
                koopa_rect = koopa.move(-camera_offset_x, 0)
                pygame.draw.rect(screen, koopa_color, koopa_rect)
                
            # Draw  if on level 3
            if current_level == 3 and not bowser_defeated:
                bowser_drawn_rect = bowser_rect.move(-camera_offset_x, 0)
                # Draws body
                pygame.draw.rect(screen, bowser_body_color, bowser_drawn_rect)
                # Draws shell
                pygame.draw.rect(screen, bowser_shell_color, pygame.Rect(bowser_drawn_rect.x, bowser_drawn_rect.y, bowser_width, bowser_height/2))
                # Draws health bar
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(bowser_drawn_rect.x, bowser_drawn_rect.y - 20, bowser_width, 10))
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(bowser_drawn_rect.x, bowser_drawn_rect.y - 20, bowser_width * (bowser_health/5), 10))
            
            # Draw the moon if it exists
            if moon_rect:
                pygame.draw.rect(screen, moon_color, moon_rect.move(-camera_offset_x, 0))

            # Draw the flagpole if it exists
            if end_point:
                pygame.draw.rect(screen, flagpole_color, end_point.move(-camera_offset_x, 0))
                pygame.draw.rect(screen, flag_color, pygame.Rect(end_point.x - camera_offset_x - 30, end_point.y, 40, 20))
                
            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(topleft=(20, 20))
            screen.blit(score_text, score_rect)
        elif game_state == 'tutorial':
            tutorial_text = tutorial_font.render("Press the UP arrow to jump!", True, (255, 255, 255))
            text_rect = tutorial_text.get_rect(center=(screen_width/2, screen_height/2 - 100))
            screen.blit(tutorial_text, text_rect)
            
            tutorial_text2 = tutorial_font.render("Press the RIGHT arrow to move on.", True, (255, 255, 255))
            text_rect2 = tutorial_font.render(f"The screen now scrolls! Mario's global x: {mario_rect.x}", True, (255, 255, 255))
            text_rect2 = tutorial_text2.get_rect(center=(screen_width/2, screen_height/2 - 50))
            screen.blit(tutorial_text2, text_rect2)
            
    pygame.display.flip()

# --- Main Game Loop ---
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == 'game_over' or game_state == 'win_screen' or game_state == 'the_end':
                    game_state = 'menu'
                    mario_rect = None
                    setup_game_screen(800, 600)
                elif game_state == 'note_screen':
                    game_state = 'win_screen'
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            if game_state == 'menu':
                menu_buttons = {
                    "Small": pygame.Rect(screen_width/2 - 100, screen_height/2, 200, 50),
                    "Medium": pygame.Rect(screen_width/2 - 100, screen_height/2 + 70, 200, 50),
                    "Large": pygame.Rect(screen_width/2 - 100, screen_height/2 + 140, 200, 50),
                    "Quit": pygame.Rect(screen_width/2 - 100, screen_height/2 + 210, 200, 50)
                }
                if menu_buttons["Small"].collidepoint(mouse_pos):
                    setup_game_screen(640, 480)
                elif menu_buttons["Medium"].collidepoint(mouse_pos):
                    setup_game_screen(800, 600)
                elif menu_buttons["Large"].collidepoint(mouse_pos):
                    setup_game_screen(1024, 768)
                elif menu_buttons["Quit"].collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            
            elif game_state == 'character_select':
                mario_button = pygame.Rect(screen_width/2 - 150, screen_height/2, 100, 50)
                luigi_button = pygame.Rect(screen_width/2 + 50, screen_height/2, 100, 50)
                
                if mario_button.collidepoint(mouse_pos):
                    mario_color = (255, 0, 0)
                    player_character = "Mario"
                    start_tutorial()
                elif luigi_button.collidepoint(mouse_pos):
                    mario_color = (0, 128, 0)
                    player_character = "Luigi"
                    start_tutorial()

    # Game logic
    if game_state == 'playing' or game_state == 'tutorial':
        handle_input()
        apply_gravity()
        check_enemy_collision()
        check_item_collision()

        # Check superstar timer
        if is_invincible and pygame.time.get_ticks() - star_timer > star_duration:
            is_invincible = False
            mario_powerup = None # The powerup state is no longer a star.
        
        # THIS IS THE FIX FOR THE TUTORIAL LEVEL
        if game_state == 'tutorial' and mario_rect and mario_rect.x > screen_width:
             setup_level_1()

        if game_state == 'playing':
            # Enemy movement
            for goomba in goomba_list:
                goomba.x -= goomba_speed
            for koopa in koopa_list:
                koopa.x -= koopa_speed
            
            # Level progression logic using a physical flagpole
            if mario_rect and end_point and mario_rect.colliderect(end_point):
                if current_level == 1:
                    setup_level_2()
                elif current_level == 2:
                    setup_level_3()
    
    elif game_state == 'level_complete':
        # Mario's victory walk
        if mario_rect.x < level_width + 100: # Make sure he walks off screen
            mario_rect.x += victory_walk_speed
        
        # After a delay, transition to the note screen
        if pygame.time.get_ticks() - win_time > win_delay:
            game_state = 'note_screen'
            
    # Drawing is now handled by a single function
    draw_game()
    
    # Set the frame rate
    clock.tick(60)