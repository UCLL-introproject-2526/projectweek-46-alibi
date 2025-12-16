import pygame
import random


class CoinManager:
    def __init__(self, speed=4, spawn_chance=0.02, max_coins=6, save_file="coins.txt"):
        self.coins = []
        self.count = 0
        self.speed = speed
        self.spawn_chance = spawn_chance
        self.max_coins = max_coins
        self.save_file = save_file
        try:
            img = pygame.image.load("img/muntje.jpg").convert_alpha()
            self.image = pygame.transform.scale(img, (32, 32))
        except Exception:
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 215, 0), (16, 16), 14)
            self.image = surf

        # load saved count if present
        try:
            with open(self.save_file, "r") as f:
                self.count = int(f.read().strip() or 0)
        except Exception:
            self.count = 0

    def spawn_at(self, x, y):
        if len(self.coins) >= self.max_coins:
            return
        rect = self.image.get_rect(x=x, y=y)
        self.coins.append(rect)

    def update(self, screen_width, screen_height):
        # move existing coins
        for rect in self.coins[:]:
            rect.x -= self.speed
            if rect.right < 0:
                self.coins.remove(rect)

        # random auto-spawn to make coins more frequent
        if len(self.coins) < self.max_coins and random.random() < self.spawn_chance:
            y = random.randint(0, max(0, screen_height - self.image.get_height()))
            self.spawn_at(screen_width, y)

    def draw(self, surface):
        for rect in self.coins:
            surface.blit(self.image, rect)

    def check_collision(self, player_rect):
        for rect in self.coins[:]:
            if rect.colliderect(player_rect):
                self.coins.remove(rect)
                self.count += 1
                self._save()
                return True
        return False

    def get_count(self):
        return self.count

    def _save(self):
        try:
            with open(self.save_file, "w") as f:
                f.write(str(self.count))
        except Exception:
            pass
