import pygame
import random
import math

# SETTINGS 
WIDTH = 600
HEIGHT = 700
FPS = 60

PLAYER_SIZE = 54
ENEMY_SIZE = 70

SPAWN_MS = 400 # enemy appearing 
BASE_ENEMY_SPEED = 6 #basic speed for enemy
SPEED_INCREASE_ON_PASS = 0.11 
PLAYER_SPEED = 7

# Level thresholds for changing difficulty
LEVEL_THRESHOLDS = [
    (1, 0),
    (2, 35),
    (3, 90),
    (4, 170),
    (5, 300),
    (6, 450)
]

# Define enemy shape/color info by level
LEVEL_SHAPES = {
    1: ['rect'],
    2: ['triangle', 'rect'],
    3: ['triangle', 'circle', 'rect'],
    4: ['triangle', 'circle', 'rect', 'hexagon'],
    5: ['triangle', 'circle', 'rect', 'hexagon', 'star'],
    6: ['star', 'hexagon', 'circle', 'rect', 'triangle'],
}
LEVEL_COLORS = {
    1: [(80, 40, 40), (120, 50, 60)],
    2: [(255, 196, 0), (255, 111, 0), (255,90,100)],
    3: [(20, 205, 40), (200, 240, 50), (100, 150, 255)],
    4: [(90, 60, 255), (140, 50, 245), (110, 132, 256), (97,201,236)],
    5: [(255, 40, 186), (202, 109, 188), (255, 128, 128), (201, 248, 144)],
    6: [(255, 253, 140), (255, 133, 129), (128, 255, 144), (255, 80, 190)],
}

BACKGROUND_COLORS = {
    1: (25, 25, 30),
    2: (30, 19, 50),
    3: (17, 30, 26),
    4: (32, 30, 50),
    5: (28, 34, 45),
    6: (7, 19, 27),
}

# Initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid The Blocks: Shapes Evolved!")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 28)
large_font = pygame.font.SysFont('Arial', 48)

# Game objects
player_rect = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 20, PLAYER_SIZE, PLAYER_SIZE)
enemies = []

# Spawn event
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, SPAWN_MS)

# Game state variables
enemy_speed = BASE_ENEMY_SPEED
score = 0
running = True
in_game = True
current_level = 1

# Get current level based on score
def get_level(score):
    level = 1
    for item in reversed(LEVEL_THRESHOLDS):
        lv = item[0]
        threshold = item[1]
        if score >= threshold:
            level = lv
            break
    return level

# Helper to pick a random shape and color by level
def get_shape_and_color_for_level(level):
    shapes = LEVEL_SHAPES.get(level, LEVEL_SHAPES[1])
    shape = random.choice(shapes)
    colors = LEVEL_COLORS.get(level, LEVEL_COLORS[1])
    color = random.choice(colors)
    return shape, color

# Helper to draw a regular polygon (such as a hexagon)
def draw_regular_polygon(surface, color, rect, sides):
    points = []
    cx, cy = rect.center
    radius = rect.width // 2
    angle_offset = -math.pi/2  # Start at top
    for i in range(sides):
        angle = angle_offset + (2*math.pi * i / sides)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((int(x), int(y)))
    pygame.draw.polygon(surface, color, points)

# Helper to draw a star
def draw_star(surface, color, rect):
    cx, cy = rect.center
    outer = rect.width // 2
    inner = outer // 2.5
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * 2 * math.pi / 10
        r = outer if i % 2 == 0 else inner
        x = cx + r * math.cos(angle)
        y = cy - r * math.sin(angle)
        points.append((int(x), int(y)))
    pygame.draw.polygon(surface, color, points)

# Spawn a new enemy with random properties and shape/color per level
def spawn_enemy():
    global current_level
    w = ENEMY_SIZE
    x = random.randint(0, WIDTH - w)
    size_options = [1.0, 1.0, 1.25, 0.75]
    size_mult = random.choice(size_options)
    enemy_width = int(ENEMY_SIZE * size_mult)
    enemy_height = enemy_width
    rect = pygame.Rect(x, -enemy_height, enemy_width, enemy_height)
    random_speed_factor = random.uniform(-0.08, 0.29)
    speed = enemy_speed * (1.0 + random_speed_factor)
    shape, color = get_shape_and_color_for_level(current_level)
    side_drift = 0
    if current_level >= 3:
        drift_direction = random.choice([-1, 1])
        drift_magnitude = random.uniform(0.8, 3.6)
        side_drift = drift_direction * drift_magnitude
    enemy_object = {
        'rect': rect,
        'speed': speed,
        'shape': shape,
        'drift': side_drift,
        'color': color,
        'level': current_level,
    }
    enemies.append(enemy_object)

