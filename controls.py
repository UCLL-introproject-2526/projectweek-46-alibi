import pygame
from window import draw_background

def show_controls(screen):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arialblack", 48)
    text_font = pygame.font.SysFont("arial", 28)
    button_font = pygame.font.SysFont("arial", 32)

    back_button = pygame.Rect(WIDTH//2 - 120, HEIGHT - 120, 240, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back"

            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.collidepoint(event.pos):
                    return "back"

        draw_background(screen, 0, scroll=False)

        # ===== TITEL =====
        title = title_font.render("CONTROLS", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 140))

        # ===== TEKST (MIDDEN) =====
        lines = [
            "⬆ PIJLTJE OMHOOG  → VIS GAAT OMHOOG",
            "⬇ PIJLTJE OMLAAG → VIS GAAT OMLAAG",
            "",
            "ONTWIJK DE HAAIEN",
            "FIGHT THE BOSS",
            "GA VOOR JE HIGHSCORE!"
        ]

        start_y = HEIGHT//2 - len(lines) * 18
        for i, line in enumerate(lines):
            text = text_font.render(line, True, (220, 230, 255))
            screen.blit(
                text,
                (WIDTH//2 - text.get_width()//2, start_y + i * 36)
            )

        # ===== TERUG KNOP =====
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
