import pygame
import random

# 초기화
pygame.init()

# 화면 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 제목
pygame.display.set_caption("슈팅 게임")

# FPS 설정
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("background.png")

# 비행기 설정
airplane = pygame.image.load("airplane.png")
airplane_size = airplane.get_rect().size
airplane_width = airplane_size[0]
airplane_height = airplane_size[1]
airplane_x = screen_width / 2 - airplane_width / 2
airplane_y = screen_height - airplane_height

# 이동할 좌표
to_x = 0

# 비행기 이동 속도
airplane_speed = 5

# 총알 설정
bullet = pygame.image.load("bullet.png")
bullet_size = bullet.get_rect().size
bullet_width = bullet_size[0]
bullet_height = bullet_size[1]
bullet_x = 0
bullet_y = airplane_y
bullet_speed = 10
bullet_state = "ready"  # "ready": 발사 준비 상태, "fire": 발사 상태

# 적 설정
enemy = pygame.image.load("enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]

# 적 생성
max_enemies = 3
enemies = []
for _ in range(max_enemies):
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = random.randint(-screen_height, 0)
    enemy_speed = random.randint(5, 10)
    enemies.append((enemy_x, enemy_y, enemy_speed))

# 점수
score = 0

# 폰트 설정
game_font = pygame.font.Font(None, 40)

# 게임 오버 메시지
game_over_font = pygame.font.Font(None, 80)

# 이벤트 루프
running = True
while running:
    dt = clock.tick(60)  # 게임 프레임 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= airplane_speed
            elif event.key == pygame.K_RIGHT:
                to_x += airplane_speed
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = airplane_x + airplane_width / 2 - bullet_width / 2
                    bullet_y = airplane_y
                    bullet_state = "fire"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    # 비행기 이동
    airplane_x += to_x

    # 경계 처리
    if airplane_x < 0:
        airplane_x = 0
    elif airplane_x > screen_width - airplane_width:
        airplane_x = screen_width - airplane_width

    # 총알 발사 처리
    if bullet_state == "fire":
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_state = "ready"

    # 적 이동
    for i in range(max_enemies):
        enemy_x, enemy_y, enemy_speed = enemies[i]
        enemy_y += enemy_speed

        # 적이 화면을 벗어나면 다시 초기 위치로 설정
        if enemy_y > screen_height:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = random.randint(-screen_height, 0)
            enemy_speed = random.randint(5, 10)

        # 충돌 처리
        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_x
        enemy_rect.top = enemy_y

        bullet_rect = bullet.get_rect()
        bullet_rect.left = bullet_x
        bullet_rect.top = bullet_y

        if bullet_rect.colliderect(enemy_rect):
            bullet_state = "ready"
            score += 1
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = random.randint(-screen_height, 0)
            enemy_speed = random.randint(5, 10)

        enemies[i] = (enemy_x, enemy_y, enemy_speed)

    # 충돌 처리
    airplane_rect = airplane.get_rect()
    airplane_rect.left = airplane_x
    airplane_rect.top = airplane_y

    for enemy_x, enemy_y, _ in enemies:
        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_x
        enemy_rect.top = enemy_y

        if airplane_rect.colliderect(enemy_rect):
            running = False

    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(airplane, (airplane_x, airplane_y))
    for enemy_x, enemy_y, _ in enemies:
        screen.blit(enemy, (enemy_x, enemy_y))
    if bullet_state == "fire":
        screen.blit(bullet, (bullet_x, bullet_y))

    # 점수 출력
    score_render = game_font.render("Score: {}".format(score), True, (255, 255, 255))
    screen.blit(score_render, (10, 10))

    pygame.display.update()

# 게임 종료
game_over_render = game_over_font.render("Game Over", True, (255, 255, 255))
screen.blit(game_over_render, (screen_width / 2 - 200, screen_height / 2 - 50))
pygame.display.update()
pygame.time.delay(2000)

pygame.quit()