# Helper function to draw text
def draw_text(surf, text, pos, font_obj, color=(255,255,255)):
    txt = font_obj.render(text, True, color)
    surf.blit(txt, pos)

# Check for collision between player and enemy
def enemy_collides_player(enemy, player_rect):
    shape = enemy['shape']
    rect = enemy['rect']
    if shape == 'rect':
        return player_rect.colliderect(rect)
    elif shape == 'circle':
        circle_rect = rect
        cx = circle_rect.centerx
        cy = circle_rect.centery
        radius = circle_rect.width // 2
        # Closest point on player rect to circle center
        closest_x = max(player_rect.left, min(cx, player_rect.right))
        closest_y = max(player_rect.top, min(cy, player_rect.bottom))
        dx = cx - closest_x
        dy = cy - closest_y
        return dx*dx + dy*dy < radius*radius
    elif shape == 'triangle' or shape == 'hexagon' or shape == 'star':
        # Use bounding rectangle for collision
        return player_rect.colliderect(rect)
    else:
        return False

# Powerup system: At each 50 points after level 2, give a random powerup: slow time or shield or clear
POWERUP_SCORE_INTERVAL = 50
powerup_active = None
powerup_timer = 0
POWERUP_DURATION = 6  # seconds
powerup_message_timer = 0

def activate_powerup(ptype):
    global powerup_active, powerup_timer, enemy_speed, enemies, powerup_message_timer
    powerup_active = ptype
    powerup_timer = POWERUP_DURATION
    powerup_message_timer = 2.5  # show the powerup name on screen for a bit
    if ptype == 'slow':
        enemy_speed /= 2.1
        for e in enemies:
            e['speed'] /= 2.1
    elif ptype == 'clear':
        enemies.clear()
    elif ptype == 'shield':
        # Shield is handled in collision (see below)
        pass

shielded = False

