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
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Font
font = pygame.font.Font("Assets/SF Pixelate Shaded Bold.ttf", 25)
font_score = pygame.font.SysFont("Arial", 30)

# Game state
game_state = "menu"

# Burung
bird_size = 30
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.3
jump_strength = -4

# Pipa
pipe_width = 60
pipe_gap = 150
pipes = []
pipe_speed = 3

# Skor
score = 0

#load assets
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
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - (height + pipe_gap))
    return [top_pipe, bottom_pipe]

# loop game
while True:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        #spasi buat terbang
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "menu":
                    game_state = "play"
                    reset_game()
                elif game_state == "play":
                    bird_velocity = jump_strength
                elif game_state == "gameover":
                    game_state = "menu"

    # menuawal
    if game_state == "menu":
        title = font.render("Chill and Jump ", True, (0, 0, 0))
        prompt = font.render("Press (SPACE) to start", True, (0, 0, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))

    # gameplay
    elif game_state == "play":
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

        # Gerak pipa
        for pipe in pipes:
            pipe.x -= pipe_speed

        # Tambah pipa baru
        if pipes[-1].x < WIDTH - 200:
            pipes.extend(create_pipe())

        # Hapus pipa lama
        if pipes[0].x < -pipe_width:
            pipes.pop(0)
            pipes.pop(0)
            score += 1

        # pipanya // atas sama bawah diflip biar g boros bg
        for i, pipe in enumerate(pipes):
            if i % 2 == 0:  # Pipa atas
                flipped_pipe = pygame.transform.flip(pipes_image, False, True) 
                screen.blit(flipped_pipe, (pipe.x, pipe.bottom - 400))
            else:  # Pipa bawah
                screen.blit(pipes_image, (pipe.x, pipe.y))

        # gambar burung
        pygame.draw.rect(screen, YELLOW, bird_rect)

        #tabrakan
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                game_state = "gameover"

        # Cek keluar layar
        if bird_y <= 0 or bird_y >= HEIGHT:
            game_state = "gameover"

        # Tampilkan skor
        score_text = font_score.render(str(score), True, (255, 0, 0))
        screen.blit(score_text, (WIDTH // 2, 20))

    # Game Over
    elif game_state == "gameover":
        game_over_text = font.render("GAME OVER", True, WHITE)
        if score >=10:
            retry_text = font.render("yaa mayanlahyaaa", True, WHITE)
        else:
            retry_text = font.render("NOOB", True, WHITE)
        final_score = font.render(f"Skor: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH //2 - game_over_text.get_width()//2, HEIGHT//3))
        screen.blit(final_score, (WIDTH //2 - final_score.get_width()//2, HEIGHT//2))
        screen.blit(retry_text, (WIDTH //2 - retry_text.get_width()//2, HEIGHT//1.5))

    pygame.display.flip()
    clock.tick(FPS)