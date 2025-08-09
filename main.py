import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chill and Jump")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Font setup
font = pygame.font.Font("Assets/SF Pixelate Shaded Bold.ttf", 20)
font_score = pygame.font.SysFont("Arial", 30)

# Game state
game_state = "menu"
selected_mode = 0
modes = ["Noob", "Pro", "Hacker"]

# Burung
bird_size = 30
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.3
jump_strength = -4.4

# Pipa
pipe_width = 60
pipes = []
pipe_speed = 3
gap_min, gap_max = 100, 150  # default

# Skor
score = 0

# Load assets and scale
background = pygame.image.load("Assets/background2.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pipes_image = pygame.image.load("Assets/pipabg.png")
pipes_image = pygame.transform.scale(pipes_image, (pipe_width, 400))


def reset_game():
    global bird_y, bird_velocity, pipes, score
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    pipes.extend(create_pipe())
    score = 0


def create_pipe():
    gap = random.randint(gap_min, gap_max)
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + gap, pipe_width, HEIGHT - (height + gap))
    return [top_pipe, bottom_pipe]


def set_difficulty(mode):
    global pipe_speed, gravity, gap_min, gap_max
    if mode == "Noob":
        pipe_speed = 3
        gravity = 0.3
        gap_min, gap_max = 150, 220
    elif mode == "Pro":
        pipe_speed = 3
        gravity = 0.3
        gap_min, gap_max = 110, 150
    elif mode == "Hacker":
        pipe_speed = 4
        gravity = 0.35
        gap_min, gap_max = 90, 130


# Loop game
while True:
    screen.blit(background, (0, 0))

    # --- Update game state ---
    mode_rects = []
    if game_state == "gamemode":
        for i, mode in enumerate(modes):
            # buat surface dulu untuk dapat rect yang tepat
            color = (255, 0, 0) if i == selected_mode else (0, 0, 0)
            mode_surf = font_score.render(mode, True, color)
            rect = mode_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
            mode_rects.append(rect)

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse hover
        if event.type == pygame.MOUSEMOTION and game_state == "gamemode":
            for i, rect in enumerate(mode_rects):
                if rect.collidepoint(event.pos):
                    selected_mode = i
                    break

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "gamemode":
            if event.button == 1:  # left click
                for i, rect in enumerate(mode_rects):
                    if rect.collidepoint(event.pos):
                        selected_mode = i
                        set_difficulty(modes[selected_mode])
                        reset_game()
                        game_state = "play"
                        break

        # Keyboard options
        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_SPACE:
                    game_state = "gamemode"

            elif game_state == "gamemode":
                if event.key == pygame.K_UP:
                    selected_mode = (selected_mode - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    selected_mode = (selected_mode + 1) % len(modes)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    set_difficulty(modes[selected_mode])
                    reset_game()
                    game_state = "play"

            elif game_state == "play":
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength

            elif game_state == "gameover":
                if event.key == pygame.K_SPACE:
                    game_state = "menu"

    # --- Render states ---
    if game_state == "menu":
        title = font.render("Chill and Jump", True, (0, 0, 0))
        prompt = font.render("Press SPACE to select mode", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))

    elif game_state == "gamemode":
        title = font.render("Select Difficulty", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        # render mode text dan highlight selected mode
        for i, mode in enumerate(modes):
            color = (255, 0, 0) if i == selected_mode else (0, 0, 0)
            mode_text = font.render(mode, True, color)
            rect = mode_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
            screen.blit(mode_text, rect)

    elif game_state == "play":
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

        # Gerak pipa
        for pipe in pipes:
            pipe.x -= pipe_speed

        # Tambah pipa baru
        if not pipes or pipes[-1].x < WIDTH - 200:
            pipes.extend(create_pipe())

        # Hapus pipa lama 
        if pipes and pipes[0].x < -pipe_width:
            if len(pipes) >= 2:
                pipes.pop(0)
                pipes.pop(0)
                score += 1

        # Gambar pipa
        for i, pipe in enumerate(pipes):
            if i % 2 == 0:
                flipped_pipe = pygame.transform.flip(pipes_image, False, True)
                screen.blit(flipped_pipe, (pipe.x, pipe.bottom - 400))
            else:
                screen.blit(pipes_image, (pipe.x, pipe.y))

        # Gambar burung
        pygame.draw.rect(screen, YELLOW, bird_rect)

        # Cek tabrakan
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                game_state = "gameover"

        # Cek keluar layar
        if bird_y <= 0 or bird_y >= HEIGHT:
            game_state = "gameover"

        # Skor
        score_text = font_score.render(str(score), True, (255, 0, 0))
        screen.blit(score_text, (WIDTH // 2, 20))

    elif game_state == "gameover":
        game_over_text = font.render("GAME OVER", True, WHITE)
        retry_text = font.render("Press SPACE to menu", True, WHITE)
        final_score = font.render(f"Skor: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()
    clock.tick(FPS)
