import pygame
import random
import sys

def run_game(screen):
    clock = pygame.time.Clock()

    WIDTH, HEIGHT = screen.get_size()

    ZEE = (0, 120, 200)
    WIT = (255, 255, 255)

    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 56)

    fish_frames = [
        pygame.image.load("fish.png").convert_alpha(),
        pygame.image.load("shark.png").convert_alpha(),
    ]
    fish_frames = [pygame.transform.smoothscale(img, (60, 40)) for img in fish_frames]

    fish_frame_index = 0
    fish_animation_timer = 0
    fish_rect = fish_frames[0].get_rect(x=100, y=HEIGHT//2)
    fish_speed = 5

    shark_image = pygame.image.load("shark.png").convert_alpha()
    shark_image = pygame.transform.scale(shark_image, (80, 50))
    sharks = []

    score = 0
    highscore = 0
    score_timer = 0
    spawn_timer = 0
    spawn_delay = 60
    shark_speed = 4
    game_over = False

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

        def draw(self):
            pygame.draw.circle(screen, (200, 220, 255), (int(self.x), int(self.y)), self.radius, 1)

    bubbles = [Bubble() for _ in range(25)]

    def reset_game():
        nonlocal sharks, score, spawn_timer, spawn_delay, shark_speed, game_over, score_timer
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

    # 🎮 GAME LOOP
    running = True
    while running:
        screen.fill(ZEE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "home"

        if not game_over:
            score_timer += 1
            if score_timer >= 30:
                score += 1
                score_timer = 0

            if score % 10 == 0 and score != 0:
                shark_speed += 0.02
                spawn_delay = max(20, spawn_delay - 1)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                fish_rect.y -= fish_speed
            if keys[pygame.K_DOWN]:
                fish_rect.y += fish_speed
            fish_rect.y = max(0, min(HEIGHT - fish_rect.height, fish_rect.y))

            spawn_timer += 1
            if spawn_timer > spawn_delay:
                spawn_timer = 0
                rect = shark_image.get_rect(x=WIDTH, y=random.randint(0, HEIGHT - 50))
                sharks.append(rect)

            for shark in sharks[:]:
                shark.x -= shark_speed
                if shark.right < 0:
                    sharks.remove(shark)
                if shark.colliderect(fish_rect):
                    game_over = True
                    highscore = max(highscore, score)

            fish_animation_timer += 1
            if fish_animation_timer >= 10:
                fish_animation_timer = 0
                fish_frame_index = (fish_frame_index + 1) % len(fish_frames)

            for bubble in bubbles:
                bubble.update()

        for bubble in bubbles:
            bubble.draw()

        if not game_over:
            screen.blit(fish_frames[fish_frame_index], fish_rect)
            for shark in sharks:
                screen.blit(shark_image, shark)
            screen.blit(font.render(f"Score: {score}", True, WIT), (10, 10))
            screen.blit(font.render(f"Highscore: {highscore}", True, WIT), (10, 40))
        else:
            screen.blit(big_font.render("GAME OVER", True, WIT), (WIDTH//2 - 150, 120))
            screen.blit(font.render("ESC = terug naar menu", True, WIT), (WIDTH//2 - 140, 180))

        pygame.display.flip()
        clock.tick(60)
