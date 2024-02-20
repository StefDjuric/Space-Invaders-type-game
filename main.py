import pygame
import os
import random
import time
from player import Player
from enemy import Enemy
from laser import collide

# Set up font to use
pygame.font.init()

FPS = 60
WIDTH, HEIGHT = 900, 500
COLORS = ['red', 'green', 'blue']
WIN = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption(title="Universe Raiders")

# Background
BACKGROUND = pygame.transform.scale(surface=pygame.image.load(os.path.join('assets', 'background-black.png')),
                                    size=(WIDTH, HEIGHT))


def main():
    """Main function for the game"""

    player = Player(425, 400)
    clock = pygame.time.Clock()
    run = True
    level = 0
    lives = 5
    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 5
    player_velocity = 5
    main_font = pygame.font.SysFont('comicsans', size=40)
    lost_font = pygame.font.SysFont('comicsans', size=50)
    lost_count = 0
    lost = False

    def draw_window():
        """Redraws the window"""
        WIN.blit(BACKGROUND, (0, 0))
        # display text
        level_label = main_font.render(f'level: {level}', 1, (0, 255, 0))
        lives_label = main_font.render(f'lives: {lives}', 1, (0, 255, 0))
        WIN.blit(level_label, (0, 440))
        WIN.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 440))
        player.redraw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (0, 255, 0))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() + 120, HEIGHT / 2))
        for enemy in enemies:
            enemy.redraw(WIN)

        pygame.display.update()

    while run:
        # Clock controls the frame rate and ensures consistency
        clock.tick(FPS)
        draw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            # The loop runs 60 times per second, so after three seconds break
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5

            # Creating new wave of enemies
            for i in range(wave_length):
                enemy = Enemy(x=random.randint(70, WIDTH - 70), y=random.randint(-1500, -100),
                              color=random.choice(COLORS))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH:
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y - player_velocity > 0:
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() < HEIGHT:
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            # Move the lasers and check if hits player
            enemy.move_lasers(laser_vel, player)

            if random.randint(0, 8 * FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

    pygame.quit()


def main_menu():
    title_font = pygame.font.SysFont('comicsans', 40)
    run = True
    while run:
        WIN.blit(BACKGROUND, (0, 0))
        title_label = title_font.render('Click the left mouse button to begin...', 1, (0, 255, 0))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and __name__ == "__main__":
                main()
    pygame.quit()


main_menu()
