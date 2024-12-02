import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ
WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pickleball Game - Character Mode")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Thông số của game
ball_radius = 10
ball_speed_x, ball_speed_y = 5, 5
paddle_speed = 10
score_left = 0
score_right = 0
winning_score = 3  # Người chơi nào đạt 3 điểm trước sẽ thắng

# Thiết lập đồng hồ
clock = pygame.time.Clock()

# Các đối tượng
font = pygame.font.SysFont(None, 36)

# Tải hình ảnh nhân vật cho chế độ sáng và tối
left_player_image_light = pygame.image.load('left_player_light.png')  # Nhân vật trái chế độ sáng
right_player_image_light = pygame.image.load('right_player_light.png')  # Nhân vật phải chế độ sáng

left_player_image_dark = pygame.image.load('left_player_dark.png')  # Nhân vật trái chế độ tối
right_player_image_dark = pygame.image.load('right_player_dark.png')  # Nhân vật phải chế độ tối

# Điều chỉnh kích thước của hình ảnh nếu cần
left_player_image_light = pygame.transform.scale(left_player_image_light, (50, 100))
right_player_image_light = pygame.transform.scale(right_player_image_light, (50, 100))
left_player_image_dark = pygame.transform.scale(left_player_image_dark, (50, 100))
right_player_image_dark = pygame.transform.scale(right_player_image_dark, (50, 100))

# Biến điều khiển chế độ (True = Dark Mode, False = Light Mode)
dark_mode = False

# Hàm vẽ lưới
def draw_net():
    net_color = BLACK if not dark_mode else WHITE  # Màu của lưới thay đổi theo chế độ
    pygame.draw.line(screen, net_color, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

# Hàm vẽ điểm
def draw_score():
    score_color = BLACK if not dark_mode else WHITE  # Màu của tỉ số thay đổi theo chế độ
    score_text = font.render(f"{score_left} - {score_right}", True, score_color)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

# Hàm vẽ nhân vật từ hình ảnh
def draw_player(x, y, image):
    screen.blit(image, (x - image.get_width() // 2, y - image.get_height() // 2))

# Hàm vẽ quả bóng
def draw_ball(ball):
    pygame.draw.circle(screen, RED, (ball[0], ball[1]), ball_radius)

# Hàm cập nhật điểm
def update_score():
    global score_left, score_right
    if ball[0] - ball_radius <= 0:  # Bên trái
        score_right += 1
        reset_ball()
    if ball[0] + ball_radius >= WIDTH:  # Bên phải
        score_left += 1
        reset_ball()

# Hàm reset quả bóng
def reset_ball():
    ball[0] = WIDTH // 2
    ball[1] = HEIGHT // 2
    ball[2] = random.choice([5, -5])
    ball[3] = random.choice([5, -5])

# Hàm điều khiển paddle
def move_paddles(left_paddle, right_paddle, left_up, left_down, right_up, right_down):
    if left_up and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if left_down and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed
    if right_up and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if right_down and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed

# Hàm đếm ngược trước khi bắt đầu
def countdown():
    
    for i in range(10, 0, -1):
        screen.fill(WHITE if not dark_mode else BLACK)
        countdown_text = font.render(f"Game starts in {i}...", True, BLACK if not dark_mode else WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(1000)  # Chờ 1 giây trước khi giảm số

# Hàm kiểm tra chiến thắng
def check_winner():
    if score_left == winning_score:
        winner_text = font.render("L Wins!", True, BLUE)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Chờ 3 giây trước khi kết thúc
        return True
    elif score_right == winning_score:
        winner_text = font.render("Kira Wins!", True, BLUE)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Chờ 3 giây trước khi kết thúc
        return True
    return False

# Thiết lập các đối tượng paddle và quả bóng
left_paddle = pygame.Rect(50, HEIGHT // 2 - 50, 20, 60)  # Paddle trái
right_paddle = pygame.Rect(WIDTH - 50 - 20, HEIGHT // 2 - 50, 20, 60)  # Paddle phải
ball = [WIDTH // 2, HEIGHT // 2, random.choice([5, -5]), random.choice([5, -5])]  # [x, y, speed_x, speed_y]

# Game loop
running = True
left_up = left_down = False
right_up = right_down = False

# Bắt đầu game với countdown
countdown()

# Vòng lặp chính của game
while running:
    # Chế độ nền
    screen.fill(BLACK if dark_mode else WHITE)
    
    # Vẽ lưới và điểm
    draw_net()
    draw_score()
    
    # Vẽ nhân vật cho người chơi trái và phải (mỗi người một màu)
    if dark_mode:
        draw_player(left_paddle.x + 10, left_paddle.y + 30, left_player_image_dark)  # Người chơi trái Dark Mode
        draw_player(right_paddle.x + 10, right_paddle.y + 30, right_player_image_dark)  # Người chơi phải Dark Mode
    else:
        draw_player(left_paddle.x + 10, left_paddle.y + 30, left_player_image_light)  # Người chơi trái Light Mode
        draw_player(right_paddle.x + 10, right_paddle.y + 30, right_player_image_light)  # Người chơi phải Light Mode

    # Vẽ quả bóng
    draw_ball(ball)
    
    # Di chuyển quả bóng
    ball[0] += ball[2]
    ball[1] += ball[3]

    # Kiểm tra va chạm với tường
    if ball[1] - ball_radius <= 0 or ball[1] + ball_radius >= HEIGHT:
        ball[3] = -ball[3]

    # Kiểm tra va chạm với paddle
    if left_paddle.colliderect(pygame.Rect(ball[0] - ball_radius, ball[1] - ball_radius, ball_radius*2, ball_radius*2)) or \
       right_paddle.colliderect(pygame.Rect(ball[0] - ball_radius, ball[1] - ball_radius, ball_radius*2, ball_radius*2)):
        ball[2] = -ball[2]

    update_score()

    # Kiểm tra nếu có người chiến thắng
    if check_winner():
        break  # Dừng vòng lặp nếu có người thắng

    # Xử lý sự kiện từ bàn phím
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                left_up = True
            if event.key == pygame.K_s:
                left_down = True
            if event.key == pygame.K_UP:
                right_up = True
            if event.key == pygame.K_DOWN:
                right_down = True
            if event.key == pygame.K_d:  # Chuyển sang Dark Mode
                dark_mode = True
            if event.key == pygame.K_l:  # Chuyển sang Light Mode
                dark_mode = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                left_up = False
            if event.key == pygame.K_s:
                left_down = False
            if event.key == pygame.K_UP:
                right_up = False
            if event.key == pygame.K_DOWN:
                right_down = False

    move_paddles(left_paddle, right_paddle, left_up, left_down, right_up, right_down)

    # Cập nhật màn hình
    pygame.display.flip()

    # Giới hạn FPS
    clock.tick(60)

# Kết thúc game
pygame.quit()
