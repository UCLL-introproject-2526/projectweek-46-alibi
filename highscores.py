import pygame


def load_scores():
    try:
        with open("scores.txt", "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
            scores.sort(reverse=True)
            return scores[:10]   # top 10
    except FileNotFoundError:
        return []


def show_highscores(screen):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arialblack", 64)
    score_font = pygame.font.SysFont("arial", 36)
    button_font = pygame.font.SysFont("arial", 32)

    back_button = pygame.Rect(WIDTH//2 - 120, HEIGHT - 100, 240, 60)

    scores = load_scores()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.collidepoint(event.pos):
                    return "home"

        screen.fill((8, 30, 70))

        # Titel
        title = title_font.render("HIGHSCORES", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))

        # Scores
        if scores:
            for i, score in enumerate(scores):
                txt = score_font.render(f"{i+1}.  {score}", True, (200, 220, 255))
                screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 160 + i * 40))
        else:
            txt = score_font.render("Nog geen scores!", True, (200, 220, 255))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 220))

        # Terug knop
        pygame.draw.rect(screen, (70, 140, 200), back_button, border_radius=14)
        pygame.draw.rect(screen, (255, 255, 255), back_button, 2, border_radius=14)

        label = button_font.render("TERUG", True, (255, 255, 255))
        screen.blit(
            label,
            (back_button.centerx - label.get_width()//2,
             back_button.centery - label.get_height()//2)
        )

        pygame.display.flip()
        clock.tick(60)