# MAIN GAME LOOP
last_powerup_score = 0
while running:
    # Wait until next frame, get elapsed time in seconds
    delta_time = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Spawn new enemy if time for it and game is running
        if in_game:
            if event.type == SPAWN_EVENT:
                spawn_enemy()
        # Restart the game if game over and any key is pressed
        if not in_game:
            if event.type == pygame.KEYDOWN:
                enemies.clear()
                enemy_speed = BASE_ENEMY_SPEED
                score = 0
                player_rect.x = WIDTH // 2 - PLAYER_SIZE // 2
                in_game = True
                current_level = 1
                powerup_active = None
                powerup_timer = 0

    keys = pygame.key.get_pressed()
    if in_game:
        # Move player left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= PLAYER_SPEED
        # Move player right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += PLAYER_SPEED

        # Clamp player to screen bounds
        player_rect.x = max(0, min(WIDTH - player_rect.width, player_rect.x))

        # Powerup processing
        if powerup_active:
            powerup_timer -= delta_time
            if powerup_timer <= 0:
                # Deactivate
                if powerup_active == 'slow':
                    enemy_speed *= 2.1
                    for e in enemies:
                        e['speed'] *= 2.1
                elif powerup_active == 'shield':
                    pass
                powerup_active = None
            if powerup_message_timer > 0:
                powerup_message_timer -= delta_time

        # Grant a new powerup every interval (after level 2)
        if current_level >= 2 and score > 0 and score % POWERUP_SCORE_INTERVAL == 0 and score != last_powerup_score:
            ptype = random.choice(['slow', 'clear', 'shield'])
            activate_powerup(ptype)
            shielded = (ptype == 'shield')
            last_powerup_score = score

        # Update enemies list and check for collisions, drift, etc
        enemies_copy = enemies[:]
        for e in enemies_copy:
            e['rect'].y = e['rect'].y + e['speed']
            # Handle side drift for level 3+
            if current_level >= 3:
                if abs(e.get('drift', 0)) > 0:
                    drift_value = int(e['drift'])
                    e['rect'].x = e['rect'].x + drift_value
                    # Bounce at edge
                    if e['rect'].left < 0 or e['rect'].right > WIDTH:
                        e['drift'] = -e['drift']

            # Collision check
            if enemy_collides_player(e, player_rect):
                if powerup_active == 'shield':
                    enemies.remove(e)
                    powerup_active = None
                    shielded = False
                    continue
                in_game = False
                break

            # Check if enemy went off bottom of screen
            if e['rect'].top > HEIGHT:
                enemies.remove(e)
                score = score + 1
                # Calculate how much more the speed should increase for higher level
                level_uplift = 1 + ((current_level - 1) * 0.16)
                enemy_speed = enemy_speed + (SPEED_INCREASE_ON_PASS * level_uplift)

        # Update level if necessary
        previous_level = current_level
        current_level = get_level(score)
        # Check if the level actually changed
        if current_level != previous_level:
            if current_level == 2:
                enemy_speed = enemy_speed + 3.1
                new_spawn_time = SPAWN_MS - 260
                if new_spawn_time < 260:
                    new_spawn_time = 260
                pygame.time.set_timer(SPAWN_EVENT, new_spawn_time)
            elif current_level == 3:
                enemy_speed = enemy_speed + 3.5
                new_spawn_time = SPAWN_MS - 340
                if new_spawn_time < 170:
                    new_spawn_time = 170
                pygame.time.set_timer(SPAWN_EVENT, new_spawn_time)
            elif current_level == 4:
                enemy_speed = enemy_speed + 4.2
                new_spawn_time = SPAWN_MS - 420
                if new_spawn_time < 120:
                    new_spawn_time = 120
                pygame.time.set_timer(SPAWN_EVENT, new_spawn_time)
            elif current_level == 5:
                enemy_speed = enemy_speed + 5.1
                new_spawn_time = SPAWN_MS - 550
                if new_spawn_time < 70:
                    new_spawn_time = 70
                pygame.time.set_timer(SPAWN_EVENT, new_spawn_time)
            elif current_level == 6:
                enemy_speed = enemy_speed + 6.5
                new_spawn_time = SPAWN_MS - 600
                if new_spawn_time < 30:
                    new_spawn_time = 30
                pygame.time.set_timer(SPAWN_EVENT, new_spawn_time)

    # DRAWING PHASE
    # Smooth background color transitions per level
    bg_color = BACKGROUND_COLORS.get(current_level, (25, 25, 30))
    screen.fill(bg_color)

    # Draw player with shield effect
    player_col = (0,25,255) if not (powerup_active == 'shield') else (0,240,255)
    pygame.draw.rect(screen, player_col, player_rect, border_radius=6)
    if powerup_active == 'shield':
        pygame.draw.ellipse(screen, (90, 220, 255, 130), player_rect.inflate(32, 32), 4)

    # Draw enemies with level-dependent shapes/colors
    for e in enemies:
        color = e.get('color', (80, 40, 40))
        shape = e['shape']
        if shape == 'rect':
            pygame.draw.rect(screen, color, e['rect'], border_radius=6)
        elif shape == 'circle':
            center = e['rect'].center
            radius = e['rect'].width // 2
            pygame.draw.circle(screen, color, center, radius)
        elif shape == 'triangle':
            r = e['rect']
            point1 = (r.centerx, r.top)
            point2 = (r.left, r.bottom)
            point3 = (r.right, r.bottom)
            points = [point1, point2, point3]
            pygame.draw.polygon(screen, color, points)
        elif shape == 'hexagon':
            draw_regular_polygon(screen, color, e['rect'], 6)
        elif shape == 'star':
            draw_star(screen, color, e['rect'])

    # HUD
    draw_text(screen, "Score: " + str(score), (12, 12), font)
    draw_text(screen, "Speed: %.2f" % enemy_speed, (12, 40), font)
    draw_text(screen, "Level: " + str(current_level), (12, 70), font)
    # Powerup HUD
    if powerup_active and powerup_message_timer > 0:
        msg = ""
        if powerup_active == 'slow':
            msg = "Time Slowed!"
        elif powerup_active == 'clear':
            msg = "Enemies Cleared!"
        elif powerup_active == 'shield':
            msg = "Shielded!"
        draw_text(screen, msg, (WIDTH//2 - 80, 16), font, (255, 255, 80))

    # Game Over Screen
    if not in_game:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        draw_text(screen, "Game Over", (WIDTH//2 - 120, HEIGHT//2 - 80), large_font)
        draw_text(screen, "Final Score: " + str(score), (WIDTH//2 - 100, HEIGHT//2 - 20), font)
        draw_text(screen, "Press any key to restart", (WIDTH//2 - 150, HEIGHT//2 + 30), font)

    pygame.display.flip()

pygame.quit()
