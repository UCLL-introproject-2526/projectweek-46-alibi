import pygame
import random
import sys

pygame.init()

# === SCHERM ===
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visje en Haaien")
clock = pygame.time.Clock()

# === KLEUREN ===
ZEE = (0, 120, 200)
WIT = (255, 255, 255)

# === LETTERTYPES ===
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 56)

# === VIS ANIMATIE ===
fish_frames = [
    pygame.image.load("fish.png").convert_alpha(),
    pygame.image.load("shark.png").convert_alpha(),
]
fish_frames = [pygame.transform.smoothscale(img, (60, 40)) for img in fish_frames]
fish_frame_index = 0
fish_animation_timer = 0
fish_rect = fish_frames[0].get_rect(x=100, y=HEIGHT//2)
fish_speed = 5

# === HAAI ===
shark_image = pygame.image.load("shark.png").convert_alpha()
shark_image = pygame.transform.scale(shark_image, (80, 50))
sharks = []

# === SCORE & MOEILIJKHEID ===
score = 0
highscore = 0
score_timer = 0
spawn_timer = 0
spawn_delay = 60
shark_speed = 4
game_over = False

# === BUBBELS ===
class Bubble:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT + random.randint(0, 200)
        self.radius = random.randint(3, 8)
        self.speed = random.uniform(0.5, 2)

    def update(self):
        self.y -= self.speed
        if self.y < -10:
            self.y = HEIGHT + random.randint(0, 200)
            self.x = random.randint(0, WIDTH)

    def draw(self, screen):
        pygame.draw.circle(screen, (200, 220, 255), (int(self.x), int(self.y)), self.radius, 1)

bubbles = [Bubble() for _ in range(25)]

# === RESET GAME ===
def reset_game():
    global sharks, score, spawn_timer, spawn_delay, shark_speed, game_over, score_timer, fish_rect
    fish_rect.x = 100
    fish_rect.y = HEIGHT // 2
    sharks = []
    score = 0
    score_timer = 0
    spawn_timer = 0
    spawn_delay = 60
    shark_speed = 4
    game_over = False

reset_game()

# === HOOFDLOOP ===
while True:
    screen.fill(ZEE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if not game_over:
        # === SCORE OPHOOG ===
        score_timer += 1
        if score_timer >= 30:
            score += 1
            score_timer = 0

        # MOEILIJKHEID
        if score % 10 == 0 and score != 0:
            shark_speed += 0.02
            spawn_delay = max(20, spawn_delay - 1)

        # VIS BEWEGEN
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            fish_rect.y -= fish_speed
        if keys[pygame.K_DOWN]:
            fish_rect.y += fish_speed
        fish_rect.y = max(0, min(HEIGHT - fish_rect.height, fish_rect.y))

        # HAAIEN SPAWNEN
        spawn_timer += 1
        if spawn_timer > spawn_delay:
            spawn_timer = 0
            rect = shark_image.get_rect()
            rect.x = WIDTH
            rect.y = random.randint(0, HEIGHT - rect.height)
            sharks.append(rect)

        # HAAIEN BEWEGEN + BOTSING
        for shark in sharks[:]:
            shark.x -= shark_speed
            if shark.right < 0:
                sharks.remove(shark)
            if shark.colliderect(fish_rect):
                game_over = True
                highscore = max(highscore, score)

        # VIS ANIMATIE
        fish_animation_timer += 1
        if fish_animation_timer >= 10:
            fish_animation_timer = 0
            fish_frame_index = (fish_frame_index + 1) % len(fish_frames)

        # BUBBELS UPDATEN
        for bubble in bubbles:
            bubble.update()

    # === TEKENEN ===
    # BUBBELS ACHTER DE VIS
    for bubble in bubbles:
        bubble.draw(screen)

    if not game_over:
        screen.blit(fish_frames[fish_frame_index], fish_rect)
        for shark in sharks:
            screen.blit(shark_image, shark)

        screen.blit(font.render(f"Score: {score}", True, WIT), (10, 10))
        screen.blit(font.render(f"Highscore: {highscore}", True, WIT), (10, 40))
    else:
        screen.blit(big_font.render("SCOREBORD", True, WIT), (WIDTH//2 - 150, 80))
        screen.blit(font.render(f"Score: {score}", True, WIT), (WIDTH//2 - 70, 160))
        screen.blit(font.render(f"Highscore: {highscore}", True, WIT), (WIDTH//2 - 90, 200))
        screen.blit(font.render("ENTER = opnieuw spelen", True, WIT), (WIDTH//2 - 150, 260))
        screen.blit(font.render("ESC = afsluiten", True, WIT), (WIDTH//2 - 120, 300))

    pygame.display.flip()
    clock.tick(60)