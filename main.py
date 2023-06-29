import pygame

# 초기화
pygame.init()

# 게임 윈도우 크기 설정
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("숫자에 따른 색 변경 게임")

# 초기 색 설정
color = (255, 0, 0)  # 초기 색은 빨간색

# 색상 딕셔너리 설정
color_dict = {
    pygame.K_1: (255, 0, 0),   # 빨간색
    pygame.K_2: (255, 165, 0), # 주황색
    pygame.K_3: (255, 255, 0), # 노란색
    pygame.K_4: (0, 255, 0),   # 초록색
    pygame.K_5: (0, 0, 255),   # 파란색
    pygame.K_6: (0, 50, 150), # 청록색
    pygame.K_7: (80, 0, 200)  # 보라색
}

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키보드 이벤트 처리
        if event.type == pygame.KEYDOWN:
            if event.key in color_dict:
                color = color_dict[event.key]

    # 게임 화면 그리기
    window.fill(color)

    # 게임 화면 업데이트
    pygame.display.flip()

# 게임 종료
pygame.quit()
